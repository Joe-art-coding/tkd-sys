from django.contrib import admin
from django.shortcuts import redirect
from .models import Student, Parent
from schools.models import School, Club

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'name', 'school', 'club', 'belt_rank', 'phone', 'is_active']
    list_filter = ['club', 'school', 'belt_rank', 'is_active']
    search_fields = ['name', 'student_id', 'phone', 'ic_number']

    class Media:
        js = ('js/student_admin.js',)

    def changelist_view(self, request, extra_context=None):
        """Redirect coaches to school list instead of student list"""
        if hasattr(request.user, 'profile') and request.user.profile.role in ['coach', 'assistant_coach']:
            return redirect('/coach-schools/')  # ← HARDCODED URL
        return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        """Filter students by current club (from middleware) and user role"""
        qs = super().get_queryset(request)

        # PRIORITY 1: Filter by current club from session/middleware (for Super Admin)
        current_club = getattr(request, 'club', None)
        if current_club:
            qs = qs.filter(club=current_club)

        # PRIORITY 2: If user is coach or assistant coach, only show their schools
        if hasattr(request.user, 'profile') and request.user.profile.role not in ['super_admin', 'club_admin']:
            user_schools = request.user.profile.schools.all()
            if user_schools:
                qs = qs.filter(school__in=user_schools)

        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter dropdowns based on current club and user role"""
        current_club = getattr(request, 'club', None)

        # Filter club dropdown (only show current club)
        if db_field.name == 'club' and current_club:
            kwargs['queryset'] = Club.objects.filter(id=current_club.id)

        # Filter school dropdown based on current club and user role
        if db_field.name == 'school':
            if current_club:
                # First filter by current club
                school_qs = School.objects.filter(club=current_club, is_active=True)

                # Then further filter by user's assigned schools if not super admin
                if hasattr(request.user, 'profile') and request.user.profile.role not in ['super_admin', 'club_admin']:
                    user_schools = request.user.profile.schools.all()
                    if user_schools:
                        school_qs = school_qs.filter(id__in=user_schools)

                kwargs['queryset'] = school_qs

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        """Auto-assign club based on current club for new students"""
        if not obj.club:
            current_club = getattr(request, 'club', None)
            if current_club:
                obj.club = current_club
        super().save_model(request, obj, form, change)


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ['get_parent_full_name', 'get_student', 'relationship', 'phone']
    list_filter = ['relationship']
    search_fields = ['user__first_name', 'user__last_name', 'user__username', 'student__name', 'student__ic_number', 'phone']
    
    def get_parent_full_name(self, obj):
        """Display parent's full name from User model"""
        if obj.user:
            # Show first_name + last_name if available
            if obj.user.first_name:
                if obj.user.last_name:
                    return f"{obj.user.first_name} {obj.user.last_name}"
                return obj.user.first_name
            # Fallback to username if no name set
            return obj.user.username
        return "-"
    get_parent_full_name.short_description = 'Parent Name'
    get_parent_full_name.admin_order_field = 'user__first_name'
    
    def get_student(self, obj):
        """Display the student for this parent"""
        return obj.student.name if obj.student else "-"
    get_student.short_description = 'Student Name'
    get_student.admin_order_field = 'student__name'

    def get_queryset(self, request):
        """Filter parents by current club"""
        qs = super().get_queryset(request)
        current_club = getattr(request, 'club', None)
        if current_club:
            return qs.filter(student__club=current_club).distinct()
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter student dropdown by current club"""
        current_club = getattr(request, 'club', None)

        if db_field.name == 'student' and current_club:
            kwargs['queryset'] = Student.objects.filter(club=current_club, is_active=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
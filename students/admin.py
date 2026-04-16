from django.contrib import admin
from .models import Student, Parent
from schools.models import School, Club

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'name', 'school', 'club', 'belt_rank', 'phone', 'is_active']
    list_filter = ['club', 'school', 'belt_rank', 'is_active']
    search_fields = ['name', 'student_id', 'phone', 'ic_number']

    class Media:
        js = ('js/student_admin.js',)

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
    list_display = ['get_students', 'user', 'relationship', 'phone']
    list_filter = ['relationship']
    search_fields = ['students__name', 'students__ic_number', 'user__username', 'phone']

    def get_students(self, obj):
        """Display all students for this parent"""
        return ", ".join([s.name for s in obj.students.all()])
    get_students.short_description = 'Students'

    def get_queryset(self, request):
        """Filter parents by current club"""
        qs = super().get_queryset(request)
        current_club = getattr(request, 'club', None)
        if current_club:
            return qs.filter(students__club=current_club).distinct()
        return qs

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """Filter student dropdown by current club"""
        current_club = getattr(request, 'club', None)

        if db_field.name == 'students' and current_club:
            kwargs['queryset'] = Student.objects.filter(club=current_club, is_active=True)

        return super().formfield_for_manytomany(db_field, request, **kwargs)
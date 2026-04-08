from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import Fee
from schools.models import School, Club
from students.models import Student


class SchoolFilter(SimpleListFilter):
    """Filter fees by school - filtered by current club"""
    title = 'School'
    parameter_name = 'school'
    
    def lookups(self, request, model_admin):
        current_club = getattr(request, 'club', None)
        
        if current_club:
            schools = School.objects.filter(club=current_club, is_active=True)
        elif hasattr(request.user, 'profile') and request.user.profile.role != 'super_admin':
            schools = request.user.profile.schools.filter(is_active=True)
        else:
            schools = School.objects.filter(is_active=True)
        
        return [(s.id, s.name) for s in schools]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(student__school_id=self.value())
        return queryset


class StudentFilter(SimpleListFilter):
    """Filter fees by student - filtered by selected school or current club"""
    title = 'Student'
    parameter_name = 'student'
    
    def lookups(self, request, model_admin):
        school_id = request.GET.get('school')
        current_club = getattr(request, 'club', None)
        
        if school_id:
            students = Student.objects.filter(school_id=school_id, is_active=True)
        elif current_club:
            students = Student.objects.filter(club=current_club, is_active=True)
        else:
            return []
        
        return [(s.id, s.name) for s in students]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(student_id=self.value())
        return queryset


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ['student', 'student_club', 'fee_type', 'amount', 'month', 'due_date', 'status', 'paid_date']
    list_filter = [SchoolFilter, StudentFilter, 'status', 'fee_type', 'month']
    search_fields = ['student__name', 'student__student_id', 'student__ic_number', 'receipt_number']
    list_editable = ['paid_date', 'status']
    list_per_page = 50
    date_hierarchy = 'due_date'
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student',),
            'classes': ('wide',)
        }),
        ('Fee Details', {
            'fields': ('fee_type', 'amount', 'month', 'due_date'),
            'classes': ('wide',)
        }),
        ('Payment Information', {
            'fields': ('paid_date', 'status', 'receipt_number', 'notes'),
            'classes': ('wide',)
        }),
    )
    
    # REMOVED readonly_fields because created_at/updated_at may not exist
    
    def student_club(self, obj):
        return obj.student.club.name if obj.student.club else '-'
    student_club.short_description = 'Club'
    student_club.admin_order_field = 'student__club__name'
    
    def get_queryset(self, request):
        """Filter fees by current club (for Super Admin with club switcher)"""
        qs = super().get_queryset(request)
        
        # PRIORITY 1: Filter by current club (for Super Admin with club switcher)
        current_club = getattr(request, 'club', None)
        if current_club:
            qs = qs.filter(student__club=current_club)
        
        # PRIORITY 2: If user is coach or assistant coach, only show their schools
        elif hasattr(request.user, 'profile') and request.user.profile.role not in ['super_admin', 'club_admin']:
            user_schools = request.user.profile.schools.all()
            if user_schools:
                qs = qs.filter(student__school__in=user_schools)
        
        # Optimize with select_related to reduce database queries
        qs = qs.select_related('student', 'student__school', 'student__club')
        
        return qs
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter student dropdown by current club"""
        current_club = getattr(request, 'club', None)
        
        if db_field.name == 'student' and current_club:
            kwargs['queryset'] = Student.objects.filter(
                club=current_club, 
                is_active=True
            ).select_related('school', 'club')
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        """Auto-update status based on paid_date"""
        if obj.paid_date and obj.status == 'pending':
            obj.status = 'paid'
        elif not obj.paid_date and obj.status == 'paid':
            obj.status = 'pending'
        super().save_model(request, obj, form, change)
    
    actions = ['mark_as_paid', 'mark_as_pending']
    
    def mark_as_paid(self, request, queryset):
        """Bulk action to mark fees as paid"""
        from django.utils import timezone
        updated = queryset.update(status='paid', paid_date=timezone.now().date())
        self.message_user(request, f'{updated} fee(s) marked as paid.')
    mark_as_paid.short_description = 'Mark selected fees as paid'
    
    def mark_as_pending(self, request, queryset):
        """Bulk action to mark fees as pending"""
        updated = queryset.update(status='pending', paid_date=None)
        self.message_user(request, f'{updated} fee(s) marked as pending.')
    mark_as_pending.short_description = 'Mark selected fees as pending'
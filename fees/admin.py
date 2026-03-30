from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import Fee
from schools.models import School
from students.models import Student

class SchoolFilter(SimpleListFilter):
    title = 'School'
    parameter_name = 'school'
    
    def lookups(self, request, model_admin):
        # If user is coach, only show their schools
        if hasattr(request.user, 'profile') and request.user.profile.role != 'super_admin':
            schools = request.user.profile.schools.filter(is_active=True)
        else:
            schools = School.objects.filter(is_active=True)
        return [(s.id, s.name) for s in schools]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(student__school_id=self.value())
        return queryset

class StudentFilter(SimpleListFilter):
    title = 'Student'
    parameter_name = 'student'
    
    def lookups(self, request, model_admin):
        school_id = request.GET.get('school')
        if school_id:
            students = Student.objects.filter(school_id=school_id, is_active=True)
            return [(s.id, s.name) for s in students]
        return []
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(student_id=self.value())
        return queryset

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ['student', 'fee_type', 'amount', 'due_date', 'status', 'paid_date']
    list_filter = [SchoolFilter, StudentFilter, 'status', 'fee_type']
    search_fields = ['student__name', 'receipt_number']
    list_editable = ['paid_date', 'status']
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student',)
        }),
        ('Fee Details', {
            'fields': ('fee_type', 'amount', 'month', 'due_date')
        }),
        ('Payment Information', {
            'fields': ('paid_date', 'status', 'receipt_number', 'notes')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # If user is coach or assistant coach, only show their schools
        if hasattr(request.user, 'profile') and request.user.profile.role != 'super_admin':
            user_schools = request.user.profile.schools.all()
            if user_schools:
                qs = qs.filter(student__school__in=user_schools)
        
        return qs
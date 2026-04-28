from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'student_school', 'date', 'class_type', 'instructor', 'is_present']
    list_filter = ['student__school', 'date', 'class_type', 'is_present']
    search_fields = ['student__name', 'student__school__name', 'instructor']
    list_editable = ['is_present']
    list_per_page = 25
    
    def student_school(self, obj):
        return obj.student.school.name
    student_school.short_description = 'School'
    student_school.admin_order_field = 'student__school'
from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'name', 'school', 'belt_rank', 'phone', 'is_active']
    list_filter = ['school', 'belt_rank', 'is_active']
    search_fields = ['name', 'student_id', 'phone']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # If user is coach or assistant coach, only show their schools
        if hasattr(request.user, 'profile') and request.user.profile.role != 'super_admin':
            user_schools = request.user.profile.schools.all()
            if user_schools:
                qs = qs.filter(school__in=user_schools)
        
        return qs
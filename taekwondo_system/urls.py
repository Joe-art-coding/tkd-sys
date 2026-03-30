from django.views.generic import RedirectView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from students.views import (
    StudentViewSet, 
    ParentLoginView, 
    ParentStudentView, 
    ParentFeesView,
    CoachLoginView,
    CoachStudentsView,
    CoachFeesView,
    CoachAttendanceView,
    CoachSchoolsView,
    DashboardView
)
from attendance.views import attendance_take

# Custom admin login view
class CustomAdminLoginView(LoginView):
    template_name = 'registration/login.html'

router = DefaultRouter()
router.register(r'students', StudentViewSet)

from students.views import DashboardPageView

urlpatterns = [
    # Homepage
    path('', TemplateView.as_view(template_name='students/home.html'), name='home'),
    
    # Custom admin login page
    path('admin/login/', CustomAdminLoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    
    path('api/', include(router.urls)),
    path('parent/', TemplateView.as_view(template_name='students/parent_login.html'), name='parent_portal'),
    path('dashboard/', DashboardPageView.as_view(), name='dashboard'),
    
    # Attendance
    path('attendance/take/', attendance_take, name='attendance_take'),
    
    # API Dashboard
    path('api/dashboard/', DashboardView.as_view(), name='dashboard_api'),
    
    # Parent API endpoints
    path('api/parent/login/', ParentLoginView.as_view(), name='parent_login'),
    path('api/parent/student/', ParentStudentView.as_view(), name='parent_student'),
    path('api/parent/fees/', ParentFeesView.as_view(), name='parent_fees'),
    
    # Coach API endpoints
    path('api/coach/login/', CoachLoginView.as_view(), name='coach_login'),
    path('api/coach/schools/', CoachSchoolsView.as_view(), name='coach_schools'),
    path('api/coach/students/', CoachStudentsView.as_view(), name='coach_students'),
    path('api/coach/fees/', CoachFeesView.as_view(), name='coach_fees'),
    path('api/coach/attendance/', CoachAttendanceView.as_view(), name='coach_attendance'),
]
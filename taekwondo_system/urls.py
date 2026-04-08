from django.views.generic import RedirectView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from students.views import (
    StudentViewSet,
    ParentLoginView,
    ParentStudentView,
    ParentFeesView,
    ParentAttendanceView,
    CoachLoginView,
    CoachStudentsView,
    CoachFeesView,
    CoachAttendanceView,
    CoachSchoolsView,
    DashboardView,
    DashboardPageView,
    MartialArtsHomeView,
    ParentDashboardView
)
from attendance.views import attendance_take
from fees import views as fees_views
from schools.views import club_switcher, clear_club_session, manage_coaches, add_coach, edit_coach, delete_coach

# Custom admin login view
class CustomAdminLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def form_invalid(self, form):
        return redirect('/?error=invalid_credentials')
    
    def get_success_url(self):
        return '/'
    
    def get_redirect_url(self):
        return '/'

# Custom logout view (handle GET request)
def custom_logout(request):
    auth_logout(request)
    return redirect('/')

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')

urlpatterns = [
    # Home
    path('', MartialArtsHomeView.as_view(), name='home'),
    
    # Club switcher (for super admins)
    path('switch-club/<int:club_id>/', club_switcher, name='switch_club'),
    path('clear-club-session/', clear_club_session, name='clear_club_session'),
    
    # Club Admin - Manage Coaches
    path('manage-coaches/', manage_coaches, name='manage_coaches'),
    path('add-coach/', add_coach, name='add_coach'),
    path('edit-coach/<int:coach_id>/', edit_coach, name='edit_coach'),
    path('delete-coach/<int:coach_id>/', delete_coach, name='delete_coach'),
    
    # Admin URLs
    path('admin/login/', CustomAdminLoginView.as_view(redirect_authenticated_user=False), name='login'),
    path('admin/logout/', custom_logout, name='admin_logout'),
    
    # FORCE REDIRECT - MUST BE BEFORE admin/ URL
    path('admin/fees/fee/', RedirectView.as_view(url='/fees/', permanent=False)),
    path('admin/fees/fee', RedirectView.as_view(url='/fees/', permanent=False)),
    
    path('admin/', admin.site.urls),
    
    # Fee management views
    path('fees/', fees_views.fee_student_list, name='fee_student_list'),
    path('fees/student/<int:student_id>/', fees_views.fee_student_detail, name='fee_student_detail'),
    path('fees/mark-paid/<int:fee_id>/', fees_views.fee_mark_paid, name='fee_mark_paid'),
    
    # Receipt download URLs (for admin/staff)
    path('fees/receipt/download/<int:fee_id>/', fees_views.download_receipt, name='download_receipt'),
    path('fees/receipt/status/<int:fee_id>/', fees_views.receipt_status, name='receipt_status'),
    
    # API URLs
    path('api/', include(router.urls)),
    
    # Parent portal
    path('parent/', ParentDashboardView.as_view(), name='parent_portal'),
    
    # Dashboard
    path('dashboard/', DashboardPageView.as_view(), name='dashboard'),
    
    # Attendance
    path('attendance/take/', attendance_take, name='attendance_take'),
    
    # API endpoints
    path('api/dashboard/', DashboardView.as_view(), name='dashboard_api'),
    path('api/parent/login/', ParentLoginView.as_view(), name='parent_login'),
    path('api/parent/student/', ParentStudentView.as_view(), name='parent_student'),
    path('api/parent/fees/', ParentFeesView.as_view(), name='parent_fees'),
    path('api/parent/attendance/', ParentAttendanceView.as_view(), name='parent_attendance'),
    
    # Parent receipt download (with token authentication)
    path('api/parent/receipt/download/<int:fee_id>/', fees_views.download_receipt, name='parent_download_receipt'),
    path('api/parent/receipt/status/<int:fee_id>/', fees_views.receipt_status, name='parent_receipt_status'),
    
    # Coach API endpoints
    path('api/coach/login/', CoachLoginView.as_view(), name='coach_login'),
    path('api/coach/schools/', CoachSchoolsView.as_view(), name='coach_schools'),
    path('api/coach/students/', CoachStudentsView.as_view(), name='coach_students'),
    path('api/coach/fees/', CoachFeesView.as_view(), name='coach_fees'),
    path('api/coach/attendance/', CoachAttendanceView.as_view(), name='coach_attendance'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
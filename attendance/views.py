from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Attendance
from students.models import Student
from schools.models import School
from datetime import datetime

@staff_member_required
def attendance_take(request):
    """Take attendance for all students in a school on a specific date"""
    
    # Get user's profile
    user_profile = request.user.profile if hasattr(request.user, 'profile') else None
    current_club = getattr(request, 'club', None)
    
    # Filter schools based on user role
    if user_profile and user_profile.role == 'super_admin':
        schools = School.objects.filter(is_active=True)
        if current_club:
            schools = schools.filter(club=current_club)
    elif user_profile and user_profile.role in ['coach', 'assistant_coach']:
        # Coach/assistant coach only sees their assigned schools
        schools = user_profile.schools.filter(is_active=True)
        if current_club:
            schools = schools.filter(club=current_club)
    else:
        # Fallback - no schools
        schools = School.objects.none()
    
    # Get all coaches for dropdown (from current club)
    coaches = []
    if current_club:
        coaches = User.objects.filter(
            profile__role__in=['coach', 'assistant_coach'],
            profile__club=current_club
        ).select_related('profile')
    elif user_profile and user_profile.club:
        coaches = User.objects.filter(
            profile__role__in=['coach', 'assistant_coach'],
            profile__club=user_profile.club
        ).select_related('profile')
    
    selected_school = None
    students = []
    selected_date = timezone.now().date()
    selected_class = ''
    present_students = []
    instructor_name = ''
    
    if request.method == 'POST':
        school_id = request.POST.get('school')
        date_str = request.POST.get('date')
        class_type = request.POST.get('class_type')
        instructor_name = request.POST.get('instructor')
        
        # Convert date string to date object
        if date_str:
            try:
                selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except (ValueError, TypeError):
                selected_date = timezone.now().date()
        else:
            selected_date = timezone.now().date()
        
        if school_id:
            # Verify coach has access to this school
            if user_profile and user_profile.role != 'super_admin':
                if not user_profile.schools.filter(id=school_id).exists():
                    messages.error(request, 'You do not have access to this school.')
                    return redirect('attendance_take')
            
            selected_school = School.objects.get(id=school_id)
            students = Student.objects.filter(school=selected_school, is_active=True)
            selected_class = class_type
            
            # Get existing present students for this date
            existing_attendance = Attendance.objects.filter(
                student__school=selected_school,
                date=selected_date,
                is_present=True
            )
            
            present_students = [att.student.id for att in existing_attendance]
        
        # If save button clicked
        if 'save_attendance' in request.POST:
            school_id = request.POST.get('school')
            class_type = request.POST.get('class_type')
            instructor_name = request.POST.get('instructor')
            present_students_list = request.POST.getlist('present')
            
            # Verify coach has access to this school before saving
            if user_profile and user_profile.role != 'super_admin':
                if not user_profile.schools.filter(id=school_id).exists():
                    messages.error(request, 'You do not have access to this school.')
                    return redirect('attendance_take')
            
            selected_school = School.objects.get(id=school_id)
            students = Student.objects.filter(school=selected_school, is_active=True)
            
            for student in students:
                is_present = str(student.id) in present_students_list
                
                # Update or create attendance record
                Attendance.objects.update_or_create(
                    student=student,
                    date=selected_date,
                    defaults={
                        'class_type': class_type,
                        'instructor': instructor_name,
                        'is_present': is_present
                    }
                )
            
            messages.success(request, f'Attendance saved for {selected_date}')
            return redirect('attendance_take')
    
    context = {
        'schools': schools,
        'selected_school': selected_school,
        'students': students,
        'selected_date': selected_date,
        'selected_class': selected_class,
        'present_students': present_students,
        'class_types': Attendance.CLASS_TYPE,
        'coaches': coaches,  # ← TAMBAH NI
    }
    return render(request, 'attendance/take_attendance.html', context)
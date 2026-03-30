from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from .models import Attendance
from students.models import Student
from schools.models import School
from datetime import datetime

@staff_member_required
def attendance_take(request):
    """Take attendance for all students in a school on a specific date"""
    
    schools = School.objects.filter(is_active=True)
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
    }
    return render(request, 'attendance/take_attendance.html', context)
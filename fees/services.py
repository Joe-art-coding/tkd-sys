# fees/services.py
from django.utils import timezone
from django.db import transaction
from datetime import date
from .models import Fee
from students.models import Student
from schools.models import School


def get_schools_for_user(user, current_club=None):
    """Return schools the user is allowed to see"""
    if hasattr(user, 'profile') and user.profile.role == 'super_admin':
        return School.objects.filter(is_active=True)
    
    if hasattr(user, 'profile'):
        schools = user.profile.schools.filter(is_active=True)
        if current_club:
            schools = schools.filter(club=current_club)
        return schools
    
    return School.objects.filter(is_active=True)


def get_students_for_school(school):
    """Get active students for a school"""
    return Student.objects.filter(school=school, is_active=True)


def get_all_students_for_user(user):
    """Get students for super_admin or coach"""
    if hasattr(user, 'profile') and user.profile.role != 'super_admin':
        schools = user.profile.schools.all()
        return Student.objects.filter(school__in=schools, is_active=True)
    return Student.objects.filter(is_active=True)


def mark_fee_as_paid(fee):
    """Business logic: mark fee as paid"""
    with transaction.atomic():
        fee.status = 'paid'
        fee.paid_date = timezone.now().date()
        fee.save()
    return fee


def waive_fees_for_month_year(month: int, year: int):
    """Bulk waive all pending fees for a specific month/year"""
    with transaction.atomic():
        fees = Fee.objects.filter(
            month__year=year,
            month__month=month
        ).exclude(status='waived')   # Note: changed to 'waived' for consistency

        count = fees.update(status='waived', paid_date=None)
    return count


def get_student_fees(student):
    """Return all fees for a student, ordered by due date"""
    return student.fees.all().order_by('due_date')


def get_latest_fee_for_student(student):
    """Return the most recent fee for a student"""
    return student.fees.order_by('-due_date').first()
# fees/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from .models import Fee
from schools.models import School
from .services import (
    get_schools_for_user,
    get_students_for_school,
    get_all_students_for_user,
    mark_fee_as_paid,
    waive_fees_for_month_year,
    get_student_fees,
)
from students.models import Student

# Import receipt utility
try:
    from .receipt_utils import generate_fee_receipt
except ImportError:
    generate_fee_receipt = None


@login_required
def fee_school_list(request):
    """Show list of schools for coach / admin"""
    current_club = getattr(request, 'club', None)
    schools = get_schools_for_user(request.user, current_club)

    context = {'schools': schools}
    return render(request, 'fees/school_list.html', context)


@login_required
def fee_school_students(request, school_id):
    school = get_object_or_404(School, id=school_id)

    # Permission check
    if hasattr(request.user, 'profile') and request.user.profile.role != 'super_admin':
        if school not in request.user.profile.schools.all():
            messages.error(request, 'You do not have access to this school.')
            return redirect('fee_school_list')

    students = get_students_for_school(school)

    context = {'school': school, 'students': students}
    return render(request, 'fees/school_students.html', context)


@staff_member_required
def fee_student_list(request):
    """Show all students with their latest fee"""
    students = get_all_students_for_user(request.user)

    student_fees = []
    for student in students:
        latest_fee = student.fees.order_by('-due_date').first()
        student_fees.append({'student': student, 'latest_fee': latest_fee})

    context = {'student_fees': student_fees}
    return render(request, 'fees/student_list.html', context)


@staff_member_required
def fee_student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    # Permission check
    if hasattr(request.user, 'profile') and request.user.profile.role != 'super_admin':
        if student.school not in request.user.profile.schools.all():
            return redirect('fee_student_list')

    fees = get_student_fees(student)

    context = {'student': student, 'fees': fees}
    return render(request, 'fees/student_detail.html', context)


@staff_member_required
def fee_mark_paid(request, fee_id):
    fee = get_object_or_404(Fee, id=fee_id)

    # Permission check
    if hasattr(request.user, 'profile') and request.user.profile.role != 'super_admin':
        if fee.student.school not in request.user.profile.schools.all():
            messages.error(request, 'You do not have permission to edit this fee.')
            return redirect('fee_student_list')

    mark_fee_as_paid(fee)

    month_str = fee.month.strftime('%B %Y') if fee.month else "Fee"
    messages.success(request, f'Fee for {fee.student.name} - {month_str} marked as paid.')

    return redirect('fee_student_detail', student_id=fee.student.id)


@require_http_methods(["GET"])
def download_receipt(request, fee_id):
    fee = get_object_or_404(Fee, id=fee_id)
    student = fee.student

    # Permission check
    if hasattr(request.user, 'profile') and request.user.profile.role != 'super_admin':
        if student.school not in request.user.profile.schools.all():
            return HttpResponse("Unauthorized", status=401)

    if fee.status != 'paid':
        messages.error(request, 'Receipt is only available for paid fees.')
        return redirect('fee_student_detail', student_id=student.id)

    if generate_fee_receipt is None:
        messages.error(request, 'Receipt generation is not configured.')
        return redirect('fee_student_detail', student_id=student.id)

    try:
        pdf_buffer = generate_fee_receipt(fee, student, student.club)
        response = HttpResponse(pdf_buffer, content_type='application/pdf')

        month_str = fee.month.strftime('%Y%m') if fee.month else 'receipt'
        filename = f"receipt_{student.student_id}_{month_str}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response

    except Exception as e:
        messages.error(request, f'Error generating receipt: {str(e)}')
        return redirect('fee_student_detail', student_id=student.id)


@require_http_methods(["GET"])
def receipt_status(request, fee_id):
    import json
    try:
        fee = Fee.objects.get(id=fee_id)

        if hasattr(request.user, 'profile') and request.user.profile.role != 'super_admin':
            if fee.student.school not in request.user.profile.schools.all():
                return HttpResponse(json.dumps({'available': False, 'error': 'Unauthorized'}),
                                  content_type='application/json', status=401)

        month_str = fee.month.strftime('%B %Y') if fee.month else str(fee.month)

        return HttpResponse(json.dumps({
            'available': fee.status == 'paid',
            'fee_id': fee.id,
            'month': month_str,
            'status': fee.status,
        }), content_type='application/json')

    except Fee.DoesNotExist:
        return HttpResponse(json.dumps({'available': False, 'error': 'Fee not found'}),
                          content_type='application/json', status=404)


@staff_member_required
def fee_waive_bulk(request):
    if request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('year')

        if not month or not year:
            messages.error(request, 'Please select both month and year.')
            return redirect('fee_student_list')

        try:
            month = int(month)
            year = int(year)
            count = waive_fees_for_month_year(month, year)

            if count == 0:
                messages.warning(request, f'No pending fees found for {month}/{year}.')
            else:
                messages.success(request, f'✅ {count} fees waived for {month}/{year}!')

        except ValueError:
            messages.error(request, 'Invalid month or year.')

        return redirect('fee_student_list')

    return render(request, 'fees/waive_fees.html')
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .models import Fee
from students.models import Student
from schools.models import School

# Import receipt utility (create this file)
try:
    from .receipt_utils import generate_fee_receipt
except ImportError:
    generate_fee_receipt = None


@staff_member_required
def fee_student_list(request):
    """Show list of students with their latest fee status"""
    
    # Filter by user's schools if not super_admin
    if hasattr(request.user, 'profile') and request.user.profile.role != 'super_admin':
        schools = request.user.profile.schools.all()
        students = Student.objects.filter(school__in=schools, is_active=True)
    else:
        students = Student.objects.filter(is_active=True)
    
    # Get latest fee for each student
    student_fees = []
    for student in students:
        latest_fee = student.fees.order_by('-due_date').first()
        student_fees.append({
            'student': student,
            'latest_fee': latest_fee,
        })
    
    context = {
        'student_fees': student_fees,
    }
    return render(request, 'fees/student_list.html', context)


@staff_member_required
def fee_student_detail(request, student_id):
    """Show full year fee history for a specific student"""
    
    student = get_object_or_404(Student, id=student_id)
    
    # Check permission
    if hasattr(request.user, 'profile') and request.user.profile.role != 'super_admin':
        if student.school not in request.user.profile.schools.all():
            return redirect('fee_student_list')
    
    fees = student.fees.all().order_by('due_date')
    
    context = {
        'student': student,
        'fees': fees,
    }
    return render(request, 'fees/student_detail.html', context)


@staff_member_required
def fee_mark_paid(request, fee_id):
    """Mark a fee as paid"""
    fee = get_object_or_404(Fee, id=fee_id)
    
    # Check permission
    if hasattr(request.user, 'profile') and request.user.profile.role != 'super_admin':
        if fee.student.school not in request.user.profile.schools.all():
            messages.error(request, 'You do not have permission to edit this fee.')
            return redirect('fee_student_list')
    
    # Mark as paid
    fee.status = 'paid'
    fee.paid_date = timezone.now().date()
    fee.save()
    
    # Format month for message (use strftime, not template filter)
    month_str = fee.month.strftime('%B %Y') if fee.month else "Fee"
    messages.success(request, f'Fee for {fee.student.name} - {month_str} marked as paid.')
    
    return redirect('fee_student_detail', student_id=fee.student.id)


@require_http_methods(["GET"])
def download_receipt(request, fee_id):
    """Download PDF receipt for a paid fee"""
    
    fee = get_object_or_404(Fee, id=fee_id)
    student = fee.student
    
    # Check permission
    if hasattr(request.user, 'profile') and request.user.profile.role != 'super_admin':
        if student.school not in request.user.profile.schools.all():
            return HttpResponse("Unauthorized", status=401)
    
    # Check if fee is paid
    if fee.status != 'paid':
        messages.error(request, 'Receipt is only available for paid fees.')
        return redirect('fee_student_detail', student_id=student.id)
    
    # Check if receipt utility is available
    if generate_fee_receipt is None:
        messages.error(request, 'Receipt generation is not configured. Please install reportlab.')
        return redirect('fee_student_detail', student_id=student.id)
    
    try:
        # Get school/club info
        school = student.school
        
        # Generate PDF receipt
        pdf_buffer = generate_fee_receipt(fee, student, school)
        
        # Create HTTP response
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        
        # Set filename
        month_str = fee.month.strftime('%Y%m') if fee.month else 'receipt'
        filename = f"receipt_{student.student_id}_{month_str}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
        
    except Exception as e:
        messages.error(request, f'Error generating receipt: {str(e)}')
        return redirect('fee_student_detail', student_id=student.id)


@require_http_methods(["GET"])
def receipt_status(request, fee_id):
    """Check if receipt is available for a fee (AJAX endpoint)"""
    import json
    
    try:
        fee = Fee.objects.get(id=fee_id)
        
        # Check permission
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
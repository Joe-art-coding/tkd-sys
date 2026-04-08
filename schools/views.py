# schools/views.py
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Club, UserProfile, School


# ==================== CLUB SWITCHER (SUPER ADMIN ONLY) ====================

@staff_member_required
def club_switcher(request, club_id):
    """
    Allows super admins to switch between clubs
    Stores the selected club in session
    """
    club = get_object_or_404(Club, id=club_id, is_active=True)
    
    # Store the selected club in session
    request.session['active_club_id'] = club.id
    
    messages.success(request, f'Switched to club: {club.name}')
    
    # Redirect back to where they came from, or to admin home
    next_url = request.GET.get('next', '/admin/')
    return redirect(next_url)


@staff_member_required
def clear_club_session(request):
    """
    Clear the club session (back to default)
    """
    if 'active_club_id' in request.session:
        del request.session['active_club_id']
        messages.success(request, 'Club session cleared. Back to default view.')
    
    return redirect(request.META.get('HTTP_REFERER', '/admin/'))


# ==================== HELPER FUNCTIONS ====================

def is_club_admin(user):
    """Check if user is club admin"""
    return hasattr(user, 'profile') and user.profile.role == 'club_admin'


def is_super_admin(user):
    """Check if user is super admin"""
    return user.is_superuser


# ==================== CLUB ADMIN - MANAGE COACHES ====================

@login_required
@user_passes_test(is_club_admin)
def manage_coaches(request):
    """Club Admin can view, create, edit, delete coaches in their club"""
    club = request.user.profile.club
    
    if not club:
        messages.error(request, 'You are not assigned to any club.')
        return redirect('/admin/')
    
    # Get all coaches in this club
    coaches = User.objects.filter(
        profile__club=club,
        profile__role__in=['coach', 'assistant_coach']
    ).select_related('profile')
    
    context = {
        'coaches': coaches,
        'club': club,
    }
    return render(request, 'schools/manage_coaches.html', context)


@login_required
@user_passes_test(is_club_admin)
def add_coach(request):
    """Club Admin can add new coach to their club"""
    club = request.user.profile.club
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        role = request.POST.get('role', 'coach')
        phone = request.POST.get('phone', '')
        
        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" already exists!')
            return redirect('manage_coaches')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create profile
        profile = UserProfile.objects.create(
            user=user,
            club=club,
            role=role,
            phone=phone
        )
        
        messages.success(request, f'Coach "{username}" created successfully! Password: {password}')
        return redirect('manage_coaches')
    
    return redirect('manage_coaches')


@login_required
@user_passes_test(is_club_admin)
def edit_coach(request, coach_id):
    """Club Admin can edit coach details"""
    club = request.user.profile.club
    coach = get_object_or_404(User, id=coach_id, profile__club=club, profile__role__in=['coach', 'assistant_coach'])
    
    if request.method == 'POST':
        coach.email = request.POST.get('email', coach.email)
        coach.first_name = request.POST.get('first_name', coach.first_name)
        coach.last_name = request.POST.get('last_name', coach.last_name)
        coach.save()
        
        # Update profile
        coach.profile.role = request.POST.get('role', coach.profile.role)
        coach.profile.phone = request.POST.get('phone', coach.profile.phone)
        coach.profile.save()
        
        # Update password if provided
        new_password = request.POST.get('password')
        if new_password:
            coach.set_password(new_password)
            coach.save()
            messages.success(request, f'Coach "{coach.username}" updated. New password: {new_password}')
        else:
            messages.success(request, f'Coach "{coach.username}" updated successfully!')
        
        return redirect('manage_coaches')
    
    return redirect('manage_coaches')


@login_required
@user_passes_test(is_club_admin)
def delete_coach(request, coach_id):
    """Club Admin can delete coach (only if not super admin)"""
    club = request.user.profile.club
    coach = get_object_or_404(User, id=coach_id, profile__club=club, profile__role__in=['coach', 'assistant_coach'])
    
    if request.method == 'POST':
        username = coach.username
        coach.delete()
        messages.success(request, f'Coach "{username}" deleted successfully!')
    
    return redirect('manage_coaches')


# ==================== CLUB ADMIN - MANAGE SCHOOLS ====================

@login_required
@user_passes_test(is_club_admin)
def manage_schools(request):
    """Club Admin can manage schools in their club"""
    club = request.user.profile.club
    
    if not club:
        messages.error(request, 'You are not assigned to any club.')
        return redirect('/admin/')
    
    schools = School.objects.filter(club=club, is_active=True)
    
    context = {
        'schools': schools,
        'club': club,
    }
    return render(request, 'schools/manage_schools.html', context)


@login_required
@user_passes_test(is_club_admin)
def add_school(request):
    """Club Admin can add new school to their club"""
    club = request.user.profile.club
    
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        address = request.POST.get('address', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        monthly_fee = request.POST.get('monthly_fee', 100)
        
        # Check if school with same code exists in this club
        if School.objects.filter(club=club, code=code).exists():
            messages.error(request, f'School with code "{code}" already exists!')
            return redirect('manage_schools')
        
        school = School.objects.create(
            club=club,
            name=name,
            code=code,
            address=address,
            phone=phone,
            email=email,
            monthly_fee=monthly_fee,
            is_active=True
        )
        
        messages.success(request, f'School "{name}" created successfully!')
        return redirect('manage_schools')
    
    return redirect('manage_schools')


@login_required
@user_passes_test(is_club_admin)
def edit_school(request, school_id):
    """Club Admin can edit school details"""
    club = request.user.profile.club
    school = get_object_or_404(School, id=school_id, club=club)
    
    if request.method == 'POST':
        school.name = request.POST.get('name', school.name)
        school.code = request.POST.get('code', school.code)
        school.address = request.POST.get('address', school.address)
        school.phone = request.POST.get('phone', school.phone)
        school.email = request.POST.get('email', school.email)
        school.monthly_fee = request.POST.get('monthly_fee', school.monthly_fee)
        school.save()
        
        messages.success(request, f'School "{school.name}" updated successfully!')
        return redirect('manage_schools')
    
    return redirect('manage_schools')


@login_required
@user_passes_test(is_club_admin)
def delete_school(request, school_id):
    """Club Admin can delete school (soft delete)"""
    club = request.user.profile.club
    school = get_object_or_404(School, id=school_id, club=club)
    
    if request.method == 'POST':
        school_name = school.name
        school.is_active = False
        school.save()
        messages.success(request, f'School "{school_name}" deleted successfully!')
    
    return redirect('manage_schools')


# ==================== CLUB ADMIN - ASSIGN COACHES TO SCHOOLS ====================

@login_required
@user_passes_test(is_club_admin)
def assign_coaches(request):
    """Club Admin can assign coaches to schools"""
    club = request.user.profile.club
    
    schools = School.objects.filter(club=club, is_active=True)
    coaches = User.objects.filter(
        profile__club=club,
        profile__role__in=['coach', 'assistant_coach']
    ).select_related('profile')
    
    if request.method == 'POST':
        coach_id = request.POST.get('coach_id')
        school_ids = request.POST.getlist('school_ids')
        
        coach = get_object_or_404(User, id=coach_id, profile__club=club)
        
        # Clear existing assignments
        coach.profile.schools.clear()
        
        # Add new assignments
        for school_id in school_ids:
            school = get_object_or_404(School, id=school_id, club=club)
            coach.profile.schools.add(school)
        
        messages.success(request, f'Coach "{coach.username}" assigned to {len(school_ids)} school(s)')
        return redirect('assign_coaches')
    
    # Prepare data for template
    coach_data = []
    for coach in coaches:
        coach_data.append({
            'user': coach,
            'assigned_schools': list(coach.profile.schools.all()),
        })
    
    context = {
        'schools': schools,
        'coaches': coach_data,
        'club': club,
    }
    return render(request, 'schools/assign_coaches.html', context)
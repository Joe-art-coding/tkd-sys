# taekwondo_system/middleware.py
from schools.models import Club
from django.shortcuts import redirect
from django.urls import reverse


class ClubMiddleware:
    """
    Detects which club is accessing based on:
    1. Session (for super admin club switcher)
    2. Subdomain (for multi-tenant setup)
    3. User profile (for Club Admin, Coach)
    4. Default club for public/unauthenticated users (Taiping Club)
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Get the host (e.g., taiping.ttc.pythonanywhere.com)
        host = request.get_host()
        
        # Extract subdomain (everything before the first dot)
        subdomain = host.split('.')[0] if '.' in host else None
        
        # Initialize club as None
        request.club = None
        request.is_switched_club = False
        request.is_subdomain_club = False
        
        # PRIORITY 1: Check if super admin has an active club in session (club switcher)
        session_club_id = request.session.get('active_club_id')
        
        if session_club_id and request.user.is_authenticated and request.user.is_superuser:
            try:
                request.club = Club.objects.get(id=session_club_id, is_active=True)
                request.is_switched_club = True
                request.club_source = 'session'
            except Club.DoesNotExist:
                # Session club doesn't exist or is inactive, clear it
                if 'active_club_id' in request.session:
                    del request.session['active_club_id']
                request.club = None
        
        # PRIORITY 2: If no session club, try subdomain
        if not request.club:
            if subdomain not in [None, 'www', 'ttc', 'localhost', '127.0.0.1']:
                # Try to find club by subdomain
                try:
                    request.club = Club.objects.get(subdomain=subdomain, is_active=True)
                    request.is_subdomain_club = True
                    request.club_source = 'subdomain'
                except Club.DoesNotExist:
                    request.club = None
        
        # PRIORITY 3: Use user's profile club (for authenticated users: Club Admin, Coach)
        if not request.club:
            if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.club:
                request.club = request.user.profile.club
                request.club_source = 'user_profile'
        
        # PRIORITY 4: Default club for public/unauthenticated users (Taiping Club - ID 1)
        if not request.club:
            # Use Taiping Club as default for public pages (before login)
            request.club = Club.objects.filter(is_active=True, id=1).first()
            
            # If ID 1 not found, fallback to first active club
            if not request.club:
                request.club = Club.objects.filter(is_active=True).first()
            
            if request.club:
                request.club_source = 'public_default'
        
        # Store subdomain in request for use in templates
        request.subdomain = subdomain
        
        # Store all clubs for super admin (for club switcher dropdown)
        if request.user.is_authenticated and request.user.is_superuser:
            request.all_clubs = Club.objects.filter(is_active=True)
        else:
            request.all_clubs = []
        
        response = self.get_response(request)
        return response
# taekwondo_system/context_processors.py
from schools.models import Club


def club_processor(request):
    """
    Makes the current club and all clubs available in all templates
    """
    # Get current club from request (set by middleware)
    current_club = getattr(request, 'club', None)
    subdomain = getattr(request, 'subdomain', None)
    is_switched_club = getattr(request, 'is_switched_club', False)
    is_subdomain_club = getattr(request, 'is_subdomain_club', False)
    club_source = getattr(request, 'club_source', None)
    
    # Get all clubs for super admin (for club switcher dropdown)
    all_clubs = []
    if request.user.is_authenticated and request.user.is_superuser:
        all_clubs = Club.objects.filter(is_active=True)
    
    return {
        'current_club': current_club,
        'subdomain': subdomain,
        'all_clubs': all_clubs,
        'is_switched_club': is_switched_club,
        'is_subdomain_club': is_subdomain_club,
        'club_source': club_source,
        'is_multi_club_mode': is_switched_club or is_subdomain_club,
    }
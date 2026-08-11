from ipware import get_client_ip
from .models import Location

def get_request_client_ip(request):
    """
    Extract client IP address using django-ipware.
    """
    client_ip, is_routable = get_client_ip(request)
    return client_ip, is_routable


def detect_user_location(request):
    """
    Detect relevant news Location for the current user session:
    1. Authenticated user's preferred location (if set on profile).
    2. Session-stored location ID (if previously selected/detected).
    3. Fallback to default primary location or None.
    """
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        profile = getattr(request.user, 'profile', None)
        if profile and hasattr(profile, 'preferred_location') and profile.preferred_location:
            return profile.preferred_location

    session_location_id = request.session.get('detected_location_id')
    if session_location_id:
        try:
            return Location.objects.get(id=session_location_id, is_active=True)
        except Location.DoesNotExist:
            pass

    # Fallback to first active State location
    return Location.objects.filter(is_active=True, parent__isnull=True).first()

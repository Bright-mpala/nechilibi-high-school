from .models import SchoolSettings


def school_settings(request):
    try:
        settings = SchoolSettings.objects.first()
    except Exception:
        settings = None
    return {'school_settings': settings}

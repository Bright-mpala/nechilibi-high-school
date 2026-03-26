def school_settings(request):
    from django_school_management.institute.models import SchoolSettings
    try:
        return {'school_settings': SchoolSettings.get()}
    except Exception:
        return {'school_settings': None}

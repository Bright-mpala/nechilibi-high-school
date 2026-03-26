"""
Email task — runs synchronously (Celery removed).
"""
import logging

from django.core.mail import send_mail
from django.conf import settings

from .models import AdmissionStudent

logger = logging.getLogger(__name__)


def send_admission_confirmation_email(student_id):
    """Send admission confirmation email synchronously."""
    try:
        student = AdmissionStudent.objects.get(id=student_id)
        send_mail(
            f'Nechilibi High School: Admission confirmed for {student.name}',
            f'Congratulations {student.name}! Your admission to {student.choosen_department} has been confirmed.',
            getattr(settings, 'EMAIL_HOST_USER', 'noreply@nechilibi.ac.zw'),
            [student.email],
            fail_silently=True,
        )
    except AdmissionStudent.DoesNotExist:
        logger.warning(f'Student {student_id} not found for admission email.')
    except Exception as e:
        logger.error(f'Failed to send admission email: {e}')

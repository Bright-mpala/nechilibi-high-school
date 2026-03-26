# Newsletter task — runs synchronously (Celery removed)
import logging
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Article

logger = logging.getLogger(__name__)


def send_latest_article(mail_list, article_id):
    """Send latest article to newsletter subscribers."""
    try:
        article = Article.objects.get(id=article_id)
        html_message = render_to_string(
            'articles/newsletter-template.html', {'article': article}
        )
        message = EmailMessage(
            f'Nechilibi High School: New Article — {article.title}',
            html_message,
            getattr(settings, 'EMAIL_HOST_USER', 'noreply@nechilibi.ac.zw'),
            mail_list,
        )
        message.content_subtype = 'html'
        message.send(fail_silently=True)
    except Exception as e:
        logger.error(f'Failed to send newsletter: {e}')

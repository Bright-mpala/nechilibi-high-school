from .base import *
from .base import env
import os

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY', env('SECRET_KEY', default='change-me-in-production'))

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', 'https://nechilibi-web-production.up.railway.app').split(',')

# Database — PostgreSQL on Railway
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Media files — use Railway Volume if mounted, else fallback
MEDIA_URL = '/media/'
_vol = os.environ.get('RAILWAY_VOLUME_MOUNT_PATH', '')
MEDIA_ROOT = _vol + '/media' if _vol else str(BASE_DIR / 'media')

# Security
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Email (console fallback for now)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

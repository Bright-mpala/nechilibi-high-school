from .base import *
from .base import env

DEBUG = True

ALLOWED_HOSTS = ['*', '127.0.0.1', 'localhost']
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000', 'http://localhost:8000']

# Override to simpler storage for local development to avoid ManifestStaticFilesStorage issues
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

import os
from pathlib import Path

import environ

from django.core.exceptions import ImproperlyConfigured
from django.contrib.messages import constants as messages

from django_school_management.accounts.constants import AccountURLConstants


######################## Django Core & Custom Configs ########################
##############################################################################

BASE_DIR = Path(__file__).parent.parent.parent

env = environ.Env(
    DEBUG=(bool, True),
    USE_PAYMENT_OPTIONS=(bool, False),
    USE_SENTRY=(bool, False),
    USE_MAILCHIMP=(bool, False),
    SSL_ISSANDBOX=(bool, True),
    USE_STRIPE=(bool, False),
    IS_DEMO_ENV=(bool, False),
)
# reading .env file
env.read_env(str(BASE_DIR / "envs/.env"))

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

try:
    DJANGO_ADMIN_URL = env('DJANGO_ADMIN_URL')
except ImproperlyConfigured:
    DJANGO_ADMIN_URL = 'admin'

DEFAULT_APPS = [
    'django_school_management.accounts.apps.AccountsConfig',  # must be on top
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # allauth required
    'django.contrib.sites',
]

LOCAL_APPS = [
    'django_school_management.students.apps.StudentsConfig',
    'django_school_management.teachers.apps.TeachersConfig',
    'django_school_management.result.apps.ResultConfig',
    'django_school_management.academics.apps.AcademicsConfig',
    'django_school_management.pages.apps.PagesConfig',
    'django_school_management.articles.apps.ArticlesConfig',
    'django_school_management.institute.apps.InstituteConfig',
    'django_school_management.payments.apps.PaymentsConfig',
    'django_school_management.notices.apps.NoticesConfig',
    # curriculum app removed — Bangladesh-specific
    'django_school_management.gallery.apps.GalleryConfig',
    'django_school_management.events.apps.EventsConfig',
    'django_school_management.downloads.apps.DownloadsConfig',
    'django_school_management.nechilibi.apps.NechilibiConfig',
]

THIRD_PARTY_APPS = [
    'crispy_forms',
    'crispy_bootstrap4',
    'rolepermissions',
    'taggit',
    'django_extensions',
    'django_filters',
    'allauth',
    'allauth.account',
    # allauth.socialaccount removed — social login not needed
    'ckeditor',
    'ckeditor_uploader',
    'mptt',
    'widget_tweaks',
    'django_social_share',
    'django_countries',
    'import_export',
    'django_tables2',
    'bootstrap4',
    'django_file_form',
    'tinymce',
]

INSTALLED_APPS = DEFAULT_APPS + LOCAL_APPS + THIRD_PARTY_APPS

SITE_ID = 1

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "context_processors.attach_resources.attach_institute_data_ctx_processor",
                "context_processors.attach_resources.attach_urls_for_common_templates",
                "context_processors.attach_resources.attach_dashboard_menu_items",
                "django_school_management.institute.context_processors.school_settings",
                "django_school_management.nechilibi.context_processors.school_settings",
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database — SQLite for development, PostgreSQL for production (Railway)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Simple in-memory cache (no Redis needed)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'accounts.User'

AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Harare'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files
STATIC_ROOT = str(BASE_DIR / 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    str(BASE_DIR / 'static')
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger'
}

MEDIA_ROOT = str(BASE_DIR / 'media')
MEDIA_URL = '/media/'

# Email — console backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = env('EMAIL_HOST', default='smtp.example.com')
EMAIL_PORT = env('EMAIL_PORT', default=587)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')

# Login/register redirects
LOGIN_REDIRECT_URL = AccountURLConstants.profile_complete
LOGOUT_REDIRECT_URL = 'account_login'
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = 'account_logout'

# Stop sending verification emails on registration
ACCOUNT_EMAIL_VERIFICATION = 'none'

######################## Third Party Configs ########################
#####################################################################

# for permission management
ROLEPERMISSIONS_MODULE = 'django_school_management.academics.roles'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

CKEDITOR_UPLOAD_PATH = 'ck-uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'extraPlugins': ['codesnippet', 'markdown'],
        'width': '100%',
    },
}

TAGGIT_CASE_INSENSITIVE = True

# =========================== PAYMENTS ===========================
# Payment gateway code is kept intact but disabled by default.
# Set USE_PAYMENT_OPTIONS=True in .env and provide gateway keys to activate.
USE_PAYMENT_OPTIONS = env('USE_PAYMENT_OPTIONS')

if USE_PAYMENT_OPTIONS:
    try:
        BRAINTREE_MERCHANT_ID = env('BRAINTREE_MERCHANT_ID')
        BRAINTREE_PUBLIC_KEY = env('BRAINTREE_PUBLIC_KEY')
        BRAINTREE_PRIVATE_KEY = env('BRAINTREE_PRIVATE_KEY')
        STORE_ID = env('STORE_ID')
        STORE_PASS = env('STORE_PASS')
        SSL_ISSANDBOX = env('SSL_ISSANDBOX')
    except ImproperlyConfigured:
        pass  # payment UI is hidden; silently skip missing keys

USE_STRIPE = env('USE_STRIPE')
if USE_STRIPE:
    try:
        STRIPE_PUBLISHABLE_KEY = env('STRIPE_PUBLISHABLE_KEY')
        STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
    except ImproperlyConfigured:
        pass

TINYMCE_DEFAULT_CONFIG = {
    "theme": "silver",
    "height": 500,
    "menubar": False,
    "plugins": "advlist,autolink,lists,link,image,charmap,print,preview,anchor,"
    "searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,paste,"
    "code,help,wordcount",
    "toolbar": "undo redo | formatselect | "
    "bold italic backcolor | alignleft aligncenter "
    "alignright alignjustify | bullist numlist outdent indent | "
    "removeformat | help",
}

IS_DEMO_ENV = env('IS_DEMO_ENV')

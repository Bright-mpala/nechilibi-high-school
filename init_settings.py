import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django_school_management.institute.models import SchoolSettings

s = SchoolSettings.get()
s.phone = '+263 XXX XXX XXX'
s.email = 'info@nechilibi.ac.zw'
s.facebook_url = 'https://www.facebook.com/'
s.save()
print('SchoolSettings initialized:', s)
print('  phone:', s.phone)
print('  email:', s.email)
print('  facebook_url:', s.facebook_url)

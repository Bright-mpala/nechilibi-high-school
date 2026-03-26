from django.urls import path
from . import public_views

app_name = 'public'

urlpatterns = [
    path('', public_views.home, name='home'),
    path('about/', public_views.about, name='about'),
    path('admissions/', public_views.admissions, name='admissions'),
    path('gallery/', public_views.gallery, name='gallery'),
    path('news/', public_views.news_list, name='news'),
    path('downloads/', public_views.downloads_page, name='downloads'),
    path('events/', public_views.events_page, name='events'),
    path('contact/', public_views.contact, name='contact'),
]

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
    path('school-notices/', public_views.notices_page, name='notices'),
    path('academic-calendar/', public_views.academic_calendar, name='academic_calendar'),
    path('results/', public_views.zimsec_results, name='zimsec_results'),
    path('fees/', public_views.fee_structure, name='fee_structure'),
    path('subjects/', public_views.subjects_offered, name='subjects_offered'),
    path('newsletter/subscribe/', public_views.newsletter_subscribe, name='newsletter_subscribe'),
    path('sports/', public_views.sports_cocurriculars, name='sports_cocurriculars'),
    path('staff/', public_views.staff_directory, name='staff_directory'),
    path('search/', public_views.search, name='search'),
]

from django.urls import path
from . import portal_views

app_name = 'student_portal'

urlpatterns = [
    path('dashboard/', portal_views.student_dashboard, name='dashboard'),
    path('results/', portal_views.student_results, name='results'),
    path('profile/', portal_views.student_profile, name='profile'),
]

from django.urls import path
from . import portal_views

app_name = 'teacher_portal'

urlpatterns = [
    path('dashboard/', portal_views.teacher_dashboard, name='dashboard'),
    path('profile/', portal_views.teacher_profile, name='profile'),
]

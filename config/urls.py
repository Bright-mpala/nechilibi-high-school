from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from django_school_management.accounts.views import dashboard

admin.site.site_header = 'Nechilibi High School — Admin'
admin.site.site_title = 'Nechilibi High School'
admin.site.index_title = 'School Administration Panel'

DJANGO_ADMIN_URL = settings.DJANGO_ADMIN_URL + '/'

urlpatterns = [
    path(DJANGO_ADMIN_URL, admin.site.urls),
    path('', include('django_school_management.pages.public_urls')),
    path('', include('django_school_management.pages.urls')),
    path('dashboard/', dashboard, name='index_view'),
    path('accounts/', include('allauth.urls')),
    path('blog/', include('django_school_management.articles.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('account/', include('django_school_management.accounts.urls')),
    path('academics/', include('django_school_management.academics.urls')),
    path('notices/', include('django_school_management.notices.site_urls')),
    path('notices/dashboard/', include('django_school_management.notices.dashboard_urls')),
    path('students/', include('django_school_management.students.urls')),
    path('student/', include('django_school_management.students.portal_urls')),
    path('tinymce/', include('tinymce.urls')),
    path('teachers/', include('django_school_management.teachers.urls')),
    path('teacher/', include('django_school_management.teachers.portal_urls')),
    path('result/', include('django_school_management.result.urls')),
    path('institute/', include('django_school_management.institute.urls')),
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='account/password/password_reset.html'
        ),
        name="password_reset",
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='account/password/password_reset_done.html'
        ),
        name="password_reset_done",
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='account/password/password_reset_confirm.html'
        ),
        name='password_reset_confirm',
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='account/password/password-reset-complete.html'
        ),
        name='password_reset_complete'
    ),
    # Payments — backend URLs kept intact, not linked from the frontend UI
    path('dashboard/payments/', include('django_school_management.payments.urls')),
    path('upload/', include('django_file_form.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve media files in all environments (including production on Railway volume)
from django.views.static import serve as _serve
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', _serve, {'document_root': settings.MEDIA_ROOT}),
]

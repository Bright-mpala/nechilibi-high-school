from django.contrib import admin
from .models import SchoolSettings, SchoolVideo, SchoolEvent, Download, Testimonial


@admin.register(SchoolSettings)
class SchoolSettingsAdmin(admin.ModelAdmin):
    list_display = ['school_name', 'email', 'phone']


@admin.register(SchoolVideo)
class SchoolVideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_featured', 'is_active', 'uploaded_at']
    list_editable = ['is_featured', 'is_active']


@admin.register(SchoolEvent)
class SchoolEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_date', 'venue', 'is_active']
    list_editable = ['is_active']


@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'uploaded_at', 'is_active']
    list_editable = ['is_active']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'is_active']
    list_editable = ['is_active']

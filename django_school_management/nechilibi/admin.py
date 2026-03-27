from django.contrib import admin
from .models import SchoolSettings, GalleryImage, SchoolVideo, SchoolEvent, Download, Testimonial


@admin.register(SchoolSettings)
class SchoolSettingsAdmin(admin.ModelAdmin):
    list_display = ['school_name', 'email', 'phone']


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_carousel', 'carousel_order', 'is_active']
    list_editable = ['is_carousel', 'carousel_order', 'is_active']
    list_filter = ['category', 'is_carousel', 'is_active']


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

from django.contrib import admin
from django.utils.html import format_html

from .models import (
    GalleryAlbum, GalleryPhoto, VideoGallery,
    Event, Download, SocialMediaLink, HeroBanner, SchoolHighlight,
)


class GalleryPhotoInline(admin.TabularInline):
    model = GalleryPhoto
    extra = 3
    fields = ('image', 'caption')


@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'photo_count', 'is_published', 'created_at')
    list_editable = ('is_published',)
    inlines = [GalleryPhotoInline]
    search_fields = ('title',)


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ('album', 'caption', 'uploaded_at')
    list_filter = ('album',)


@admin.register(VideoGallery)
class VideoGalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created_at')
    list_editable = ('is_published',)
    search_fields = ('title',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'location', 'is_published')
    list_editable = ('is_published',)
    list_filter = ('is_published',)
    search_fields = ('title', 'location')
    date_hierarchy = 'start_date'


@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'created_at')
    list_editable = ('is_published',)
    list_filter = ('category', 'is_published')
    search_fields = ('title',)


@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'is_active')
    list_editable = ('url', 'is_active')


@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(SchoolHighlight)
class SchoolHighlightAdmin(admin.ModelAdmin):
    list_display = ('value', 'label', 'icon_class', 'order')
    list_editable = ('order',)

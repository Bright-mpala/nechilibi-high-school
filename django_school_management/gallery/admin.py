from django.contrib import admin
from .models import GalleryCategory, GalleryImage, VideoGallery


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 3
    fields = ['image', 'title', 'is_featured', 'is_active', 'order']


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [GalleryImageInline]


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'is_active', 'order', 'uploaded_at']
    list_filter = ['category', 'is_featured', 'is_active']
    list_editable = ['is_featured', 'is_active', 'order']
    search_fields = ['title', 'caption']


@admin.register(VideoGallery)
class VideoGalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'order', 'created_at']
    list_filter = ['is_published']
    list_editable = ['is_published', 'order']
    search_fields = ['title', 'description']

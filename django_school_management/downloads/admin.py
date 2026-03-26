from django.contrib import admin
from .models import DownloadCategory, Download

class DownloadInline(admin.TabularInline):
    model = Download
    extra = 1

@admin.register(DownloadCategory)
class DownloadCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    inlines = [DownloadInline]

@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_published', 'uploaded_at']
    list_filter = ['category', 'is_published']
    list_editable = ['is_published']

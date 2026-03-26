from import_export import resources
from import_export.admin import ImportExportModelAdmin

from django.contrib import admin

from .models import (
    InstituteProfile, TextWidget,
    ListWidget, WidgetListItem, City, EducationBoard,
    SchoolSettings,
)


class InstituteProfileResource(resources.ModelResource):
    class Meta:
        model = InstituteProfile


class InstituteProfileAdmin(ImportExportModelAdmin):
    resource_class = InstituteProfileResource


class WidgetListItemResource(resources.ModelResource):
    class Meta:
        model = WidgetListItem


class WidgetListItemInline(admin.TabularInline):
    model = WidgetListItem


class ListWidgetResource(resources.ModelResource):
    class Meta:
        model = ListWidget


class ListWidgetAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    inlines = [
            WidgetListItemInline,
    ]
    resource_class = ListWidgetResource


class TextWidgetResource(resources.ModelResource):
    class Meta:
        model = TextWidget


class TextWidgetAdmin(ImportExportModelAdmin):
    resource_class = TextWidgetResource


class CityResource(resources.ModelResource):
    class Meta:
        model = City


class CityAdmin(ImportExportModelAdmin):
    resource_class = CityResource
    list_display = ('name', 'country', 'code')
    list_filter = ('country',)
    search_fields = ('name', 'code')


admin.site.register(InstituteProfile, InstituteProfileAdmin)
admin.site.register(TextWidget, TextWidgetAdmin)
admin.site.register(ListWidget, ListWidgetAdmin)
admin.site.register(WidgetListItem)
admin.site.register(City, CityAdmin)


class EducationBoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'country')
    list_filter = ('country',)
    search_fields = ('name', 'code')


admin.site.register(EducationBoard, EducationBoardAdmin)


@admin.register(SchoolSettings)
class SchoolSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('School Identity', {
            'fields': ('school_name', 'tagline', 'logo', 'hero_background')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'youtube_url', 'whatsapp_number')
        }),
        ('Homepage Content', {
            'fields': ('hero_heading', 'hero_subheading', 'about_text', 'total_students', 'total_teachers')
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance
        return not SchoolSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

from django.contrib import admin
from .models import SchoolSettings, SchoolVideo, Download, Testimonial, TermDate, CalendarEvent, ZIMSECResult, SubjectResult


@admin.register(SchoolSettings)
class SchoolSettingsAdmin(admin.ModelAdmin):
    list_display = ['school_name', 'email', 'phone']


@admin.register(SchoolVideo)
class SchoolVideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_featured', 'is_active', 'uploaded_at']
    list_editable = ['is_featured', 'is_active']


@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'uploaded_at', 'is_active']
    list_editable = ['is_active']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'is_active']
    list_editable = ['is_active']


@admin.register(TermDate)
class TermDateAdmin(admin.ModelAdmin):
    list_display = ['academic_year', 'term', 'start_date', 'end_date', 'duration_weeks', 'is_current']
    list_editable = ['is_current']
    list_filter = ['academic_year']
    ordering = ['academic_year', 'term']


@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'date_from', 'date_to', 'academic_year']
    list_filter = ['event_type', 'academic_year']
    ordering = ['date_from']


class SubjectResultInline(admin.TabularInline):
    model = SubjectResult
    extra = 1
    fields = ['subject', 'candidates', 'passes', 'distinctions']


@admin.register(ZIMSECResult)
class ZIMSECResultAdmin(admin.ModelAdmin):
    list_display  = ['year', 'get_level', 'total_candidates', 'total_passes', 'pass_rate', 'distinctions', 'is_published']
    list_editable = ['is_published']
    list_filter   = ['level', 'year']
    ordering      = ['-year', 'level']
    inlines       = [SubjectResultInline]

    @admin.display(description='Level')
    def get_level(self, obj):
        return obj.get_level_display()

    @admin.display(description='Pass Rate %')
    def pass_rate(self, obj):
        return f'{obj.pass_rate}%'

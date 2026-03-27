from django.contrib import admin
from .models import Teacher, Designation


@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ('title',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'designation', 'email', 'mobile', 'is_active')
    list_filter = ('role', 'is_active')
    list_editable = ('role', 'is_active')
    search_fields = ('name', 'email', 'employee_id')
    filter_horizontal = ('subjects',)
    fieldsets = (
        ('Basic Info', {
            'fields': ('employee_id', 'name', 'photo', 'date_of_birth', 'role', 'designation', 'bio', 'is_active')
        }),
        ('Subjects', {
            'fields': ('subjects', 'expertise')
        }),
        ('Contact', {
            'fields': ('email', 'mobile')
        }),
        ('Social Media', {
            'fields': ('facebook', 'twitter', 'linkedin', 'whatsapp'),
            'classes': ('collapse',),
        }),
        ('System', {
            'fields': ('institute', 'created_by'),
            'classes': ('collapse',),
        }),
    )

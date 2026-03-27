from django.contrib import admin
from .models import Teacher, Designation


@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('title', 'role')
    list_editable = ('role',)
    ordering = ('role', 'title')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'email', 'mobile', 'is_active', 'joining_date')
    list_filter = ('designation__role', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('name', 'email', 'employee_id')
    filter_horizontal = ('subjects',)
    fieldsets = (
        ('Basic Info', {
            'fields': ('employee_id', 'name', 'photo', 'date_of_birth', 'designation', 'bio', 'is_active')
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

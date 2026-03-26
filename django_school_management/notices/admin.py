from django.contrib import admin
from .models import Notice, NotifyGroup, NoticeResponse, NoticeDocument


class NoticeDocumentInline(admin.TabularInline):
    model = NoticeDocument
    extra = 1


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'notice_type', 'created', 'expires_at', 'uploaded_by', 'is_past_due')
    list_filter = ('notice_type', 'expires_at')
    search_fields = ('title',)
    inlines = [NoticeDocumentInline]

    def is_past_due(self, obj):
        return obj.is_past_due
    is_past_due.boolean = True
    is_past_due.short_description = 'Expired'


@admin.register(NoticeDocument)
class NoticeDocumentAdmin(admin.ModelAdmin):
    list_display = ('notice',)


@admin.register(NotifyGroup)
class NotifyGroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'created_by')
    search_fields = ('group_name',)


@admin.register(NoticeResponse)
class NoticeResponseAdmin(admin.ModelAdmin):
    list_display = ('notice', 'responder', 'created')
    list_filter = ('created',)
    search_fields = ('notice__title',)

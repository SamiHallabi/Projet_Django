from django.contrib import admin
from .models import Ad, Category, AdImage, Message, Profile, Report

admin.site.register(Category)
admin.site.register(Ad)
admin.site.register(AdImage)
admin.site.register(Message)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('ad', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('ad__title', 'user__username', 'reason')
    actions = ['mark_as_resolved']

    def mark_as_resolved(self, request, queryset):
        queryset.update(status='resolved')
        self.message_user(request, "Selected reports marked as resolved.")
    mark_as_resolved.short_description = "Mark selected reports as resolved"
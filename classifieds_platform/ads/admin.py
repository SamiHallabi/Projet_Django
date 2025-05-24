from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Ad, Category, AdImage, Message, Profile, Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('ad', 'user', 'status', 'created_at', 'manage_link')
    list_filter = ('status', 'created_at')
    search_fields = ('ad__title', 'user__username', 'reason')
    actions = ['mark_as_resolved']

    def mark_as_resolved(self, request, queryset):
        queryset.update(status='resolved')
        self.message_user(request, "Selected reports marked as resolved.")
    mark_as_resolved.short_description = "Mark selected reports as resolved"

    def manage_link(self, obj):
        url = reverse('report_management')
        return format_html('<a href="{}">Manage Reports</a>', url)
    manage_link.short_description = 'Custom Management'
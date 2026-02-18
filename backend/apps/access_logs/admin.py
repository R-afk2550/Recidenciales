"""
Admin configuration for Access Logs app
"""
from django.contrib import admin
from .models import AccessLog


@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    """Admin for AccessLog model"""
    list_display = [
        'person_name', 'access_type', 'access_method', 'status',
        'access_point', 'timestamp'
    ]
    list_filter = [
        'status', 'access_type', 'access_method', 'access_point',
        'timestamp'
    ]
    search_fields = [
        'person_name', 'person_document', 'code_used',
        'resident__first_name', 'resident__last_name',
        'visitor__first_name', 'visitor__last_name'
    ]
    ordering = ['-timestamp']
    readonly_fields = ['timestamp', 'created_at']
    autocomplete_fields = ['resident', 'visitor', 'access_point', 'authorized_by']
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('Person Information', {
            'fields': ('resident', 'visitor', 'person_name', 'person_document')
        }),
        ('Access Information', {
            'fields': ('access_point', 'access_type', 'access_method', 'code_used')
        }),
        ('Codes', {
            'fields': ('temporary_code', 'access_code')
        }),
        ('Result', {
            'fields': ('status', 'denial_reason', 'authorized_by')
        }),
        ('Metadata', {
            'fields': ('timestamp', 'vehicle_plate', 'temperature', 'photo', 'notes')
        }),
        ('Technical', {
            'fields': ('ip_address', 'device_id')
        }),
    )
    
    def has_add_permission(self, request):
        # Logs are created automatically, not manually
        return False
    
    def has_change_permission(self, request, obj=None):
        # Logs should not be modified
        return False

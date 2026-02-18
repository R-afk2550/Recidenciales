"""
Admin configuration for Access Control app
"""
from django.contrib import admin
from .models import AccessPoint, AccessCode


@admin.register(AccessPoint)
class AccessPointAdmin(admin.ModelAdmin):
    """Admin for AccessPoint model"""
    list_display = ['name', 'code', 'access_type', 'location', 'building', 'is_entry', 'is_exit', 'is_active']
    list_filter = ['access_type', 'is_entry', 'is_exit', 'is_active', 'building']
    search_fields = ['name', 'code', 'location']
    ordering = ['name']
    autocomplete_fields = ['building']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'access_type', 'location', 'building')
        }),
        ('Capabilities', {
            'fields': ('supports_qr', 'supports_rfid', 'supports_numeric')
        }),
        ('Configuration', {
            'fields': ('is_entry', 'is_exit', 'is_active')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )


@admin.register(AccessCode)
class AccessCodeAdmin(admin.ModelAdmin):
    """Admin for AccessCode model"""
    list_display = ['code', 'resident', 'code_type', 'is_active', 'issued_date', 'expiry_date']
    list_filter = ['code_type', 'is_active', 'issued_date', 'expiry_date']
    search_fields = ['code', 'resident__first_name', 'resident__last_name']
    ordering = ['-issued_date']
    readonly_fields = ['issued_date', 'created_at', 'updated_at']
    autocomplete_fields = ['resident', 'issued_by']
    filter_horizontal = ['access_points']
    
    fieldsets = (
        ('Code Information', {
            'fields': ('resident', 'code', 'code_type')
        }),
        ('Access Points', {
            'fields': ('access_points',)
        }),
        ('Validity', {
            'fields': ('is_active', 'issued_date', 'expiry_date', 'issued_by')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )

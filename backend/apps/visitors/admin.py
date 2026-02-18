"""
Admin configuration for Visitors app
"""
from django.contrib import admin
from .models import Visitor, TemporaryCode


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    """Admin for Visitor model"""
    list_display = ['full_name', 'unit', 'visitor_type', 'status', 'expected_date', 'phone']
    list_filter = ['status', 'visitor_type', 'expected_date']
    search_fields = ['first_name', 'last_name', 'document_id', 'phone', 'company']
    ordering = ['-expected_date', '-created_at']
    autocomplete_fields = ['unit', 'resident', 'authorized_by']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'document_id', 'phone', 'email', 'photo')
        }),
        ('Visit Information', {
            'fields': ('visitor_type', 'status', 'unit', 'resident', 'purpose', 
                      'expected_date', 'expected_time', 'company')
        }),
        ('Vehicle Information', {
            'fields': ('vehicle_plate',)
        }),
        ('Authorization', {
            'fields': ('authorized_by', 'check_in_time', 'check_out_time')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )


@admin.register(TemporaryCode)
class TemporaryCodeAdmin(admin.ModelAdmin):
    """Admin for TemporaryCode model"""
    list_display = ['code', 'visitor', 'code_type', 'valid_from', 'valid_until', 'times_used', 'is_active']
    list_filter = ['code_type', 'is_active', 'valid_from', 'valid_until']
    search_fields = ['code', 'visitor__first_name', 'visitor__last_name']
    ordering = ['-created_at']
    readonly_fields = ['times_used', 'last_used_at', 'created_at', 'updated_at']
    autocomplete_fields = ['visitor', 'generated_by']
    
    fieldsets = (
        ('Code Information', {
            'fields': ('visitor', 'code', 'code_type', 'qr_code_image', 'secret_key')
        }),
        ('Validity', {
            'fields': ('valid_from', 'valid_until', 'max_uses', 'is_active')
        }),
        ('Usage', {
            'fields': ('times_used', 'last_used_at', 'generated_by')
        }),
    )

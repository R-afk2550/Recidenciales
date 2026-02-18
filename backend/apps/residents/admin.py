"""
Admin configuration for Residents app
"""
from django.contrib import admin
from .models import Building, Unit, Resident


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    """Admin for Building model"""
    list_display = ['code', 'name', 'floors', 'units_per_floor', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code', 'address']
    ordering = ['code', 'name']


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    """Admin for Unit model"""
    list_display = ['__str__', 'building', 'floor', 'owner_name', 'owner_phone', 'is_occupied']
    list_filter = ['building', 'floor', 'is_occupied']
    search_fields = ['number', 'owner_name', 'owner_phone']
    ordering = ['building', 'floor', 'number']
    autocomplete_fields = ['building']


@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    """Admin for Resident model"""
    list_display = ['full_name', 'unit', 'document_id', 'phone', 'resident_type', 'is_authorized', 'is_active']
    list_filter = ['resident_type', 'is_authorized', 'unit__building']
    search_fields = ['first_name', 'last_name', 'document_id', 'phone', 'email']
    ordering = ['-created_at']
    autocomplete_fields = ['unit', 'user']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'document_id', 'phone', 'email', 'photo')
        }),
        ('Residence Information', {
            'fields': ('unit', 'resident_type', 'user', 'is_authorized')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone')
        }),
        ('Dates', {
            'fields': ('move_in_date', 'move_out_date')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )

"""
Serializers for Residents app
"""
from rest_framework import serializers
from .models import Building, Unit, Resident


class BuildingSerializer(serializers.ModelSerializer):
    """Serializer for Building model"""
    total_units = serializers.SerializerMethodField()
    
    class Meta:
        model = Building
        fields = [
            'id', 'name', 'code', 'address', 'floors', 'units_per_floor',
            'is_active', 'total_units', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_total_units(self, obj):
        return obj.units.count()


class UnitSerializer(serializers.ModelSerializer):
    """Serializer for Unit model"""
    building_name = serializers.CharField(source='building.name', read_only=True)
    building_code = serializers.CharField(source='building.code', read_only=True)
    resident_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Unit
        fields = [
            'id', 'building', 'building_name', 'building_code', 'number', 'floor',
            'owner_name', 'owner_phone', 'is_occupied', 'notes',
            'resident_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_resident_count(self, obj):
        return obj.residents.filter(is_authorized=True, move_out_date__isnull=True).count()


class ResidentSerializer(serializers.ModelSerializer):
    """Serializer for Resident model"""
    unit_display = serializers.CharField(source='unit.__str__', read_only=True)
    full_name = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Resident
        fields = [
            'id', 'user', 'unit', 'unit_display', 'first_name', 'last_name', 'full_name',
            'document_id', 'phone', 'email', 'photo', 'resident_type',
            'emergency_contact_name', 'emergency_contact_phone', 'is_authorized',
            'move_in_date', 'move_out_date', 'notes', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ResidentMinimalSerializer(serializers.ModelSerializer):
    """Minimal serializer for resident references"""
    full_name = serializers.CharField(read_only=True)
    unit_display = serializers.CharField(source='unit.__str__', read_only=True)
    
    class Meta:
        model = Resident
        fields = ['id', 'full_name', 'unit_display', 'phone']

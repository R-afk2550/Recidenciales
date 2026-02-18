"""
Serializers for Access Control app
"""
from rest_framework import serializers
from .models import AccessPoint, AccessCode


class AccessPointSerializer(serializers.ModelSerializer):
    """Serializer for AccessPoint model"""
    building_name = serializers.CharField(source='building.name', read_only=True)
    
    class Meta:
        model = AccessPoint
        fields = [
            'id', 'name', 'code', 'access_type', 'location', 'building', 'building_name',
            'supports_qr', 'supports_rfid', 'supports_numeric',
            'is_entry', 'is_exit', 'is_active', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AccessCodeSerializer(serializers.ModelSerializer):
    """Serializer for AccessCode model"""
    resident_name = serializers.CharField(source='resident.full_name', read_only=True)
    is_valid = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = AccessCode
        fields = [
            'id', 'resident', 'resident_name', 'code', 'code_type',
            'access_points', 'is_active', 'issued_date', 'expiry_date',
            'issued_by', 'notes', 'is_valid', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'issued_date', 'created_at', 'updated_at']


class ValidateAccessRequestSerializer(serializers.Serializer):
    """Serializer for access validation request"""
    code = serializers.CharField(max_length=100)
    access_point_id = serializers.IntegerField()
    access_type = serializers.ChoiceField(
        choices=['ENTRY', 'EXIT'],
        default='ENTRY'
    )

"""
Serializers for Visitors app
"""
from rest_framework import serializers
from .models import Visitor, TemporaryCode
from apps.residents.serializers import UnitSerializer, ResidentMinimalSerializer


class VisitorSerializer(serializers.ModelSerializer):
    """Serializer for Visitor model"""
    unit_display = serializers.CharField(source='unit.__str__', read_only=True)
    full_name = serializers.CharField(read_only=True)
    resident_name = serializers.CharField(source='resident.full_name', read_only=True)
    is_currently_inside = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Visitor
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'document_id',
            'phone', 'email', 'photo', 'visitor_type', 'status',
            'unit', 'unit_display', 'resident', 'resident_name',
            'purpose', 'expected_date', 'expected_time', 'vehicle_plate',
            'company', 'authorized_by', 'check_in_time', 'check_out_time',
            'notes', 'is_currently_inside', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class VisitorMinimalSerializer(serializers.ModelSerializer):
    """Minimal serializer for visitor references"""
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Visitor
        fields = ['id', 'full_name', 'phone', 'status']


class TemporaryCodeSerializer(serializers.ModelSerializer):
    """Serializer for TemporaryCode model"""
    visitor_name = serializers.CharField(source='visitor.full_name', read_only=True)
    is_valid = serializers.BooleanField(read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = TemporaryCode
        fields = [
            'id', 'visitor', 'visitor_name', 'code', 'code_type',
            'qr_code_image', 'secret_key', 'valid_from', 'valid_until',
            'max_uses', 'times_used', 'is_active', 'generated_by',
            'last_used_at', 'is_valid', 'is_expired', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'times_used', 'last_used_at', 'created_at', 'updated_at']


class GenerateCodeRequestSerializer(serializers.Serializer):
    """Serializer for code generation request"""
    visitor_id = serializers.IntegerField()
    code_type = serializers.ChoiceField(choices=TemporaryCode.CodeType.choices)
    valid_hours = serializers.IntegerField(min_value=1, max_value=168, default=24)
    max_uses = serializers.IntegerField(min_value=1, default=1)


class ValidateCodeRequestSerializer(serializers.Serializer):
    """Serializer for code validation request"""
    code = serializers.CharField(max_length=100)
    access_point_id = serializers.IntegerField(required=False)

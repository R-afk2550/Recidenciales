"""
Serializers for Access Logs app
"""
from rest_framework import serializers
from .models import AccessLog


class AccessLogSerializer(serializers.ModelSerializer):
    """Serializer for AccessLog model"""
    access_point_name = serializers.CharField(source='access_point.name', read_only=True)
    is_successful = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = AccessLog
        fields = [
            'id', 'resident', 'visitor', 'person_name', 'person_document',
            'access_point', 'access_point_name', 'access_type', 'access_method',
            'code_used', 'temporary_code', 'access_code', 'status', 'denial_reason',
            'timestamp', 'vehicle_plate', 'temperature', 'photo', 'authorized_by',
            'notes', 'ip_address', 'device_id', 'is_successful', 'created_at'
        ]
        read_only_fields = ['id', 'timestamp', 'created_at']


class AccessLogMinimalSerializer(serializers.ModelSerializer):
    """Minimal serializer for access log list"""
    access_point_name = serializers.CharField(source='access_point.name', read_only=True)
    
    class Meta:
        model = AccessLog
        fields = [
            'id', 'person_name', 'access_point_name', 'access_type',
            'access_method', 'status', 'timestamp'
        ]


class AccessStatsSerializer(serializers.Serializer):
    """Serializer for access statistics"""
    total_accesses = serializers.IntegerField()
    successful_accesses = serializers.IntegerField()
    denied_accesses = serializers.IntegerField()
    entries = serializers.IntegerField()
    exits = serializers.IntegerField()
    unique_residents = serializers.IntegerField()
    unique_visitors = serializers.IntegerField()
    by_access_method = serializers.DictField()
    by_access_point = serializers.DictField()
    recent_accesses = AccessLogMinimalSerializer(many=True)

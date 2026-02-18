"""
Serializers for Users app
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'phone', 'photo', 'is_active_employee',
            'is_active', 'date_joined', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'date_joined', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating users"""
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name',
            'role', 'phone', 'photo'
        ]
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserMinimalSerializer(serializers.ModelSerializer):
    """Minimal serializer for user references"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'role']
    
    def get_full_name(self, obj):
        return obj.get_full_name()

"""
Views for Users app
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import UserSerializer, UserCreateSerializer, UserMinimalSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users
    """
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'list_minimal':
            return UserMinimalSerializer
        return UserSerializer
    
    def get_queryset(self):
        # Regular users can only see themselves
        if not self.request.user.is_staff:
            return User.objects.filter(id=self.request.user.id)
        return User.objects.all()
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def list_minimal(self, request):
        """Get minimal user list for dropdowns"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

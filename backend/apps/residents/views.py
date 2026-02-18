"""
Views for Residents app
"""
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Building, Unit, Resident
from .serializers import (
    BuildingSerializer, UnitSerializer, ResidentSerializer, ResidentMinimalSerializer
)


class BuildingViewSet(viewsets.ModelViewSet):
    """ViewSet for managing buildings"""
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code', 'address']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['code']


class UnitViewSet(viewsets.ModelViewSet):
    """ViewSet for managing units"""
    queryset = Unit.objects.select_related('building').all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['number', 'owner_name', 'building__name', 'building__code']
    ordering_fields = ['building__code', 'floor', 'number', 'created_at']
    ordering = ['building', 'floor', 'number']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        building_id = self.request.query_params.get('building', None)
        if building_id:
            queryset = queryset.filter(building_id=building_id)
        return queryset


class ResidentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing residents"""
    queryset = Resident.objects.select_related('unit', 'unit__building', 'user').all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'document_id', 'phone', 'email', 'unit__number']
    ordering_fields = ['first_name', 'last_name', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list_minimal':
            return ResidentMinimalSerializer
        return ResidentSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        unit_id = self.request.query_params.get('unit', None)
        building_id = self.request.query_params.get('building', None)
        is_active = self.request.query_params.get('is_active', None)
        
        if unit_id:
            queryset = queryset.filter(unit_id=unit_id)
        if building_id:
            queryset = queryset.filter(unit__building_id=building_id)
        if is_active is not None:
            if is_active.lower() == 'true':
                queryset = queryset.filter(is_authorized=True, move_out_date__isnull=True)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def list_minimal(self, request):
        """Get minimal resident list for dropdowns"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

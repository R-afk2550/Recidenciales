"""
Views for Access Logs app
"""
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import AccessLog
from .serializers import AccessLogSerializer, AccessLogMinimalSerializer, AccessStatsSerializer


class AccessLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing access logs"""
    queryset = AccessLog.objects.select_related(
        'resident', 'visitor', 'access_point', 'authorized_by'
    ).all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['person_name', 'person_document', 'code_used']
    ordering_fields = ['timestamp', 'created_at']
    ordering = ['-timestamp']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AccessLogMinimalSerializer
        return AccessLogSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filters
        resident_id = self.request.query_params.get('resident', None)
        visitor_id = self.request.query_params.get('visitor', None)
        access_point_id = self.request.query_params.get('access_point', None)
        access_type = self.request.query_params.get('access_type', None)
        status = self.request.query_params.get('status', None)
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        
        if resident_id:
            queryset = queryset.filter(resident_id=resident_id)
        if visitor_id:
            queryset = queryset.filter(visitor_id=visitor_id)
        if access_point_id:
            queryset = queryset.filter(access_point_id=access_point_id)
        if access_type:
            queryset = queryset.filter(access_type=access_type)
        if status:
            queryset = queryset.filter(status=status)
        if date_from:
            queryset = queryset.filter(timestamp__gte=date_from)
        if date_to:
            queryset = queryset.filter(timestamp__lte=date_to)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get access statistics"""
        # Date range filter
        days = int(request.query_params.get('days', 7))
        start_date = timezone.now() - timedelta(days=days)
        
        queryset = AccessLog.objects.filter(timestamp__gte=start_date)
        
        # Calculate statistics
        total_accesses = queryset.count()
        successful_accesses = queryset.filter(status=AccessLog.Status.SUCCESS).count()
        denied_accesses = queryset.filter(status=AccessLog.Status.DENIED).count()
        entries = queryset.filter(access_type=AccessLog.AccessType.ENTRY).count()
        exits = queryset.filter(access_type=AccessLog.AccessType.EXIT).count()
        unique_residents = queryset.filter(resident__isnull=False).values('resident').distinct().count()
        unique_visitors = queryset.filter(visitor__isnull=False).values('visitor').distinct().count()
        
        # By access method
        by_access_method = dict(
            queryset.values('access_method').annotate(count=Count('id')).values_list('access_method', 'count')
        )
        
        # By access point
        by_access_point = dict(
            queryset.values('access_point__name').annotate(count=Count('id')).values_list('access_point__name', 'count')
        )
        
        # Recent accesses
        recent_accesses = queryset.order_by('-timestamp')[:10]
        
        stats = {
            'total_accesses': total_accesses,
            'successful_accesses': successful_accesses,
            'denied_accesses': denied_accesses,
            'entries': entries,
            'exits': exits,
            'unique_residents': unique_residents,
            'unique_visitors': unique_visitors,
            'by_access_method': by_access_method,
            'by_access_point': by_access_point,
            'recent_accesses': recent_accesses
        }
        
        serializer = AccessStatsSerializer(stats)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def resident_logs(self, request):
        """Get access logs for a specific resident"""
        resident_id = request.query_params.get('resident_id', None)
        if not resident_id:
            return Response({'error': 'resident_id parameter required'}, status=400)
        
        queryset = self.get_queryset().filter(resident_id=resident_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def visitor_logs(self, request):
        """Get access logs for a specific visitor"""
        visitor_id = request.query_params.get('visitor_id', None)
        if not visitor_id:
            return Response({'error': 'visitor_id parameter required'}, status=400)
        
        queryset = self.get_queryset().filter(visitor_id=visitor_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

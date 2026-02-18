"""
Views for Visitors app
"""
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.core.files.base import ContentFile

from .models import Visitor, TemporaryCode
from .serializers import (
    VisitorSerializer, VisitorMinimalSerializer, TemporaryCodeSerializer,
    GenerateCodeRequestSerializer, ValidateCodeRequestSerializer
)
from utils.code_generator import generate_temporary_access_code, generate_otp
from utils.qr_generator import generate_visitor_qr


class VisitorViewSet(viewsets.ModelViewSet):
    """ViewSet for managing visitors"""
    queryset = Visitor.objects.select_related('unit', 'resident', 'authorized_by').all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'document_id', 'phone', 'company']
    ordering_fields = ['expected_date', 'created_at']
    ordering = ['-expected_date', '-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list_minimal':
            return VisitorMinimalSerializer
        return VisitorSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status', None)
        visitor_type = self.request.query_params.get('visitor_type', None)
        unit_id = self.request.query_params.get('unit', None)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if visitor_type:
            queryset = queryset.filter(visitor_type=visitor_type)
        if unit_id:
            queryset = queryset.filter(unit_id=unit_id)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def list_minimal(self, request):
        """Get minimal visitor list"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def generate_code(self, request):
        """Generate temporary access code for a visitor"""
        serializer = GenerateCodeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        visitor_id = serializer.validated_data['visitor_id']
        code_type = serializer.validated_data['code_type']
        valid_hours = serializer.validated_data['valid_hours']
        max_uses = serializer.validated_data['max_uses']
        
        try:
            visitor = Visitor.objects.get(id=visitor_id)
        except Visitor.DoesNotExist:
            return Response(
                {'error': 'Visitor not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Generate code based on type
        if code_type == TemporaryCode.CodeType.OTP:
            code, secret_key = generate_otp()
        elif code_type == TemporaryCode.CodeType.NUMERIC:
            code = generate_temporary_access_code('numeric', length=6)
            secret_key = ''
        elif code_type == TemporaryCode.CodeType.ALPHANUMERIC:
            code = generate_temporary_access_code('alphanumeric', length=8)
            secret_key = ''
        else:  # QR
            code = generate_temporary_access_code('alphanumeric', length=12)
            secret_key = ''
        
        # Create temporary code
        temp_code = TemporaryCode.objects.create(
            visitor=visitor,
            code=code,
            code_type=code_type,
            secret_key=secret_key,
            valid_from=timezone.now(),
            valid_until=timezone.now() + timedelta(hours=valid_hours),
            max_uses=max_uses,
            generated_by=request.user
        )
        
        # Generate QR code if needed
        if code_type == TemporaryCode.CodeType.QR:
            qr_image = generate_visitor_qr(code, visitor.full_name)
            temp_code.qr_code_image.save(
                f'visitor_{visitor.id}_{temp_code.id}.png',
                ContentFile(qr_image.read()),
                save=True
            )
        
        # Update visitor status
        if visitor.status == Visitor.Status.PENDING:
            visitor.status = Visitor.Status.APPROVED
            visitor.save()
        
        code_serializer = TemporaryCodeSerializer(temp_code)
        return Response(code_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def validate_code(self, request):
        """Validate a temporary access code"""
        serializer = ValidateCodeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        code = serializer.validated_data['code']
        
        try:
            temp_code = TemporaryCode.objects.select_related('visitor').get(code=code)
        except TemporaryCode.DoesNotExist:
            return Response(
                {'valid': False, 'error': 'Invalid code'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if code is valid
        if not temp_code.is_valid:
            error = 'Code has expired' if temp_code.is_expired else 'Code is not active or has been used'
            return Response(
                {'valid': False, 'error': error},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Increment usage
        temp_code.increment_usage()
        
        # Update visitor status
        visitor = temp_code.visitor
        if visitor.status == Visitor.Status.APPROVED:
            visitor.status = Visitor.Status.CHECKED_IN
            visitor.check_in_time = timezone.now()
            visitor.save()
        
        return Response({
            'valid': True,
            'visitor': VisitorSerializer(visitor).data,
            'code': TemporaryCodeSerializer(temp_code).data
        })


class TemporaryCodeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing temporary codes"""
    queryset = TemporaryCode.objects.select_related('visitor', 'generated_by').all()
    serializer_class = TemporaryCodeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['code', 'visitor__first_name', 'visitor__last_name']
    ordering_fields = ['created_at', 'valid_until']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        visitor_id = self.request.query_params.get('visitor', None)
        is_active = self.request.query_params.get('is_active', None)
        
        if visitor_id:
            queryset = queryset.filter(visitor_id=visitor_id)
        if is_active is not None:
            if is_active.lower() == 'true':
                queryset = queryset.filter(
                    is_active=True,
                    valid_until__gt=timezone.now()
                )
        
        return queryset

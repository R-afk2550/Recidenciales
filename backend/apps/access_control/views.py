"""
Views for Access Control app
"""
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .models import AccessPoint, AccessCode
from .serializers import (
    AccessPointSerializer, AccessCodeSerializer, ValidateAccessRequestSerializer
)
from apps.visitors.models import TemporaryCode
from apps.access_logs.models import AccessLog


class AccessPointViewSet(viewsets.ModelViewSet):
    """ViewSet for managing access points"""
    queryset = AccessPoint.objects.select_related('building').all()
    serializer_class = AccessPointSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code', 'location']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        is_active = self.request.query_params.get('is_active', None)
        access_type = self.request.query_params.get('access_type', None)
        
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        if access_type:
            queryset = queryset.filter(access_type=access_type)
        
        return queryset


class AccessCodeViewSet(viewsets.ModelViewSet):
    """ViewSet for managing access codes"""
    queryset = AccessCode.objects.select_related('resident', 'issued_by').prefetch_related('access_points').all()
    serializer_class = AccessCodeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['code', 'resident__first_name', 'resident__last_name']
    ordering_fields = ['issued_date', 'expiry_date', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        resident_id = self.request.query_params.get('resident', None)
        is_active = self.request.query_params.get('is_active', None)
        
        if resident_id:
            queryset = queryset.filter(resident_id=resident_id)
        if is_active is not None:
            if is_active.lower() == 'true':
                queryset = queryset.filter(is_active=True)
        
        return queryset
    
    @action(detail=False, methods=['post'])
    def validate(self, request):
        """Validate access code and log access"""
        serializer = ValidateAccessRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        code = serializer.validated_data['code']
        access_point_id = serializer.validated_data['access_point_id']
        access_type = serializer.validated_data['access_type']
        
        # Get access point
        try:
            access_point = AccessPoint.objects.get(id=access_point_id)
        except AccessPoint.DoesNotExist:
            return Response(
                {'valid': False, 'error': 'Invalid access point'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Try to find code in permanent codes
        try:
            access_code = AccessCode.objects.select_related('resident').get(code=code)
            
            # Validate code
            if not access_code.is_valid:
                error = 'Code has expired' if access_code.expiry_date and access_code.expiry_date < timezone.now().date() else 'Code is not active'
                
                # Log denied access
                AccessLog.objects.create(
                    resident=access_code.resident,
                    person_name=access_code.resident.full_name,
                    person_document=access_code.resident.document_id,
                    access_point=access_point,
                    access_type=access_type,
                    access_method=AccessLog.AccessMethod.RFID if access_code.code_type == AccessCode.CodeType.RFID else AccessLog.AccessMethod.NUMERIC_CODE,
                    code_used=code,
                    access_code=access_code,
                    status=AccessLog.Status.DENIED,
                    denial_reason=error,
                    authorized_by=request.user
                )
                
                return Response(
                    {'valid': False, 'error': error},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if code has access to this point
            if access_code.access_points.exists() and access_point not in access_code.access_points.all():
                # Log denied access
                AccessLog.objects.create(
                    resident=access_code.resident,
                    person_name=access_code.resident.full_name,
                    person_document=access_code.resident.document_id,
                    access_point=access_point,
                    access_type=access_type,
                    access_method=AccessLog.AccessMethod.RFID if access_code.code_type == AccessCode.CodeType.RFID else AccessLog.AccessMethod.NUMERIC_CODE,
                    code_used=code,
                    access_code=access_code,
                    status=AccessLog.Status.DENIED,
                    denial_reason='Access point not authorized',
                    authorized_by=request.user
                )
                
                return Response(
                    {'valid': False, 'error': 'Access point not authorized'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Log successful access
            AccessLog.objects.create(
                resident=access_code.resident,
                person_name=access_code.resident.full_name,
                person_document=access_code.resident.document_id,
                access_point=access_point,
                access_type=access_type,
                access_method=AccessLog.AccessMethod.RFID if access_code.code_type == AccessCode.CodeType.RFID else AccessLog.AccessMethod.NUMERIC_CODE,
                code_used=code,
                access_code=access_code,
                status=AccessLog.Status.SUCCESS,
                authorized_by=request.user
            )
            
            return Response({
                'valid': True,
                'person_type': 'resident',
                'person_name': access_code.resident.full_name,
                'unit': str(access_code.resident.unit)
            })
            
        except AccessCode.DoesNotExist:
            # Try temporary codes
            try:
                temp_code = TemporaryCode.objects.select_related('visitor').get(code=code)
                
                if not temp_code.is_valid:
                    error = 'Code has expired' if temp_code.is_expired else 'Code is not active or has been used'
                    
                    # Log denied access
                    AccessLog.objects.create(
                        visitor=temp_code.visitor,
                        person_name=temp_code.visitor.full_name,
                        person_document=temp_code.visitor.document_id,
                        access_point=access_point,
                        access_type=access_type,
                        access_method=AccessLog.AccessMethod.QR_CODE if temp_code.code_type == TemporaryCode.CodeType.QR else AccessLog.AccessMethod.ALPHANUMERIC_CODE,
                        code_used=code,
                        temporary_code=temp_code,
                        status=AccessLog.Status.DENIED,
                        denial_reason=error,
                        authorized_by=request.user
                    )
                    
                    return Response(
                        {'valid': False, 'error': error},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Increment usage
                temp_code.increment_usage()
                
                # Update visitor status
                visitor = temp_code.visitor
                if access_type == 'ENTRY' and visitor.status != visitor.Status.CHECKED_IN:
                    visitor.status = visitor.Status.CHECKED_IN
                    visitor.check_in_time = timezone.now()
                    visitor.save()
                elif access_type == 'EXIT' and visitor.status == visitor.Status.CHECKED_IN:
                    visitor.status = visitor.Status.CHECKED_OUT
                    visitor.check_out_time = timezone.now()
                    visitor.save()
                
                # Log successful access
                AccessLog.objects.create(
                    visitor=visitor,
                    person_name=visitor.full_name,
                    person_document=visitor.document_id,
                    access_point=access_point,
                    access_type=access_type,
                    access_method=AccessLog.AccessMethod.QR_CODE if temp_code.code_type == TemporaryCode.CodeType.QR else AccessLog.AccessMethod.ALPHANUMERIC_CODE,
                    code_used=code,
                    temporary_code=temp_code,
                    status=AccessLog.Status.SUCCESS,
                    authorized_by=request.user
                )
                
                return Response({
                    'valid': True,
                    'person_type': 'visitor',
                    'person_name': visitor.full_name,
                    'unit': str(visitor.unit)
                })
                
            except TemporaryCode.DoesNotExist:
                # Log denied access - code not found
                AccessLog.objects.create(
                    person_name='Unknown',
                    access_point=access_point,
                    access_type=access_type,
                    access_method=AccessLog.AccessMethod.OTHER,
                    code_used=code,
                    status=AccessLog.Status.DENIED,
                    denial_reason='Invalid code',
                    authorized_by=request.user
                )
                
                return Response(
                    {'valid': False, 'error': 'Invalid code'},
                    status=status.HTTP_404_NOT_FOUND
                )

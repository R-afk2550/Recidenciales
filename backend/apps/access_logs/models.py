"""
Access Logs models for Access Control System
"""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class AccessLog(models.Model):
    """
    Log of all access events in the system
    """
    
    class AccessType(models.TextChoices):
        ENTRY = 'ENTRY', _('Entry')
        EXIT = 'EXIT', _('Exit')
    
    class AccessMethod(models.TextChoices):
        QR_CODE = 'QR_CODE', _('QR Code')
        RFID = 'RFID', _('RFID Card')
        NUMERIC_CODE = 'NUMERIC_CODE', _('Numeric Code')
        ALPHANUMERIC_CODE = 'ALPHANUMERIC_CODE', _('Alphanumeric Code')
        MANUAL = 'MANUAL', _('Manual Entry')
        BIOMETRIC = 'BIOMETRIC', _('Biometric')
        OTHER = 'OTHER', _('Other')
    
    class Status(models.TextChoices):
        SUCCESS = 'SUCCESS', _('Success')
        DENIED = 'DENIED', _('Denied')
        ERROR = 'ERROR', _('Error')
    
    # Who accessed
    resident = models.ForeignKey(
        'residents.Resident',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='access_logs',
        help_text=_('Resident (if applicable)')
    )
    
    visitor = models.ForeignKey(
        'visitors.Visitor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='access_logs',
        help_text=_('Visitor (if applicable)')
    )
    
    person_name = models.CharField(
        max_length=200,
        help_text=_('Name of person accessing')
    )
    
    person_document = models.CharField(
        max_length=50,
        blank=True,
        help_text=_('Document ID of person')
    )
    
    # Where and how
    access_point = models.ForeignKey(
        'access_control.AccessPoint',
        on_delete=models.SET_NULL,
        null=True,
        related_name='access_logs',
        help_text=_('Access point used')
    )
    
    access_type = models.CharField(
        max_length=20,
        choices=AccessType.choices,
        default=AccessType.ENTRY,
        help_text=_('Type of access (entry/exit)')
    )
    
    access_method = models.CharField(
        max_length=30,
        choices=AccessMethod.choices,
        help_text=_('Method used to access')
    )
    
    # Code/credentials used
    code_used = models.CharField(
        max_length=100,
        blank=True,
        help_text=_('Code or credential used')
    )
    
    temporary_code = models.ForeignKey(
        'visitors.TemporaryCode',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='access_logs',
        help_text=_('Temporary code used (if applicable)')
    )
    
    access_code = models.ForeignKey(
        'access_control.AccessCode',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='access_logs',
        help_text=_('Permanent access code used (if applicable)')
    )
    
    # Result
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SUCCESS,
        help_text=_('Access status')
    )
    
    denial_reason = models.TextField(
        blank=True,
        help_text=_('Reason for denial (if denied)')
    )
    
    # Metadata
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text=_('When the access occurred')
    )
    
    vehicle_plate = models.CharField(
        max_length=20,
        blank=True,
        help_text=_('Vehicle plate (if applicable)')
    )
    
    temperature = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        help_text=_('Temperature reading (if applicable)')
    )
    
    photo = models.ImageField(
        upload_to='logs/photos/',
        blank=True,
        null=True,
        help_text=_('Photo taken at access point')
    )
    
    authorized_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='authorized_access_logs',
        help_text=_('Guard who authorized (for manual entry)')
    )
    
    notes = models.TextField(
        blank=True,
        help_text=_('Additional notes')
    )
    
    # IP and device info
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text=_('IP address of access point device')
    )
    
    device_id = models.CharField(
        max_length=100,
        blank=True,
        help_text=_('Device identifier')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Access Log')
        verbose_name_plural = _('Access Logs')
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['resident', '-timestamp']),
            models.Index(fields=['visitor', '-timestamp']),
            models.Index(fields=['access_point', '-timestamp']),
            models.Index(fields=['status', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.person_name} - {self.get_access_type_display()} at {self.timestamp}"
    
    @property
    def is_successful(self):
        """Check if access was successful"""
        return self.status == self.Status.SUCCESS
    
    @property
    def is_entry(self):
        """Check if this is an entry log"""
        return self.access_type == self.AccessType.ENTRY
    
    @property
    def is_exit(self):
        """Check if this is an exit log"""
        return self.access_type == self.AccessType.EXIT

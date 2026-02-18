"""
Visitors models for Access Control System
"""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from utils.validators import validate_phone_number


class Visitor(models.Model):
    """
    Visitor registered in the system
    """
    
    class VisitorType(models.TextChoices):
        GUEST = 'GUEST', _('Guest')
        DELIVERY = 'DELIVERY', _('Delivery')
        SERVICE = 'SERVICE', _('Service Provider')
        CONTRACTOR = 'CONTRACTOR', _('Contractor')
        OTHER = 'OTHER', _('Other')
    
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        APPROVED = 'APPROVED', _('Approved')
        CHECKED_IN = 'CHECKED_IN', _('Checked In')
        CHECKED_OUT = 'CHECKED_OUT', _('Checked Out')
        DENIED = 'DENIED', _('Denied')
    
    first_name = models.CharField(
        max_length=100,
        help_text=_('Visitor first name')
    )
    
    last_name = models.CharField(
        max_length=100,
        help_text=_('Visitor last name')
    )
    
    document_id = models.CharField(
        max_length=50,
        blank=True,
        help_text=_('ID document number')
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[validate_phone_number],
        help_text=_('Contact phone number')
    )
    
    email = models.EmailField(
        blank=True,
        help_text=_('Email address')
    )
    
    photo = models.ImageField(
        upload_to='visitors/photos/',
        blank=True,
        null=True,
        help_text=_('Visitor photo')
    )
    
    visitor_type = models.CharField(
        max_length=20,
        choices=VisitorType.choices,
        default=VisitorType.GUEST,
        help_text=_('Type of visitor')
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        help_text=_('Current status')
    )
    
    unit = models.ForeignKey(
        'residents.Unit',
        on_delete=models.CASCADE,
        related_name='visitors',
        help_text=_('Unit being visited')
    )
    
    resident = models.ForeignKey(
        'residents.Resident',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='visitors',
        help_text=_('Resident being visited')
    )
    
    purpose = models.TextField(
        blank=True,
        help_text=_('Purpose of visit')
    )
    
    expected_date = models.DateField(
        help_text=_('Expected date of visit')
    )
    
    expected_time = models.TimeField(
        null=True,
        blank=True,
        help_text=_('Expected time of arrival')
    )
    
    vehicle_plate = models.CharField(
        max_length=20,
        blank=True,
        help_text=_('Vehicle license plate number')
    )
    
    company = models.CharField(
        max_length=200,
        blank=True,
        help_text=_('Company name (for delivery/service)')
    )
    
    authorized_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='authorized_visitors',
        help_text=_('User who authorized this visitor')
    )
    
    check_in_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('Actual check-in time')
    )
    
    check_out_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('Actual check-out time')
    )
    
    notes = models.TextField(
        blank=True,
        help_text=_('Additional notes')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Visitor')
        verbose_name_plural = _('Visitors')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.unit} ({self.get_status_display()})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_currently_inside(self):
        """Check if visitor is currently checked in"""
        return self.status == self.Status.CHECKED_IN


class TemporaryCode(models.Model):
    """
    Temporary access codes for visitors
    """
    
    class CodeType(models.TextChoices):
        NUMERIC = 'NUMERIC', _('Numeric Code')
        ALPHANUMERIC = 'ALPHANUMERIC', _('Alphanumeric Code')
        QR = 'QR', _('QR Code')
        OTP = 'OTP', _('One-Time Password')
    
    visitor = models.ForeignKey(
        Visitor,
        on_delete=models.CASCADE,
        related_name='access_codes',
        help_text=_('Visitor this code belongs to')
    )
    
    code = models.CharField(
        max_length=100,
        unique=True,
        help_text=_('The access code')
    )
    
    code_type = models.CharField(
        max_length=20,
        choices=CodeType.choices,
        default=CodeType.ALPHANUMERIC,
        help_text=_('Type of code')
    )
    
    qr_code_image = models.ImageField(
        upload_to='codes/qr/',
        blank=True,
        null=True,
        help_text=_('QR code image')
    )
    
    secret_key = models.CharField(
        max_length=100,
        blank=True,
        help_text=_('Secret key for OTP generation')
    )
    
    valid_from = models.DateTimeField(
        default=timezone.now,
        help_text=_('Code valid from this time')
    )
    
    valid_until = models.DateTimeField(
        help_text=_('Code expires at this time')
    )
    
    max_uses = models.PositiveIntegerField(
        default=1,
        help_text=_('Maximum number of times this code can be used')
    )
    
    times_used = models.PositiveIntegerField(
        default=0,
        help_text=_('Number of times this code has been used')
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text=_('Whether this code is active')
    )
    
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='generated_codes',
        help_text=_('User who generated this code')
    )
    
    last_used_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('Last time this code was used')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Temporary Code')
        verbose_name_plural = _('Temporary Codes')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.code} - {self.visitor.full_name}"
    
    @property
    def is_valid(self):
        """Check if code is currently valid"""
        now = timezone.now()
        return (
            self.is_active and
            self.valid_from <= now <= self.valid_until and
            self.times_used < self.max_uses
        )
    
    @property
    def is_expired(self):
        """Check if code has expired"""
        return timezone.now() > self.valid_until
    
    def increment_usage(self):
        """Increment the usage counter"""
        self.times_used += 1
        self.last_used_at = timezone.now()
        if self.times_used >= self.max_uses:
            self.is_active = False
        self.save()

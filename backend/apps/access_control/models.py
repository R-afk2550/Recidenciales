"""
Access Control models for Access Control System
"""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from utils.validators import validate_rfid_code


class AccessPoint(models.Model):
    """
    Physical access points (doors, gates, etc.)
    """
    
    class AccessType(models.TextChoices):
        MAIN_GATE = 'MAIN_GATE', _('Main Gate')
        PEDESTRIAN = 'PEDESTRIAN', _('Pedestrian Door')
        VEHICLE = 'VEHICLE', _('Vehicle Gate')
        BUILDING_DOOR = 'BUILDING_DOOR', _('Building Door')
        GARAGE = 'GARAGE', _('Garage')
        POOL = 'POOL', _('Pool/Amenities')
        GYM = 'GYM', _('Gym')
        OTHER = 'OTHER', _('Other')
    
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text=_('Access point name')
    )
    
    code = models.CharField(
        max_length=20,
        unique=True,
        help_text=_('Short code identifier')
    )
    
    access_type = models.CharField(
        max_length=20,
        choices=AccessType.choices,
        default=AccessType.MAIN_GATE,
        help_text=_('Type of access point')
    )
    
    location = models.CharField(
        max_length=200,
        help_text=_('Physical location description')
    )
    
    building = models.ForeignKey(
        'residents.Building',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='access_points',
        help_text=_('Associated building (if any)')
    )
    
    supports_qr = models.BooleanField(
        default=True,
        help_text=_('Supports QR code scanning')
    )
    
    supports_rfid = models.BooleanField(
        default=False,
        help_text=_('Supports RFID card reading')
    )
    
    supports_numeric = models.BooleanField(
        default=True,
        help_text=_('Supports numeric code entry')
    )
    
    is_entry = models.BooleanField(
        default=True,
        help_text=_('Is this an entry point')
    )
    
    is_exit = models.BooleanField(
        default=True,
        help_text=_('Is this an exit point')
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text=_('Whether this access point is active')
    )
    
    notes = models.TextField(
        blank=True,
        help_text=_('Additional notes')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Access Point')
        verbose_name_plural = _('Access Points')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class AccessCode(models.Model):
    """
    Permanent access codes (RFID, PIN, etc.)
    """
    
    class CodeType(models.TextChoices):
        RFID = 'RFID', _('RFID Card')
        PIN = 'PIN', _('PIN Code')
        BIOMETRIC = 'BIOMETRIC', _('Biometric')
        OTHER = 'OTHER', _('Other')
    
    resident = models.ForeignKey(
        'residents.Resident',
        on_delete=models.CASCADE,
        related_name='access_codes',
        help_text=_('Resident this code belongs to')
    )
    
    code = models.CharField(
        max_length=100,
        unique=True,
        help_text=_('The access code/card number')
    )
    
    code_type = models.CharField(
        max_length=20,
        choices=CodeType.choices,
        default=CodeType.RFID,
        help_text=_('Type of access code')
    )
    
    access_points = models.ManyToManyField(
        AccessPoint,
        blank=True,
        related_name='allowed_codes',
        help_text=_('Access points where this code is valid')
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text=_('Whether this code is active')
    )
    
    issued_date = models.DateField(
        auto_now_add=True,
        help_text=_('Date when code was issued')
    )
    
    expiry_date = models.DateField(
        null=True,
        blank=True,
        help_text=_('Expiry date (if applicable)')
    )
    
    issued_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='issued_access_codes',
        help_text=_('User who issued this code')
    )
    
    notes = models.TextField(
        blank=True,
        help_text=_('Additional notes')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Access Code')
        verbose_name_plural = _('Access Codes')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.code} - {self.resident.full_name}"
    
    @property
    def is_valid(self):
        """Check if code is currently valid"""
        if not self.is_active:
            return False
        if self.expiry_date and self.expiry_date < timezone.now().date():
            return False
        return True

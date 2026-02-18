"""
Residents models for Access Control System
"""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from utils.validators import validate_phone_number, validate_unit_number


class Building(models.Model):
    """
    Building or Tower in the residential complex
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text=_('Building name or identifier')
    )
    
    code = models.CharField(
        max_length=10,
        unique=True,
        help_text=_('Short code for the building (e.g., A, B, T1)')
    )
    
    address = models.TextField(
        blank=True,
        help_text=_('Physical address of the building')
    )
    
    floors = models.PositiveIntegerField(
        default=1,
        help_text=_('Number of floors in the building')
    )
    
    units_per_floor = models.PositiveIntegerField(
        default=1,
        help_text=_('Number of units per floor')
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text=_('Whether this building is active')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Building')
        verbose_name_plural = _('Buildings')
        ordering = ['code', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class Unit(models.Model):
    """
    Unit or Apartment in a building
    """
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='units',
        help_text=_('Building this unit belongs to')
    )
    
    number = models.CharField(
        max_length=10,
        validators=[validate_unit_number],
        help_text=_('Unit number (e.g., 101, 2A, PH1)')
    )
    
    floor = models.PositiveIntegerField(
        help_text=_('Floor number')
    )
    
    owner_name = models.CharField(
        max_length=200,
        blank=True,
        help_text=_('Name of the unit owner')
    )
    
    owner_phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[validate_phone_number],
        help_text=_('Owner contact phone')
    )
    
    is_occupied = models.BooleanField(
        default=True,
        help_text=_('Whether this unit is currently occupied')
    )
    
    notes = models.TextField(
        blank=True,
        help_text=_('Additional notes about the unit')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')
        ordering = ['building', 'floor', 'number']
        unique_together = ['building', 'number']
    
    def __str__(self):
        return f"{self.building.code}-{self.number}"


class Resident(models.Model):
    """
    Resident living in a unit
    """
    
    class ResidentType(models.TextChoices):
        OWNER = 'OWNER', _('Owner')
        TENANT = 'TENANT', _('Tenant')
        FAMILY = 'FAMILY', _('Family Member')
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resident_profile',
        help_text=_('Associated user account')
    )
    
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name='residents',
        help_text=_('Unit where resident lives')
    )
    
    first_name = models.CharField(
        max_length=100,
        help_text=_('First name')
    )
    
    last_name = models.CharField(
        max_length=100,
        help_text=_('Last name')
    )
    
    document_id = models.CharField(
        max_length=50,
        unique=True,
        help_text=_('ID document number')
    )
    
    phone = models.CharField(
        max_length=20,
        validators=[validate_phone_number],
        help_text=_('Primary phone number')
    )
    
    email = models.EmailField(
        blank=True,
        help_text=_('Email address')
    )
    
    photo = models.ImageField(
        upload_to='residents/photos/',
        blank=True,
        null=True,
        help_text=_('Resident photo')
    )
    
    resident_type = models.CharField(
        max_length=20,
        choices=ResidentType.choices,
        default=ResidentType.OWNER,
        help_text=_('Type of resident')
    )
    
    emergency_contact_name = models.CharField(
        max_length=200,
        blank=True,
        help_text=_('Emergency contact name')
    )
    
    emergency_contact_phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[validate_phone_number],
        help_text=_('Emergency contact phone')
    )
    
    is_authorized = models.BooleanField(
        default=True,
        help_text=_('Whether resident has access authorization')
    )
    
    move_in_date = models.DateField(
        null=True,
        blank=True,
        help_text=_('Date when resident moved in')
    )
    
    move_out_date = models.DateField(
        null=True,
        blank=True,
        help_text=_('Date when resident moved out')
    )
    
    notes = models.TextField(
        blank=True,
        help_text=_('Additional notes')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Resident')
        verbose_name_plural = _('Residents')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.unit}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_active(self):
        """Check if resident is currently active (authorized and not moved out)"""
        return self.is_authorized and (self.move_out_date is None)

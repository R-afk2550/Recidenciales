"""
User models for Access Control System
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    
    Roles:
    - ADMIN: System administrator
    - GUARD: Security guard
    - RESIDENT: Resident user
    """
    
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Administrator')
        GUARD = 'GUARD', _('Security Guard')
        RESIDENT = 'RESIDENT', _('Resident')
    
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.GUARD,
        help_text=_('User role in the system')
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text=_('Contact phone number')
    )
    
    photo = models.ImageField(
        upload_to='users/photos/',
        blank=True,
        null=True,
        help_text=_('User profile photo')
    )
    
    is_active_employee = models.BooleanField(
        default=True,
        help_text=_('Whether this employee is currently active')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN
    
    @property
    def is_guard(self):
        return self.role == self.Role.GUARD
    
    @property
    def is_resident_user(self):
        return self.role == self.Role.RESIDENT

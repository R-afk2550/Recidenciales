"""
Custom validators for Access Control System
"""
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


def validate_phone_number(value):
    """
    Validate phone number format
    
    Accepts formats like: +1234567890, 1234567890, (123) 456-7890
    """
    # Remove common formatting characters
    cleaned = re.sub(r'[\s\-\(\)]', '', value)
    
    # Check if it contains only digits and optional leading +
    if not re.match(r'^\+?\d{10,15}$', cleaned):
        raise ValidationError(
            _('%(value)s is not a valid phone number'),
            params={'value': value},
        )


def validate_code_format(value):
    """
    Validate access code format (alphanumeric, 6-12 characters)
    """
    if not re.match(r'^[A-Z0-9]{6,12}$', value):
        raise ValidationError(
            _('Code must be 6-12 alphanumeric characters (uppercase)'),
        )


def validate_unit_number(value):
    """
    Validate unit/apartment number format
    """
    if not re.match(r'^[A-Z0-9\-]{1,10}$', value.upper()):
        raise ValidationError(
            _('Unit number must be 1-10 alphanumeric characters'),
        )


def validate_rfid_code(value):
    """
    Validate RFID code format (typically hex string)
    """
    if not re.match(r'^[A-F0-9]{8,16}$', value.upper()):
        raise ValidationError(
            _('RFID code must be 8-16 hexadecimal characters'),
        )


def validate_positive_integer(value):
    """
    Validate that a value is a positive integer
    """
    if value < 0:
        raise ValidationError(
            _('Value must be a positive integer'),
        )


def validate_dni_or_passport(value):
    """
    Validate DNI (ID) or Passport number format
    """
    # Allow letters and numbers, 5-20 characters
    if not re.match(r'^[A-Z0-9]{5,20}$', value.upper()):
        raise ValidationError(
            _('ID/Passport must be 5-20 alphanumeric characters'),
        )

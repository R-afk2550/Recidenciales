"""
Temporary Code Generator for Access Control System
"""
import pyotp
import secrets
import string
from datetime import datetime, timedelta
from django.utils import timezone


def generate_numeric_code(length=6):
    """
    Generate a random numeric code
    
    Args:
        length: Length of the code (default: 6)
        
    Returns:
        String containing numeric code
    """
    return ''.join(secrets.choice(string.digits) for _ in range(length))


def generate_alphanumeric_code(length=8):
    """
    Generate a random alphanumeric code
    
    Args:
        length: Length of the code (default: 8)
        
    Returns:
        String containing alphanumeric code
    """
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_otp(secret_key=None, interval=30):
    """
    Generate a Time-based One-Time Password (TOTP)
    
    Args:
        secret_key: Secret key for TOTP (generates new if None)
        interval: Time interval in seconds (default: 30)
        
    Returns:
        Tuple of (otp_code, secret_key)
    """
    if not secret_key:
        secret_key = pyotp.random_base32()
    
    totp = pyotp.TOTP(secret_key, interval=interval)
    otp_code = totp.now()
    
    return otp_code, secret_key


def verify_otp(otp_code, secret_key, interval=30, valid_window=1):
    """
    Verify a Time-based One-Time Password
    
    Args:
        otp_code: OTP code to verify
        secret_key: Secret key used to generate the OTP
        interval: Time interval in seconds (default: 30)
        valid_window: Number of intervals to check (default: 1)
        
    Returns:
        Boolean indicating if OTP is valid
    """
    totp = pyotp.TOTP(secret_key, interval=interval)
    return totp.verify(otp_code, valid_window=valid_window)


def generate_temporary_access_code(code_type='numeric', length=6):
    """
    Generate a temporary access code
    
    Args:
        code_type: Type of code ('numeric' or 'alphanumeric')
        length: Length of the code
        
    Returns:
        Generated code string
    """
    if code_type == 'numeric':
        return generate_numeric_code(length)
    elif code_type == 'alphanumeric':
        return generate_alphanumeric_code(length)
    else:
        raise ValueError(f"Unknown code type: {code_type}")


def calculate_expiry_time(hours=24):
    """
    Calculate expiry time for temporary codes
    
    Args:
        hours: Number of hours until expiry (default: 24)
        
    Returns:
        DateTime object representing expiry time
    """
    return timezone.now() + timedelta(hours=hours)


def is_code_expired(expiry_time):
    """
    Check if a code has expired
    
    Args:
        expiry_time: DateTime object representing expiry time
        
    Returns:
        Boolean indicating if code is expired
    """
    return timezone.now() > expiry_time


def generate_visitor_code(visitor_name, duration_hours=24):
    """
    Generate a complete visitor access code with metadata
    
    Args:
        visitor_name: Name of the visitor
        duration_hours: How long the code is valid (default: 24 hours)
        
    Returns:
        Dictionary with code, expiry, and metadata
    """
    code = generate_alphanumeric_code(8)
    expiry = calculate_expiry_time(duration_hours)
    
    return {
        'code': code,
        'expiry': expiry,
        'visitor_name': visitor_name,
        'created_at': timezone.now()
    }

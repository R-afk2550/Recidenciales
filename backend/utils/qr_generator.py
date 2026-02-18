"""
QR Code Generator for Access Control System
"""
import qrcode
from io import BytesIO
from PIL import Image
import base64


def generate_qr_code(data, size=300):
    """
    Generate a QR code from the given data
    
    Args:
        data: String data to encode in QR
        size: Size of the QR code in pixels (default: 300)
        
    Returns:
        BytesIO object containing the QR code image
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Resize if needed
    if size != 300:
        img = img.resize((size, size), Image.LANCZOS)
    
    # Save to BytesIO
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return buffer


def generate_qr_code_base64(data, size=300):
    """
    Generate a QR code and return it as base64 string
    
    Args:
        data: String data to encode in QR
        size: Size of the QR code in pixels (default: 300)
        
    Returns:
        Base64 encoded string of the QR code image
    """
    buffer = generate_qr_code(data, size)
    img_base64 = base64.b64encode(buffer.read()).decode()
    return f"data:image/png;base64,{img_base64}"


def generate_visitor_qr(visitor_code, visitor_name=None):
    """
    Generate QR code specifically for visitor access
    
    Args:
        visitor_code: Unique visitor code
        visitor_name: Optional visitor name
        
    Returns:
        BytesIO object containing the QR code image
    """
    data = f"VISITOR:{visitor_code}"
    if visitor_name:
        data += f"|{visitor_name}"
    
    return generate_qr_code(data)


def generate_access_qr(code_type, code_value, metadata=None):
    """
    Generate QR code for different access types
    
    Args:
        code_type: Type of access (VISITOR, DELIVERY, SERVICE, etc.)
        code_value: The actual code value
        metadata: Optional dictionary with additional data
        
    Returns:
        BytesIO object containing the QR code image
    """
    data = f"{code_type}:{code_value}"
    if metadata:
        for key, value in metadata.items():
            data += f"|{key}={value}"
    
    return generate_qr_code(data)

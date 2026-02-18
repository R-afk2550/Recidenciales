# 🔌 API Reference

Complete API reference for the Sistema de Control de Acceso Residencial.

## Base URL
- Development: `http://localhost:8000/api/`
- Production: `https://your-app.onrender.com/api/`

## Authentication

All API endpoints (except login) require JWT authentication.

### Headers
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

### Endpoints

#### POST /api/auth/login/
Obtain JWT access and refresh tokens.

**Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### POST /api/auth/refresh/
Refresh access token using refresh token.

**Request:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### POST /api/auth/verify/
Verify if a token is valid.

**Request:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## Users

### GET /api/users/
List all users (admins only).

**Query Parameters:**
- `search`: Search by username, email, name
- `ordering`: Order by field (e.g., `-date_joined`)

**Response:**
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@test.com",
      "role": "ADMIN",
      "is_active": true
    }
  ]
}
```

### GET /api/users/me/
Get current authenticated user profile.

### POST /api/users/
Create new user.

### GET /api/users/{id}/
Get user details.

### PUT /api/users/{id}/
Update user.

### DELETE /api/users/{id}/
Delete user.

---

## Buildings

### GET /api/buildings/
List all buildings.

**Response:**
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "name": "Torre A",
      "code": "A",
      "floors": 10,
      "units_per_floor": 4,
      "total_units": 3
    }
  ]
}
```

### POST /api/buildings/
Create new building.

### GET /api/buildings/{id}/
Get building details.

### PUT /api/buildings/{id}/
Update building.

### DELETE /api/buildings/{id}/
Delete building.

---

## Units

### GET /api/units/
List all units.

**Query Parameters:**
- `building`: Filter by building ID
- `search`: Search by number, owner name

**Response:**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "building": 1,
      "building_name": "Torre A",
      "number": "101",
      "floor": 1,
      "owner_name": "Carlos González",
      "is_occupied": true,
      "resident_count": 2
    }
  ]
}
```

### POST /api/units/
Create new unit.

### GET /api/units/{id}/
Get unit details.

### PUT /api/units/{id}/
Update unit.

### DELETE /api/units/{id}/
Delete unit.

---

## Residents

### GET /api/residents/
List all residents.

**Query Parameters:**
- `unit`: Filter by unit ID
- `building`: Filter by building ID
- `is_active`: Filter active residents
- `search`: Search by name, document, phone

**Response:**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "first_name": "Carlos",
      "last_name": "González",
      "full_name": "Carlos González",
      "document_id": "ID123456",
      "phone": "+52 55 9876 5432",
      "email": "carlos@email.com",
      "unit": 1,
      "unit_display": "A-101",
      "resident_type": "OWNER",
      "is_authorized": true,
      "is_active": true
    }
  ]
}
```

### POST /api/residents/
Create new resident.

### GET /api/residents/{id}/
Get resident details.

### PUT /api/residents/{id}/
Update resident.

### DELETE /api/residents/{id}/
Delete resident.

### GET /api/residents/list_minimal/
Get minimal resident list for dropdowns.

---

## Visitors

### GET /api/visitors/
List all visitors.

**Query Parameters:**
- `status`: Filter by status (PENDING, APPROVED, CHECKED_IN, etc.)
- `visitor_type`: Filter by type (GUEST, DELIVERY, SERVICE, etc.)
- `unit`: Filter by unit ID
- `search`: Search by name, document, company

**Response:**
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "first_name": "Juan",
      "last_name": "Pérez",
      "full_name": "Juan Pérez",
      "visitor_type": "GUEST",
      "status": "APPROVED",
      "unit": 1,
      "unit_display": "A-101",
      "resident_name": "Carlos González",
      "expected_date": "2026-02-18",
      "is_currently_inside": false
    }
  ]
}
```

### POST /api/visitors/
Register new visitor.

**Request:**
```json
{
  "first_name": "Juan",
  "last_name": "Pérez",
  "phone": "+52 55 1111 1111",
  "visitor_type": "GUEST",
  "unit": 1,
  "resident": 1,
  "purpose": "Visita social",
  "expected_date": "2026-02-18"
}
```

### POST /api/visitors/generate_code/
Generate temporary access code for visitor.

**Request:**
```json
{
  "visitor_id": 1,
  "code_type": "QR",
  "valid_hours": 24,
  "max_uses": 2
}
```

**Response:**
```json
{
  "id": 1,
  "visitor": 1,
  "code": "ABC123XYZ",
  "code_type": "QR",
  "qr_code_image": "/media/codes/qr/visitor_1.png",
  "valid_from": "2026-02-18T14:00:00Z",
  "valid_until": "2026-02-19T14:00:00Z",
  "is_valid": true
}
```

### POST /api/visitors/validate_code/
Validate visitor access code.

**Request:**
```json
{
  "code": "ABC123XYZ",
  "access_point_id": 1
}
```

**Response:**
```json
{
  "valid": true,
  "visitor": {
    "id": 1,
    "full_name": "Juan Pérez",
    "unit_display": "A-101"
  },
  "code": {
    "id": 1,
    "times_used": 1,
    "max_uses": 2
  }
}
```

---

## Temporary Codes

### GET /api/codes/
List temporary codes.

**Query Parameters:**
- `visitor`: Filter by visitor ID
- `is_active`: Filter active codes

---

## Access Points

### GET /api/access/points/
List all access points.

**Response:**
```json
{
  "count": 4,
  "results": [
    {
      "id": 1,
      "name": "Puerta Principal",
      "code": "MAIN-01",
      "access_type": "MAIN_GATE",
      "location": "Entrada principal",
      "supports_qr": true,
      "supports_rfid": true,
      "supports_numeric": true,
      "is_active": true
    }
  ]
}
```

### POST /api/access/points/
Create new access point.

### GET /api/access/points/{id}/
Get access point details.

### PUT /api/access/points/{id}/
Update access point.

### DELETE /api/access/points/{id}/
Delete access point.

---

## Access Codes

### GET /api/access/codes/
List all permanent access codes.

**Query Parameters:**
- `resident`: Filter by resident ID
- `is_active`: Filter active codes

**Response:**
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "resident": 1,
      "resident_name": "Carlos González",
      "code": "RFID123456",
      "code_type": "RFID",
      "is_active": true,
      "is_valid": true
    }
  ]
}
```

### POST /api/access/codes/
Create new access code.

### POST /api/access/codes/validate/
Validate access and log entry.

**Request:**
```json
{
  "code": "RFID123456",
  "access_point_id": 1,
  "access_type": "ENTRY"
}
```

**Response:**
```json
{
  "valid": true,
  "person_type": "resident",
  "person_name": "Carlos González",
  "unit": "A-101"
}
```

---

## Access Logs

### GET /api/logs/
List access logs.

**Query Parameters:**
- `resident`: Filter by resident ID
- `visitor`: Filter by visitor ID
- `access_point`: Filter by access point ID
- `access_type`: Filter by type (ENTRY, EXIT)
- `status`: Filter by status (SUCCESS, DENIED)
- `date_from`: Filter from date
- `date_to`: Filter to date

**Response:**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "person_name": "Carlos González",
      "access_point_name": "Puerta Principal",
      "access_type": "ENTRY",
      "access_method": "RFID",
      "status": "SUCCESS",
      "timestamp": "2026-02-18T13:00:00Z"
    }
  ]
}
```

### GET /api/logs/{id}/
Get log details.

### GET /api/logs/stats/
Get access statistics.

**Query Parameters:**
- `days`: Number of days to include (default: 7)

**Response:**
```json
{
  "total_accesses": 100,
  "successful_accesses": 95,
  "denied_accesses": 5,
  "entries": 52,
  "exits": 48,
  "unique_residents": 15,
  "unique_visitors": 8,
  "by_access_method": {
    "RFID": 60,
    "QR_CODE": 30,
    "NUMERIC_CODE": 10
  },
  "by_access_point": {
    "Puerta Principal": 70,
    "Garage": 30
  },
  "recent_accesses": [...]
}
```

### GET /api/logs/resident_logs/
Get logs for specific resident.

**Query Parameters:**
- `resident_id`: Resident ID (required)

### GET /api/logs/visitor_logs/
Get logs for specific visitor.

**Query Parameters:**
- `visitor_id`: Visitor ID (required)

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid data",
  "details": {
    "field": ["Error message"]
  }
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. This should be added in production.

## Pagination

All list endpoints support pagination:
- Default page size: 20
- Query parameters: `?page=2&page_size=50`

## Filtering & Search

Most list endpoints support:
- **Search**: `?search=query`
- **Ordering**: `?ordering=-created_at`
- **Filtering**: `?status=APPROVED&unit=1`

---

## Code Types

### Visitor Code Types
- `NUMERIC`: 6-digit numeric code
- `ALPHANUMERIC`: 8-character code
- `QR`: QR code image
- `OTP`: Time-based one-time password

### Access Code Types
- `RFID`: RFID card
- `PIN`: PIN code
- `BIOMETRIC`: Biometric access
- `OTHER`: Other types

### Access Point Types
- `MAIN_GATE`: Main gate
- `PEDESTRIAN`: Pedestrian door
- `VEHICLE`: Vehicle gate
- `BUILDING_DOOR`: Building door
- `GARAGE`: Garage
- `POOL`: Pool/Amenities
- `GYM`: Gym
- `OTHER`: Other

### User Roles
- `ADMIN`: System administrator
- `GUARD`: Security guard
- `RESIDENT`: Resident user

### Visitor Types
- `GUEST`: Guest
- `DELIVERY`: Delivery
- `SERVICE`: Service provider
- `CONTRACTOR`: Contractor
- `OTHER`: Other

### Visitor Status
- `PENDING`: Pending approval
- `APPROVED`: Approved
- `CHECKED_IN`: Currently inside
- `CHECKED_OUT`: Left
- `DENIED`: Access denied

### Resident Types
- `OWNER`: Owner
- `TENANT`: Tenant
- `FAMILY`: Family member

### Access Types
- `ENTRY`: Entry
- `EXIT`: Exit

### Access Methods
- `QR_CODE`: QR code
- `RFID`: RFID card
- `NUMERIC_CODE`: Numeric code
- `ALPHANUMERIC_CODE`: Alphanumeric code
- `MANUAL`: Manual entry
- `BIOMETRIC`: Biometric
- `OTHER`: Other

### Access Log Status
- `SUCCESS`: Successful access
- `DENIED`: Access denied
- `ERROR`: Error occurred

---

## Best Practices

1. **Always include Authorization header** with valid JWT token
2. **Use proper HTTP methods**: GET for reading, POST for creating, PUT for updating, DELETE for deleting
3. **Check response status codes** before parsing response
4. **Handle pagination** for list endpoints
5. **Use filters** to reduce data transfer
6. **Validate data** before sending
7. **Handle errors gracefully**
8. **Refresh tokens** before they expire (60 min lifetime)
9. **Log all access attempts** for audit trail
10. **Use HTTPS** in production

---

**Last Updated**: February 18, 2026  
**API Version**: 1.0  
**Django Version**: 5.2.11  
**DRF Version**: 3.14+

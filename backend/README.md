# 🏘️ Sistema de Control de Acceso Residencial - Backend

Backend API desarrollado con Django y Django REST Framework para el sistema de control de acceso residencial.

## 📋 Características

- ✅ **Gestión de Residentes**: Administración de edificios, unidades y residentes
- ✅ **Control de Visitantes**: Registro y gestión de visitantes con códigos temporales
- ✅ **Códigos de Acceso**: Generación de códigos QR, numéricos y RFID
- ✅ **Registro de Accesos**: Historial completo de entradas y salidas
- ✅ **API REST**: Endpoints completos para todas las funcionalidades
- ✅ **Autenticación JWT**: Sistema de autenticación seguro con tokens
- ✅ **Admin Personalizado**: Panel de administración de Django customizado

## 🛠️ Stack Tecnológico

- **Framework**: Django 5.0+
- **API**: Django REST Framework 3.14+
- **Base de datos**: PostgreSQL (SQLite para desarrollo)
- **Autenticación**: JWT (djangorestframework-simplejwt)
- **Códigos QR**: qrcode + Pillow
- **Códigos OTP**: pyotp
- **CORS**: django-cors-headers
- **Static Files**: WhiteNoise
- **Variables de entorno**: python-decouple

## 📦 Instalación

### Requisitos Previos

- Python 3.10 o superior
- PostgreSQL (opcional, SQLite para desarrollo)
- pip

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/R-afk2550/Recidenciales.git
cd Recidenciales/backend
```

2. **Crear y activar entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. **Ejecutar migraciones**
```bash
python manage.py migrate
```

6. **Crear superusuario**
```bash
python manage.py createsuperuser
```

7. **Recolectar archivos estáticos (producción)**
```bash
python manage.py collectstatic
```

8. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000`

## 🗂️ Estructura del Proyecto

```
backend/
├── config/                         # Configuración principal
│   ├── settings.py                # Configuración de Django
│   ├── urls.py                    # URLs principales
│   ├── wsgi.py                    # WSGI para producción
│   └── asgi.py                    # ASGI para async
├── apps/                          # Aplicaciones del proyecto
│   ├── users/                     # Gestión de usuarios
│   ├── residents/                 # Gestión de residentes
│   ├── visitors/                  # Gestión de visitantes
│   ├── access_control/            # Control de acceso
│   └── access_logs/               # Registro de accesos
├── utils/                         # Utilidades
│   ├── qr_generator.py           # Generación de QR
│   ├── code_generator.py         # Generación de códigos
│   └── validators.py             # Validadores custom
├── static/                        # Archivos estáticos
├── media/                         # Archivos subidos
├── manage.py                      # CLI de Django
├── requirements.txt               # Dependencias
├── .env.example                   # Ejemplo de variables de entorno
├── .gitignore                     # Archivos ignorados por git
├── build.sh                       # Script de build para Render
└── render.yaml                    # Configuración de Render

```

## 🔌 API Endpoints

### Autenticación

- `POST /api/auth/login/` - Obtener token JWT
- `POST /api/auth/refresh/` - Refrescar token
- `POST /api/auth/verify/` - Verificar token

### Usuarios

- `GET /api/users/` - Listar usuarios
- `POST /api/users/` - Crear usuario
- `GET /api/users/{id}/` - Detalle de usuario
- `PUT /api/users/{id}/` - Actualizar usuario
- `DELETE /api/users/{id}/` - Eliminar usuario
- `GET /api/users/me/` - Perfil del usuario actual

### Edificios y Unidades

- `GET /api/buildings/` - Listar edificios
- `POST /api/buildings/` - Crear edificio
- `GET /api/units/` - Listar unidades
- `POST /api/units/` - Crear unidad

### Residentes

- `GET /api/residents/` - Listar residentes
- `POST /api/residents/` - Crear residente
- `GET /api/residents/{id}/` - Detalle de residente
- `PUT /api/residents/{id}/` - Actualizar residente
- `DELETE /api/residents/{id}/` - Eliminar residente

### Visitantes

- `GET /api/visitors/` - Listar visitantes
- `POST /api/visitors/` - Registrar visitante
- `GET /api/visitors/{id}/` - Detalle de visitante
- `POST /api/visitors/generate_code/` - Generar código temporal
- `POST /api/visitors/validate_code/` - Validar código

### Control de Acceso

- `GET /api/access/points/` - Listar puntos de acceso
- `POST /api/access/points/` - Crear punto de acceso
- `GET /api/access/codes/` - Listar códigos de acceso
- `POST /api/access/codes/` - Crear código de acceso
- `POST /api/access/codes/validate/` - Validar acceso

### Registro de Accesos

- `GET /api/logs/` - Listar accesos
- `GET /api/logs/{id}/` - Detalle de acceso
- `GET /api/logs/stats/` - Estadísticas de accesos
- `GET /api/logs/resident_logs/` - Accesos de un residente
- `GET /api/logs/visitor_logs/` - Accesos de un visitante

## 🔐 Autenticación

El sistema utiliza JWT (JSON Web Tokens) para la autenticación:

1. **Obtener token**:
```bash
POST /api/auth/login/
{
  "username": "usuario",
  "password": "contraseña"
}
```

Respuesta:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

2. **Usar token en requests**:
```bash
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## 🎨 Panel de Administración

Accede al panel de administración en `http://localhost:8000/admin/`

- Gestión completa de todos los modelos
- Búsqueda y filtros avanzados
- Acciones masivas
- Visualización de estadísticas

## 🌐 Deployment en Render

1. **Crear cuenta en Render**: https://render.com
2. **Conectar repositorio de GitHub**
3. **Configurar variables de entorno**:
   - `SECRET_KEY`: Clave secreta de Django
   - `DEBUG`: False
   - `ALLOWED_HOSTS`: tu-dominio.onrender.com
   - `DATABASE_URL`: Automático desde Render PostgreSQL
   - `CORS_ALLOWED_ORIGINS`: URLs permitidas para CORS

4. **Deploy automático**: Render detectará el `render.yaml` y hará el deploy

## 🔧 Variables de Entorno

Copia `.env.example` a `.env` y configura:

```env
SECRET_KEY=tu-clave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos (opcional para desarrollo)
DATABASE_URL=postgresql://user:password@localhost:5432/recidenciales

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

## 🧪 Testing

```bash
# Ejecutar tests
python manage.py test

# Con coverage
coverage run manage.py test
coverage report
```

## 📝 Modelos Principales

### CustomUser
- Usuario personalizado con roles (Admin, Guard, Resident)

### Building
- Edificios o torres del residencial

### Unit
- Unidades o departamentos

### Resident
- Residentes con información personal y de contacto

### Visitor
- Visitantes registrados

### TemporaryCode
- Códigos temporales para visitantes (QR, numéricos, OTP)

### AccessPoint
- Puntos de acceso físicos (puertas, portones, etc.)

### AccessCode
- Códigos de acceso permanentes (RFID, PIN)

### AccessLog
- Registro de todos los accesos

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👨‍💻 Autor

**R-afk2550**

## 📞 Soporte

Para preguntas o soporte, abre un issue en GitHub.

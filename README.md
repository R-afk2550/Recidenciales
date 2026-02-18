# 🏘️ Sistema de Control de Acceso Residencial

Sistema completo de control de acceso para residenciales desarrollado con Django y Django REST Framework.

## 🚀 Características

- ✅ **Control de Acceso**: Gestión de entrada/salida de residentes y visitantes
- ✅ **Códigos Temporales**: Generación de códigos QR y numéricos para visitantes
- ✅ **Gestión de Residentes**: Base de datos completa de usuarios autorizados con edificios y unidades
- ✅ **Registro de Accesos**: Historial completo de entradas y salidas con estadísticas
- ✅ **Panel de Administración**: Interfaz web Django Admin personalizada
- ✅ **API REST**: Endpoints completos para integración con apps móviles
- ✅ **Soporte RFID**: Integración con lectores de tarjetas RFID
- ✅ **Autenticación JWT**: Sistema seguro de tokens para API
- ✅ **Generación de QR**: Códigos QR automáticos para visitantes
- ✅ **OTP**: Códigos de un solo uso basados en tiempo (TOTP)

## 🛠️ Stack Tecnológico

### Backend
- **Framework**: Django 5.0+
- **API**: Django REST Framework 3.14+
- **Base de datos**: PostgreSQL (SQLite para desarrollo)
- **Autenticación**: JWT (djangorestframework-simplejwt)
- **Códigos QR**: qrcode + Pillow
- **Códigos temporales**: pyotp
- **CORS**: django-cors-headers
- **Static Files**: WhiteNoise
- **WSGI**: Gunicorn

## 📦 Instalación Local

### Requisitos Previos
- Python 3.10 o superior
- PostgreSQL (opcional, SQLite para desarrollo)
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/R-afk2550/Recidenciales.git
cd Recidenciales/backend
```

2. **Crear entorno virtual**
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

6. **Poblar base de datos con datos de ejemplo (opcional)**
```bash
python manage.py populate_sample_data
```
Este comando crea:
- Usuario admin: `admin` / `admin123`
- Usuario guardia: `guard1` / `guard123`
- 2 edificios con 5 unidades
- 5 residentes
- 3 visitantes con códigos temporales
- 4 puntos de acceso
- Registros de acceso de ejemplo

7. **O crear superusuario manualmente**
```bash
python manage.py createsuperuser
```

8. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

Visita: 
- Admin: `http://localhost:8000/admin`
- API: `http://localhost:8000/api/`

## 📱 Estructura del Proyecto

```
Recidenciales/
├── backend/                    # Backend Django
│   ├── config/                # Configuración principal
│   ├── apps/                  # Aplicaciones Django
│   │   ├── users/            # Gestión de usuarios
│   │   ├── residents/        # Gestión de residentes
│   │   ├── visitors/         # Gestión de visitantes
│   │   ├── access_control/   # Control de acceso
│   │   └── access_logs/      # Registro de accesos
│   ├── utils/                # Utilidades (QR, códigos, validadores)
│   ├── static/               # Archivos estáticos
│   ├── media/                # Archivos subidos
│   ├── manage.py             # CLI de Django
│   ├── requirements.txt      # Dependencias Python
│   ├── build.sh             # Script de build para Render
│   ├── render.yaml          # Configuración de Render
│   └── README.md            # Documentación del backend
└── README.md                # Este archivo
```

## 🔌 API Endpoints

Ver la [documentación completa del backend](./backend/README.md) para una lista detallada de todos los endpoints.

### Endpoints Principales

**Autenticación**
- `POST /api/auth/login/` - Login JWT
- `POST /api/auth/refresh/` - Refresh token

**Residentes**
- `GET /api/residents/` - Listar residentes
- `POST /api/residents/` - Crear residente
- `GET /api/buildings/` - Listar edificios
- `GET /api/units/` - Listar unidades

**Visitantes**
- `POST /api/visitors/` - Registrar visitante
- `POST /api/visitors/generate_code/` - Generar código temporal
- `POST /api/visitors/validate_code/` - Validar código

**Control de Acceso**
- `POST /api/access/codes/validate/` - Validar acceso
- `GET /api/access/points/` - Listar puntos de acceso

**Logs**
- `GET /api/logs/` - Historial de accesos
- `GET /api/logs/stats/` - Estadísticas

## 🎨 Panel de Administración Django

El sistema incluye un panel de administración completo y personalizado:

### Características del Admin:
- ✅ Gestión visual de todos los modelos
- ✅ Búsqueda y filtros avanzados
- ✅ Acciones masivas
- ✅ Ordenamiento personalizado
- ✅ Campos de solo lectura para logs
- ✅ Autocompletado en relaciones
- ✅ Visualización jerárquica de datos

### Acceso al Admin:
```
URL: http://localhost:8000/admin/
Usuario: admin
Contraseña: admin123
```

### Módulos del Admin:
1. **Usuarios**: Gestión de admins, guardias y usuarios residentes
2. **Edificios y Unidades**: Administración de la infraestructura
3. **Residentes**: Base de datos de residentes autorizados
4. **Visitantes**: Registro y autorización de visitantes
5. **Códigos Temporales**: Gestión de códigos de acceso temporal
6. **Puntos de Acceso**: Configuración de puertas y entradas
7. **Códigos de Acceso**: Tarjetas RFID y PINs permanentes
8. **Logs de Acceso**: Historial completo (solo lectura)

## 🌐 Deployment en Render

### Pasos para Deployment:

1. **Crear cuenta en Render**: https://render.com

2. **Conectar repositorio de GitHub**

3. **Render detectará automáticamente** el archivo `render.yaml` con la configuración:
   - Web Service para el backend Django
   - PostgreSQL Database
   - Variables de entorno
   - Build command automático

4. **Configurar variables de entorno adicionales**:
   - `ALLOWED_HOSTS`: `tu-app.onrender.com`
   - `CORS_ALLOWED_ORIGINS`: URLs de tu frontend
   - Las demás se configuran automáticamente

5. **Deploy**: Render ejecutará automáticamente:
   - Instalación de dependencias
   - Migraciones de base de datos
   - Recolección de archivos estáticos
   - Inicio del servidor Gunicorn

### URLs después del deploy:
- Backend API: `https://tu-app.onrender.com/api/`
- Django Admin: `https://tu-app.onrender.com/admin/`

## 🔐 Seguridad

El sistema implementa múltiples capas de seguridad:

- ✅ **Autenticación JWT**: Tokens seguros para API
- ✅ **Permisos por roles**: Admin, Guardia, Residente
- ✅ **Variables de entorno**: Datos sensibles protegidos
- ✅ **CORS configurado**: Control de orígenes permitidos
- ✅ **Validación de datos**: Serializers con validación estricta
- ✅ **HTTPS en producción**: SSL/TLS obligatorio
- ✅ **Cookies seguras**: Session y CSRF cookies con flag secure
- ✅ **HSTS**: HTTP Strict Transport Security habilitado

## 📊 Modelos de Base de Datos

### Diagrama de Relaciones:

```
CustomUser (usuarios del sistema)
    ↓
Resident (residentes) → Unit (unidades) → Building (edificios)
    ↓
AccessCode (códigos permanentes) → AccessPoint (puntos de acceso)
    ↓
AccessLog (registro de accesos)
    ↑
Visitor (visitantes) → TemporaryCode (códigos temporales)
```

### Modelos Principales:

1. **CustomUser**: Usuarios del sistema (Admin, Guardia, Residente)
2. **Building**: Edificios o torres del residencial
3. **Unit**: Unidades o departamentos
4. **Resident**: Residentes con datos personales y de contacto
5. **Visitor**: Visitantes registrados con propósito y fecha
6. **TemporaryCode**: Códigos temporales (QR, numéricos, OTP)
7. **AccessPoint**: Puntos de acceso físicos (puertas, portones)
8. **AccessCode**: Códigos permanentes (RFID, PIN)
9. **AccessLog**: Registro inmutable de todos los accesos

## 🧪 Testing

```bash
# Ejecutar tests
python manage.py test

# Ejecutar tests con coverage
pip install coverage
coverage run manage.py test
coverage report
coverage html  # Genera reporte HTML
```

## 📝 Utilidades Incluidas

### 1. Generador de Códigos QR (`utils/qr_generator.py`)
- Generación de códigos QR para visitantes
- Soporte para diferentes tamaños
- Exportación a imagen o base64

### 2. Generador de Códigos Temporales (`utils/code_generator.py`)
- Códigos numéricos aleatorios
- Códigos alfanuméricos
- OTP basados en tiempo (TOTP)
- Verificación de códigos
- Cálculo de tiempo de expiración

### 3. Validadores Personalizados (`utils/validators.py`)
- Validación de números telefónicos
- Validación de formatos de códigos
- Validación de números de unidad
- Validación de códigos RFID
- Validación de documentos de identidad

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👨‍💻 Autor

**R-afk2550**

GitHub: [@R-afk2550](https://github.com/R-afk2550)

## 📞 Soporte

Para preguntas, sugerencias o reportar problemas:
- Abre un [Issue](https://github.com/R-afk2550/Recidenciales/issues) en GitHub
- Contacta al autor

## 🎯 Roadmap

### Próximas Características:
- [ ] Frontend con React/Vue
- [ ] App móvil con React Native
- [ ] Integración física con hardware RFID
- [ ] Sistema de notificaciones push
- [ ] Reportes avanzados y analytics
- [ ] Dashboard con gráficas en tiempo real
- [ ] Sistema de permisos granular
- [ ] API de webhooks para integraciones
- [ ] Soporte para múltiples residenciales
- [ ] Backup automático de base de datos

---

⭐ Si te gusta este proyecto, dale una estrella en GitHub
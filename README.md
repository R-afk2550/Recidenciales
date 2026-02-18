# 🏘️ Sistema de Control de Acceso Residencial

Sistema completo de control de acceso para residenciales desarrollado con Django y Django REST Framework.

## 🚀 Características

- ✅ **Control de Acceso**: Gestión de entrada/salida de residentes y visitantes
- ✅ **Códigos Temporales**: Generación de códigos QR y numéricos para visitantes
- ✅ **Gestión de Residentes**: Base de datos completa de usuarios autorizados
- ✅ **Registro de Accesos**: Historial completo de entradas y salidas
- ✅ **Panel de Administración**: Interfaz web para administradores
- ✅ **API REST**: Endpoints para integración con apps móviles
- ✅ **Soporte RFID**: Integración con lectores de tarjetas

## 🛠️ Stack Tecnológico

- **Backend**: Django 5.0+
- **API**: Django REST Framework
- **Base de datos**: PostgreSQL
- **Autenticación**: JWT (Simple JWT)
- **Códigos QR**: qrcode + Pillow
- **Códigos temporales**: pyotp

## 📦 Instalación Local

### Requisitos Previos
- Python 3.10+
- PostgreSQL (o usar SQLite para desarrollo)
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/R-afk2550/Recidenciales.git
cd Recidenciales
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

6. **Crear superusuario**
```bash
python manage.py createsuperuser
```

7. **Correr el servidor**
```bash
python manage.py runserver
```

Visita: `http://localhost:8000/admin`

## 📱 Estructura del Proyecto

```
backend/
├── config/              # Configuración principal
├── apps/
│   ├── residents/      # Gestión de residentes
│   ├── visitors/       # Visitantes y códigos temporales
│   ├── access_control/ # Control de acceso
│   ├── access_logs/    # Registro de accesos
│   └── users/          # Usuarios del sistema
├── utils/              # Utilidades (QR, códigos, etc.)
├── static/             # Archivos estáticos
└── media/              # Archivos subidos
```

## 🔌 API Endpoints

### Autenticación
- `POST /api/auth/login/` - Login
- `POST /api/auth/refresh/` - Refresh token

### Residentes
- `GET /api/residents/` - Listar residentes
- `POST /api/residents/` - Crear residente
- `GET /api/residents/{id}/` - Detalle

### Visitantes
- `POST /api/visitors/` - Registrar visitante
- `POST /api/visitors/generate-code/` - Generar código temporal
- `POST /api/visitors/validate-code/` - Validar código

### Control de Acceso
- `POST /api/access/validate/` - Validar acceso

### Logs
- `GET /api/logs/` - Historial de accesos
- `GET /api/logs/stats/` - Estadísticas

## 🌐 Deployment en Render

El proyecto está configurado para desplegarse fácilmente en Render.

1. Crear cuenta en [Render](https://render.com)
2. Conectar tu repositorio de GitHub
3. Configurar variables de entorno
4. Deploy automático 🚀

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👨‍💻 Autor

**R-afk2550**

## 📞 Soporte

Para preguntas o soporte, abre un issue en GitHub.

---

⭐ Si te gusta este proyecto, dale una estrella en GitHub
# Sistema de Gestión de Flota - PepsiCo Chile

Sistema web completo para la gestión de vehículos, mecánicos, repuestos y control de acceso en talleres.

## Características Principales

- **Gestión de Vehículos**: Registro y seguimiento de vehículos en taller
- **Control de Mecánicos**: Asignación de trabajos y seguimiento de progreso
- **Sistema de Repuestos**: Control de inventario y entregas
- **Control de Acceso**: Registro fotográfico de ingresos
- **Gestión de Llaves**: Control de entrega y devolución
- **Órdenes de Trabajo**: Flujo completo desde recepción hasta cierre
- **Roles de Usuario**: Sistema completo de permisos y accesos

## Requisitos

- Python 3.10+
- PowerShell (Windows)

## Instalación

### 1. Crear entorno virtual e instalar dependencias

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Inicializar base de datos

La base de datos se crea automáticamente al ejecutar la aplicación por primera vez.

### 3. Crear usuarios del sistema

Usar el script unificado `create_users.py`:

```powershell
# Crear administrador
python create_users.py --username admin --password admin123 --role admin

# Crear mecánico
python create_users.py --username juan --password pass123 --role mechanic --name "Juan Pérez" --phone "123456789"

# Crear asistente de repuestos
python create_users.py --username repuestos --password pass123 --role parts_assistant

# Crear encargado de llaves
python create_users.py --username llaves --password pass123 --role key_manager

# Crear recepcionista
python create_users.py --username recepcion --password pass123 --role receptionist

# Crear guardia
python create_users.py --username guardia --password pass123 --role guard
```

### 4. Ejecutar la aplicación

```powershell
python app.py
```

La aplicación estará disponible en `http://127.0.0.1:5000`

## Estructura del Proyecto

```
PROYECTO_PEPSICO/
├── app.py                      # Aplicación principal Flask
├── models.py                   # Modelos de base de datos
├── extensions.py               # Extensiones de Flask (db, login_manager)
├── create_users.py            # Script unificado para crear usuarios
├── create_sample_parts.py     # Script para crear repuestos de ejemplo
├── create_default_mechanic.py # Script para crear mecánico por defecto
├── db_utils.py                # Utilidades de inspección de BD
├── apply_migrations.py        # Script para aplicar migraciones
├── migrate.py                 # Configuración de Flask-Migrate
├── requirements.txt           # Dependencias del proyecto
├── run.ps1                    # Script de PowerShell para ejecutar
├── templates/                 # Plantillas HTML
├── static/                    # Archivos estáticos (CSS, imágenes)
├── migrations/                # Migraciones de base de datos
└── logs/                      # Logs de la aplicación
```

## Roles del Sistema

- **admin**: Administrador del sistema (acceso completo)
- **supervisor**: Jefe de taller (asigna mecánicos, aprueba vehículos)
- **mechanic**: Mecánico (ve sus órdenes de trabajo y solicita repuestos)
- **parts_assistant**: Asistente de repuestos (gestiona inventario y entregas)
- **key_manager**: Encargado de llaves (controla entrega/devolución)
- **receptionist**: Recepcionista (crea órdenes de trabajo)
- **guard**: Guardia de acceso (registra ingresos con fotos)
- **operator**: Operador general

## Utilidades

### Inspeccionar Base de Datos

```powershell
# Listar usuarios
python db_utils.py --list-users

# Listar tablas
python db_utils.py --list-tables

# Inspeccionar estructura de tabla
python db_utils.py --inspect-table vehicle

# Ver estadísticas
python db_utils.py --stats
```

### Crear Repuestos de Ejemplo

```powershell
python create_sample_parts.py
```

## Documentación Adicional

- `ASISTENTE_REPUESTOS_README.md`: Guía del módulo de repuestos
- `KEYS_MANAGER_README.md`: Guía del módulo de llaves

## Notas de Desarrollo

- La aplicación usa SQLite por defecto (archivo `app.db`)
- El modo debug está habilitado por defecto en desarrollo
- Las imágenes de acceso se guardan en `static/uploads/`
- Las migraciones se gestionan con Flask-Migrate

## Seguridad

⚠️ **IMPORTANTE**: Este es un entorno de desarrollo. Para producción:
- Cambiar `SECRET_KEY` a un valor seguro
- Usar un servidor WSGI (gunicorn, uwsgi)
- Configurar HTTPS
- Usar base de datos más robusta (PostgreSQL, MySQL)
- Implementar respaldos regulares

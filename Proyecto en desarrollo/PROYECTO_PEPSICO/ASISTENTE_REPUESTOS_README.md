# Rol: Asistente de Repuestos

## Descripción
El rol **Asistente de Repuestos** (`parts_assistant`) gestiona el inventario de repuestos y registra las entregas a los mecánicos.

## Funcionalidades

### 1. Gestión de Repuestos
- **Crear nuevos repuestos**: Registrar piezas con código único, nombre, descripción y stock inicial
- **Editar repuestos**: Actualizar información y ajustar niveles de stock
- **Control de stock**: Sistema de alertas cuando el stock está bajo o crítico
- **Stock mínimo**: Configurar nivel de alerta para cada repuesto

### 2. Registro de Entregas
- **Registrar entrega a mecánico**: Asignar repuestos a mecánicos específicos
- **Actualización automática de stock**: El stock se reduce automáticamente al registrar entregas
- **Asociar a orden de trabajo**: Vincular entregas con órdenes de trabajo específicas (opcional)
- **Notas y observaciones**: Agregar comentarios sobre cada entrega

### 3. Historial y Seguimiento
- **Historial completo**: Ver todas las entregas realizadas con fecha, hora y detalles
- **Información de entrega**: Quién entregó, a quién, qué cantidad y cuándo
- **Trazabilidad**: Seguimiento completo de movimientos de inventario

## Credenciales de Acceso

### Usuario de Prueba
- **Username**: `asistente_repuestos`
- **Password**: `repuestos123`
- **Rol**: `parts_assistant`

## Rutas Disponibles

### Dashboard y Gestión
- `/parts/dashboard` - Panel principal con estadísticas y alertas
- `/parts/list` - Lista completa de repuestos
- `/parts/new` - Crear nuevo repuesto
- `/parts/<id>/edit` - Editar repuesto existente

### Entregas
- `/parts/delivery/new` - Registrar nueva entrega a mecánico
- `/parts/delivery/history` - Historial completo de entregas

## Estructura de Datos

### Tabla: `part`
```
id                INTEGER PRIMARY KEY
code              VARCHAR(100) UNIQUE  # Código único del repuesto
name              VARCHAR(200)         # Nombre del repuesto
description       TEXT                 # Descripción detallada
stock             INTEGER              # Cantidad disponible
min_stock         INTEGER              # Stock mínimo (alerta)
created_by        INTEGER FK(user.id)  # Usuario que lo creó
created_at        DATETIME
updated_at        DATETIME
```

### Tabla: `part_delivery`
```
id                INTEGER PRIMARY KEY
part_id           INTEGER FK(part.id)       # Repuesto entregado
mechanic_id       INTEGER FK(mechanic.id)   # Mecánico receptor
assignment_id     INTEGER FK(assignment.id) # Orden de trabajo (opcional)
quantity          INTEGER                   # Cantidad entregada
delivered_by      INTEGER FK(user.id)       # Usuario que entregó
note              TEXT                      # Observaciones
created_at        DATETIME                  # Fecha y hora de entrega
```

## Características del Sistema

### Alertas de Stock
- **Crítico**: Stock ≤ stock mínimo (badge rojo)
- **Bajo**: Stock ≤ 2 × stock mínimo (badge amarillo)
- **Normal**: Stock > 2 × stock mínimo (badge verde)

### Validaciones
- ✅ Códigos únicos de repuestos
- ✅ Verificación de stock disponible antes de entregar
- ✅ Actualización automática de inventario
- ✅ Restricción de cantidad máxima según stock disponible

### Interfaz
- Dashboard con estadísticas en tiempo real
- Tablas responsivas con diseño profesional
- Alertas visuales para stock bajo
- Navegación intuitiva con Bootstrap Icons

## Flujo de Trabajo

1. **Registro de Repuestos**
   - El asistente registra nuevos repuestos en el sistema
   - Define código, nombre, stock inicial y stock mínimo

2. **Solicitud de Mecánico**
   - El mecánico solicita repuestos para una reparación
   - El asistente verifica disponibilidad en el sistema

3. **Registro de Entrega**
   - El asistente registra la entrega con:
     - Repuesto entregado
     - Mecánico receptor
     - Cantidad
     - Orden de trabajo relacionada (si aplica)
     - Observaciones

4. **Actualización Automática**
   - El sistema reduce el stock automáticamente
   - Genera alertas si el stock queda bajo

5. **Seguimiento**
   - Todo queda registrado en el historial
   - Trazabilidad completa de movimientos

## Crear Usuario Adicional

Si necesitas crear más usuarios con este rol:

```python
python create_parts_assistant_user.py
```

O manualmente desde el script:
```python
from app import create_app
from extensions import db
from models import User

app = create_app()
with app.app_context():
    user = User(username='nuevo_asistente', role='parts_assistant')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
```

## Migraciones

Las tablas fueron creadas mediante migración de Alembic:

```
migrations/versions/c5432e87ab3f_add_parts_and_deliveries_tables.py
```

Para aplicar la migración en otro entorno:
```bash
python apply_migrations.py
```

## Permisos y Seguridad

- Solo usuarios con rol `parts_assistant` pueden acceder a las rutas de repuestos
- El decorator `@role_required('parts_assistant')` protege todas las rutas
- Login requerido para todas las funciones
- El rol está excluido del dashboard general

## Integración con Otros Roles

- **Mecánicos**: Reciben repuestos registrados por el asistente
- **Supervisor**: Puede ver las entregas asociadas a órdenes de trabajo
- **Admin**: Puede crear y gestionar usuarios con rol `parts_assistant`

## Notas Técnicas

- Base de datos: SQLite
- Framework: Flask 2.3.2
- ORM: SQLAlchemy
- Templates: Jinja2 + Bootstrap 5
- Sistema de migraciones: Alembic (Flask-Migrate)

# 🚀 Guía Rápida de Uso - Sistema de Gestión de Flota PepsiCo

## ⚡ Inicio Rápido

### 1. Ejecutar la Aplicación
```powershell
python app.py
```
Visitar: http://127.0.0.1:5000

### 2. Credenciales de Usuarios Existentes
Ver los usuarios disponibles:
```powershell
python db_utils.py --list-users
```

---

## 📌 Comandos Más Usados

### Gestión de Usuarios

```powershell
# Crear administrador
python create_users.py --username admin --password admin123 --role admin

# Crear mecánico
python create_users.py --username juan --password pass123 --role mechanic --name "Juan Pérez" --phone "987654321"

# Crear asistente de repuestos
python create_users.py --username repuestos --password pass123 --role parts_assistant

# Crear guardia
python create_users.py --username guardia --password pass123 --role guard

# Crear recepcionista
python create_users.py --username recepcion --password pass123 --role receptionist

# Crear encargado de llaves
python create_users.py --username llaves --password pass123 --role key_manager
```

### Inspección de Base de Datos

```powershell
# Ver estadísticas
python db_utils.py --stats

# Listar usuarios
python db_utils.py --list-users

# Listar tablas
python db_utils.py --list-tables

# Inspeccionar tabla
python db_utils.py --inspect-table vehicle
```

### Datos de Ejemplo

```powershell
# Crear repuestos de ejemplo
python create_sample_parts.py

# Crear mecánico por defecto
python create_default_mechanic.py
```

---

## 🔐 Roles y Accesos

| Rol | Accesos Principales |
|-----|-------------------|
| **admin** | Gestión completa de usuarios, acceso total |
| **supervisor** | Asignación de mecánicos, aprobación de vehículos |
| **mechanic** | Ver órdenes asignadas, solicitar repuestos, registrar progreso |
| **parts_assistant** | Gestionar inventario, procesar solicitudes, registrar entregas |
| **key_manager** | Control de llaves, registrar entregas/devoluciones |
| **receptionist** | Crear órdenes de trabajo, validar documentos |
| **guard** | Registrar ingresos con fotos |

---

## 🔄 Flujo de Trabajo Típico

### 1. Ingreso de Vehículo
**Guardia** → Registra ingreso con fotos (`/guard/entry/new`)

### 2. Recepción
**Recepcionista** → Crea orden de trabajo (`/reception/workorders/new`)

### 3. Registro de Vehículo
**Supervisor** → Registra vehículo en sistema (`/vehicles/new`)

### 4. Asignación
**Supervisor** → Asigna mecánico al vehículo (`/vehicles/{id}/assign`)

### 5. Trabajo
**Mecánico** → Ve sus órdenes (`/me/dashboard`)
**Mecánico** → Solicita repuestos si necesita (`/mechanic/part-requests/new`)

### 6. Gestión de Repuestos
**Asistente** → Procesa solicitudes (`/parts/requests`)
**Asistente** → Registra entrega (`/parts/delivery/new`)

### 7. Progreso
**Mecánico** → Registra avance del trabajo (`/assignments/{id}/progress`)

### 8. Gestión de Llaves
**Encargado** → Registra devolución de llaves (`/keys/return`)
**Encargado** → Ve historial (`/keys/history`)

---

## 🛠️ Solución de Problemas Comunes

### La aplicación no inicia
```powershell
# Verificar que el entorno virtual está activado
.\.venv\Scripts\Activate.ps1

# Reinstalar dependencias
pip install -r requirements.txt
```

### Error "Base de datos bloqueada"
- Cerrar todas las instancias de la aplicación
- Reiniciar el servidor

### No puedo crear usuarios
- Verificar que la aplicación se ejecutó al menos una vez (crea las tablas)
- Verificar permisos de escritura en el directorio

### Olvidé mi contraseña
Admin puede resetear contraseñas desde `/admin/users`

---

## 📊 Estructura de URLs

### Públicas
- `/` - Página principal con login

### Admin
- `/admin/users` - Gestión de usuarios
- `/admin/users/new` - Crear usuario

### Dashboard
- `/dashboard` - Dashboard general

### Vehículos
- `/vehicles` - Lista de vehículos
- `/vehicles/new` - Registrar vehículo
- `/vehicles/{id}/assign` - Asignar mecánico

### Mecánicos
- `/mechanics` - Lista de mecánicos
- `/mechanics/new` - Registrar mecánico
- `/me/dashboard` - Dashboard del mecánico

### Repuestos
- `/parts/dashboard` - Dashboard de repuestos
- `/parts/requests` - Solicitudes pendientes
- `/parts/delivery/new` - Registrar entrega

### Llaves
- `/keys/dashboard` - Dashboard de llaves
- `/keys/return` - Registrar devolución
- `/keys/history` - Historial

### Órdenes de Trabajo
- `/reception/workorders` - Lista de OT
- `/reception/workorders/new` - Nueva OT

---

## 📝 Notas Importantes

- ✅ Todas las contraseñas se almacenan hasheadas
- ✅ Las imágenes se guardan en `static/uploads/`
- ✅ La base de datos es `app.db` (SQLite)
- ⚠️ No usar en producción sin configurar seguridad adicional
- ⚠️ Hacer respaldos periódicos de `app.db`

---

## 🆘 Soporte

Para más información, consultar:
- `README.md` - Documentación completa
- `CHANGELOG.md` - Historial de cambios
- `ASISTENTE_REPUESTOS_README.md` - Módulo de repuestos
- `KEYS_MANAGER_README.md` - Módulo de llaves

# Migración de Pendientes: JSON a BD

## Resumen

Se ha migrado el almacenamiento de **ventas pendientes** de un archivo `pendientes.json` (file-backed) a tablas en la base de datos SQLite/Postgres. Esta mejora resuelve problemas de concurrencia y persistencia en producción.

## Cambios Realizados

### 1. **Nuevos Modelos SQLAlchemy** (`models_alchemy.py`)

Se añadieron dos modelos ORM:

- **`Pendiente`**: tabla `pendientes`

  - `id` (PK): entero
  - `fecha`: string (fecha de creación)
  - `usuario_id` (FK): ref. a usuarios
  - `total`: float (total de la venta)

- **`PendienteDetalle`**: tabla `pendiente_detalles`
  - `id` (PK): entero
  - `pendiente_id` (FK): ref. a pendientes
  - `producto_id` (FK): ref. a productos
  - `nombre`: string (nombre del producto en el momento de la venta)
  - `cantidad`: integer
  - `precio`: float (precio unitario)
  - `subtotal`: float

### 2. **Actualización de Funciones** (`models/venta.py`)

Las funciones de manejo de pendientes ahora usan la BD en lugar de JSON:

#### `guardar_pendiente(productos_cantidades, usuario_id=None)`

- Calcula el total y detalles.
- Crea un registro `Pendiente` y sus `PendienteDetalle` en la BD.
- Retorna `(True, mensaje)` o `(False, mensaje)`.

#### `obtener_pendientes()`

- Consulta la tabla `pendientes` (ordenadas por ID desc).
- Construye un dict similar al anterior formato JSON (con `detalles` anidados).
- Retorna lista de pendientes o vacía en caso de error.

#### `obtener_pendiente_por_id(pendiente_id)`

- Obtiene un pendiente específico con sus detalles desde la BD.
- Retorna dict o `None`.

#### `eliminar_pendiente(pendiente_id)`

- Elimina un pendiente y sus detalles de la BD.
- Usa transacciones para atomicidad.
- Retorna `(True, mensaje)` o `(False, mensaje)`.

**Cambio importante**: Se eliminó la dependencia de `pendientes.json` y los imports `json`, `os` ya no son necesarios para el manejo de pendientes.

### 3. **Migración Alembic** (`migrations/versions/8fa4e17944b7_add_pendientes_tables.py`)

Se generó automáticamente una migración que crea las dos tablas con sus relaciones.

**Comandos usados:**

```bash
flask db migrate -m "add pendientes tables"
flask db upgrade
```

### 4. **Script de Data Migration** (`scripts/migrate_pendientes.py`)

Se proporciona un script para migrar pendientes existentes desde `pendientes.json` a la BD:

```bash
python scripts/migrate_pendientes.py
```

Si `pendientes.json` existe, el script:

1. Lee el archivo JSON.
2. Crea registros `Pendiente` y `PendienteDetalle` para cada pendiente.
3. Los inserta en la BD.
4. Reporta cuántos se migraron.

Si no existe, el script termina sin hacer nada.

## Archivo `pendientes.json`

Se ha **eliminado** `pendientes.json` del repo. Los datos se persisten ahora en la BD.

**Si tienes pendientes en `pendientes.json` en producción**, ejecuta `migrate_pendientes.py` antes de eliminar el archivo.

## Compatibilidad

La interfaz de las funciones de pendientes se mantiene igual: retornan dicts con estructura idéntica a la anterior. Esto asegura que las rutas (`routes/registros_routes.py`, `routes/ventas_routes.py`, etc.) no requieren cambios.

## Tests

Todos los tests pasan (7 tests, 0 fallos):

```
=============================================== 7 passed ===============================================
```

## Deploymentproducción

1. Aplicar migraciones en la BD de producción:
   ```bash
   flask db upgrade
   ```
2. Si tienes datos en `pendientes.json` legacy, ejecuta el script de migración:
   ```bash
   python scripts/migrate_pendientes.py
   ```
3. Elimina `pendientes.json` después de validar que los datos se migraron correctamente.

## Ventajas

✅ **Concurrencia**: BD maneja locks y transacciones atómicamente.
✅ **Escalabilidad**: múltiples instancias/workers pueden acceder simultáneamente.
✅ **Persistencia robusta**: no hay race conditions de lectura/escritura en archivo.
✅ **Integridad referencial**: las FK garantizan consistencia de datos.
✅ **Paginación/búsqueda**: más fácil consultar pendientes (orden, filtros, etc.) vía SQL.
✅ **Backups**: la BD ya está siendo respaldada; pendientes se incluyen automáticamente.

## Commit

- **Hash**: `e1c1c73`
- **Mensaje**: `feat: persistir pendientes en DB - modelos migracion script`
- **Archivos modificados**:
  - `models_alchemy.py` (+19 líneas: nuevos modelos)
  - `models/venta.py` (+142/-129 líneas: reimplement con BD)
  - `migrations/versions/8fa4e17944b7_add_pendientes_tables.py` (nueva migración)
  - `scripts/migrate_pendientes.py` (nuevo script)
  - `pendientes.json` (eliminado del repo)

# 💾 Guía: Persistencia de Datos en Kairos

## El Problema Original

Cuando el ejecutable se ejecutaba por primera vez, al reiniciarlo perdía todos los datos:

- ❌ Usuarios desaparecían
- ❌ Productos desaparecían
- ❌ Ventas desaparecían
- ❌ La BD se creaba nuevamente vacía

## La Solución

Se implementó un sistema de almacenamiento **persistente** que guarda todos los datos en una carpeta especial.

### 📁 Ubicación de los Datos

```
C:\Users\ASUS\kairos\dist\
├── Kairos.exe              ← El programa ejecutable
├── INICIAR_KAIROS.bat      ← Lanzador rápido
└── datos/                  ← 📍 AQUÍ SE GUARDAN LOS DATOS
    └── kairos.db          ← Base de datos SQLite
```

**Nota importante:** La carpeta `datos/` se crea automáticamente en la primera ejecución.

## Cómo Funciona

### 1️⃣ Primera Ejecución (Primera vez)

```
Kairos.exe → detecta que es ejecutable →
→ crea carpeta "datos/" →
→ crea BD en datos/kairos.db →
→ crea usuario admin/admin123
```

**Resultado:**

- ✅ BD vacía inicializada
- ✅ Admin user creado
- ✅ Listo para usar

### 2️⃣ Uso Normal

```
Usuario agrega producto → se guarda en datos/kairos.db
Usuario crea venta → se guarda en datos/kairos.db
Usuario crea usuario → se guarda en datos/kairos.db
```

**Resultado:**

- ✅ Todos los cambios se guardan automáticamente en tiempo real

### 3️⃣ Reinicio (Cerramos y reabrimos Kairos.exe)

```
Kairos.exe → detecta que BD ya existe en datos/ →
→ NO crea nueva BD →
→ carga datos existentes de datos/kairos.db →
→ "Usuario admin ya existe" (no lo crea de nuevo)
```

**Resultado:**

- ✅ Productos que agregaste: están ahí
- ✅ Ventas que registraste: están ahí
- ✅ Usuarios que creaste: están ahí
- ✅ Cambios en inventario: están ahí

## Cambios Técnicos Implementados

### En `run.py`

```python
# Detecta si está corriendo como ejecutable compilado
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
    DATA_DIR = BASE_DIR / "datos"      # ← Carpeta persistente
    DATA_DIR.mkdir(exist_ok=True)       # ← Crea si no existe
```

**Qué hace:**

1. Detecta si es ejecutable (`frozen`)
2. Crea carpeta `datos/` en la misma ubicación que `Kairos.exe`
3. Guarda la variable en `os.environ["KAIROS_DATA_DIR"]`

### En `config.py`

```python
# Lee la ruta de datos del executible
data_dir = os.environ.get("KAIROS_DATA_DIR")
if data_dir:
    db_path = os.path.join(data_dir, "kairos.db")  # ← Usa carpeta persistente
else:
    db_path = os.path.join(base_dir, "kairos.db")  # ← Fallback para desarrollo
```

**Qué hace:**

1. Verifica si existe `KAIROS_DATA_DIR` (configurado por `run.py`)
2. Si existe: guarda BD en `dist/datos/kairos.db` ✅ (Ejecutable)
3. Si no existe: guarda BD en `kairos.db` ✅ (Desarrollo)

## Ejemplo Práctico

### Sesión 1: Agregamos datos

```
1. Ejecutamos: INICIAR_KAIROS.bat
2. Login: admin / admin123
3. Agregamos producto "Coca Cola"
4. Agregamos producto "Heineken"
5. Registramos una venta (Coca Cola x2)
6. Cerramos Kairos (CTRL+C)

✅ Los datos se guardan automáticamente en:
   C:\Users\ASUS\kairos\dist\datos\kairos.db
```

### Sesión 2: Los datos siguen ahí

```
1. Ejecutamos: INICIAR_KAIROS.bat (nuevamente)
2. Login: admin / admin123
3. Vamos a Inventario
   → ✅ "Coca Cola" sigue aquí
   → ✅ "Heineken" sigue aquí
4. Vamos a Registros
   → ✅ La venta que hicimos sigue registrada
5. Vamos a Usuarios
   → ✅ El usuario "prueba" que creamos sigue aquí
```

## Protección de Datos

### Lo que necesitas saber

1. **La carpeta `datos/` es crítica**

   - Contiene toda la BD
   - No la borres a menos que quieras empezar de cero

2. **Para hacer backup:**

   ```bash
   # Simplemente copia la carpeta datos/
   Copy-Item -Path "C:\Users\ASUS\kairos\dist\datos" -Destination "C:\backup\datos_respaldo" -Recurse
   ```

3. **Para restaurar:**

   ```bash
   # Pega la carpeta de respaldo
   Copy-Item -Path "C:\backup\datos_respaldo\*" -Destination "C:\Users\ASUS\kairos\dist\datos" -Recurse
   ```

4. **Para empezar de cero:**
   ```bash
   # Elimina la carpeta datos (se crea nuevamente vacía en el siguiente inicio)
   Remove-Item "C:\Users\ASUS\kairos\dist\datos" -Recurse -Force
   ```

## Distribución a Otros

Si quieres compartir Kairos con otros:

```
Kairos_v1.0/
├── Kairos.exe
├── INICIAR_KAIROS.bat
└── datos/              ← IMPORTANTE: incluir esta carpeta
    └── kairos.db       ← (puede estar vacía, se inicializa al primer uso)
```

**En el archivo zip:**

- ✅ Kairos.exe
- ✅ INICIAR_KAIROS.bat
- ✅ Carpeta `datos/` (vacía está bien)
- ✅ Opcional: README.txt con instrucciones

**Otros usuarios:**

1. Descargan el zip
2. Extraen en carpeta (ej: `C:\Kairos\`)
3. Ejecutan `INICIAR_KAIROS.bat`
4. ¡Listo! Los datos se guardan automáticamente

## Preguntas Frecuentes

### P: ¿Dónde están exactamente los datos?

**R:** En `C:\Users\ASUS\kairos\dist\datos\kairos.db`

### P: ¿Puedo mover la carpeta `datos/` a otra ubicación?

**R:** No recomendado. Debe estar al lado de `Kairos.exe` para que funcione automáticamente.

### P: ¿Qué pasa si elimino `datos/kairos.db`?

**R:** Al reiniciar Kairos, se crea nuevamente vacía. Se pierden todos los datos.

### P: ¿Es seguro el almacenamiento?

**R:** Sí, usa SQLite (base de datos estándar). Puedes hacer backup fácilmente.

### P: ¿Los datos se sincronizan si tengo múltiples Kairos.exe?

**R:** Cada instalación tiene su propia carpeta `datos/`. No se sincronizan automáticamente.

### P: ¿Puedo acceder a los datos con otras herramientas?

**R:** Sí, SQLite es estándar. Puedes usar:

- **DB Browser for SQLite** (gratuito)
- **SQLiteOnline**
- Herramientas de desarrollo Python
- DataGrip de JetBrains

### P: ¿Se copian los datos si creo un duplicado de Kairos.exe?

**R:** No. Cada Kairos.exe crea su propia carpeta `datos/` en su ubicación.

## Resumen

| Aspecto        | Antes ❌     | Ahora ✅       |
| -------------- | ------------ | -------------- |
| Almacenamiento | Temporal     | Persistente    |
| Ubicación      | Desconocida  | `dist/datos/`  |
| Reinicio       | Pierde datos | Recupera datos |
| Backup         | Imposible    | Fácil          |
| Distribución   | Problemática | Simple         |

**En resumen:** Los datos ahora se guardan en `dist/datos/kairos.db` y persisten entre reinicios del programa. ¡Funciona correctamente! 🎉

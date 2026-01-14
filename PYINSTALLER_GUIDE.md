# 📦 Guía: Empaquetar Kairos con PyInstaller

## 📋 Resumen Rápido

**3 pasos para reconstruir el ejecutable:**

```bash
cd c:\Users\ASUS\kairos
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue
python -m PyInstaller kairos.spec -y
```

El ejecutable estará en `dist/Kairos.exe` y los datos se guardarán en `%APPDATA%\Kairos\datos\kairos.db`

## 1️⃣ Instalación de PyInstaller

```bash
pip install pyinstaller
```

## 2️⃣ Características Implementadas

### ✅ Inicialización Automática de Base de Datos

- La BD se crea automáticamente en: `%APPDATA%\Kairos\datos\kairos.db`
- Si no existe admin, se crea con credenciales: `admin` / `admin123`
- Los datos **persisten** entre reinicios y actualizaciones

### ✅ Almacenamiento Persistente Seguro

Los datos se guardan en **AppData/Roaming** (estándar de Windows):

```
C:\Users\[TU_USUARIO]\AppData\Roaming\Kairos\datos\
└── kairos.db                    ← Base de datos SQLite
```

**Ventajas:**

- ✅ **Persiste entre actualizaciones** del ejecutable
- ✅ **No se elimina** cuando regeneras el exe
- ✅ **Instalación multi-computadora** segura
- ✅ **Backup fácil** - solo copia la carpeta AppData\Kairos

## 3️⃣ Usar el Ejecutable

### Opción A: Lanzador Automático (Recomendado)

```bash
cd dist
.\INICIAR_KAIROS.bat
```

### Opción B: Ejecutable Directo

```bash
cd dist
.\Kairos.exe
```

## 4️⃣ Credenciales por Defecto

En la **primera ejecución**:

- 👤 **Usuario:** `admin`
- 🔑 **Contraseña:** `admin123`

Puedes crear más usuarios desde el panel de administración después de login.

## 5️⃣ Persistencia de Datos

**Importante:** Los datos se guardan automáticamente en `%APPDATA%\Kairos\datos\kairos.db`

✅ Usuarios se conservan entre reinicios
✅ Productos se conservan
✅ Ventas se conservan
✅ Cambios se guardan en tiempo real
✅ **Los datos NO se pierden al actualizar el ejecutable**

## 6️⃣ Instalación en Otra Computadora

Para instalar en otra PC:

1. **Copia el ejecutable:**

   ```bash
   # Desde tu PC
   Copy-Item "C:\Users\ASUS\kairos\dist\*" -Destination "D:\Kairos_dist" -Recurse
   ```

2. **En la otra PC:**

   ```bash
   # Pega los archivos
   # Ejecuta: INICIAR_KAIROS.bat
   ```

3. **Resultado:**
   - ✅ Se crea automáticamente `%APPDATA%\Kairos\datos\kairos.db` en la nueva PC
   - ✅ Datos completamente independientes
   - ✅ No hay conflictos entre computadoras

## 7️⃣ Actualización del Ejecutable

### ✅ Método Seguro (Recomendado)

Usa el script `ACTUALIZAR_KAIROS.bat`:

```bash
# Ejecuta el script de actualización
.\ACTUALIZAR_KAIROS.bat
```

**Qué hace automáticamente:**

1. ✅ Hace backup de tu BD actual
2. ✅ Regenera el ejecutable
3. ✅ Los datos siguen intactos en AppData

### ❌ Método Manual (No recomendado)

```bash
# ❌ Esto ELIMINA la carpeta dist/ y tus datos si están ahí
python -m PyInstaller kairos.spec -y
```

## 🚀 Flujo Completo

### Desarrollo:

```bash
python run.py  # Pruebas en development
```

### Compilación:

```bash
python -m PyInstaller kairos.spec -y
```

### Distribución:

```bash
# Copia dist/ a otras computadoras
# Los datos se guardan automáticamente en AppData de cada PC
```

### Actualización:

```bash
# Usa ACTUALIZAR_KAIROS.bat para preservar datos
.\ACTUALIZAR_KAIROS.bat
```

## 📁 Archivo Spec (kairos.spec)

El archivo `kairos.spec` contiene la configuración de PyInstaller:

- ✅ Punto de entrada: `run.py`
- ✅ Datos incluidos: templates, migrations, config.py
- ✅ Módulos ocultos: Flask, SQLAlchemy, Jinja2, etc.
- ✅ Salida: `dist/Kairos.exe` (single file)

**No edites manualmente** - PyInstaller lo mantiene actualizado.

## 🐛 Solución de Problemas

### "No se encontró la tabla usuarios"

✅ **SOLUCIONADO** - Ahora se crea automáticamente en la primera ejecución

### "Los datos desaparecen al reiniciar"

✅ **SOLUCIONADO** - Se guardan en `%APPDATA%\Kairos\datos\kairos.db` (persistente)

### "Los datos desaparecen al actualizar"

✅ **SOLUCIONADO** - AppData no se elimina al regenerar el ejecutable

### "No puedo loguearme"

- Verifica que escribiste bien: `admin` / `admin123`
- Si la BD se corrompió, elimina `%APPDATA%\Kairos` y reinicia (se crea nuevamente)

### "El ejecutable no inicia"

- Verifica que tienes Python 3.10+ instalado
- Ejecuta desde `dist/` o usa la ruta completa
- Revisa los logs en `dist/logs/`

## 📦 Distribución

Para compartir Kairos con otros:

```
Kairos_v1.0.zip
├── Kairos.exe
├── INICIAR_KAIROS.bat
├── ACTUALIZAR_KAIROS.bat    ← Para futuras actualizaciones
└── README.txt
```

**Ejemplo para compartir:**

```
Kairos_v1.0.zip
├── Kairos.exe
├── INICIAR_KAIROS.bat
├── ACTUALIZAR_KAIROS.bat
└── README.txt
```

**En el archivo zip:**

- ✅ Kairos.exe
- ✅ INICIAR_KAIROS.bat
- ✅ ACTUALIZAR_KAIROS.bat (para actualizaciones seguras)
- ❌ **NO incluir carpeta datos/** (se crea automáticamente en AppData)

## 🔧 Modificaciones Recientes

**run.py (v4.0):**

- ✅ Detecta automáticamente si está como ejecutable compilado
- ✅ Usa `%APPDATA%\Kairos\datos\` para almacenamiento persistente
- ✅ Crea directorio automáticamente si no existe
- ✅ Muestra ubicación de datos en consola

**config.py (v3.0):**

- ✅ Lee variable de entorno `KAIROS_DATA_DIR`
- ✅ Guarda BD en ubicación persistente cuando está compilado
- ✅ Mantiene compatibilidad con desarrollo desde código fuente

**ACTUALIZAR_KAIROS.bat:**

- ✅ Script para actualizar sin perder datos
- ✅ Hace backup automático antes de regenerar
- ✅ Restaura datos automáticamente

## 📝 Notas Finales

- El ejecutable es **standalone** - no necesita Python instalado
- Los datos están en formato SQLite - puedes abrirlos con cualquier viewer SQLite
- Los logs se guardan en `dist/logs/`
- Para actualizar, usa `ACTUALIZAR_KAIROS.bat` para preservar datos
- Cada instalación tiene sus propios datos (independientes)

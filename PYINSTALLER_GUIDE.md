# 📦 Guía: Empaquetar Kairos con PyInstaller

## 📋 Resumen Rápido

**3 pasos para reconstruir el ejecutable:**

```bash
cd c:\Users\ASUS\kairos
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue
python -m PyInstaller kairos.spec -y
```

El ejecutable estará en `dist/Kairos.exe` y los datos se guardarán en `dist/datos/kairos.db`

## 1️⃣ Instalación de PyInstaller

```bash
pip install pyinstaller
```

## 2️⃣ Características Implementadas

### ✅ Inicialización Automática de Base de Datos

- La BD se crea automáticamente en: `dist/datos/kairos.db`
- Si no existe admin, se crea con credenciales: `admin` / `admin123`
- Los datos **persisten** entre reinicios del ejecutable

### ✅ Almacenamiento Persistente

Los datos se guardan en una carpeta especial `datos/` dentro de `dist/`:

```
dist/
├── Kairos.exe          ← Ejecutable
├── datos/              ← Carpeta de datos (PERSISTEN AQUÍ)
│   └── kairos.db      ← Base de datos SQLite
├── logs/               ← Logs de la aplicación
└── INICIAR_KAIROS.bat  ← Lanzador rápido
```

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

**Importante:** Los datos se guardan automáticamente en `dist/datos/kairos.db`

✅ Usuarios se conservan entre reinicios
✅ Productos se conservan
✅ Ventas se conservan
✅ Cambios se guardan en tiempo real

**No pierdas la carpeta `dist/datos/`** - ahí están todos tus datos.

## 🚀 Flujo Completo

1. **Desarrollo:**

   ```bash
   python run.py  # Pruebas en development
   ```

2. **Antes de compilar:**

   ```bash
   pytest  # Verificar que todo funciona
   ```

3. **Compilar ejecutable:**

   ```bash
   python -m PyInstaller kairos.spec -y
   ```

4. **Usar ejecutable:**

   ```bash
   cd dist
   .\INICIAR_KAIROS.bat
   ```

5. **Acceder:**
   - Abre navegador: `http://localhost:5000`
   - Login: `admin` / `admin123`

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

✅ **SOLUCIONADO** - Se guardan en `dist/datos/kairos.db` (persistente)

### "No puedo loguearme"

- Verifica que escribiste bien: `admin` / `admin123`
- Si la BD se corrompió, elimina `dist/datos/kairos.db` y reinicia (se crea nuevamente)

### "El ejecutable no inicia"

- Verifica que tienes Python 3.10+ instalado
- Ejecuta desde `dist/` o usa la ruta completa
- Revisa los logs en `dist/logs/`

## 📦 Distribución

Para compartir Kairos con otros:

1. Copia la carpeta `dist/` completa
2. Incluye: `Kairos.exe`, `INICIAR_KAIROS.bat`, carpeta `datos/`
3. Otros usuarios ejecutan: `INICIAR_KAIROS.bat`
4. ¡Listo! Los datos se guardan automáticamente

**Ejemplo para compartir:**

```
Kairos_v1.0.zip
├── Kairos.exe
├── INICIAR_KAIROS.bat
├── datos/
│   └── kairos.db  (inicial vacío, se crea al primer uso)
└── README.txt
```

## 🔧 Modificaciones Recientes

**run.py (v3.0):**

- ✅ Detecta automáticamente si está ejecutando como exe compilado
- ✅ Crea directorio `dist/datos/` para guardar la BD
- ✅ Inicializa la BD automáticamente si no existe
- ✅ Crea usuario admin por defecto

**config.py (v2.0):**

- ✅ Lee variable de entorno `KAIROS_DATA_DIR`
- ✅ Guarda la BD en `dist/datos/` cuando está compilado
- ✅ Mantiene compatibilidad con desarrollo desde código fuente

## 📝 Notas Finales

- El ejecutable es **standalone** - no necesita Python instalado
- Los datos están en formato SQLite - puedes abrirlos con cualquier viewer SQLite
- Los logs se guardan en `dist/logs/`
- Para actualizar, simplemente recompila: `python -m PyInstaller kairos.spec -y`

### Opción 1: Doble clic en `INICIAR_KAIROS.bat`

```
dist/INICIAR_KAIROS.bat
```

### Opción 2: Doble clic directo en `Kairos.exe`

```
dist/Kairos.exe
```

## 🔑 Credenciales por Defecto

Al iniciar el ejecutable por primera vez:

```
Usuario: admin
Contraseña: admin123
```

## 📋 Lo que Inicializa Automáticamente

✅ Base de datos SQLite (si no existe)
✅ Todas las tablas necesarias
✅ Usuario admin por defecto
✅ Directorios de logs
✅ Archivos de configuración

## ⚠️ Problemas Comunes y Soluciones

### ❌ "No se encuentran los templates"

✅ **Solucionado:** El spec file incluye `datas = [('templates', 'templates')]`

### ❌ "Module not found: sqlalchemy"

✅ **Solucionado:** Incluido en `hiddenimports`

### ❌ "Database file not found"

✅ **Solucionado:** El `run.py` detecta si está en ejecutable y crea la BD automáticamente

### ❌ "No se crea usuario admin"

✅ **Solucionado:** `run.py` verifica y lo crea si no existe

### ❌ El ejecutable se cierra inmediatamente

✅ **Solución:** Ejecutar desde `INICIAR_KAIROS.bat` que mantiene la ventana abierta

## 📊 Distribución del Ejecutable

**Para compartir con otros:**

1. Copiar toda la carpeta `dist/` a otra máquina
2. Doble clic en `INICIAR_KAIROS.bat`
3. ¡Listo! La aplicación inicia automáticamente

**Tamaño:** ~150-200 MB (incluye todas las dependencias)

## 🛠️ Personalización

Si necesitas cambiar las credenciales por defecto, edita `run.py` en la función `init_database()`:

```python
admin = User(
    username="admin",  # Cambiar aquí
    password=generate_password_hash("admin123"),  # Y aquí
    nombre="Administrador",
    rol="admin",
)
```

Luego regenera el ejecutable.

## 💡 Optimizaciones Futuras

Para reducir tamaño:

```bash
python -m PyInstaller kairos.spec --exclude-module=numpy --exclude-module=pandas
```

Para acelerar inicio:

```bash
# En spec file cambiar:
console=True  # a False (sin ventana de consola)
```

---

## 🎯 Resumen Rápido

```bash
# 1. Instalar PyInstaller (una sola vez)
pip install pyinstaller

# 2. Regenerar ejecutable
cd c:\Users\ASUS\kairos
python -m PyInstaller kairos.spec -y

# 3. Ejecutar
.\dist\INICIAR_KAIROS.bat
```

### ❌ El ejecutable se cierra inmediatamente

**Solución:** Asegurar que `console=True` en el spec file

## 🎯 Distribución

Después de generar `Kairos.exe`:

1. **Opción Simple:** Copiar `dist/` carpeta completa a otros PCs
2. **Opción Profesional:** Crear un instalador NSIS (ver paso siguiente)

## 🚀 Crear Instalador NSIS (Avanzado)

Si quieres un `.exe` instalador:

```bash
pip install pyinstaller-nsis
```

Luego crear script NSIS...

---

## 📊 Comparativa de Métodos

| Método                  | Tamaño   | Facilidad | Profesional |
| ----------------------- | -------- | --------- | ----------- |
| PyInstaller onefile     | 150MB+   | ⭐        | ⭐⭐        |
| PyInstaller onedir      | 200MB    | ⭐        | ⭐          |
| Spec file personalizado | 120MB    | ⭐⭐      | ⭐⭐⭐      |
| NSIS Instalador         | Variable | ⭐⭐⭐    | ⭐⭐⭐⭐    |

---

## 💡 Optimizaciones

Para reducir tamaño:

```bash
# Excluir módulos no usados
pyinstaller kairos.spec --exclude-module=numpy --exclude-module=pandas
```

Para acelerar inicio:

```bash
# Ejecutable sin consola
# En spec file: console=False
```

# Kairos - Sistema de Gestión de Inventario y Ventas

## 📋 Descripción

Kairos es una aplicación web Flask para gestión integral de inventario y registros de ventas, con validación completa, logging centralizado y pruebas automatizadas.

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.9+
- pip o conda

### Instalación

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/ortiz-ivan/kairos.git
   cd kairos
   ```

2. **Crear entorno virtual:**

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Inicializar base de datos:**

   ```bash
   flask db upgrade
   flask seed
   ```

   - Crea usuario admin con credenciales: `admin / admin123` (configurable con `ADMIN_PASSWORD`)

5. **Ejecutar la aplicación:**
   ```bash
   python manage.py
   ```
   - Acceder en: `http://localhost:5000`

## 🧪 Testing

### Ejecutar Tests Localmente

```bash
# Todos los tests
pytest

# Con reporte de cobertura
pytest --cov=. --cov-report=html

# Verbose
pytest -v

# Test específico
pytest tests/test_products_crud.py::test_products_crud -v
```

### Configuración de Pre-commit

**Instalación inicial:**

```bash
pip install pre-commit
pre-commit install
```

**Hooks configurados:**

- `trailing-whitespace`: Elimina espacios al final de líneas
- `end-of-file-fixer`: Asegura newline al final de archivos
- `check-yaml`: Valida sintaxis YAML
- `black`: Formatea código Python
- `flake8`: Linting (máx 120 caracteres por línea)
- `isort`: Ordena imports automáticamente
- `mypy`: Type hints checking

**Ejecutar manualmente:**

```bash
# Todos los hooks
pre-commit run --all-files

# Hook específico
pre-commit run black --all-files
pre-commit run flake8 --all-files
```

### GitHub Actions CI/CD

Los tests se ejecutan automáticamente en:

- **Pushes** a `main` o `develop`
- **Pull Requests** a `main` o `develop`

**Matriz de testing:**

- Python 3.9, 3.10, 3.11
- Reporte de cobertura en Codecov

**Estatus del build:**
![Tests](https://github.com/ortiz-ivan/kairos/actions/workflows/tests.yml/badge.svg)

## 📁 Estructura del Proyecto

```
kairos/
├── app.py                      # App factory y configuración Flask
├── manage.py                   # Comandos CLI (migraciones, seeding)
├── database.py                 # Utilitarios de DB (legacy)
├── requirements.txt            # Dependencias Python
├── pytest.ini                  # Configuración pytest
├── .pre-commit-config.yaml     # Configuración pre-commit
├── .github/
│   └── workflows/
│       └── tests.yml          # Workflow GitHub Actions
├── models/
│   ├── __init__.py
│   ├── producto.py            # Modelo Producto (CRUD)
│   ├── usuario.py             # Modelo Usuario (auth)
│   ├── venta.py               # Modelo Venta (registro)
│   └── inventario.py          # Modelo Inventario (stock)
├── routes/
│   ├── auth_routes.py         # Autenticación (login/logout)
│   ├── productos_routes.py    # CRUD de Productos
│   ├── ventas_routes.py       # Registro de Ventas
│   ├── inventario_routes.py   # Gestión de Inventario
│   └── admin_routes.py        # Panel Administrativo
├── templates/
│   ├── base.html              # Plantilla base
│   ├── login.html             # Formulario login
│   ├── productos.html         # Listado de productos
│   ├── agregar_producto.html  # Crear/editar producto
│   ├── ventas.html            # Historial de ventas
│   ├── agregar_venta.html     # Registrar venta
│   ├── inventario.html        # Gestión de inventario
│   ├── admin_usuarios.html    # Gestión de usuarios
│   ├── admin_usuario_form.html# Crear/editar usuario
│   └── error.html             # Página de errores
├── static/
│   ├── css/                   # Estilos CSS
│   └── js/                    # Scripts JavaScript
├── utils/
│   ├── logging_config.py      # Configuración de logs
│   └── error_handlers.py      # Manejadores de errores HTTP
├── tests/
│   ├── conftest.py            # Fixtures pytest
│   ├── test_setup_app.py      # Tests de inicialización
│   ├── test_products_crud.py  # Tests CRUD de productos
│   ├── test_ventas_flow.py    # Tests de flujo de ventas
│   └── test_error_handlers.py # Tests de manejadores de error
├── logs/                      # Archivos de logs (generado)
│   ├── kairos.log
│   └── kairos_errors.log
└── kairos.db                  # Base de datos SQLite

```

## 🔐 Características de Seguridad

- **Hashing de contraseñas:** Werkzeug.security.generate_password_hash
- **Sesiones seguras:** Cookies HTTPS-only, SameSite=Lax
- **Control de acceso:** Decoradores role-based (admin/vendedor)
- **Validación de entrada:** Backend + frontend
- **CSRF protection:** Habilitado en formularios
- **Logging de acceso:** Todas las operaciones administrativas registradas

## 📊 Logging

**Archivos generados:**

- `logs/kairos.log` — Logs generales (rotación: 5 archivos x 10MB)
- `logs/kairos_errors.log` — Errores críticos

**Niveles según ambiente:**

- Desarrollo: DEBUG (todos los eventos)
- Producción: INFO (solo eventos importantes)

**Formato:** `timestamp | logger | level | mensaje`

## 🐛 Validación y Manejo de Errores

### Validaciones Implementadas

- **Usuarios:** Nombre (max 100 chars), username único, contraseña fuerte
- **Productos:** Código de barras único, precio > 0, stock >= 0
- **Ventas:** Cantidad válida, stock disponible, monto total correcto

### Manejadores de Error HTTP

- **404:** Página no encontrada (con sugerencias)
- **403:** Acceso denegado (solo para admins)
- **500:** Error interno (log detallado + mensaje genérico)
- **400:** Solicitud inválida

## 🔄 Migraciones de Base de Datos

```bash
# Crear migración nueva
flask db migrate -m "descripción del cambio"

# Aplicar migraciones
flask db upgrade

# Ver historial
flask db history

# Revertir última migración
flask db downgrade
```

## 🌍 Variables de Entorno

```bash
# Ambiente
FLASK_ENV=development      # o 'production'
PRODUCTION=0               # Para activar HTTPS forzado

# Seguridad
SECRET_KEY=your-secret-key
ADMIN_PASSWORD=admin123    # Para seeding

# Debug
FLASK_DEBUG=1
```

## 📈 Próximos Pasos Sugeridos

1. **Backup automático de DB:** Configurar cronjob con `sqlite3 kairos.db ".backup backup.db"`
2. **Deployment:** Docker, Render.com, Heroku, DigitalOcean VPS
3. **Monitoreo:** Sentry para error tracking, Prometheus para métricas
4. **Auditoría:** Tabla de logs con timestamp, usuario, acción
5. **Búsqueda avanzada:** Full-text search en productos
6. **Reportes:** Generación de PDF/Excel con gráficos de ventas

## 🤝 Contribuciones

1. Fork el proyecto
2. Crear rama de feature: `git checkout -b feature/AmazingFeature`
3. Commit cambios: `git commit -m 'Add AmazingFeature'`
4. Push a rama: `git push origin feature/AmazingFeature`
5. Abrir Pull Request

**Nota:** Asegurar que todos los tests pasen y pre-commit hooks estén configurados antes de pushear.

## 📧 Contacto

[ivanzitro18@gmail.com]

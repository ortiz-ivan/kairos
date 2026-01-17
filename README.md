#  Kairos - Sistema de Gestión de Ventas SaaS

> ** Proyecto Personal**

---

## Descripción del Proyecto

**Kairos** es un sistema integral de gestión de ventas y inventario diseñado como aplicación SaaS empresarial para negocios minoristas y comerciales. Proporciona una plataforma moderna, intuitiva y de alto rendimiento para gestionar productos, registrar ventas, analizar datos y administrar usuarios.

### Propósito

El proyecto demuestra una arquitectura profesional de aplicación web moderna con:
- Diseño UX/UI especializado en dark mode para uso intensivo
- Backend Flask escalable con SQLAlchemy ORM
- Sistema modular de JavaScript sin dependencias externas
- Arquitectura responsable y mantenible
- Documentación técnica exhaustiva
- Preparado para producción (Docker, Gunicorn, Nginx)

---

## Características Principales

### 1. **Gestión de Ventas**
- Búsqueda rápida de productos por código o nombre
- Preview en tiempo real de producto seleccionado
- Tabla editable de productos en venta
- Panel de resumen con totales automáticos
- Confirmación y registro de ventas

### 2. **Inventario**
- Visualización completa de productos
- Indicadores de stock bajo
- Valor total del inventario
- Producto más vendido
- Búsqueda y filtrado avanzado
- Paginación (10 productos por página)

### 3. **Registros y Reportes**
- Historial completo de ventas
- Filtros por fecha, usuario, monto
- Gráficos de ventas por mes/semana
- Productos más vendidos
- Estadísticas diarias y generales
- Exportable y paginado

### 4. **Gestión de Usuarios** (Admin)
- CRUD completo de usuarios
- Roles: Admin, Usuario
- Validación de username único
- Cifrado de contraseñas con Werkzeug
- Verificación de disponibilidad en tiempo real

### 5. **Sistema de Diseño Profesional**
- Dark mode OLED-friendly (#0D1117)
- 50+ variables CSS reutilizables
- Componentes accesibles (WCAG AA+)
- Tipografía escalada
- Paleta de colores semántica
- Responsive design (Mobile-first)

---

## Stack Tecnológico

### Backend
- **Framework:** Flask 3.0+
- **ORM:** SQLAlchemy 2.0
- **Base de Datos:** SQLite (desarrollo), PostgreSQL (producción)
- **Autenticación:** Werkzeug (password hashing)
- **Logging:** Sistema centralizado con rotación

### Frontend
- **HTML5:** Jinja2 templating
- **CSS3:** Design system modular (700+ líneas)
- **JavaScript:** Vanilla ES6+ (sin jQuery, sin frameworks)
- **Responsive:** Bootstrap 5 (compatibilidad)
- **Iconos:** Bootstrap Icons

### DevOps
- **Contenedorización:** Docker & Docker Compose
- **Servidor Web:** Gunicorn + Nginx
- **BD Persistencia:** PostgreSQL en contenedor
- **Linting:** Flake8, Black, isort
- **Pre-commit:** Hooks automáticos

---

## Estructura del Proyecto

```
kairos/
├── app.py                          # Punto de entrada Flask
├── config.py                       # Configuración por ambiente
├── models/                         # Modelos de datos
│   ├── usuario.py
│   ├── producto.py
│   ├── venta.py
│   └── inventario.py
├── routes/                         # Blueprints Flask
│   ├── auth_routes.py             # Login/Logout
│   ├── ventas_routes.py           # Sistema de ventas
│   ├── productos_routes.py        # Gestión de productos
│   ├── inventario_routes.py       # Vista de inventario
│   ├── registros_routes.py        # Reportes y análisis
│   └── admin_routes.py            # Gestión de usuarios
├── services/                       # Lógica de negocio
│   ├── ventas_service.py
│   └── productos_service.py
├── static/
│   ├── css/
│   │   ├── design-system.css      # Sistema de diseño (700 líneas)
│   │   ├── login.css              # Estilos login
│   │   └── ventas.css             # Estilos ventas
│   └── js/
│       ├── product-search.js      # Búsqueda de productos
│       ├── sales-table.js         # Tabla de ventas
│       ├── summary-panel.js       # Panel de resumen
│       └── search-modal.js        # Modal de búsqueda
├── templates/
│   ├── base.html                  # Template base
│   ├── login.html                 # Página de login (standalone)
│   ├── agregar_venta.html         # Sistema de ventas
│   ├── inventario.html            # Inventario
│   ├── productos.html             # Lista de productos
│   ├── registros/                 # Vistas de reportes
│   └── admin/                     # Gestión de usuarios
├── tests/                         # Suite de tests
├── utils/
│   ├── decorators.py              # @login_required, @admin_required
│   ├── error_handlers.py          # Manejo de errores
│   └── logging_config.py          # Configuración de logs
├── Documentacion/                 # Documentación técnica
│   ├── DESIGN_SYSTEM.md
│   ├── ARQUITECTURA_MODULAR_VENTAS.md
│   └── ... (20+ archivos)
├── Dockerfile                     # Multi-stage Dockerfile
├── docker-compose.yml             # Orquestación de contenedores
├── requirements.txt               # Dependencias Python
└── README.md                      # Este archivo
```

---

## Sistema de Diseño

El proyecto implementa un **sistema de diseño profesional** basado en principios SaaS:

### Paleta de Colores
```css
/* Dark Mode OLED-Friendly */
--bg-primary: #0D1117          /* Fondo principal */
--bg-secondary: #161B22        /* Cards, panels */
--color-primary: #3B82F6       /* Acciones primarias */
--color-success: #10B981       /* Operaciones exitosas */
--color-danger: #EF4444        /* Errores */
```

### Componentes
- Botones (4 variantes × 3 tamaños)
- Inputs (5 estados: default, focus, error, disabled, loading)
- Cards (header, body, footer)
- Forms con validación progresiva
- Alertas (success, error, warning, info)
- Tablas responsivas

---

## Seguridad

- Contraseñas hasheadas con Werkzeug (PBKDF2)
- Sesiones seguras con SECRET_KEY
- CSRF protection (Flask-WTF)
- Decoradores @login_required y @admin_required
- Control de acceso basado en roles (RBAC)
- Validación en cliente y servidor
- Sanitización de inputs

---

## Flujos Principales

### Flujo de Venta
```
Usuario busca producto (código/nombre)
    ↓
Backend busca en BD (sin restricción admin)
    ↓
Frontend muestra preview con: nombre, precio, stock
    ↓
Usuario confirma cantidad
    ↓
Se agrega a tabla con cálculo automático de total
    ↓
Usuario confirma venta
    ↓
Backend registra venta, actualiza stock
    ↓
Confirmación con resumen
```

### Flujo de Registro/Reportes
```
Usuario accede a Registros (admin)
    ↓
Puede filtrar por: fecha, usuario, monto, búsqueda
    ↓
Ve gráficos: ventas por mes, productos más vendidos
    ↓
Estadísticas: total recaudado, cantidad ventas, etc
    ↓
Tabla paginada con detalles de cada venta
```

---

## Rendimiento

- **Búsqueda de productos:** < 100ms (índice en BD)
- **Carga de página:** < 2s (lazy loading)
- **CSS:** 980 líneas (optimizado, sin duplicados)
- **JavaScript:** ~2KB por módulo (minificado)
- **Images:** SVG + iconos Font Awesome

---

## Testing

Suite de tests incluida:
```bash
pytest tests/
```

Cobertura:
- Error handlers (404, 500)
- Logging configuration
- CRUD de productos
- Setup de aplicación
- Flujo completo de ventas

---

## Documentación

Se incluye documentación técnica exhaustiva en `/Documentacion/`:

| Documento | Descripción |
|-----------|------------|
| DESIGN_SYSTEM.md | Sistema de diseño completo |
| ARQUITECTURA_MODULAR_VENTAS.md | Arquitectura de módulos JS |
| REFACTORING_MODULAR_VENTAS.md | Detalles de refactorización |
| UX_UI_PRINCIPLES.md | Principios UX/UI |
| CHEATSHEET_MODULOS.md | API rápida de módulos |
| TESTING_CHECKLIST.md | Checklist para testing |

---

## Deployment

El proyecto está configurado para producción:

### Docker
```bash
docker-compose up --build
```

### Gunicorn + Nginx
```bash
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

### Configuración por Ambiente
- **Development:** SQLite, DEBUG=True
- **Production:** PostgreSQL, DEBUG=False, HTTPS

---

## Dependencias Principales

```
Flask==3.0.0
SQLAlchemy==2.0.0
Werkzeug==3.0.0
python-dotenv==1.0.0
Gunicorn==21.0.0
psycopg2-binary==2.9.0  # PostgreSQL
```

Ver `requirements.txt` para lista completa.

---

## Aprendizajes y Mejores Prácticas

Este proyecto demuestra:

 **Arquitectura escalable**
- Separación de concerns (routes, models, services, templates)
- Blueprints Flask para modularidad
- ORM centralizado con SQLAlchemy

**Frontend modular**
- JavaScript sin dependencias externas
- Eventos personalizados para comunicación entre módulos
- Macros Jinja2 para componentes reutilizables

**UX/UI profesional**
- Dark mode optimizado para uso intensivo
- Validación progresiva
- Accesibilidad WCAG AA+
- Responsive design mobile-first

**DevOps y producción**
- Docker multi-stage para optimización
- Configuración por ambiente
- Logging centralizado
- Pre-commit hooks automáticos

---

## Estado del Proyecto

- **Backend:** Completo y funcional
- **Frontend:** Diseño modular implementado
- **Documentación:** Exhaustiva
- **Pruebas:** Suite básica incluida
- **Deployment:** Docker y Gunicorn configurados
- **Mejoras futuras:** Exportación a PDF, integración con APIs externas

---

**Última actualización:** 17 de enero de 2026

---


## Notas Importantes

### Este es un Proyecto Personal
- Demuestra habilidades en desarrollo full-stack
- Muestra arquitectura profesional y mejores prácticas
- Sirve como portafolio técnico

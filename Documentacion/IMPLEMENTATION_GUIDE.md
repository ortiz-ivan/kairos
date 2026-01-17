# 🎯 Guía de Implementación - Componentes UI/UX

## 📋 Archivos Creados

```
static/
├── css/
│   ├── design-system.css    ← Variables, componentes base
│   └── login.css            ← Estilos específicos login
└── js/
    └── form-validation.js   ← Validación en cliente

templates/
└── login.html               ← Nueva interfaz de login (profesional)

DESIGN_SYSTEM.md            ← Documentación completa del sistema
```

---

## 🎨 Sistema de Diseño - Características Clave

### 1. Variables CSS (tokens de diseño)

Todas las variables están en `:root` en `design-system.css`:

```css
/* Acceso universal */
--bg-primary: #0D1117          /* Fondo principal */
--color-primary: #3B82F6       /* Acciones CTA */
--text-primary: #E5E7EB        /* Texto legible */
```

**Beneficio**: Cambiar colores en un solo lugar afecta toda la app.

### 2. Componentes Base (Reutilizables)

#### Botones

```html
<!-- Primario (acciones principales) -->
<button class="btn btn-primary">Guardar</button>

<!-- Secundario (acciones comunes) -->
<button class="btn btn-secondary">Cancelar</button>

<!-- Terciario (links) -->
<button class="btn btn-tertiary">Más opciones</button>

<!-- Peligroso (eliminar) -->
<button class="btn btn-danger">Eliminar</button>

<!-- Tamaños -->
<button class="btn btn-primary btn-sm">Pequeño</button>
<button class="btn btn-primary btn-lg">Grande</button>
```

#### Inputs con Validación

```html
<div class="form-group">
  <label for="email">Email <span class="required">*</span></label>
  <input
    type="email"
    id="email"
    name="email"
    placeholder="usuario@empresa.com"
    class="is-valid"
    <!--
    O
    is-invalid
    --
  />
  >
  <span class="help-text">Verifica este correo</span>
  <span class="error-message" style="display: none;">Email inválido</span>
</div>
```

**Estados de input:**

- ✅ Válido: `class="is-valid"` (borde verde + ícono ✓)
- ❌ Inválido: `class="is-invalid"` (borde rojo + ícono ✗)
- ⭕ Neutral: Sin clase (estado normal)

#### Tarjetas

```html
<div class="card">
  <div class="card-header">
    <h3 class="card-title">Título</h3>
    <button class="btn btn-tertiary">Acción</button>
  </div>
  <div class="card-body">Contenido aquí</div>
  <div class="card-footer">
    <button class="btn btn-secondary">Cancelar</button>
    <button class="btn btn-primary">Guardar</button>
  </div>
</div>
```

### 3. Sistema de Espaciado (8px base)

```
--space-xs: 4px      /* Espacios micro */
--space-sm: 8px      /* Padding botones, gaps pequeños */
--space-md: 16px     /* Padding cards, margins normales */
--space-lg: 24px     /* Secciones */
--space-xl: 32px     /* Separaciones principales */
--space-xxl: 48px    /* Áreas amplias */
```

**Uso en HTML:**

```html
<div class="p-lg mb-lg">
  <button class="btn gap-md">Icon + Text</button>
</div>
```

### 4. Tipografía Coherente

```
H1: 28px Bold       → Títulos principales
H2: 24px Semibold   → Subtítulos
H3: 18px Semibold   → Encabezados menores
Body: 14px Normal   → Contenido
Small: 12px Normal  → Ayudas
```

---

## ⚡ Login - Funcionalidades Implementadas

### 1. Validación en Cliente (Real-time)

```javascript
const validator = new FormValidator("#loginForm");

validator
  .addRule("username", [ValidationRules.required])
  .addRule("password", [
    ValidationRules.required,
    ValidationRules.minLength(6),
  ]);
```

**Features:**

- ✅ Debounce de 300ms (no valida demasiado rápido)
- ✅ Mensaje de error claro bajo el campo
- ✅ Ícono visual (✓ o ✗)
- ✅ Validación al salir del campo (blur)
- ✅ Validación al enviar

### 2. Toggle de Contraseña

```html
<div class="password-toggle">
  <input type="password" id="password" />
  <button class="password-toggle-btn">👁️</button>
</div>
```

**Funcionalidad:**

- Click en ojo → muestra/oculta contraseña
- Permanece funcional en mobile
- Accessibile (ARIA labels)

### 3. Alertas Visuales

```javascript
// Desde JavaScript
Alert.success('Bienvenido, usuario');
Alert.error('Usuario o contraseña incorrectos');
Alert.info('Recuerda cambiar tu contraseña');

// Desde servidor (Flask)
flash('Mensaje', 'success')  # → alerta verde
flash('Mensaje', 'error')    # → alerta roja
```

### 4. Loading State

```javascript
LoadingState.enable("#submitBtn");
// Botón muestra spinner
LoadingState.disable("#submitBtn");
// Botón vuelve a normal
```

### 5. Accesibilidad (WCAG)

✅ Contraste 4.5:1 (WCAG AA)
✅ Focus visible en todos elementos interactivos
✅ Labels asociados a inputs
✅ Atributos aria-\* en componentes
✅ Navegación por teclado (Tab, Enter, Escape)

---

## 🔧 Cómo Usar en Otros Templates

### Paso 1: Importar CSS en el `<head>`

```html
<link
  rel="stylesheet"
  href="{{ url_for('static', filename='css/design-system.css') }}"
/>
<!-- Estilos adicionales si es necesario -->
<link
  rel="stylesheet"
  href="{{ url_for('static', filename='css/login.css') }}"
/>
```

### Paso 2: Usar Componentes

```html
<!-- Botón -->
<button class="btn btn-primary">Crear Venta</button>

<!-- Card con tabla -->
<div class="card">
  <div class="card-header">
    <h3 class="card-title">Últimas Ventas</h3>
  </div>
  <div class="card-body">
    <table>
      <!-- Contenido -->
    </table>
  </div>
</div>

<!-- Formulario con validación -->
<div class="form-group">
  <label>Monto <span class="required">*</span></label>
  <input type="number" required />
  <span class="help-text">Ingresa el monto en guaraní</span>
</div>
```

### Paso 3: Inicializar Validador (si es necesario)

```html
<script src="{{ url_for('static', filename='js/form-validation.js') }}"></script>

<script>
  const validator = new FormValidator("#miForm");
  validator.addRule("email", [ValidationRules.email]);
  validator.addRule("password", [
    ValidationRules.required,
    ValidationRules.strongPassword,
  ]);
</script>
```

---

## 📊 Próximos Componentes a Implementar

### 1. Dashboard Layout

```html
<div class="dashboard">
  <aside class="sidebar"><!-- Navegación --></aside>
  <main class="main-content">
    <header class="top-header"><!-- Search, user menu --></header>
    <div class="content"><!-- Contenido dinámico --></div>
  </main>
</div>
```

### 2. Tabla de Datos (Ventas, Productos)

```html
<table class="data-table">
  <thead>
    <tr>
      <th><input type="checkbox" /></th>
      <th sortable>Columna 1</th>
      <th>Acciones</th>
    </tr>
  </thead>
  <tbody>
    <tr class="hover:bg-tertiary">
      <td><input type="checkbox" /></td>
      <td>Dato</td>
      <td class="actions">
        <button class="btn btn-sm btn-tertiary">Editar</button>
        <button class="btn btn-sm btn-danger">Eliminar</button>
      </td>
    </tr>
  </tbody>
</table>
```

### 3. Formularios CRUD

```html
<form id="productoForm" class="form-crud">
  <div class="form-group">
    <label>Nombre Producto <span class="required">*</span></label>
    <input type="text" name="nombre" required />
  </div>

  <div class="form-group">
    <label>Precio <span class="required">*</span></label>
    <input type="number" name="precio" step="0.01" required />
  </div>

  <div class="card-footer">
    <button type="reset" class="btn btn-secondary">Limpiar</button>
    <button type="submit" class="btn btn-primary">Guardar Producto</button>
  </div>
</form>
```

---

## 🎯 Reglas de Consistencia Visual

### ✅ HACER

1. **Usar siempre variables CSS** - Nunca hardcodear colores
2. **Paleta limitada** - Solo 7 colores semánticos
3. **Spacing consistente** - Múltiplos de 8px
4. **Validación visual clara** - Iconos + color + mensaje
5. **Contraste suficiente** - 4.5:1 mínimo
6. **Animaciones <300ms** - Rápidas y sutiles
7. **Responsive first** - Mobile primero, luego desktop
8. **Nombres significativos** - `btn-primary`, no `btn-blue`

### ❌ NO HACER

1. ❌ Colores hardcodeados: `style="color: #3B82F6"`
2. ❌ Espacios aleatorios: `margin: 23px` (no múltiplo de 8)
3. ❌ Demasiados colores: > 7 en interfaz
4. ❌ Botones invisibles: Alto < 44px en mobile
5. ❌ Sin tooltips: Iconos sin explicación
6. ❌ Animaciones largas: > 500ms
7. ❌ Scroll horizontal necesario: Usar wrap o scroll native
8. ❌ Eliminar sin confirmación

---

## 🚀 Testing & Validación

### Desktop

```bash
# Firefox
# Chrome
# Edge
```

### Mobile

```bash
# iPhone 12/13
# Android (Chrome)
# iPad
```

### Accesibilidad

```bash
# Navegación solo con teclado (Tab, Shift+Tab)
# Screen reader (NVDA, JAWS)
# Contraste (use https://webaim.org/resources/contrastchecker/)
```

### Performance

```bash
# Design System CSS: < 15KB
# Validación JS: < 8KB
# Total: < 30KB (gzipped)
```

---

## 📱 Ejemplo: Página de Productos (usando componentes)

```html
{% extends "base.html" %} {% block content %}

<div class="card">
  <div class="card-header flex-between">
    <h2 class="card-title">Gestión de Productos</h2>
    <a href="/productos/nuevo" class="btn btn-primary btn-sm">
      ➕ Nuevo Producto
    </a>
  </div>

  <div class="card-body">
    <!-- Filtros -->
    <div class="mb-lg" style="display: flex; gap: var(--space-md);">
      <input
        type="search"
        placeholder="Buscar producto..."
        class="search-input"
        style="flex: 1;"
      />
      <select style="width: auto;">
        <option>Todas las categorías</option>
      </select>
    </div>

    <!-- Tabla -->
    <table class="data-table">
      <thead>
        <tr>
          <th><input type="checkbox" /></th>
          <th>Nombre</th>
          <th class="text-right">Precio</th>
          <th class="text-right">Stock</th>
          <th>Categoría</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        {% for producto in productos %}
        <tr>
          <td><input type="checkbox" /></td>
          <td>{{ producto.nombre }}</td>
          <td class="text-right">₲{{ producto.precio }}</td>
          <td class="text-right">{{ producto.stock }}</td>
          <td>{{ producto.categoria }}</td>
          <td class="flex gap-sm">
            <a
              href="/productos/{{ producto.id }}/editar"
              class="btn btn-tertiary btn-sm"
            >
              ✎ Editar
            </a>
            <button class="btn btn-danger btn-sm">🗑️ Eliminar</button>
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>

  <div class="card-footer">
    <span class="text-secondary">
      Mostrando {{ productos|length }} de {{ total_productos }}
    </span>
    <!-- Paginación aquí -->
  </div>
</div>

{% endblock %}
```

---

## 💡 Tips & Tricks

### 1. Dark Mode Automático

El CSS ya está optimizado para dark mode. Si necesitas toggle:

```javascript
// Cambiar tema
document.documentElement.style.colorScheme = "dark"; // o 'light'
```

### 2. Animaciones Reducidas (Accesibilidad)

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
  }
}
```

### 3. Alto Contraste (Accesibilidad)

```css
@media (prefers-contrast: more) {
  /* Borders más gruesos, colores más vibrantes */
}
```

### 4. Modo Foco (Screen Reader)

```css
:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

---

## 📞 Soporte

Para agregar nuevos componentes:

1. Definir variables CSS en `:root`
2. Crear clase CSS con `btn-*`, `.card`, etc.
3. Documentar en esta guía
4. Usar en 2+ vistas para validar reutilización

---

**Última actualización:** 15 de enero, 2026
**Version:** 1.0 (Base)
**Próximos:** Dashboard layout, tablas, sidebar

# ⚡ Quick Reference - Sistema de Diseño Kairos

## 🎨 Colores (Usar variables, NUNCA hardcodear)

```css
/* BACKGROUNDS */
--bg-primary: #0D1117         /* Fondo principal */
--bg-secondary: #161B22       /* Cards, panels */
--bg-tertiary: #21262D        /* Hover, active */

/* ACCIONES & ESTADOS */
--color-primary: #3B82F6      /* Botón primario, acciones */
--color-success: #10B981      /* Éxito, ventas ✓ */
--color-danger: #EF4444       /* Error, validación ✗ */
--color-warning: #F59E0B      /* Advertencia ⚠ */
--color-info: #06B6D4         /* Info ℹ */

/* TEXTO */
--text-primary: #E5E7EB       /* Texto principal */
--text-secondary: #9CA3AF     /* Metadata, help */
--text-tertiary: #6B7280      /* Desactivado */
```

**Uso:**

```html
<div style="color: var(--text-primary); background: var(--bg-secondary);">
  Usar SIEMPRE variables
</div>
```

---

## 📐 Espaciado (8px base)

```
--space-xs: 4px      ← Gap mínimo
--space-sm: 8px      ← Padding botones, gaps
--space-md: 16px     ← Padding cards
--space-lg: 24px     ← Secciones
--space-xl: 32px     ← Separaciones principales
--space-xxl: 48px    ← Áreas amplias
```

**Uso:**

```html
<div class="p-lg mb-lg">Padding: 24px, Margin-bottom: 24px</div>

<div class="flex gap-md">Gap: 16px entre elementos</div>
```

---

## 🔤 Tipografía

| Uso     | Tamaño | Peso     | Ejemplo          |
| ------- | ------ | -------- | ---------------- |
| H1      | 28px   | Bold     | Título principal |
| H2      | 24px   | Semibold | Subtítulo        |
| H3      | 18px   | Semibold | Encabezado       |
| Body    | 14px   | Normal   | Texto contenido  |
| Small   | 12px   | Normal   | Help text        |
| Caption | 11px   | Medium   | Etiquetas        |

**Uso:**

```html
<h1>Título principal</h1>
<h2>Subtítulo</h2>
<p>Párrafo normal</p>
<small>Texto pequeño</small>
<span class="caption">ETIQUETA</span>
```

---

## 🔘 Componentes Básicos

### Botón

```html
<button class="btn btn-primary">Guardar</button> ← Primario (azul)
<button class="btn btn-secondary">Cancelar</button> ← Secundario (gris)
<button class="btn btn-danger">Eliminar</button> ← Destructivo (rojo)
<button class="btn btn-primary btn-lg">Grande</button> ← Tamaño
<button class="btn btn-primary btn-sm">Pequeño</button> ← Tamaño
```

### Input

```html
<input type="text" placeholder="Escribe aquí" />
<input type="email" placeholder="correo@ejemplo.com" />
<input type="password" placeholder="••••••••" />
```

**Estados:**

```html
<input class="is-valid" /> ← Verde + ✓ (válido) <input class="is-invalid" /> ←
Rojo + ✗ (inválido) <input disabled /> ← Desactivado
```

### Card

```html
<div class="card">
  <div class="card-header">
    <h3 class="card-title">Título</h3>
  </div>
  <div class="card-body">Contenido</div>
  <div class="card-footer">
    <button class="btn btn-primary">Guardar</button>
  </div>
</div>
```

---

## ✅ Validación - Reglas Comunes

```javascript
ValidationRules.required; // Campo obligatorio
ValidationRules.email; // Email válido
ValidationRules.minLength(8); // Mínimo 8 caracteres
ValidationRules.maxLength(100); // Máximo 100 caracteres
ValidationRules.strongPassword; // 8+, mayús, número, especial
ValidationRules.matches("#otroField"); // Coincide con otro campo
ValidationRules.pattern(/^\d{3}$/, "msg"); // Patrón regex
```

**Uso:**

```javascript
const validator = new FormValidator("#miForm");
validator.addRule("email", [ValidationRules.email]);
validator.addRule("password", [
  ValidationRules.required,
  ValidationRules.minLength(8),
]);
```

---

## 🚨 Alertas

```javascript
Alert.success("✓ Cambios guardados"); // Verde, auto-close 3s
Alert.error("✗ Error de conexión"); // Rojo, manual close
Alert.warning("⚠ Cambios sin guardar"); // Naranja
Alert.info("ℹ Información útil"); // Azul
```

---

## 📱 Responsive

```
Mobile:   < 640px   (1 columna, full-width)
Tablet:   640-1024px (2 columnas)
Desktop:  > 1024px  (sidebar + 3 columnas)
```

**Reglas:**

- Botones: Mínimo 44x44px (touch)
- Inputs: Full width en mobile
- Tablas: Card view en mobile
- Sidebar: Drawer collapsable

---

## ♿ Accesibilidad - Esencial

```html
<!-- LABELS (siempre) -->
<label for="email">Email</label>
<input id="email" type="email" />

<!-- FOCUS VISIBLE (siempre) -->
:focus-visible { outline: 2px solid var(--color-primary); }

<!-- CONTRASTE (4.5:1 mínimo) -->
color: #E5E7EB; ← Legible background: #0D1117; ← Ratio 10.7:1 ✓

<!-- ARIA (en componentes complejos) -->
<div role="dialog" aria-labelledby="title">
  <h2 id="title">Confirmar</h2>
</div>

<!-- ALT TEXT (imágenes) -->
<img src="chart.png" alt="Ventas por mes" />
```

---

## 🎬 Transiciones & Animaciones

```css
--transition-fast: 150ms     /* Hover effects */
--transition-normal: 300ms   /* Modal entrance */
--transition-slow: 500ms     /* Complex animations */
```

**Regla:** Nunca > 500ms, preferentemente < 300ms

---

## 🔍 Validación en Cliente (Flujo)

```
Usuario escribe
    ↓
Debounce 300ms
    ↓
Validar localmente
    ↓
Mostrar resultado (✓ o ✗)
    ↓
Si submit:
  - Validar TODO
  - Si falla → mensaje error
  - Si ok → enviar servidor
```

---

## 📋 Formulario - Estructura Estándar

```html
<form id="miForm" novalidate>
  <div class="form-group">
    <label for="campo">
      Etiqueta
      <span class="required">*</span>
    </label>
    <input type="text" id="campo" name="campo" required />
    <span class="help-text">Texto de ayuda</span>
    <span class="error-message" style="display: none;"></span>
  </div>

  <div class="card-footer">
    <button type="reset" class="btn btn-secondary">Limpiar</button>
    <button type="submit" class="btn btn-primary">Guardar</button>
  </div>
</form>
```

---

## 🎯 Tabla de Datos - Estructura

```html
<table>
  <thead>
    <tr>
      <th><input type="checkbox" /></th>
      <th>Columna 1</th>
      <th>Acciones</th>
    </tr>
  </thead>
  <tbody>
    <tr style="height: 44px;">
      ← Mínimo para mobile
      <td><input type="checkbox" /></td>
      <td>Dato</td>
      <td>
        <button class="btn btn-sm btn-tertiary">Editar</button>
        <button class="btn btn-sm btn-danger">Eliminar</button>
      </td>
    </tr>
  </tbody>
</table>
```

---

## 🏗️ Layout Principal (Post-Login)

```html
<div class="dashboard">
  <header class="header">Logo | Search | User Menu</header>

  <aside class="sidebar">Navegación</aside>

  <main class="main-content">
    <div class="card">Contenido</div>
  </main>
</div>
```

---

## 🚀 Checklist Rápido

- [ ] ¿Uso variables CSS? (`var(--...)`)
- [ ] ¿Espaciado en 8px? (`--space-*`)
- [ ] ¿Validación cliente?
- [ ] ¿Confirmación destructiva?
- [ ] ¿Responsive 640px?
- [ ] ¿Focus visible?
- [ ] ¿Contraste 4.5:1?
- [ ] ¿Botones 44x44px?
- [ ] ¿Mensajes claros?
- [ ] ¿Animaciones < 300ms?

---

## 🔗 Documentación Completa

- [DESIGN_SYSTEM.md](./DESIGN_SYSTEM.md) - Sistema completo
- [UX_UI_PRINCIPLES.md](./UX_UI_PRINCIPLES.md) - Filosofía
- [IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md) - Guía de uso
- [COMPONENT_EXAMPLES.md](./COMPONENT_EXAMPLES.md) - Ejemplos prácticos
- [TESTING_CHECKLIST.md](./TESTING_CHECKLIST.md) - Validación

---

**Imprime esto o guárdalo como referencia rápida.**

**Última actualización:** 15 de enero, 2026

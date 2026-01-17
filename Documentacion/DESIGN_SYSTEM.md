# 🎨 Sistema de Diseño Kairos - SaaS Empresarial

## 📋 Filosofía de Diseño

**Principios Core:**

- ✅ **Minimalismo funcional**: Cada píxel tiene propósito
- ✅ **Dark mode nativo**: Reduce fatiga ocular en uso intensivo
- ✅ **Jerarquía clara**: Usuario sabe dónde está y qué hacer
- ✅ **Velocidad visual**: Información se procesa en < 2 segundos
- ✅ **Escalabilidad**: Funciona con 10 usuarios o 10.000 registros

---

## 🎯 Paleta de Colores

### Colores Primarios (Dark Mode Base)

```
Background Principal:    #0D1117 (casi negro, OLED-friendly)
Background Secundario:   #161B22 (cards, panels)
Superficie Terciaria:    #21262D (hover states)
Borde Sutil:             #30363D (dividers)
```

### Acciones & Estados

```
Primario (CTA):          #3B82F6 (azul profesional, acciones principales)
Secundario:              #6B7280 (neutral, acciones secundarias)
Éxito:                   #10B981 (ventas, datos positivos)
Advertencia:             #F59E0B (atención, cambios pendientes)
Crítico/Error:           #EF4444 (eliminar, problemas)
Info:                    #06B6D4 (información, tips)
```

### Texto

```
Primario:                #E5E7EB (blanco suave, legible)
Secundario:              #9CA3AF (ayuda, metadatos)
Terciario:               #6B7280 (desactivado, placeholders)
```

---

## 📐 Tipografía

### Jerarquía

```
H1: 28px / 700 / 36px (títulos principales)
H2: 24px / 600 / 32px (subtítulos, secciones)
H3: 18px / 600 / 24px (encabezados menores)
Body: 14px / 400 / 20px (contenido, tablas)
Small: 12px / 400 / 16px (ayuda, metadata)
Caption: 11px / 500 / 14px (etiquetas)
```

### Font Stack

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen",
  "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans", sans-serif;
```

---

## 🔲 Espaciado (8px base)

```
xs: 4px     (espacios mínimos)
sm: 8px     (padding botones, gaps)
md: 16px    (padding cards, margins)
lg: 24px    (secciones)
xl: 32px    (principales)
xxl: 48px   (hero sections)
```

---

## 🏗️ Arquitectura de Componentes

### 1️⃣ Layout Principal (Post-Login)

```
┌─────────────────────────────────────────────┐
│  Header (logo, search, user menu)           │
├──────────┬──────────────────────────────────┤
│          │                                  │
│ Sidebar  │    Main Content Area             │
│ (nav)    │    - Breadcrumb                  │
│          │    - Title + Actions             │
│          │    - Dashboard/Table/Form        │
│          │    - Pagination                  │
│          │                                  │
└──────────┴──────────────────────────────────┘
```

**Sidebar (collapsible)**

- Ancho: 240px (expandido), 64px (colapsado)
- Menú principal con iconos
- Sub-menús con hover
- Indicador activo (borde izquierdo azul)

**Header**

- Logo + search bar
- Breadcrumb (hilo de navegación)
- Acciones contextuales (+ Nueva Venta, etc)
- User menu (avatar, opciones, logout)

---

## 📊 Tablas de Datos (Componente Crítico)

### Principios

- Máx 10 columnas visibles (horizontal scroll para más)
- Altura fila: 44px (touch-friendly)
- Compresión: hover grey (#21262D) en filas
- Selectable: checkbox izquierda + acciones bulk

### Estructura

```html
<table>
  <thead>
    <!-- Fila pegajosa (sticky) en scroll -->
    <tr>
      <th><input type="checkbox" /></th>
      <th>Columna 1</th>
      <th>Columna 2</th>
      <th class="text-right">Monto</th>
      <th>Acciones</th>
    </tr>
  </thead>
  <tbody>
    <!-- Fila normal -->
    <tr class="hover:bg-surface-tertiary">
      ...
    </tr>
    <!-- Fila seleccionada -->
    <tr class="selected">
      ...
    </tr>
    <!-- Fila vacía -->
    <tr class="empty-state">
      ...
    </tr>
  </tbody>
</table>
```

**Acciones:**

- Inline: editar, ver (iconos sutiles)
- Bulk: checkbox múltiple + barra acciones flotante inferior
- Filtros: sidebar lateral o collapse superior

---

## 📝 Formularios & Validaciones

### Estados Input

```
Default:     Border #30363D, bg #0D1117
Focus:       Border #3B82F6, outline glow azul sutil
Valid:       Border #10B981, icon ✓
Error:       Border #EF4444, icon ✗, msg roja
Disabled:    Bg #161B22, cursor not-allowed, text #6B7280
Loading:     Spinner dentro del input
```

### Validación en Cliente

- Real-time (debounce 300ms)
- Mensajes claros debajo del input
- No desactives el envío hasta validar server
- Iconos visuales (✓ verde, ✗ rojo)

### Estructura Formulario

```html
<form>
  <div class="form-group">
    <label>Campo Requerido *</label>
    <input type="text" required />
    <span class="error-message">Mínimo 3 caracteres</span>
    <span class="help-text">Información útil aquí</span>
  </div>

  <button type="submit" class="btn btn-primary">Guardar</button>
  <button type="button" class="btn btn-secondary">Cancelar</button>
</form>
```

---

## 🚨 Jerarquía de Botones

### Primario (CTA Principal)

```
Fondo: #3B82F6 → Hover: #2563EB → Active: #1D4ED8
Padding: 10px 24px
Radius: 8px
Icon-left: sí
```

### Secundario (Acciones Comunes)

```
Fondo: #21262D → Hover: #30363D
Border: 1px #30363D
```

### Tertiary (Links/Acciones Menores)

```
Bg: transparent
Color: #3B82F6
Underline: hover
```

### Destructivo (Eliminar)

```
Fondo: #7F1D1D (rojo oscuro, menos agresivo)
Hover: #EF4444
```

---

## 🎭 Estados & Animaciones

### Transiciones

```css
Rápidas:   150ms (hover effects, color changes)
Normales:  300ms (modal entrance, slide-in)
Lentas:    500ms (complex animations, page transitions)
Easing:    cubic-bezier(0.4, 0, 0.2, 1) (material design)
```

### Loading States

- Spinner: 24px, rotación suave, #3B82F6
- Skeleton: pulso sutil de opacidad

### Empty States

- Icono grande (64px) en gray
- Mensaje claro: "No hay datos"
- CTA: "Crear primero +" en azul

---

## ♿ Accesibilidad Requerida

- ✅ Contraste mínimo 4.5:1 (WCAG AA)
- ✅ Focus visible en todos los elementos interactivos
- ✅ Labels asociados a inputs
- ✅ Roles ARIA en componentes complejos
- ✅ Navegación por teclado funcional (Tab, Enter, Escape)
- ✅ Nombres descriptivos para botones

---

## 📱 Responsive Design

### Breakpoints

```
Mobile:    < 640px  (1 columna, sidebar drawer)
Tablet:    640-1024px (2 columnas, sidebar colapsable)
Desktop:   > 1024px (layout completo)
```

### Comportamientos

- Sidebar → Drawer (hamburger icon)
- Tablas → Scroll horizontal + mobile view
- Modales → Full screen en mobile
- Tipografía → Escala según viewport

---

## 🚫 Errores Comunes a Evitar

❌ **NO HACER:**

1. Colores en rojo por todo (desensibilizar alertas)
2. Más de 7 colores en interfaz
3. Tablas sin paginación (UI lenta con 1000 rows)
4. Inputs sin validación visual
5. Iconos sin tooltip en acciones destructivas
6. Animaciones > 500ms (frustración)
7. Botones pequeños (< 44px altura mobile)
8. Mensajes de error genéricos ("Error")
9. Contraseña visible por defecto
10. Guardar sin confirmación en datos críticos

✅ **HACER:**

1. Paleta limitada pero coherente
2. Validación progresiva (paso a paso)
3. Preload datos mientras se espera
4. Acciones reversibles (undo, soft-delete)
5. Contexto en cada vista (breadcrumb, título)
6. Iconografía consistente
7. Loading states claros
8. Feedback táctil (toast, skeleton)
9. Mencionar cambios pending antes de navegar
10. Exportar datos en múltiples formatos

---

## 🔐 Login (Primera Pantalla)

**Objetivo:** Acceso rápido, seguro, claro

**Componentes:**

- Logo + marca
- Campos: email/usuario, contraseña
- Validación real-time
- "Recuérdame" checkbox (seguro)
- "¿Olvidaste contraseña?" link
- Opción social login (si aplica)
- Registro link (si SaaS abierto)

**UX Priorities:**

1. Cargar en < 2s
2. Contraseña visible toggle
3. Mensaje de error claro
4. Redirect a dashboard post-login automático

---

## 🎯 Próximos Pasos

1. ✅ **Login** (actualmente)
2. Dashboard principal
3. Tablas (ventas, productos, usuarios)
4. Formularios CRUD
5. Panel administrativo
6. Reportes y exportación

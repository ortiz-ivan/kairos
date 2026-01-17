# 🎭 Principios UX/UI - Kairos SaaS

## Filosofía Core

Kairos es una herramienta para uso **intensivo diario** en entornos empresariales. El usuario promedio:

- Pasa 6-8 horas/día en la app
- Realiza decenas de transacciones
- Necesita precisión (datos financieros)
- Exige velocidad (no tolera delays)

**Objetivo:** Interfaz que se "desaparece" - el usuario ve los datos, no la UI.

---

## 1️⃣ Velocidad Visual

### Principio: "Primero la información, luego la decoración"

**Lo que VERÁ el usuario:**

```
┌─ Ventas del Día ─────────────┐
│  ₲ 45.000.000                │  ← Número GRANDE
│  ↑ 12% vs. ayer              │  ← Contexto
│                              │
│  Últimas 5 transacciones:    │
│  - Juan López  ₲ 450.000 ✓  │
│  - María García ₲ 890.000 ✓ │
│  ...                         │
└──────────────────────────────┘
```

**Lo que NO verá:**

- ❌ Animaciones innecesarias
- ❌ Scrolls profundos (máx 3 scrolls para ver todo importante)
- ❌ Modales anidados (nunca modales dentro de modales)
- ❌ Cargas asincrónicas no indicadas

### Regla: "3 segundos o menos para decisión"

Toda acción primaria debe llevar ≤ 3 segundos:

- Ver reporte: <1s (precargado)
- Abrir formulario: <1s (validación en cliente)
- Ejecutar acción: <3s (con feedback)

---

## 2️⃣ Claridad Visual - Jerarquía Obsesiva

### Pirámide de Importancia

```
NIVEL 1 (TOP): Métrica principal
├─ Número grande (28px)
├─ Comparativa (12px subtle)
└─ CTA principal (AZUL, conspicuo)

NIVEL 2 (MEDIUM): Datos contextuales
├─ Tablas/listas
├─ Botones secundarios
└─ Información complementaria

NIVEL 3 (BAJO): Metadata
├─ Timestamps
├─ Versiones
└─ Links secundarios
```

### Ejemplo - Dashboard Ventas

```
╔════════════════════════════════════════════╗
║  HHeader: [Logo] [Search] [User Menu]    ║
╠════════════════════════════════════════════╣
║                                            ║
║  HOJA HOY                                  ║
║  ₲45.000.000    ↑12% vs. Ayer            ║  ← MÉTRICA PRINCIPAL
║                                            ║
║  ┌─ Actividad ─────┬─ Top Productos ─┐   ║
║  │ 248 transacs    │ 1. Producto A   │   ║  ← INFORMACIÓN SECUNDARIA
║  │ 89% tasa éxito  │ 2. Producto B   │   ║
║  └─────────────────┴─────────────────┘   ║
║                                            ║
║  ┌─ Últimas Transacciones ────────────┐  ║
║  │ Juan López    ₲450k  2:34 PM   ✓ │  ║  ← DETALLE (scroll si es necesario)
║  │ María García  ₲890k  2:30 PM   ✓ │  ║
║  │ Carlos Pérez  ₲230k  2:25 PM   ✓ │  ║
║  └────────────────────────────────────┘  ║
║                                            ║
╚════════════════════════════════════════════╝
```

**Regla:** Si usas ROJO, usa solo 1-2 veces máximo en toda la pantalla (criticidad).

---

## 3️⃣ Reducción de Errores - Prevención antes que Corrección

### Estrategia por Tipo de Error

#### Error: Campo requerido vacío

```
❌ MALO: Enviar form → Error server → Mostrar rojo

✅ BUENO: Usuario entra campo → Mostrar debajo:
          "Este campo es requerido"
          (Evita envío innecesario)
```

#### Error: Email duplicado

```
❌ MALO: Llenar todo → Enviar → Error server

✅ BUENO:
  1. Usuario entra email
  2. Validar formato en cliente (inmediato)
  3. Al salir del campo → Verificar en servidor (async)
  4. Si duplicado → Mostrar icono ✗ + "Este email ya existe"
  5. Botón submit desactivado hasta resolver
```

#### Error: Datos perdidos

```
❌ MALO: Navegar sin guardar → Perder todo

✅ BUENO:
  1. Auto-save cada 30s de inactividad en campos
  2. Mostrar "Guardado" suave en verde
  3. Si navega sin guardar → Modal: "¿Descartar cambios?"
  4. Botón "Volver atrás" para recuperar
```

#### Error: Eliminación permanente

```
❌ MALO: Click en "Eliminar" → Adiós datos

✅ BUENO:
  1. Click en "Eliminar" → Modal de confirmación
  2. Mostrar: "¿Eliminar 'Producto XYZ'?"
  3. 2 botones: "Cancelar" | "Sí, eliminar"
  4. Focus en "Cancelar" (safe default)
  5. Post-eliminación: Toast con "Eliminado" + botón "Deshacer" (10s)
```

### Checklist de Prevención

- ✅ Validación en cliente (< 300ms feedback)
- ✅ Validación en servidor (seguridad)
- ✅ Confirmación para acciones destructivas
- ✅ Undo/restore para datos eliminados
- ✅ Auto-save para formularios largos
- ✅ Indicación clara de campos requeridos
- ✅ Mensajes de error específicos (NO: "Error", SÍ: "Email debe contener @")
- ✅ Focus automático en campo con error

---

## 4️⃣ Dark Mode - Lo Que SÍ Funciona

### Por qué Dark Mode en SaaS empresarial:

1. **Fatiga ocular reducida** - 6+ horas diarias
2. **Velocidad perceptual** - Mejor contraste
3. **Menos errores** - Datos más legibles

### Implementación Correcta

```css
/* ❌ MALO: Blanco puro (#FFFFFF) */
color: #FFFFFF;  ← Quema la retina

/* ✅ BUENO: Blanco suave (#E5E7EB) */
color: #E5E7EB;  ← Cómodo, profesional

/* ❌ MALO: Negro puro (#000000) */
background: #000000;  ← Demasiado profundo

/* ✅ BUENO: Negro OLED-friendly (#0D1117) */
background: #0D1117;  ← Mejor consumo en OLED, softer
```

### Colores Semánticos (Nunca cambien)

| Estado      | Color     | Uso                             |
| ----------- | --------- | ------------------------------- |
| Éxito       | `#10B981` | Compras, confirmaciones, ✓      |
| Error       | `#EF4444` | Validación, ✗, alertas críticas |
| Advertencia | `#F59E0B` | Cambios pendientes, ⚠           |
| Info        | `#06B6D4` | Tips, ℹ, notas                  |
| Primario    | `#3B82F6` | Botones, enlaces, CTA           |

**Regla:** Si ves rojo en diseño != siempre significa "malo".

- Rojo suave (#EF4444) = error normal
- Rojo oscuro (#7F1D1D) = destructivo (eliminar)
- Rojo claro (#FEE2E2) = background error

---

## 5️⃣ Tablas de Datos - El Centro del Negocio

### Problemas Típicos

```
❌ Demasiadas columnas (10+) → Horizontal scroll horror
❌ Filas minúsculas (< 40px) → Imposible clickear en mobile
❌ Datos sin contexto → ¿Qué significa este número?
❌ Acciones escondidas → Hover reveal (mobile no tiene hover)
❌ Sin paginación → Scroll interminable (performance)
```

### Solución: Tabla Kairos

```html
<!-- ESTRUCTURA ÓPTIMA -->
<table class="data-table">
  <thead>
    <tr>
      <!-- Columna 1: Checkbox (seleccionar múltiples) -->
      <th><input type="checkbox" /></th>

      <!-- Columnas 2-5: Datos principales (máx 5 visibles) -->
      <th sort="id">ID</th>
      <th sort="fecha">Fecha</th>
      <th sort="monto">Monto</th>
      <th>Estado</th>

      <!-- Última columna: Acciones -->
      <th>Acciones</th>
    </tr>
  </thead>
  <tbody>
    <tr class="selectable">
      <!-- Fila normal -->
      <td><input type="checkbox" /></td>
      <td>#V001</td>
      <td>15 ene 2026</td>
      <td class="text-right">₲45.000</td>
      <td><span class="badge badge-success">✓ Pago</span></td>
      <td>
        <a href="/edit/1" class="btn-icon">✎</a>
        <a href="#" class="btn-icon" onclick="...">👁️</a>
      </td>
    </tr>

    <tr class="selected">
      <!-- Fila seleccionada (bg sutil) -->
    </tr>
  </tbody>
</table>

<!-- PAGINACIÓN -->
<nav class="pagination">
  <button disabled>← Anterior</button>
  <span>Página 1 de 12</span>
  <button>Siguiente →</button>
</nav>

<!-- BARRA DE ACCIONES (Float en bottom) -->
<div class="actions-bar">
  <span>2 seleccionados</span>
  <button class="btn btn-secondary">Deseleccionar</button>
  <button class="btn btn-primary">Exportar PDF</button>
  <button class="btn btn-danger">Eliminar</button>
</div>
```

### Características Clave

1. **Altura mínima de fila: 44px** (mobile touch-friendly)
2. **Máx 5-6 columnas** (más = scroll lateral)
3. **Acciones siempre visibles** (NO hover reveal)
4. **Paginación clara** (muestro en qué página estoy)
5. **Bulk actions** (checkbox + barra inferior)
6. **Sort by column** (click en encabezado)
7. **Responsive**: En mobile = mobile view (cards)

---

## 6️⃣ Formularios CRUD - El Flujo Seguro

### Patrón de Formulario

```html
<form id="productForm" novalidate>
  <!-- HEADER -->
  <div class="form-header">
    <h2>{{ 'Nuevo' if not product else 'Editar' }} Producto</h2>
    <button type="button" class="btn-icon" onclick="closeForm()">✕</button>
  </div>

  <!-- CAMPOS AGRUPADOS -->
  <fieldset>
    <legend>Información Básica</legend>

    <!-- Campo con validación -->
    <div class="form-group">
      <label for="nombre">
        Nombre del Producto
        <span class="required">*</span>
      </label>
      <input
        type="text"
        id="nombre"
        name="nombre"
        placeholder="Ej: Laptop Lenovo"
        required
        minlength="3"
        maxlength="100"
      />
      <span class="help-text">Max 100 caracteres</span>
      <span class="error-message" style="display: none;"></span>
    </div>

    <!-- Campo numérico -->
    <div class="form-group">
      <label for="precio">Precio (₲) <span class="required">*</span></label>
      <input
        type="number"
        id="precio"
        name="precio"
        placeholder="0.00"
        step="0.01"
        min="0"
        required
      />
      <span class="help-text">Precio en guaraní</span>
    </div>

    <!-- Campo select -->
    <div class="form-group">
      <label for="categoria">Categoría <span class="required">*</span></label>
      <select id="categoria" name="categoria" required>
        <option value="">-- Selecciona una categoría --</option>
        {% for cat in categories %}
        <option value="{{ cat.id }}">{{ cat.nombre }}</option>
        {% endfor %}
      </select>
    </div>
  </fieldset>

  <!-- FOOTER CON BOTONES -->
  <div class="form-footer">
    <div class="form-status">
      <span id="autoSaveStatus" class="text-secondary" style="display: none;">
        ✓ Guardado automático
      </span>
    </div>
    <div class="form-actions">
      <button type="reset" class="btn btn-secondary">Limpiar</button>
      <button type="button" class="btn btn-tertiary" onclick="closeForm()">
        Cancelar
      </button>
      <button type="submit" class="btn btn-primary">Guardar Producto</button>
    </div>
  </div>
</form>

<!-- SCRIPT DE VALIDACIÓN -->
<script>
  const validator = new FormValidator("#productForm");

  validator
    .addRule("nombre", [
      ValidationRules.required,
      ValidationRules.minLength(3),
      ValidationRules.maxLength(100),
    ])
    .addRule("precio", [
      ValidationRules.required,
      {
        validate: (v) => ({
          valid: parseFloat(v) > 0,
          message: "Precio debe ser mayor a 0",
        }),
      },
    ])
    .addRule("categoria", [ValidationRules.required]);

  // Auto-save cada 30s
  let autoSaveTimer;
  document.getElementById("productForm").addEventListener("input", () => {
    clearTimeout(autoSaveTimer);
    autoSaveTimer = setTimeout(() => {
      // Enviar datos parciales al servidor
      console.log("Auto-save...");
      document.getElementById("autoSaveStatus").style.display = "inline";
    }, 30000);
  });
</script>
```

### Flujo de Envío Seguro

```
Usuario hace click en "Guardar"
    ↓
1. Validación LOCAL (< 100ms)
   └─ Si falla → Mostrar error, NO continuar
    ↓
2. Mostrar loading en botón
    ↓
3. Enviar datos al servidor
    ↓
4. Si OK (200) → Modal éxito → Redirect
   Si ERROR (400+) → Toast con error específico
   Si TIMEOUT → Reintentar automático (3 intentos)
```

---

## 7️⃣ Notificaciones - El Sistema de Retroalimentación

### Tipos de Notificación

| Tipo        | Color   | Duración          | Ubicación  | Ejemplo                 |
| ----------- | ------- | ----------------- | ---------- | ----------------------- |
| **Success** | Verde   | 3s auto-close     | Top-right  | "✓ Venta registrada"    |
| **Error**   | Rojo    | 5s + botón cerrar | Top-right  | "✗ Email ya existe"     |
| **Warning** | Naranja | Sin auto-close    | Banner top | "⚠ Cambios sin guardar" |
| **Info**    | Azul    | Sin auto-close    | In-context | "ℹ Usa @ en email"      |

### Implementación

```javascript
// Éxito - Auto-desaparece
Alert.success("Venta guardada correctamente", 3000);

// Error - Usuario decide cuándo cerrar
Alert.error("Error de conexión. Reintentar?", 0); // 0 = sin auto-close

// Warning - Persistente
Alert.warning("Tienes cambios sin guardar", 0);

// Info - Inline (en el form)
<span class="help-text">Usa @ en el email</span>;
```

---

## 8️⃣ Responsive Design - Mobile First

### Breakpoints Kairos

```
Mobile:   < 640px  (1 columna, full-width)
Tablet:   640-1024px (2 columnas)
Desktop:  > 1024px (sidebar + 3 columnas)
```

### Comportamientos Adaptativos

```
┌─ DESKTOP (1440px) ──────────────────┐
│ [Logo] [Search] ────── [User Menu]  │
├────────┬──────────────────────────────┤
│ Sidebar│ Main Content (tablas, cards)│
│ (240px)│                              │
└────────┴──────────────────────────────┘

┌─ TABLET (800px) ─────────────────┐
│ [☰] [Logo] [Search] [User Menu]  │
├───────────────────────────────────┤
│ Main Content (full width)         │
│ Sidebar = drawer (slide from left)│
└───────────────────────────────────┘

┌─ MOBILE (375px) ──────────┐
│ [☰] [Logo] [⋯]           │
├───────────────────────────┤
│ Main Content              │
│ (1 columna, full scroll)  │
│ Tables → Card view        │
│ Buttons → Full width      │
└───────────────────────────┘
```

### Regla Mobile

- ✅ Botones: Mínimo 44x44px (dedo humano)
- ✅ Inputs: Full width menos padding
- ✅ Tablas: Convertir a cards horizontales
- ✅ Sidebar: Drawer collapsable
- ✅ Modales: Full screen en mobile

---

## 9️⃣ Performance UX - Velocidad es Feature

### Métricas Objetivo

| Métrica                            | Objetivo | Impacto                  |
| ---------------------------------- | -------- | ------------------------ |
| **LCP** (Largest Contentful Paint) | < 2.5s   | Cuando aparece contenido |
| **FID** (First Input Delay)        | < 100ms  | Respuesta a clicks       |
| **CLS** (Cumulative Layout Shift)  | < 0.1    | Cambios inesperados      |
| **TTFB** (Time to First Byte)      | < 600ms  | Respuesta servidor       |

### Optimizaciones Implementadas

```python
# Backend (Flask)
@app.route('/api/ventas')
def get_ventas():
    # Cache de 30s
    cached = cache.get('ventas_list')
    if cached:
        return cached

    # Paginar: MAX 25 items/página
    ventas = Venta.query.paginate(page=1, per_page=25)
    return jsonify(ventas)
```

```javascript
// Frontend
// 1. Lazy load imágenes
<img src="placeholder.jpg" loading="lazy" />;

// 2. Debounce en buscar
const searchInput = document.querySelector("#search");
let searchTimeout;
searchInput.addEventListener("input", (e) => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    fetch(`/api/buscar?q=${e.target.value}`);
  }, 300);
});

// 3. Virtual scrolling en listas grandes
// Usar plugin: https://github.com/Akryum/vue-virtual-scroller
```

---

## 🔟 Accesibilidad - Inclusión desde Día 1

### WCAG AA Compliance

```html
<!-- ✅ Labels siempre asociados -->
<label for="email">Email</label>
<input id="email" type="email" />

<!-- ✅ ARIA para componentes complejos -->
<div role="dialog" aria-labelledby="title">
  <h2 id="title">Confirmar eliminación</h2>
</div>

<!-- ✅ Focus visible en TODO -->
<style>
  :focus-visible {
    outline: 2px solid var(--color-primary);
    outline-offset: 2px;
  }
</style>

<!-- ✅ Contraste 4.5:1 -->
color: #E5E7EB; /* 16 pt */ background: #0D1117; /* Ratio: 10.7:1 ✓ */

<!-- ✅ Alt text en imágenes -->
<img src="chart.png" alt="Ventas por mes: enero 45M, febrero 52M" />

<!-- ✅ Reduce motion para usuarios sensibles -->
@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }
```

---

## 📋 Checklist Final (Pre-Launch)

### Visual

- ✅ Dark mode coherente
- ✅ Paleta de 7 colores máximo
- ✅ Tipografía: H1-H3, Body, Small
- ✅ Espaciado: múltiplos de 8px
- ✅ Bordes: radius consistente (4, 8, 12px)

### Interacción

- ✅ Validación en cliente en tiempo real
- ✅ Confirmación para acciones destructivas
- ✅ Undo/restore disponible
- ✅ Loading states claros
- ✅ Mensajes de error específicos

### Rendimiento

- ✅ CSS < 20KB
- ✅ JS < 15KB
- ✅ Imágenes optimizadas (lazy load)
- ✅ Caching implementado
- ✅ Paginación en tablas

### Accesibilidad

- ✅ Contraste 4.5:1
- ✅ Focus visible
- ✅ Navegación solo teclado
- ✅ ARIA labels
- ✅ Alt text

### Mobile

- ✅ Botones: 44x44px mínimo
- ✅ Inputs: full width
- ✅ Sidebar: drawer
- ✅ Tablas: card view
- ✅ Responsive: 640px breakpoint

---

**Principios = Guía para decisiones futuras**
Cuando dudes entre dos opciones de diseño, elige la que:

1. Sea más rápida
2. Causen menos errores
3. Sea más clara
4. Sea más accesible

En ese orden.

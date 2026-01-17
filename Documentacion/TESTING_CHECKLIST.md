# 🧪 Testing Checklist - UI/UX Redesign

## Antes de publicar cualquier cambio en una vista, verificar:

---

## 1️⃣ Visual & Design

### Colores

- [ ] ¿Usa solo variables CSS? (`--color-*`, `--bg-*`, `--text-*`)
- [ ] ¿Evita hardcoding de colores? (No: `color: #E5E7EB`)
- [ ] ¿Contraste >= 4.5:1? (Verificar con WebAIM)
- [ ] ¿Dark mode se ve bien?
- [ ] ¿Paleta coherente? (Max 7 colores semánticos)

### Tipografía

- [ ] ¿Usa escala tipográfica? (H1-H3, Body, Small)
- [ ] ¿Títulos tienen peso adecuado? (Bold o Semibold)
- [ ] ¿Tamaño mínimo 12px en body?
- [ ] ¿Line-height adecuado? (~1.5 en body)

### Espaciado

- [ ] ¿Usa sistema 8px? (`--space-sm: 8px`, etc)
- [ ] ¿No hay espacios aleatorios? (`margin: 23px` ❌)
- [ ] ¿Consistencia entre componentes?
- [ ] ¿Respeta padding interno?

### Componentes

- [ ] ¿Botones tienen estado hover/active?
- [ ] ¿Inputs tienen validación visual?
- [ ] ¿Cards tienen shadow consistente?
- [ ] ¿Modales tienen overlay semi-transparent?

---

## 2️⃣ Interactividad & UX

### Feedback Visual

- [ ] ¿Los clicks tienen respuesta? (Color, shadow, etc)
- [ ] ¿Los estados se distinguen? (Hover, active, disabled)
- [ ] ¿Las transiciones son <300ms?
- [ ] ¿Hay loading states indicados?

### Formularios

- [ ] ¿Validación en cliente? (No solo server)
- [ ] ¿Debounce en búsqueda/verificación?
- [ ] ¿Mensajes de error claros?
- [ ] ¿Focus visible después de error?
- [ ] ¿Campos requeridos indicados?

### Acciones Destructivas

- [ ] ¿Confirmación antes de eliminar?
- [ ] ¿Opción de "Deshacer" (10s)?
- [ ] ¿Botón "Cancelar" en focus por defecto?
- [ ] ¿Mensaje claro de advertencia?

### Tablas de Datos

- [ ] ¿Filas > 44px altura (touch)?
- [ ] ¿Acciones siempre visibles?
- [ ] ¿Paginación clara?
- [ ] ¿Bulk actions funcionales?
- [ ] ¿Sort by column?

---

## 3️⃣ Responsiveness

### Desktop (> 1024px)

- [ ] ¿Layout correcto?
- [ ] ¿Sidebar visible?
- [ ] ¿Máximo 1440px de ancho?

### Tablet (640-1024px)

- [ ] ¿Sidebar colapsable?
- [ ] ¿Navegación por drawer?
- [ ] ¿Contenido legible?

### Mobile (< 640px)

- [ ] ¿Full width sin scroll horizontal?
- [ ] ¿Botones >= 44x44px?
- [ ] ¿Inputs full width?
- [ ] ¿Tablas convertidas a cards?
- [ ] ¿Sidebar como drawer?
- [ ] ¿Modales full screen?

### Testing en Dispositivos Reales

- [ ] iPhone 13 (390x844)
- [ ] Android Pixel 6 (412x915)
- [ ] iPad (1024x1366)
- [ ] Desktop 1920x1080

---

## 4️⃣ Accesibilidad (WCAG AA)

### Contraste

- [ ] 4.5:1 en texto normal
- [ ] 3:1 en elementos grandes
- [ ] Usar: https://webaim.org/resources/contrastchecker/

### Navegación por Teclado

- [ ] Tab: navega todos elementos
- [ ] Shift+Tab: navega hacia atrás
- [ ] Enter: activa botones/links
- [ ] Escape: cierra modales
- [ ] Arrow keys: navega selects/tabs

### Focus Visible

- [ ] Todos botones: focus visible
- [ ] Todos inputs: focus visible
- [ ] Todos links: focus visible
- [ ] Color de focus contrastado

### Labels & ARIA

- [ ] Todo input tiene `<label>`
- [ ] Labels ligados con `for=`
- [ ] Botones tienen texto claro
- [ ] Modales tienen `role="dialog"`
- [ ] Breadcrumb tiene `aria-current`

### Screen Reader

- [ ] Prueba con NVDA o JAWS
- [ ] Anuncios claros de cambios
- [ ] Estructura semántica correcta
- [ ] Tablas tienen `<thead>`, `<tbody>`

### Animaciones

- [ ] Respetar `prefers-reduced-motion`
- [ ] Opción para deshabilitar animaciones
- [ ] No usar parpadeos rápidos (> 3/s)

---

## 5️⃣ Performance

### CSS

- [ ] `design-system.css` < 20KB
- [ ] Estilos específicos en `login.css` < 10KB
- [ ] Minificado y comprimido con gzip

### JavaScript

- [ ] `form-validation.js` < 15KB
- [ ] Sin librerías innecesarias
- [ ] Event listeners limpios (no memory leaks)
- [ ] Debouncing en inputs/scroll

### Imágenes

- [ ] Formato moderno (WebP con fallback)
- [ ] Dimensiones correctas (no upscale)
- [ ] Lazy loading en non-critical
- [ ] Comprimidas

### Métricas (Lighthouse)

- [ ] LCP (Largest Contentful Paint) < 2.5s
- [ ] FID (First Input Delay) < 100ms
- [ ] CLS (Cumulative Layout Shift) < 0.1
- [ ] Performance Score > 90

---

## 6️⃣ Browser Compatibility

### Desktop Browsers

- [ ] Chrome 120+ ✓
- [ ] Firefox 121+ ✓
- [ ] Safari 17+ ✓
- [ ] Edge 120+ ✓

### Mobile Browsers

- [ ] Chrome (Android)
- [ ] Safari (iOS)
- [ ] Firefox (Android)
- [ ] Samsung Internet

### Verificar

- [ ] Display grid/flex funciona
- [ ] CSS variables soportadas
- [ ] Border-radius funciona
- [ ] Box-shadow funciona
- [ ] Transiciones suaves

---

## 7️⃣ Seguridad

### XSS Prevention

- [ ] No usar `innerHTML` con datos del usuario
- [ ] Escapar valores en Jinja2: `{{ value|e }}`
- [ ] CSRF token en formularios

### Input Validation

- [ ] Server-side validation siempre
- [ ] No confiar solo en validación cliente
- [ ] Sanitizar datos

### HTTPS

- [ ] Página sobre HTTPS en producción
- [ ] No cargar recursos vía HTTP
- [ ] Certificados válidos

---

## 8️⃣ Cross-Browser Testing

### Usar Herramientas

```bash
# BrowserStack (online testing)
https://www.browserstack.com/

# LambdaTest
https://www.lambdatest.com/

# Sauce Labs
https://saucelabs.com/

# Local testing
# Firefox DevTools > Responsive Design Mode
# Chrome DevTools > Device Toolbar
```

### Verificar

- [ ] Layouts sin bordes cortados
- [ ] Colores se ven bien
- [ ] Fuentes cargan correctamente
- [ ] Animaciones funcionan
- [ ] Formularios funcionan

---

## 9️⃣ Testing Manual

### Flujo de Usuario - Login

```
1. Abro página login
   ✓ Se carga en < 2 segundos
   ✓ Se ve profesional (dark mode)
   ✓ Tiene foco en campo usuario

2. Escribo usuario
   ✓ Texto aparece
   ✓ No hay validación aún (campo puede estar vacío)

3. Tab a contraseña
   ✓ Foco se mueve
   ✓ Usuario validado localmente (si hubo salida)
   ✓ Sin mensaje de error (campo vacío es ok)

4. Escribo contraseña
   ✓ Puntos en lugar de texto
   ✓ Botón "ojo" visible

5. Click en botón ojo
   ✓ Contraseña se muestra como texto
   ✓ Ícono cambia
   ✓ Click nuevamente = oculta

6. Checkbox "Recuérdame"
   ✓ Cambio estado visualmente
   ✓ Label clickeable

7. Click "Acceder"
   ✓ Validación en cliente
   ✓ Si error → mensaje debajo del input
   ✓ Si ok → botón muestra spinner
   ✓ Esperar respuesta servidor

8a. Respuesta OK (201)
    ✓ Toast success "Bienvenido"
    ✓ Redirect a dashboard
    ✓ No vuelve a login

8b. Respuesta ERROR (401)
    ✓ Toast error "Usuario o contraseña incorrectos"
    ✓ Botón vuelve a normal
    ✓ Foco en campo usuario
    ✓ Campos conservan valores
```

### Flujo de Usuario - Tabla

```
1. Abro página de productos
   ✓ Se carga tabla
   ✓ Filas tienen altura >= 44px
   ✓ Scroll horizontal si necesario

2. Click checkbox fila
   ✓ Fila se selecciona (bg color)
   ✓ Aparece barra de acciones flotante

3. Selecciono múltiples
   ✓ Cuenta correcta ("2 seleccionados")
   ✓ Botones de acciones activos

4. Click "Editar"
   ✓ Modal abre con datos
   ✓ Formulario tiene focus automático

5. Cambio dato y click "Guardar"
   ✓ Validación en cliente
   ✓ Loading state visible
   ✓ Respuesta del servidor
   ✓ Toast con resultado

6. Click "Eliminar"
   ✓ Modal de confirmación aparece
   ✓ "Cancelar" en focus
   ✓ Si confirmo → se elimina
   ✓ Toast "Eliminado" con opción "Deshacer"
```

---

## 🔟 Checklist Final Pre-Deploy

**Antes de mergear a `main`:**

- [ ] Todo visual cumple con `DESIGN_SYSTEM.md`
- [ ] Formularios validan en cliente
- [ ] Acciones destructivas piden confirmación
- [ ] Responsive hasta 375px
- [ ] Accesibilidad: teclado + screen reader
- [ ] Performance: < 50KB CSS+JS
- [ ] Mensajes claros para usuarios
- [ ] Testing en 3+ navegadores
- [ ] Testing en mobile real
- [ ] No hay console errors
- [ ] No hay memory leaks
- [ ] HTTPS en producción

---

## 📝 Ejemplo: Testing en Terminal

```bash
# Instalar lighthouse localmente
npm install -g lighthouse

# Auditar página
lighthouse https://tu-app.com/login --view

# Ver reporte en navegador automáticamente
lighthouse https://tu-app.com/login --output=html --output-path=./report.html

# Testing de accesibilidad
npm install -g axe-core
# (Luego usar browser extension: AxeDevTools)
```

---

## 🎯 Prioridades de Testing

**Crítico (Hacer siempre):**

1. ✅ Visual en desktop + mobile
2. ✅ Validación formularios
3. ✅ Acciones destructivas (confirmar)
4. ✅ Responsive (640px breakpoint)

**Importante (Hacer si hay cambios):** 5. ⭕ Accesibilidad (teclado + screen reader) 6. ⭕ Performance (Lighthouse) 7. ⭕ Cross-browser (Chrome, Firefox, Safari)

**Nice-to-Have (Ocasional):** 8. 💡 Múltiples dispositivos 9. 💡 Testing de carga 10. 💡 SEO audit

---

**Última actualización:** 15 de enero, 2026

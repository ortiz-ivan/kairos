# ⚡ 5-Minuto Quickstart

## 🎯 Lo Esencial

### ¿Qué cambió?

```
ANTES: agregar_venta.html (684 líneas)
       - HTML + JS todo junto
       - Imposible de testear
       - No reutilizable

DESPUÉS: agregar_venta.html (45 líneas)
         - Usa macros
         - Carga 4 módulos JS
         - Limpio y modular
```

### ¿Por qué?

✅ Código más limpio
✅ Fácil de mantener
✅ Fácil de testear
✅ Reutilizable

---

## 📂 Qué Existe Ahora

```
templates/
├── agregar_venta.html            ← Template simple (45 líneas)
└── macros_ventas.html            ← Componentes reutilizables

static/js/
├── product-search.js             ← Búsqueda y preview
├── sales-table.js                ← Gestión de tabla
├── summary-panel.js              ← Resumen POS
└── search-modal.js               ← Modal de búsqueda
```

---

## 💻 Usar en Consola (Ahora Mismo)

```javascript
// 1. Ver productos agregados
window.salesTableManager.getProductsData();

// 2. Ver total
window.salesTableManager.getSummaryData();

// 3. Agregar producto
document.dispatchEvent(
  new CustomEvent("productSelected", {
    detail: {
      producto: { id: 1, nombre: "Test", precio: 100000, stock: 10 },
    },
  })
);

// 4. Validar
window.salesTableManager.isValid();
```

---

## 🏗️ Arquitectura en 1 Imagen

```
┌─────────────────────┐
│ agregar_venta.html  │
├─────────────────────┤
│ (45 líneas limpio)  │
└──────────┬──────────┘
           │
    ┌──────┼──────┐
    │      │      │
    ↓      ↓      ↓
 HTML   Macros   JS

 Macros
 ──────
 • Componentes HTML
   reutilizables

 JS Modules
 ──────────
 • ProductSearch
 • SalesTable
 • SummaryPanel
 • SearchModal
```

---

## 🔄 Flujo de Datos

```
User escanea código
        ↓
ProductSearchManager busca
        ↓
Emite evento 'productSelected'
        ↓
SalesTableManager agrega a tabla
        ↓
Emite evento 'tableUpdated'
        ↓
SummaryPanelManager actualiza totales
        ↓
User ve cambios ✨
```

---

## 📚 Leer Más

| Nivel           | Documento                                                        | Tiempo |
| --------------- | ---------------------------------------------------------------- | ------ |
| ⭐ Principiante | [RESUMEN_REFACTORIZACION.md](RESUMEN_REFACTORIZACION.md)         | 15 min |
| ⭐⭐ Intermedio | [ARQUITECTURA_MODULAR_VENTAS.md](ARQUITECTURA_MODULAR_VENTAS.md) | 30 min |
| ⭐⭐⭐ Avanzado | [EJEMPLOS_PRACTICOS_MODULOS.md](EJEMPLOS_PRACTICOS_MODULOS.md)   | 45 min |
| 📋 Referencia   | [CHEATSHEET_MODULOS.md](CHEATSHEET_MODULOS.md)                   | 5 min  |

---

## ✅ Checklist

- [ ] Entiendo por qué se refactorizó
- [ ] Conozco los 4 módulos principales
- [ ] Puedo acceder a datos desde consola
- [ ] Entiendo el flujo de eventos

**Si marcaste todo:** ¡Listo para usar! 🚀

**Si no:** Lee [RESUMEN_REFACTORIZACION.md](RESUMEN_REFACTORIZACION.md)

---

**¿Preguntas?** → Mira [CHEATSHEET_MODULOS.md](CHEATSHEET_MODULOS.md)

**¿Ejemplos?** → Mira [EJEMPLOS_PRACTICOS_MODULOS.md](EJEMPLOS_PRACTICOS_MODULOS.md)

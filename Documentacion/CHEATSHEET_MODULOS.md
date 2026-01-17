# ⚡ Cheatsheet - Módulos de Ventas

## 🚀 Quick Start

### Cargar módulos

```html
<script src="{{ url_for('static', filename='js/product-search.js') }}"></script>
<script src="{{ url_for('static', filename='js/sales-table.js') }}"></script>
<script src="{{ url_for('static', filename='js/summary-panel.js') }}"></script>
<script src="{{ url_for('static', filename='js/search-modal.js') }}"></script>
```

### Usar módulos desde consola

```javascript
// Instancias globales disponibles automáticamente:
window.productSearchManager;
window.salesTableManager;
window.summaryPanelManager;
window.searchModalManager;
```

---

## 📊 API Pública en 60 Segundos

### ProductSearchManager

```javascript
// Métodos
window.productSearchManager.getCurrentProduct()    // Get producto
window.productSearchManager.showError(msg)          // Mostrar error
window.productSearchManager.hideError()             // Ocultar error

// Eventos que dispara
'productSelected' → detail: { producto: {...} }

// Ejemplo
document.addEventListener('productSelected', (e) => {
    console.log('Producto:', e.detail.producto.nombre);
});
```

### SalesTableManager

```javascript
// Métodos
window.salesTableManager.addProduct(producto)      // Agregar
window.salesTableManager.getProductsData()         // Array para envío
window.salesTableManager.isValid()                 // ¿Válido?
window.salesTableManager.getSummaryData()          // Datos resumen
window.salesTableManager.submit()                  // Validar y preparar

// Eventos que escucha
'productSelected'

// Eventos que dispara
'tableUpdated' → detail: { total, items, ... }

// Ejemplo
const datos = window.salesTableManager.getProductsData();
console.log(datos); // [{ id: 1, cantidad: 2 }, ...]
```

### SummaryPanelManager

```javascript
// Métodos
window.summaryPanelManager.updateDisplay(data); // Actualizar
window.summaryPanelManager.numberToSpanish(num); // Convertir

// Eventos que escucha
("tableUpdated");

// Ejemplo
const letras = window.summaryPanelManager.numberToSpanish(5000000);
console.log(letras); // "cinco millones guaraníes"
```

### ProductSearchModalManager

```javascript
// Métodos
window.searchModalManager.open()                   // Abrir
window.searchModalManager.close()                  // Cerrar
window.searchModalManager.reset()                  // Limpiar

// Eventos que dispara
'productSelected' → detail: { producto: {...} }

// Ejemplo
window.searchModalManager.open();
```

---

## 🎯 Tareas Comunes

### Obtener datos de la venta actual

```javascript
const datos = window.salesTableManager.getProductsData();
console.log(JSON.stringify(datos, null, 2));
```

### Validar antes de enviar

```javascript
if (window.salesTableManager.isValid()) {
  console.log("✅ Venta válida");
} else {
  console.log("❌ Errores en venta");
}
```

### Ver resumen

```javascript
const resumen = window.salesTableManager.getSummaryData();
console.table({
  Total: `₲${resumen.total.toLocaleString()}`,
  Items: resumen.items,
  Errores: resumen.errores,
  Válida: resumen.hasProducts && resumen.errores === 0,
});
```

### Escuchar cambios

```javascript
document.addEventListener("tableUpdated", (e) => {
  const { total, items } = e.detail;
  console.log(`Total: ${total}, Items: ${items}`);
});
```

### Agregar producto manualmente

```javascript
document.dispatchEvent(
  new CustomEvent("productSelected", {
    detail: {
      producto: {
        id: 5,
        nombre: "Laptop",
        precio: 2500000,
        stock: 3,
        codigo_barras: "1234567890",
        categoria: "Electrónica",
      },
    },
  })
);
```

### Abrir modal de búsqueda

```javascript
window.searchModalManager.open();
```

---

## 🔧 Configuración

### ProductSearchManager

```javascript
new ProductSearchManager({
  inputId: "codigo_barras", // Input principal
  datalistId: "sugerencias", // Datalist
  previewId: "previewProducto", // Preview card
  errorId: "mensaje_error", // Error msg
});
```

### SalesTableManager

```javascript
new SalesTableManager({
  formId: "form_venta", // Form
  errorId: "mensaje_error", // Error msg
});
```

### SummaryPanelManager

```javascript
new SummaryPanelManager({
  totalDisplayId: "total_venta_grande",
  totalLetrasId: "total_venta_letras",
  itemsCountId: "total_items_count",
  productosSinStockId: "productos_sin_stock",
  erroresCountId: "errores_count",
  submitBtnId: "btnRegistrar",
});
```

### ProductSearchModalManager

```javascript
new ProductSearchModalManager({
  modalId: "modalBuscarProducto",
  openBtnId: "btnBuscarModal",
  searchInputId: "inputBuscarProducto",
  resultsTableId: "tablaResultados",
  resultsContainerId: "tablaResultadosContainer",
  noResultsId: "sinResultados",
  initialMessageId: "mensajeInicial",
  spinnerId: "spinnerCargando",
});
```

---

## 🐛 Debugging

### Ver productos agregados

```javascript
console.table(window.salesTableManager.productsMap);
```

### Ver producto en preview

```javascript
console.log(window.productSearchManager.getCurrentProduct());
```

### Ver errores de cantidad

```javascript
const resumen = window.salesTableManager.getSummaryData();
console.log(`Errores: ${resumen.errores}`);
```

### Trace completo

```javascript
console.log("=== TRACE ===");
console.log("Preview:", window.productSearchManager.getCurrentProduct());
console.log("Tabla:", window.salesTableManager.getProductsData());
console.log("Resumen:", window.salesTableManager.getSummaryData());
```

---

## ✅ Testing Rápido

### Agregar 3 productos

```javascript
async function testAgregar3() {
  for (let i = 0; i < 3; i++) {
    document.dispatchEvent(
      new CustomEvent("productSelected", {
        detail: {
          producto: {
            id: i + 1,
            nombre: `Producto ${i + 1}`,
            precio: 100000 * (i + 1),
            stock: 10,
            codigo_barras: `123456789${i}`,
            categoria: "Test",
          },
        },
      })
    );
    await new Promise((r) => setTimeout(r, 100));
  }
}
testAgregar3();
```

### Validar tabla

```javascript
const tabla = window.salesTableManager;
console.assert(tabla.getProductsData().length > 0, "No hay productos");
console.assert(tabla.isValid(), "Tabla inválida");
console.log("✅ Tests pasados");
```

---

## 🎨 HTML con Macros

### Usar en template

```html
{% import "macros_ventas.html" as ventas %} {{ ventas.barcode_input() }} {{
ventas.products_table() }} {{ ventas.summary_panel() }} {{ ventas.search_modal()
}}
```

### Macros disponibles

- `flash_messages()` - Alertas
- `barcode_input()` - Input + preview
- `products_table()` - Tabla (vacía, se llena por JS)
- `summary_panel()` - Panel sticky
- `search_modal()` - Modal
- `product_preview()` - Preview solo

---

## 🔗 Enlaces Útiles

| Documento                                                              | Uso        |
| ---------------------------------------------------------------------- | ---------- |
| [RESUMEN_REFACTORIZACION.md](RESUMEN_REFACTORIZACION.md)               | Empezar    |
| [ARQUITECTURA_MODULAR_VENTAS.md](ARQUITECTURA_MODULAR_VENTAS.md)       | Entender   |
| [REFACTORING_MODULAR_VENTAS.md](REFACTORING_MODULAR_VENTAS.md)         | Detalles   |
| [EJEMPLOS_PRACTICOS_MODULOS.md](EJEMPLOS_PRACTICOS_MODULOS.md)         | Ejemplos   |
| [DIAGRAMAS_VISUALES_REFACTORING.md](DIAGRAMAS_VISUALES_REFACTORING.md) | Visualizar |

---

## 📝 Notas

- ✅ Los módulos se auto-inicializan con `DOMContentLoaded`
- ✅ Comunicación por eventos CustomEvent
- ✅ No hay dependencias externas (vanilla JS)
- ✅ Compatible con Bootstrap 5.3
- ✅ Compatible con Jinja2 templates

---

¡Listo para usar! 🚀

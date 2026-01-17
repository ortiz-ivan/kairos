# 🏗️ Arquitectura Visual - Módulos de Ventas

## Estructura del Proyecto

```
templates/
├── agregar_venta.html              ← Template principal (45 líneas)
│   ├── import macros_ventas
│   ├── cargar product-search.js
│   ├── cargar sales-table.js
│   ├── cargar summary-panel.js
│   └── cargar search-modal.js
│
└── macros_ventas.html               ← Componentes reutilizables (130 líneas)
    ├── product_preview()            ← Tarjeta de preview
    ├── barcode_input()              ← Input + preview
    ├── products_table()             ← Tabla dinámicamente poblada
    ├── summary_panel()              ← Panel sticky POS
    ├── search_modal()               ← Modal de búsqueda
    └── flash_messages()             ← Alertas del servidor

static/js/
├── product-search.js                ← ProductSearchManager (100 líneas)
│   • Autocompletado por código
│   • Preview de producto
│   • Búsqueda por Enter
│   • Emite: productSelected
│
├── sales-table.js                   ← SalesTableManager (140 líneas)
│   • Agregar/incrementar productos
│   • Validar cantidad
│   • Eliminar productos
│   • Calcular subtotales
│   • Escucha: productSelected
│   • Emite: tableUpdated
│
├── summary-panel.js                 ← SummaryPanelManager (90 líneas)
│   • Actualizar total
│   • Convertir a letras (guaraní)
│   • Habilitar botón
│   • Escucha: tableUpdated
│
└── search-modal.js                  ← ProductSearchModalManager (150 líneas)
    • Búsqueda por nombre (real-time)
    • Mostrar resultados
    • Agregar desde modal
    • Emite: productSelected
```

---

## Flujo de Datos (Secuencia)

### Escenario 1: Agregar por código de barras

```
User escribe código en input
        ↓
ProductSearchManager.handleAutocomplete()
  ├─ Busca en /inventario/sugerencias
  ├─ Llena datalist con sugerencias
        ↓
User presiona Enter
        ↓
ProductSearchManager.searchAndSelect()
  ├─ Fetch a /ventas/buscar/{codigo}
  ├─ Valida stock > 0
  ├─ Dispara CustomEvent 'productSelected'
        ↓
SalesTableManager escucha 'productSelected'
  ├─ Si existe: incrementa cantidad
  ├─ Si no existe: crea fila en tabla
  ├─ Actualiza subtotal
  ├─ Dispara CustomEvent 'tableUpdated'
        ↓
SummaryPanelManager escucha 'tableUpdated'
  ├─ Actualiza total (₲)
  ├─ Convierte a letras
  ├─ Actualiza contadores
  └─ Habilita/deshabilita botón
```

### Escenario 2: Agregar por búsqueda (modal)

```
User hace click en botón "Buscar"
        ↓
SearchModalManager.open()
  ├─ Abre modal Bootstrap
  └─ Enfoca input de búsqueda
        ↓
User escribe en input de búsqueda
        ↓
SearchModalManager.handleSearch()
  ├─ Espera 300ms (debounce)
  ├─ Fetch a /ventas/productos/buscar?q=...
  ├─ Llena tabla de resultados
  ├─ Muestra badges de stock
        ↓
User hace click en "Agregar"
        ↓
SearchModalManager.addFromModal()
  ├─ Obtiene datos del producto
  ├─ Dispara 'productSelected'
  ├─ Cierra modal
        ↓
[Mismo flujo que Escenario 1 a partir de aquí]
```

### Escenario 3: Cambiar cantidad en tabla

```
User modifica cantidad en input
        ↓
SalesTableManager.handleQuantityChange()
  ├─ Valida cantidad > 0
  ├─ Valida cantidad ≤ stock
  ├─ Actualiza productosMap[id].cantidad
  ├─ Actualiza subtotal visualmente
  └─ Dispara 'tableUpdated'
        ↓
SummaryPanelManager recalcula todo
  └─ Actualiza display
```

### Escenario 4: Enviar formulario

```
User hace click en "Registrar Venta"
        ↓
formVenta.addEventListener('submit')
        ↓
SalesTableManager.submit()
  ├─ Valida isValid()
  ├─ Obtiene getProductsData()
  ├─ JSON.stringify() en #productos_input
  └─ Retorna true/false
        ↓
Si válido: form.submit() → POST /ventas/agregar
Si inválido: muestra error
```

---

## Responsabilidades Claras

### ProductSearchManager

**Entrada:** Input de código/cambios en campo
**Salida:** Evento `productSelected` + preview visual

**Métodos Públicos:**

- `getCurrentProduct()` - Get producto actual en preview
- `showError(mensaje)` - Mostrar error
- `hideError()` - Ocultar error

---

### SalesTableManager

**Entrada:** Evento `productSelected`
**Salida:** Evento `tableUpdated` + tabla actualizada

**Métodos Públicos:**

- `addProduct(producto)` - Agregar producto a tabla
- `getProductsData()` - Array para enviar al servidor
- `isValid()` - Validar antes de enviar
- `getSummaryData()` - Datos para el resumen
- `submit()` - Preparar y validar antes de submit

---

### SummaryPanelManager

**Entrada:** Evento `tableUpdated`
**Salida:** Display actualizado + estado botón

**Métodos Públicos:**

- `updateDisplay(data)` - Actualizar display
- `numberToSpanish(num)` - Convertir número a letras

---

### ProductSearchModalManager

**Entrada:** Click en botón "Buscar", input de búsqueda
**Salida:** Evento `productSelected` + modal abierto/cerrado

**Métodos Públicos:**

- `open()` - Abrir modal
- `close()` - Cerrar modal
- `reset()` - Limpiar estado

---

## Comunicación Entre Módulos

```javascript
// ✅ CORRECTO: Comunicación desacoplada por eventos

// Módulo A dispara evento
document.dispatchEvent(new CustomEvent('productSelected', {
    detail: { producto: {...} }
}));

// Módulo B escucha
document.addEventListener('productSelected', (e) => {
    this.addProduct(e.detail.producto);
});
```

```javascript
// ❌ EVITAR: Acoplamiento directo

// productSearchManager.salesTableManager.addProduct(...) ← MAL
// Crea dependencias entre módulos
```

---

## Ventajas de Esta Arquitectura

| Aspecto           | Antes        | Después                                |
| ----------------- | ------------ | -------------------------------------- |
| **Líneas HTML**   | 684          | 45 (-93%)                              |
| **Líneas JS**     | Todo en HTML | 470 (modular)                          |
| **Archivos**      | 1 monolítico | 6 (separados)                          |
| **Testabilidad**  | Difícil      | Fácil (cada módulo)                    |
| **Reutilización** | No           | Sí (macros + managers)                 |
| **Debugging**     | Difícil      | Fácil (console logs por módulo)        |
| **Escalabilidad** | Limitada     | Alta (nueva funcionalidad sin afectar) |
| **Mantenimiento** | Costoso      | Bajo                                   |

---

## Cómo Extender

### Agregar nueva funcionalidad

**Opción 1: Dentro de un módulo existente**

```javascript
// En SalesTableManager
addDiscount(percentage) {
    // nueva lógica
    this.updateTotal();
}
```

**Opción 2: Nuevo módulo que escucha eventos**

```javascript
// discount-manager.js
class DiscountManager {
  constructor() {
    document.addEventListener("tableUpdated", (e) => {
      this.calculateDiscount(e.detail);
    });
  }
}
```

### Reutilizar en otra página

```html
{# otra-pagina.html #} {% import "macros_ventas.html" as ventas %} {# Usar solo
el componente que necesitas #} {{ ventas.product_preview() }}
```

```javascript
// Usar solo el manager que necesitas
new ProductSearchManager({
  inputId: "mi-input-personalizado",
});
```

---

## Testing Example

```javascript
// test-sales-table.js
describe("SalesTableManager", () => {
  let manager;

  beforeEach(() => {
    document.body.innerHTML = `
            <form id="form_venta">
                <tbody></tbody>
            </form>
        `;
    manager = new SalesTableManager();
  });

  it("debería agregar producto nuevo", () => {
    const producto = { id: 1, nombre: "Test", precio: 100, stock: 10 };
    manager.addProduct(producto);

    expect(manager.productosMap[1]).toBeDefined();
    expect(manager.productosMap[1].cantidad).toBe(1);
  });

  it("debería incrementar cantidad si existe", () => {
    const producto = { id: 1, nombre: "Test", precio: 100, stock: 10 };
    manager.addProduct(producto);
    manager.addProduct(producto);

    expect(manager.productosMap[1].cantidad).toBe(2);
  });

  it("debería validar cantidad máxima", () => {
    const producto = { id: 1, nombre: "Test", precio: 100, stock: 5 };
    manager.addProduct(producto);
    // Intentar agregar más de lo disponible
    for (let i = 0; i < 10; i++) {
      manager.addProduct(producto);
    }

    expect(manager.productosMap[1].cantidad).toBe(5);
  });
});
```

---

¡Arquitectura moderna, escalable y profesional! 🚀

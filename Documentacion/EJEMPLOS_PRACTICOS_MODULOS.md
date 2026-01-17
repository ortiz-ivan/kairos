# 💻 Ejemplos Prácticos - Módulos de Ventas

## 1. Acceso a Datos en Consola del Navegador

```javascript
// Después de cargar la página agregar_venta.html

// ========== BÚSQUEDA DE PRODUCTOS ==========

// Obtener el producto actualmente en preview
const productoActual = window.productSearchManager.getCurrentProduct();
console.log(productoActual);
// Output: { id: 5, nombre: 'Laptop', precio: 2500000, stock: 3, ... }

// ========== TABLA DE PRODUCTOS ==========

// Obtener todos los productos agregados
const productos = window.salesTableManager.getProductsData();
console.log(productos);
// Output: [
//   { id: 5, cantidad: 2 },
//   { id: 10, cantidad: 1 }
// ]

// Validar antes de enviar
const esValido = window.salesTableManager.isValid();
console.log(`¿Venta válida? ${esValido}`);

// Obtener datos del resumen
const resumen = window.salesTableManager.getSummaryData();
console.log(resumen);
// Output: {
//   total: 6250000,
//   items: 3,
//   productosSinStock: 0,
//   errores: 0,
//   hasProducts: true
// }

// ========== RESUMEN ==========

// Obtener el total formateado
const totalFormato = document.getElementById("total_venta_grande").textContent;
console.log(totalFormato); // "₲6.250.000"

// Obtener el total en letras
const totalLetras = document.getElementById("total_venta_letras").textContent;
console.log(totalLetras); // "seis millones doscientos cincuenta mil guaraníes"
```

---

## 2. Agregar Productos Mediante Código

### Método 1: Simular escaneo de código de barras

```javascript
// Simular que el usuario escanea un código
const codigoBarras = "1234567890";

async function simularEscaneo(codigo) {
  // 1. Buscar el producto
  const response = await fetch(`/ventas/buscar/${encodeURIComponent(codigo)}`);
  const data = await response.json();

  if (data.success) {
    // 2. Disparar evento de selección
    document.dispatchEvent(
      new CustomEvent("productSelected", {
        detail: { producto: data.producto },
      })
    );

    console.log(`Producto agregado: ${data.producto.nombre}`);
  } else {
    console.error("Producto no encontrado");
  }
}

// Usar la función
simularEscaneo(codigoBarras);
```

### Método 2: Agregar directamente desde el gestor

```javascript
// Si tienes los datos del producto
const producto = {
  id: 1,
  nombre: "Monitor",
  precio: 450000,
  stock: 5,
  codigo_barras: "9876543210",
  categoria: "Electrónica",
};

// Agregar a la tabla
window.salesTableManager.addProduct(producto);

// La tabla se actualiza automáticamente
// El resumen se actualiza automáticamente
console.log("Producto agregado correctamente");
```

---

## 3. Validaciones Personalizadas

```javascript
// Validar que hay productos antes de hacer algo
if (window.salesTableManager.isValid()) {
  console.log("✅ Venta lista para enviar");

  // Obtener datos para envío
  const datos = window.salesTableManager.getProductsData();

  // Hacer algo especial (ej: analytics)
  gtag("event", "venta_iniciada", {
    items: datos.length,
    total: window.summaryPanelManager.total,
  });
} else {
  console.log("❌ Errores en la venta:");
  const resumen = window.salesTableManager.getSummaryData();
  console.log(`- Productos sin stock: ${resumen.productosSinStock}`);
  console.log(`- Errores de cantidad: ${resumen.errores}`);
}
```

---

## 4. Operaciones Avanzadas

### Cambiar el total manualmente (ej: descuento)

```javascript
// ANTES: total es ₲5,000,000
// Aplicar descuento del 10%

const resumen = window.salesTableManager.getSummaryData();
const descuento = resumen.total * 0.1; // 10%
const nuevoTotal = resumen.total - descuento;

// Mostrar en UI
document.getElementById(
  "total_venta_grande"
).textContent = `₲${nuevoTotal.toLocaleString()}`;

// ⚠️ IMPORTANTE: Si das submit del formulario, se recalculará
// Para mantener el descuento, debes:
// 1. Agregar campo hidden con descuento
// 2. O modificar el backend para aceptar descuento
```

### Filtrar solo productos sin stock

```javascript
const resumen = window.salesTableManager.getSummaryData();

if (resumen.productosSinStock > 0) {
  console.warn(`⚠️ Hay ${resumen.productosSinStock} productos sin stock`);

  // Obtener cuáles son
  const productos = window.salesTableManager.getProductsData();
  const sinStock = productos.filter((p) => {
    // Necesitarías acceso a los datos completos
    // Esto es un ejemplo
    return !productosMap[p.id].stock;
  });
}
```

---

## 5. Monitorizar Cambios (Eventos)

```javascript
// Escuchar cuando se actualiza la tabla
document.addEventListener("tableUpdated", (e) => {
  const { total, items, productosSinStock, errores, hasProducts } = e.detail;

  // Hacer algo cuando cambia
  console.log(`📊 Venta actualizada:`);
  console.log(`  Total: ₲${total.toLocaleString()}`);
  console.log(`  Items: ${items}`);
  console.log(`  ¿Válida?: ${hasProducts && errores === 0}`);

  // Ejemplo: enviar a analytics
  if (hasProducts) {
    // Hacer tracking
  }
});

// Escuchar cuando se selecciona un producto
document.addEventListener("productSelected", (e) => {
  const { producto } = e.detail;
  console.log(`🎯 Producto seleccionado: ${producto.nombre}`);

  // Hacer algo (ej: reproducir sonido)
  // new Audio('/static/sounds/beep.mp3').play();
});
```

---

## 6. Integración con Servicios Externos

### Enviar analytics cuando se registra venta

```javascript
// Hook en el formulario
const form = document.getElementById("form_venta");
form.addEventListener("submit", (e) => {
  if (e.defaultPrevented) return; // Ya hay validación

  const datos = window.salesTableManager.getProductsData();
  const resumen = window.salesTableManager.getSummaryData();

  // Enviar a Google Analytics
  gtag("event", "venta", {
    value: resumen.total,
    currency: "PYG",
    items: resumen.items,
    transaction_id: `venta-${Date.now()}`,
  });
});
```

### Imprimir ticket antes de enviar

```javascript
async function imprimirTicketAntes() {
  const resumen = window.salesTableManager.getSummaryData();
  const productos = window.salesTableManager.getProductsData();

  // Generar HTML del ticket
  const ticketHTML = `
        <h2>COMPROBANTE DE VENTA</h2>
        <p>Total: ₲${resumen.total.toLocaleString()}</p>
        <p>${productos.length} productos</p>
    `;

  // Abrir en nueva ventana y imprimir
  const ventana = window.open("", "", "width=400,height=600");
  ventana.document.write(ticketHTML);
  ventana.print();
}
```

---

## 7. Debugging

### Ver estado completo del gestor de tabla

```javascript
// Object con todos los productos
console.table(window.salesTableManager.productsMap);

// Output en tabla de consola:
// id  | nombre    | precio  | stock | cantidad
// ----|-----------|---------|-------|----------
// 5   | Laptop    | 2500000 | 3     | 2
// 10  | Mouse     | 80000   | 50    | 1
```

### Ver estado del gestor de búsqueda

```javascript
// Producto actual en preview
console.log(
  "Producto en preview:",
  window.productSearchManager.getCurrentProduct()
);

// Mensajes de error
document.addEventListener("DOMContentLoaded", () => {
  // Ver todos los errores que se muestren
  const mensajeError = document.getElementById("mensaje_error");
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      console.log("Error mostrado:", mensajeError.textContent);
    });
  });
  observer.observe(mensajeError, {
    childList: true,
    subtree: true,
  });
});
```

### Trace completo de un producto

```javascript
console.log("=== TRACE: Flujo de un producto ===");

// 1. Desde búsqueda
const producto = window.productSearchManager.getCurrentProduct();
console.log("1. En preview:", producto);

// 2. En tabla
const datos = window.salesTableManager.getProductsData();
const productoEnTabla = datos.find((p) => p.id === producto.id);
console.log("2. En tabla:", productoEnTabla);

// 3. En mapa interno
const productoInterno = window.salesTableManager.productsMap[producto.id];
console.log("3. Mapa interno:", productoInterno);

// 4. En resumen
const resumen = window.salesTableManager.getSummaryData();
console.log("4. Contribuye al total:", resumen);
```

---

## 8. Casos de Uso Avanzados

### Cargar carrito guardado

```javascript
// Supongamos que tienes datos guardados
const carritoGuardado = [
  { id: 5, cantidad: 2 },
  { id: 10, cantidad: 1 },
];

// Restaurar el carrito
async function restaurarCarrito(carrito) {
  for (const item of carrito) {
    const response = await fetch(`/productos/${item.id}`);
    const producto = await response.json();

    // Agregar N veces
    for (let i = 0; i < item.cantidad; i++) {
      window.salesTableManager.addProduct(producto);
    }
  }

  console.log("✅ Carrito restaurado");
}

// Usar
restaurarCarrito(carritoGuardado);
```

### Exportar venta como JSON

```javascript
function exportarVenta() {
  const datos = {
    timestamp: new Date().toISOString(),
    productos: window.salesTableManager.getProductsData(),
    resumen: window.salesTableManager.getSummaryData(),
    usuario: document.querySelector("[data-user-id]")?.dataset.userId,
  };

  // Descargar como archivo
  const json = JSON.stringify(datos, null, 2);
  const blob = new Blob([json], { type: "application/json" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = `venta-${Date.now()}.json`;
  a.click();

  URL.revokeObjectURL(url);
}
```

### Validación personalizada antes de enviar

```javascript
// Hook personalizado
window.validateVentaPersonalizado = function () {
  const resumen = window.salesTableManager.getSummaryData();

  // Validaciones extra
  if (resumen.total < 10000) {
    console.error("❌ Venta mínima: ₲10.000");
    return false;
  }

  if (resumen.total > 100000000) {
    console.warn("⚠️ Venta muy grande, revisar");
    // Aunque permitir continuar
  }

  return true;
};

// Usar antes de enviar
const form = document.getElementById("form_venta");
form.addEventListener("submit", (e) => {
  if (!window.validateVentaPersonalizado()) {
    e.preventDefault();
    alert("Validación personalizada fallida");
  }
});
```

---

## 9. Testing en Consola

```javascript
// Test 1: Agregar producto
console.log("Test 1: Agregar producto");
window.salesTableManager.addProduct({
  id: 999,
  nombre: "Producto Test",
  precio: 50000,
  stock: 10,
});
console.assert(
  window.salesTableManager.productsMap[999],
  "Producto no agregado"
);
console.log("✅ Pasó");

// Test 2: Validar cantidad máxima
console.log("Test 2: Cantidad máxima");
const tabla = window.salesTableManager;
tabla.addProduct({ id: 1000, nombre: "Test", precio: 100, stock: 5 });
// Intentar cambiar a 10
const input = document.querySelector("#cantidad_1000");
input.value = 10;
input.dispatchEvent(new Event("input"));
console.assert(
  tabla.productsMap[1000].cantidad <= 5,
  "Cantidad no limitada al stock"
);
console.log("✅ Pasó");
```

---

¡Ahora tienes ejemplos prácticos para todo! 🚀

/**
 * Módulo para gestionar el panel de resumen (POS style)
 * Responsabilidad: Mostrar totales, items, estado del botón
 *
 * Dependencias: sales-table.js (escucha eventos 'tableUpdated')
 * Eventos globales: 'tableUpdated'
 */

class SummaryPanelManager {
    constructor(options = {}) {
        this.totalDisplay = document.getElementById(options.totalDisplayId || 'total_venta_grande');
        this.totalLetras = document.getElementById(options.totalLetrasId || 'total_venta_letras');
        this.itemsCount = document.getElementById(options.itemsCountId || 'total_items_count');
        this.productosSinStock = document.getElementById(options.productosSinStockId || 'productos_sin_stock');
        this.erroresCount = document.getElementById(options.erroresCountId || 'errores_count');
        this.submitBtn = document.getElementById(options.submitBtnId || 'btnRegistrar');

        this.init();
    }

    init() {
        // Escuchar cambios en la tabla
        document.addEventListener('tableUpdated', (e) => {
            this.updateDisplay(e.detail);
        });

        // Manejar envío del formulario
        if (this.submitBtn) {
            this.submitBtn.addEventListener('click', () => {
                if (window.salesTableManager) {
                    window.salesTableManager.submit();
                }
            });
        }

        // Inicializar estado
        this.updateDisplay({
            total: 0,
            items: 0,
            productosSinStock: 0,
            errores: 0,
            hasProducts: false
        });
    }

    /**
     * Actualizar display con los datos del resumen
     */
    updateDisplay(data) {
        const { total, items, productosSinStock, errores, hasProducts } = data;

        // Actualizar total
        this.totalDisplay.textContent = `₲${total.toLocaleString()}`;
        this.totalLetras.textContent = this.numberToSpanish(Math.round(total));

        // Actualizar contadores
        if (this.itemsCount) this.itemsCount.textContent = items;
        if (this.productosSinStock) this.productosSinStock.textContent = productosSinStock;
        if (this.erroresCount) this.erroresCount.textContent = errores;

        // Actualizar estado del botón
        this.updateButtonState(hasProducts);
    }

    /**
     * Actualizar estado del botón
     */
    updateButtonState(hasProducts) {
        if (!this.submitBtn) return;

        this.submitBtn.disabled = !hasProducts;
        this.submitBtn.title = hasProducts
            ? 'Registrar venta'
            : 'Debe agregar al menos un producto';
    }

    /**
     * Convertir número a palabras en español (guaraní)
     */
    numberToSpanish(num) {
        if (num === 0) return 'Cero guaraníes';

        const unidades = ['', 'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve'];
        const especiales = ['diez', 'once', 'doce', 'trece', 'catorce', 'quince', 'dieciséis',
                           'diecisiete', 'dieciocho', 'diecinueve'];
        const decenas = ['', '', 'veinte', 'treinta', 'cuarenta', 'cincuenta', 'sesenta',
                        'setenta', 'ochenta', 'noventa'];
        const centenas = ['', 'ciento', 'doscientos', 'trescientos', 'cuatrocientos', 'quinientos',
                         'seiscientos', 'setecientos', 'ochocientos', 'novecientos'];

        const convertirCientos = (n) => {
            if (n === 0) return '';
            if (n < 10) return unidades[n];
            if (n < 20) return especiales[n - 10];
            if (n < 100) {
                const dec = Math.floor(n / 10);
                const uni = n % 10;
                if (uni === 0) return decenas[dec];
                return decenas[dec] + ' y ' + unidades[uni];
            }
            const cent = Math.floor(n / 100);
            const resto = n % 100;
            if (resto === 0) return centenas[cent];
            return centenas[cent] + ' ' + convertirCientos(resto);
        };

        if (num < 1000) {
            return convertirCientos(num) + ' guaraní' + (num !== 1 ? 'es' : '');
        }

        const miles = Math.floor(num / 1000);
        const resto = num % 1000;

        let resultado = miles === 1 ? 'mil' : convertirCientos(miles) + ' mil';

        if (resto > 0) {
            resultado += ' ' + convertirCientos(resto);
        }

        return resultado + ' guaraní' + (num !== 1 ? 'es' : '');
    }
}

// Inicializar automáticamente
document.addEventListener('DOMContentLoaded', () => {
    window.summaryPanelManager = new SummaryPanelManager();
});

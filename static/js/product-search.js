/**
 * Módulo de búsqueda y preview de productos
 * Responsabilidad: Gestionar búsqueda por código, autocompletado y vista previa
 *
 * Dependencias: ninguna
 * Eventos globales: 'productSelected' - se dispara cuando se selecciona un producto
 */

class ProductSearchManager {
    constructor(options = {}) {
        this.inputCodigo = document.getElementById(options.inputId || 'codigo_barras');
        this.datalist = document.getElementById(options.datalistId || 'sugerencias');
        this.previewCard = document.getElementById(options.previewId || 'previewProducto');
        this.mensajeError = document.getElementById(options.errorId || 'mensaje_error');

        this.previewElements = {
            nombre: document.getElementById('previewNombre'),
            precio: document.getElementById('previewPrecio'),
            stock: document.getElementById('previewStock'),
            categoria: document.getElementById('previewCategoria')
        };

        this.currentProduct = null;
        this.autocompleteTimer = null;

        this.init();
    }

    init() {
        if (!this.inputCodigo) return;

        // Autocompletado al escribir
        this.inputCodigo.addEventListener('input', (e) => this.handleAutocomplete());

        // Mostrar preview al seleccionar del datalist
        this.inputCodigo.addEventListener('change', (e) => this.handlePreview());

        // Limpiar preview al vaciar input
        this.inputCodigo.addEventListener('input', (e) => {
            if (this.inputCodigo.value.trim() === '') {
                this.hidePreview();
            }
        });

        // Buscar por Enter
        this.inputCodigo.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.searchAndSelect();
            }
        });
    }

    /**
     * Búsqueda de autocompletado mientras el usuario escribe
     */
    async handleAutocomplete() {
        const q = this.inputCodigo.value.trim();

        if (!q) {
            this.datalist.innerHTML = '';
            return;
        }

        clearTimeout(this.autocompleteTimer);
        this.autocompleteTimer = setTimeout(async () => {
            try {
                const response = await fetch(`/inventario/sugerencias?q=${encodeURIComponent(q)}`);
                const data = await response.json();

                this.datalist.innerHTML = '';
                data.forEach(producto => {
                    const option = document.createElement('option');
                    option.value = producto.codigo_barras;
                    option.text = producto.nombre;
                    this.datalist.appendChild(option);
                });
            } catch (error) {
                console.error('Error en autocompletado:', error);
            }
        }, 300); // Debounce 300ms
    }

    /**
     * Mostrar vista previa del producto seleccionado
     */
    async handlePreview() {
        const codigo = this.inputCodigo.value.trim();

        if (!codigo) {
            this.hidePreview();
            return;
        }

        try {
            const response = await fetch(`/ventas/buscar/${encodeURIComponent(codigo)}`);
            const data = await response.json();

            if (data.success) {
                this.displayProduct(data.producto);
            } else {
                this.hidePreview();
            }
        } catch (error) {
            console.error('Error al obtener preview:', error);
            this.hidePreview();
        }
    }

    /**
     * Mostrar el producto en la tarjeta de preview
     */
    displayProduct(producto) {
        this.currentProduct = producto;

        this.previewElements.nombre.textContent = producto.nombre;
        this.previewElements.precio.textContent = `₲${producto.precio.toLocaleString()}`;
        this.previewElements.stock.textContent =
            `${producto.stock} unidad${producto.stock !== 1 ? 'es' : ''}`;
        this.previewElements.categoria.textContent = producto.categoria;

        this.previewCard.style.display = 'block';
    }

    /**
     * Ocultar tarjeta de preview
     */
    hidePreview() {
        this.currentProduct = null;
        this.previewCard.style.display = 'none';
    }

    /**
     * Buscar producto por código y disparar evento de selección
     */
    async searchAndSelect() {
        const codigo = this.inputCodigo.value.trim();

        if (!codigo) {
            this.showError('Por favor, ingrese un código de barras.');
            return;
        }

        try {
            const response = await fetch(`/ventas/buscar/${encodeURIComponent(codigo)}`);
            const data = await response.json();

            if (data.success) {
                const producto = data.producto;

                // Validar stock
                if (producto.stock <= 0) {
                    this.showError(`'${producto.nombre}' no tiene stock disponible.`);
                    this.inputCodigo.value = '';
                    return;
                }

                // Disparar evento global
                document.dispatchEvent(new CustomEvent('productSelected', {
                    detail: { producto }
                }));

                this.hideError();
                this.inputCodigo.value = '';
                this.inputCodigo.focus();
            } else {
                this.showError(data.mensaje || 'Producto no encontrado o código inválido.');
                this.inputCodigo.value = '';
            }
        } catch (error) {
            console.error('Error al buscar:', error);
            this.showError('Error al conectar con el servidor.');
        }
    }

    /**
     * Mostrar mensaje de error
     */
    showError(mensaje) {
        this.mensajeError.textContent = mensaje;
        this.mensajeError.style.display = 'block';
    }

    /**
     * Ocultar mensaje de error
     */
    hideError() {
        this.mensajeError.style.display = 'none';
    }

    /**
     * Obtener el producto actualmente en preview
     */
    getCurrentProduct() {
        return this.currentProduct;
    }
}

// Inicializar automáticamente
document.addEventListener('DOMContentLoaded', () => {
    window.productSearchManager = new ProductSearchManager();
});

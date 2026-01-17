/**
 * Módulo para gestionar la tabla de productos en ventas
 * Responsabilidad: CRUD de productos en la tabla, cálculo de subtotales
 *
 * Dependencias: ninguna
 * Eventos globales: 'productSelected', 'tableUpdated'
 */

class SalesTableManager {
    constructor(options = {}) {
        this.form = document.getElementById(options.formId || 'form_venta');
        this.tableBody = this.form?.querySelector('tbody');
        this.mensajeError = document.getElementById(options.errorId || 'mensaje_error');

        this.productsMap = {}; // Map de productos agregados: { id: { ...producto, cantidad } }

        this.init();
    }

    init() {
        if (!this.tableBody) return;

        // Escuchar evento global de producto seleccionado
        document.addEventListener('productSelected', (e) => {
            this.addProduct(e.detail.producto);
        });

        // Cambio de cantidad
        this.tableBody.addEventListener('input', (e) => this.handleQuantityChange(e));

        // Eliminar producto
        this.tableBody.addEventListener('click', (e) => this.handleDelete(e));
    }

    /**
     * Agregar o incrementar un producto
     */
    addProduct(producto) {
        const { id, nombre, stock } = producto;

        if (this.productsMap[id]) {
            // Producto ya existe: incrementar cantidad
            const current = this.productsMap[id];

            if (current.cantidad < stock) {
                current.cantidad += 1;
                document.getElementById(`cantidad_${id}`).value = current.cantidad;
                this.updateSubtotal(id);
                this.hideError();
            } else {
                this.showError(
                    `No hay suficiente stock para '${nombre}'. Disponible: ${stock}`
                );
            }
        } else {
            // Producto nuevo
            this.productsMap[id] = { ...producto, cantidad: 1 };
            this.addRow(producto);
            this.hideError();
        }

        this.updateTotal();
    }

    /**
     * Agregar fila a la tabla
     */
    addRow(producto) {
        const { id, codigo_barras, nombre, precio, stock } = producto;

        const row = document.createElement('tr');
        row.id = `fila_${id}`;
        row.innerHTML = `
            <td>${codigo_barras}</td>
            <td>${nombre}</td>
            <td>₲${precio.toLocaleString()}</td>
            <td>
                <input type="number" id="cantidad_${id}" class="form-control cantidad"
                       value="1" min="1" max="${stock}" required>
                <small class="form-text text-muted">Máx: ${stock} disponibles</small>
            </td>
            <td id="subtotal_${id}">₲${precio.toLocaleString()}</td>
            <td>
                <button type="button" class="btn btn-danger btn-sm eliminar"
                        data-id="${id}" title="Eliminar producto">
                    &times;
                </button>
            </td>
        `;

        this.tableBody.appendChild(row);
    }

    /**
     * Manejar cambio de cantidad
     */
    handleQuantityChange(e) {
        if (!e.target.classList.contains('cantidad')) return;

        const id = parseInt(e.target.id.split('_')[1]);
        const product = this.productsMap[id];
        let newQuantity = parseInt(e.target.value) || 0;

        // Validar: cantidad > 0
        if (newQuantity <= 0) {
            e.target.value = 1;
            newQuantity = 1;
        }

        // Validar: no exceder stock
        if (newQuantity > product.stock) {
            e.target.classList.add('is-invalid');
            e.target.title = `Stock máximo: ${product.stock}`;
            newQuantity = product.stock;
            e.target.value = product.stock;
        } else {
            e.target.classList.remove('is-invalid');
            e.target.title = '';
        }

        product.cantidad = newQuantity;
        this.updateSubtotal(id);
    }

    /**
     * Eliminar producto de la tabla
     */
    handleDelete(e) {
        if (!e.target.classList.contains('eliminar')) return;

        e.preventDefault();

        const id = parseInt(e.target.dataset.id);
        delete this.productsMap[id];

        const row = document.getElementById(`fila_${id}`);
        if (row) row.remove();

        this.updateTotal();
        this.hideError();
    }

    /**
     * Actualizar subtotal de un producto
     */
    updateSubtotal(id) {
        const product = this.productsMap[id];
        const subtotal = product.precio * product.cantidad;
        const element = document.getElementById(`subtotal_${id}`);

        if (element) {
            element.textContent = `₲${subtotal.toLocaleString()}`;
        }

        this.updateTotal();
    }

    /**
     * Obtener array de productos para enviar al servidor
     */
    getProductsData() {
        return Object.values(this.productsMap).map(p => ({
            id: p.id,
            cantidad: p.cantidad
        }));
    }

    /**
     * Validar que haya productos válidos
     */
    isValid() {
        const productsCount = Object.keys(this.productsMap).length;

        if (productsCount === 0) {
            this.showError('Debe agregar al menos un producto a la venta.');
            return false;
        }

        // Validar cada producto
        for (const id in this.productsMap) {
            const prod = this.productsMap[id];
            if (prod.cantidad <= 0 || prod.cantidad > prod.stock) {
                this.showError(
                    `Error en cantidad del producto '${prod.nombre}'. ` +
                    `Cantidad debe ser entre 1 y ${prod.stock}.`
                );
                return false;
            }
        }

        return true;
    }

    /**
     * Obtener datos para resumen
     */
    getSummaryData() {
        let total = 0;
        let items = 0;
        let productosSinStock = 0;
        let errores = 0;

        for (const id in this.productsMap) {
            const prod = this.productsMap[id];
            total += (prod.precio || 0) * (prod.cantidad || 0);
            items += prod.cantidad || 0;

            if (!prod.stock || prod.stock <= 0) productosSinStock++;
            if (!prod.cantidad || prod.cantidad <= 0 || prod.cantidad > prod.stock) errores++;
        }

        return {
            total,
            items,
            productosSinStock,
            errores,
            hasProducts: Object.keys(this.productsMap).length > 0
        };
    }

    /**
     * Enviar datos del formulario
     */
    submit() {
        if (!this.isValid()) return false;

        const inputProductos = this.form.querySelector('#productos_input');
        inputProductos.value = JSON.stringify(this.getProductsData());

        this.hideError();
        return true;
    }

    showError(mensaje) {
        this.mensajeError.textContent = mensaje;
        this.mensajeError.style.display = 'block';
    }

    hideError() {
        this.mensajeError.style.display = 'none';
    }

    /**
     * Actualizar total (dispara evento para que el SummaryPanel lo maneje)
     */
    updateTotal() {
        document.dispatchEvent(new CustomEvent('tableUpdated', {
            detail: this.getSummaryData()
        }));
    }
}

// Inicializar automáticamente
document.addEventListener('DOMContentLoaded', () => {
    window.salesTableManager = new SalesTableManager();
});

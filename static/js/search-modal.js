/**
 * Módulo para gestionar el modal de búsqueda de productos
 * Responsabilidad: Búsqueda por nombre, visualización de resultados, agregar desde modal
 *
 * Dependencias: ninguna
 * Eventos globales: dispara 'productSelected' cuando se selecciona un producto
 */

class ProductSearchModalManager {
    constructor(options = {}) {
        this.modalElement = document.getElementById(options.modalId || 'modalBuscarProducto');
        this.openBtn = document.getElementById(options.openBtnId || 'btnBuscarModal');
        this.searchInput = document.getElementById(options.searchInputId || 'inputBuscarProducto');
        this.resultsTable = document.getElementById(options.resultsTableId || 'tablaResultados');
        this.resultsContainer = document.getElementById(options.resultsContainerId || 'tablaResultadosContainer');
        this.noResults = document.getElementById(options.noResultsId || 'sinResultados');
        this.initialMessage = document.getElementById(options.initialMessageId || 'mensajeInicial');
        this.spinner = document.getElementById(options.spinnerId || 'spinnerCargando');

        this.modal = null;
        this.searchTimer = null;

        this.init();
    }

    init() {
        if (!this.modalElement) return;

        // Inicializar modal Bootstrap
        this.modal = new bootstrap.Modal(this.modalElement);

        // Botón para abrir modal
        if (this.openBtn) {
            this.openBtn.addEventListener('click', () => this.open());
        }

        // Búsqueda en tiempo real
        if (this.searchInput) {
            this.searchInput.addEventListener('input', () => this.handleSearch());
        }
    }

    /**
     * Abrir modal
     */
    open() {
        this.reset();
        this.modal.show();
        if (this.searchInput) {
            setTimeout(() => this.searchInput.focus(), 300);
        }
    }

    /**
     * Cerrar modal
     */
    close() {
        this.modal.hide();
    }

    /**
     * Resetear estado del modal
     */
    reset() {
        if (this.searchInput) this.searchInput.value = '';
        this.resultsTable.innerHTML = '';
        this.resultsContainer.style.display = 'none';
        this.noResults.style.display = 'none';
        this.spinner.style.display = 'none';
        this.initialMessage.style.display = 'block';
    }

    /**
     * Manejar búsqueda
     */
    handleSearch() {
        clearTimeout(this.searchTimer);
        const query = this.searchInput.value.trim();

        // Mostrar estado inicial si query muy corta
        if (query.length < 2) {
            this.resultsTable.innerHTML = '';
            this.resultsContainer.style.display = 'none';
            this.noResults.style.display = 'none';
            this.spinner.style.display = 'none';
            this.initialMessage.style.display = 'block';
            return;
        }

        // Mostrar spinner
        this.showSpinner();

        // Debounce: esperar 300ms antes de buscar
        this.searchTimer = setTimeout(() => {
            this.performSearch(query);
        }, 300);
    }

    /**
     * Ejecutar búsqueda en el servidor
     */
    async performSearch(query) {
        try {
            const response = await fetch(`/ventas/productos/buscar?q=${encodeURIComponent(query)}`);
            const data = await response.json();

            this.hideSpinner();

            if (data.productos && data.productos.length > 0) {
                this.displayResults(data.productos);
            } else {
                this.displayNoResults();
            }
        } catch (error) {
            console.error('Error en búsqueda:', error);
            this.hideSpinner();
            this.noResults.textContent =
                '<i class="bi bi-exclamation-triangle"></i> Error al buscar productos.';
            this.noResults.style.display = 'block';
            this.resultsContainer.style.display = 'none';
            this.initialMessage.style.display = 'none';
        }
    }

    /**
     * Mostrar resultados en la tabla
     */
    displayResults(productos) {
        this.resultsTable.innerHTML = productos.map(p => `
            <tr>
                <td>
                    <strong>${this.escapeHtml(p.nombre)}</strong>
                </td>
                <td>
                    <code>${this.escapeHtml(p.codigo_barras)}</code>
                </td>
                <td>
                    <span class="badge bg-secondary">${this.escapeHtml(p.categoria)}</span>
                </td>
                <td>
                    <strong>₲${parseInt(p.precio).toLocaleString('es-ES')}</strong>
                </td>
                <td>
                    <span class="badge ${p.stock > 0 ? 'bg-success' : 'bg-danger'}">
                        ${p.stock} ${p.stock === 1 ? 'unidad' : 'unidades'}
                    </span>
                </td>
                <td>
                    ${p.stock > 0
                        ? `<button type="button" class="btn btn-sm btn-success add-from-modal"
                                  data-id="${p.id}" data-nombre="${this.escapeHtml(p.nombre)}"
                                  data-precio="${p.precio}">
                            <i class="bi bi-plus-circle"></i> Agregar
                          </button>`
                        : `<button type="button" class="btn btn-sm btn-secondary" disabled>
                            Sin stock
                          </button>`
                    }
                </td>
            </tr>
        `).join('');

        // Agregar listeners a botones de agregar
        this.resultsTable.querySelectorAll('.add-from-modal').forEach(btn => {
            btn.addEventListener('click', (e) => this.addFromModal(e));
        });

        this.resultsContainer.style.display = 'block';
        this.noResults.style.display = 'none';
        this.initialMessage.style.display = 'none';
    }

    /**
     * Mostrar mensaje sin resultados
     */
    displayNoResults() {
        this.resultsTable.innerHTML = '';
        this.resultsContainer.style.display = 'none';
        this.noResults.innerHTML =
            '<i class="bi bi-info-circle"></i> No se encontraron productos que coincidan con la búsqueda.';
        this.noResults.style.display = 'block';
        this.initialMessage.style.display = 'none';
    }

    /**
     * Agregar producto desde el modal
     */
    addFromModal(e) {
        e.preventDefault();

        const btn = e.target.closest('.add-from-modal');
        const productoId = parseInt(btn.dataset.id);
        const nombre = btn.dataset.nombre;
        const precio = parseInt(btn.dataset.precio);

        // Obtener datos completos del producto
        const query = encodeURIComponent(nombre);
        fetch(`/ventas/productos/buscar?q=${query}`)
            .then(response => response.json())
            .then(data => {
                const producto = data.productos.find(p => p.id === productoId);
                if (producto) {
                    // Disparar evento para que el table manager lo maneje
                    document.dispatchEvent(new CustomEvent('productSelected', {
                        detail: { producto }
                    }));

                    // Cerrar modal
                    this.close();
                }
            })
            .catch(error => console.error('Error al agregar producto:', error));
    }

    /**
     * Mostrar spinner de carga
     */
    showSpinner() {
        this.spinner.style.display = 'block';
        this.resultsContainer.style.display = 'none';
        this.noResults.style.display = 'none';
        this.initialMessage.style.display = 'none';
    }

    /**
     * Ocultar spinner
     */
    hideSpinner() {
        this.spinner.style.display = 'none';
    }

    /**
     * Escapar HTML para seguridad (prevenir XSS)
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Inicializar automáticamente
document.addEventListener('DOMContentLoaded', () => {
    window.searchModalManager = new ProductSearchModalManager();
});

# 📋 Ejemplos de Implementación - Componentes

Este archivo muestra ejemplos prácticos de cómo usar el sistema de diseño en diferentes vistas.

---

## 1. Dashboard Principal (Mostración de Métricas)

```html
{% extends "base.html" %} {% block content %}

<div class="dashboard-hero">
  <!-- HEADER CON TÍTULO Y ACCIONES -->
  <div class="flex-between mb-lg">
    <div>
      <h1>Dashboard</h1>
      <p class="text-secondary">Resumen de hoy - 15 de enero, 2026</p>
    </div>
    <div class="flex gap-md">
      <button class="btn btn-secondary btn-sm">📅 Filtrar fecha</button>
      <button class="btn btn-primary btn-sm">➕ Nueva venta</button>
    </div>
  </div>

  <!-- MÉTRICAS PRINCIPALES (KPIs) -->
  <div
    style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: var(--space-lg);"
  >
    <!-- Métrica 1: Ventas -->
    <div class="card">
      <div class="card-body">
        <p class="text-secondary caption">💰 Total Ventas</p>
        <h2 style="font-size: 32px; margin: var(--space-md) 0;">
          ₲ 45.000.000
        </h2>
        <p class="text-success">↑ 12% vs. ayer</p>
      </div>
    </div>

    <!-- Métrica 2: Transacciones -->
    <div class="card">
      <div class="card-body">
        <p class="text-secondary caption">📊 Transacciones</p>
        <h2 style="font-size: 32px; margin: var(--space-md) 0;">248</h2>
        <p class="text-success">↑ 8 más que ayer</p>
      </div>
    </div>

    <!-- Métrica 3: Ticket Promedio -->
    <div class="card">
      <div class="card-body">
        <p class="text-secondary caption">🎯 Ticket Promedio</p>
        <h2 style="font-size: 32px; margin: var(--space-md) 0;">₲ 181.000</h2>
        <p class="text-warning">→ sin cambios</p>
      </div>
    </div>

    <!-- Métrica 4: Tasa Éxito -->
    <div class="card">
      <div class="card-body">
        <p class="text-secondary caption">✅ Tasa Éxito</p>
        <h2 style="font-size: 32px; margin: var(--space-md) 0;">98%</h2>
        <p class="text-info">ℹ Solo 5 rechazadas</p>
      </div>
    </div>
  </div>
</div>

<!-- TABLA DE ÚLTIMAS VENTAS -->
<div class="card mt-lg">
  <div class="card-header flex-between">
    <h3 class="card-title">Últimas Transacciones</h3>
    <a href="/registros" class="btn btn-tertiary btn-sm">Ver todas →</a>
  </div>

  <div class="card-body">
    <table style="width: 100%; border-collapse: collapse;">
      <thead style="border-bottom: 1px solid var(--border-default);">
        <tr>
          <th style="text-align: left; padding: var(--space-md);">ID</th>
          <th style="text-align: left; padding: var(--space-md);">Cliente</th>
          <th style="text-align: left; padding: var(--space-md);">Monto</th>
          <th style="text-align: left; padding: var(--space-md);">Hora</th>
          <th style="text-align: left; padding: var(--space-md);">Estado</th>
          <th style="text-align: center; padding: var(--space-md);">
            Acciones
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          style="border-bottom: 1px solid var(--border-default); hover: background-color: var(--bg-hover);"
        >
          <td style="padding: var(--space-md);">#V001</td>
          <td style="padding: var(--space-md);">Juan López</td>
          <td style="padding: var(--space-md); text-align: right;">
            ₲ 450.000
          </td>
          <td style="padding: var(--space-md);">2:34 PM</td>
          <td style="padding: var(--space-md);">
            <span
              style="
                            display: inline-block;
                            padding: 4px 12px;
                            background-color: var(--color-success-light);
                            color: var(--color-success);
                            border-radius: var(--radius-sm);
                            font-size: var(--font-size-small);
                            font-weight: var(--font-weight-medium);
                        "
            >
              ✓ Pago
            </span>
          </td>
          <td style="padding: var(--space-md); text-align: center;">
            <button class="btn btn-tertiary btn-sm">Ver</button>
          </td>
        </tr>
        <!-- Más filas aquí -->
      </tbody>
    </table>
  </div>
</div>

{% endblock %}
```

---

## 2. Formulario de Producto (CRUD)

```html
{% extends "base.html" %}
{% block content %}

<div class="card" style="max-width: 600px;">
    <div class="card-header">
        <h2 class="card-title">{{ 'Nuevo' if not product else 'Editar' }} Producto</h2>
    </div>

    <form id="productForm" method="POST" novalidate>
        <div class="card-body">

            <!-- Campo: Nombre -->
            <div class="form-group">
                <label for="nombre">
                    Nombre del Producto
                    <span class="required">*</span>
                </label>
                <input
                    type="text"
                    id="nombre"
                    name="nombre"
                    value="{{ product.nombre if product else '' }}"
                    placeholder="Ej: Laptop Lenovo ThinkPad"
                    required
                    minlength="3"
                    maxlength="100"
                />
                <span class="help-text">Máximo 100 caracteres, mínimo 3</span>
            </div>

            <!-- Campo: Precio -->
            <div class="form-group">
                <label for="precio">
                    Precio (₲)
                    <span class="required">*</span>
                </label>
                <input
                    type="number"
                    id="precio"
                    name="precio"
                    value="{{ product.precio if product else '' }}"
                    placeholder="0.00"
                    step="0.01"
                    min="0"
                    required
                />
                <span class="help-text">Precio en guaraní sin puntuación</span>
            </div>

            <!-- Campo: Stock -->
            <div class="form-group">
                <label for="stock">
                    Stock Actual
                    <span class="required">*</span>
                </label>
                <input
                    type="number"
                    id="stock"
                    name="stock"
                    value="{{ product.stock if product else '0' }}"
                    min="0"
                    required
                />
                <span class="help-text">Unidades disponibles</span>
            </div>

            <!-- Campo: Categoría -->
            <div class="form-group">
                <label for="categoria">
                    Categoría
                    <span class="required">*</span>
                </label>
                <select id="categoria" name="categoria" required>
                    <option value="">-- Selecciona una categoría --</option>
                    {% for cat in categories %}
                        <option
                            value="{{ cat.id }}"
                            {% if product and product.categoria == cat.id %}selected{% endif %}
                        >
                            {{ cat.nombre }}
                        </option>
                    {% endfor %}
                </select>
                <span class="help-text">Organiza tus productos</span>
            </div>

            <!-- Campo: Código de Barras -->
            <div class="form-group">
                <label for="codigo_barras">
                    Código de Barras (Opcional)
                </label>
                <input
                    type="text"
                    id="codigo_barras"
                    name="codigo_barras"
                    value="{{ product.codigo_barras if product else '' }}"
                    placeholder="Ej: 7501001234567"
                />
                <span class="help-text">Será verificado para evitar duplicados</span>
            </div>

        </div>

        <!-- Footer con botones -->
        <div class="card-footer">
            <div style="text-align: right;">
                <button
                    type="reset"
                    class="btn btn-secondary"
                    title="Limpiar formulario"
                >
                    Limpiar
                </button>
                <button
                    type="button"
                    class="btn btn-tertiary"
                    onclick="window.history.back()"
                >
                    Cancelar
                </button>
                <button
                    type="submit"
                    class="btn btn-primary"
                    id="submitBtn"
                >
                    {{ 'Crear Producto' if not product else 'Guardar Cambios' }}
                </button>
            </div>
        </div>
    </form>
</div>

<!-- SCRIPT DE VALIDACIÓN -->
<script src="{{ url_for('static', filename='js/form-validation.js') }}"></script>
<script>
    const validator = new FormValidator('#productForm');

    // Agregar reglas
    validator
        .addRule('nombre', [
            ValidationRules.required,
            ValidationRules.minLength(3),
            ValidationRules.maxLength(100)
        ])
        .addRule('precio', [
            ValidationRules.required,
            {
                validate: (v) => ({
                    valid: parseFloat(v) > 0,
                    message: 'El precio debe ser mayor a 0'
                })
            }
        ])
        .addRule('stock', [
            ValidationRules.required,
            {
                validate: (v) => ({
                    valid: parseInt(v) >= 0,
                    message: 'Stock no puede ser negativo'
                })
            }
        ])
        .addRule('categoria', [ValidationRules.required]);

    // Override del submit para agregar feedback
    const originalSubmit = validator.submitForm.bind(validator);
    validator.submitForm = function() {
        LoadingState.enable('#submitBtn');
        setTimeout(originalSubmit, 300);
    };
</script>

{% endblock %}
```

---

## 3. Tabla de Productos (Con Filtros y Acciones)

```html
{% extends "base.html" %}
{% block content %}

<!-- HEADER -->
<div class="flex-between mb-lg">
    <div>
        <h1>Gestión de Productos</h1>
        <p class="text-secondary">{{ total_products }} productos en total</p>
    </div>
    <a href="/productos/nuevo" class="btn btn-primary btn-lg">
        ➕ Nuevo Producto
    </a>
</div>

<!-- FILTROS -->
<div class="card mb-lg">
    <div class="card-body">
        <form method="GET" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: var(--space-md);">
            <div class="form-group">
                <input
                    type="search"
                    name="q"
                    placeholder="🔍 Buscar por nombre..."
                    value="{{ search_query }}"
                    style="margin-bottom: 0;"
                />
            </div>
            <div class="form-group">
                <select name="categoria" style="margin-bottom: 0;">
                    <option value="">-- Todas las categorías --</option>
                    {% for cat in categories %}
                        <option value="{{ cat.id }}">{{ cat.nombre }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group">
                <select name="stock" style="margin-bottom: 0;">
                    <option value="">-- Stock: Todos --</option>
                    <option value="bajo">Stock Bajo (< 5)</option>
                    <option value="ok">Stock Normal</option>
                    <option value="alto">Stock Alto (> 50)</option>
                </select>
            </div>
            <div class="flex gap-md">
                <button type="submit" class="btn btn-primary" style="flex: 1;">
                    🔍 Filtrar
                </button>
                <button type="reset" class="btn btn-secondary" style="flex: 1;">
                    ✕ Limpiar
                </button>
            </div>
        </form>
    </div>
</div>

<!-- TABLA -->
<div class="card">
    <div class="card-body" style="overflow-x: auto;">
        <table style="width: 100%; min-width: 800px;">
            <thead style="background-color: var(--bg-tertiary); border-bottom: 1px solid var(--border-default);">
                <tr>
                    <th style="padding: var(--space-md); text-align: left;">
                        <input type="checkbox" id="selectAll" />
                    </th>
                    <th style="padding: var(--space-md); text-align: left; cursor: pointer;">
                        Nombre ↕
                    </th>
                    <th style="padding: var(--space-md); text-align: right; cursor: pointer;">
                        Precio ↕
                    </th>
                    <th style="padding: var(--space-md); text-align: center; cursor: pointer;">
                        Stock ↕
                    </th>
                    <th style="padding: var(--space-md); text-align: left;">
                        Categoría
                    </th>
                    <th style="padding: var(--space-md); text-align: center;">
                        Acciones
                    </th>
                </tr>
            </thead>
            <tbody>
                {% for product in products %}
                <tr
                    class="product-row"
                    style="
                        border-bottom: 1px solid var(--border-default);
                        transition: background-color var(--transition-fast);
                    "
                    onmouseover="this.style.backgroundColor = 'var(--bg-tertiary)'"
                    onmouseout="this.style.backgroundColor = 'transparent'"
                >
                    <td style="padding: var(--space-md);">
                        <input type="checkbox" class="product-checkbox" value="{{ product.id }}" />
                    </td>
                    <td style="padding: var(--space-md);">
                        <strong>{{ product.nombre }}</strong>
                    </td>
                    <td style="padding: var(--space-md); text-align: right;">
                        ₲ {{ "{:,.0f}".format(product.precio) }}
                    </td>
                    <td style="padding: var(--space-md); text-align: center;">
                        {% if product.stock < 5 %}
                            <span style="
                                display: inline-block;
                                padding: 4px 12px;
                                background-color: var(--color-danger-light);
                                color: var(--color-danger);
                                border-radius: var(--radius-sm);
                                font-weight: var(--font-weight-medium);
                            ">
                                {{ product.stock }}
                            </span>
                        {% else %}
                            <span>{{ product.stock }}</span>
                        {% endif %}
                    </td>
                    <td style="padding: var(--space-md);">
                        {{ product.categoria }}
                    </td>
                    <td style="padding: var(--space-md); text-align: center;">
                        <div class="flex" style="justify-content: center; gap: var(--space-sm);">
                            <a
                                href="/productos/{{ product.id }}/editar"
                                class="btn btn-tertiary btn-sm"
                                title="Editar producto"
                            >
                                ✎
                            </a>
                            <button
                                class="btn btn-danger btn-sm"
                                title="Eliminar producto"
                                onclick="confirmDelete({{ product.id }}, '{{ product.nombre }}')"
                            >
                                🗑️
                            </button>
                        </div>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        {% if not products %}
        <div style="text-align: center; padding: var(--space-xxl); color: var(--text-secondary);">
            <p style="font-size: 48px; margin-bottom: var(--space-md);">📦</p>
            <p>No hay productos</p>
            <a href="/productos/nuevo" class="btn btn-primary mt-lg">Crear el primero</a>
        </div>
        {% endif %}
    </div>

    <!-- Footer con info y paginación -->
    <div class="card-footer flex-between">
        <span class="text-secondary">
            Mostrando {{ products|length }} de {{ total_products }} productos
        </span>
        {% if total_pages > 1 %}
        <nav>
            <button class="btn btn-sm btn-tertiary" {% if page == 1 %}disabled{% else %}onclick="goToPage({{ page - 1 }})"{% endif %}>
                ← Anterior
            </button>
            <span class="text-secondary" style="padding: 0 var(--space-md);">
                Página {{ page }} de {{ total_pages }}
            </span>
            <button class="btn btn-sm btn-tertiary" {% if page == total_pages %}disabled{% else %}onclick="goToPage({{ page + 1 }})"{% endif %}>
                Siguiente →
            </button>
        </nav>
        {% endif %}
    </div>
</div>

<!-- Barra de acciones flotante (cuando hay seleccionados) -->
<div id="bulkActionsBar" class="bulk-actions-bar" style="
    display: none;
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background-color: var(--bg-secondary);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-lg);
    padding: var(--space-md) var(--space-lg);
    box-shadow: var(--shadow-lg);
    z-index: 1000;
    animation: slide-in-up var(--transition-normal);
">
    <div class="flex-between">
        <span id="selectedCount" class="text-primary" style="font-weight: var(--font-weight-semibold);">
            <!-- "X seleccionados" -->
        </span>
        <div class="flex gap-md">
            <button type="button" class="btn btn-secondary btn-sm" onclick="deselectAll()">
                Deseleccionar
            </button>
            <button type="button" class="btn btn-primary btn-sm">
                📊 Exportar
            </button>
            <button type="button" class="btn btn-danger btn-sm" onclick="bulkDelete()">
                🗑️ Eliminar
            </button>
        </div>
    </div>
</div>

<!-- SCRIPTS -->
<script>
    // Seleccionar todos
    document.getElementById('selectAll').addEventListener('change', (e) => {
        document.querySelectorAll('.product-checkbox').forEach(cb => {
            cb.checked = e.target.checked;
        });
        updateBulkActionsBar();
    });

    // Actualizar barra de acciones
    document.querySelectorAll('.product-checkbox').forEach(cb => {
        cb.addEventListener('change', updateBulkActionsBar);
    });

    function updateBulkActionsBar() {
        const selected = document.querySelectorAll('.product-checkbox:checked').length;
        const bar = document.getElementById('bulkActionsBar');

        if (selected > 0) {
            bar.style.display = 'flex';
            document.getElementById('selectedCount').textContent =
                `${selected} producto${selected > 1 ? 's' : ''} seleccionado${selected > 1 ? 's' : ''}`;
        } else {
            bar.style.display = 'none';
        }
    }

    function confirmDelete(id, nombre) {
        if (confirm(`¿Eliminar "${nombre}"? Esta acción no se puede deshacer.`)) {
            window.location.href = `/productos/${id}/eliminar`;
        }
    }

    function deselectAll() {
        document.querySelectorAll('.product-checkbox').forEach(cb => cb.checked = false);
        document.getElementById('selectAll').checked = false;
        updateBulkActionsBar();
    }
</script>

{% endblock %}
```

---

## Notas de Implementación

1. **Siempre usar variables CSS**: No hardcodear colores
2. **Espaciado consistente**: Múltiplos de 8px
3. **Validación en cliente**: Feedback inmediato
4. **Mobile-friendly**: Botones 44x44px mínimo
5. **Accesibilidad**: Labels, ARIA, focus visible
6. **Performance**: Lazy load, paginación, caching

---

**Estos ejemplos pueden ser adaptados a tus vistas específicas.**

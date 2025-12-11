from functools import wraps

from flask import (
    Blueprint,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from models.producto import obtener_productos
from services.ventas_service import paginate
from utils.logging_config import get_logger

logger = get_logger(__name__)

inventario_bp = Blueprint("inventario", __name__, url_prefix="/inventario")


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if g.usuario is None:
            flash("Debe iniciar sesión.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if g.usuario is None or g.usuario["rol"] != "admin":
            flash("Acceso denegado. Solo administradores.", "error")
            return redirect(url_for("ventas.agregar_venta_view"))
        return f(*args, **kwargs)

    return decorated


@inventario_bp.route("/")
@login_required
@admin_required
def inventario_view():
    logger.info(f"Admin {g.usuario['username']} accedió a inventario")
    productos_list = obtener_productos()
    categorias = sorted({p["categoria"] for p in productos_list})

    # Filtro de categoría (no aplica a los datos del servidor por ahora, pero mantener seleccion)
    filtro_categoria = request.args.get("categoria", "").strip()

    # Paginación (10 por página)
    page_arg = request.args.get("page", 1)
    per_page = 10
    productos_pagina, page, per_page, total_items, total_pages = paginate(
        productos_list, page=page_arg, per_page=per_page
    )

    # Calcular estadísticas avanzadas
    total_stock = sum(p["stock"] for p in productos_list)
    valor_total_inventario = sum(p["stock"] * p["precio"] for p in productos_list)

    # Indicadores de stock (calculados sobre la lista completa)
    stock_bajo_threshold = 5
    stock_bajo_count = len(
        [p for p in productos_list if p["stock"] <= stock_bajo_threshold]
    )
    stock_medio_count = len(
        [
            p
            for p in productos_list
            if p["stock"] > stock_bajo_threshold
            and p["stock"] <= stock_bajo_threshold + 5
        ]
    )

    # Obtener producto más vendido (de las ventas registradas)
    from models.venta import obtener_detalle_venta, obtener_ventas

    ventas_list = obtener_ventas()
    producto_mas_vendido = None
    ventas_por_producto = {}

    for venta in ventas_list:
        detalles = obtener_detalle_venta(venta["id"])
        for detalle in detalles:
            producto_id = detalle["id"]
            cantidad = detalle["cantidad"]
            ventas_por_producto[producto_id] = (
                ventas_por_producto.get(producto_id, 0) + cantidad
            )

    if ventas_por_producto:
        producto_id_mas_vendido = max(ventas_por_producto, key=ventas_por_producto.get)
        cantidad_vendida = ventas_por_producto[producto_id_mas_vendido]
        # Buscar el producto en la lista
        for p in productos_list:
            if p["id"] == producto_id_mas_vendido:
                producto_mas_vendido = {
                    "nombre": p["nombre"],
                    "cantidad_vendida": cantidad_vendida,
                }
                break

    return render_template(
        "inventario.html",
        productos=productos_pagina,
        stock_bajo=5,
        categorias=categorias,
        filtro_categoria=filtro_categoria,
        total_stock=total_stock,
        valor_total_inventario=valor_total_inventario,
        producto_mas_vendido=producto_mas_vendido,
        # Paginación
        page=page,
        per_page=per_page,
        total_items=total_items,
        total_pages=total_pages,
        stock_bajo_count=stock_bajo_count,
        stock_medio_count=stock_medio_count,
    )


@inventario_bp.route("/sugerencias")
@login_required
@admin_required
def sugerencias_producto():
    q = request.args.get("q", "")
    logger.debug(f"Búsqueda de producto - Admin: {g.usuario['username']}, Query: {q}")
    productos = obtener_productos()

    resultados = [
        {"id": p["id"], "codigo_barras": p["codigo_barras"], "nombre": p["nombre"]}
        for p in productos
        if q in p["codigo_barras"]
    ][:10]

    return jsonify(resultados)

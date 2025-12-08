import json
from functools import wraps
from math import ceil

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

from models.producto import obtener_producto_por_codigo
from models.venta import obtener_detalle_venta, obtener_ventas, registrar_venta
from utils.logging_config import get_logger

logger = get_logger(__name__)
ventas_bp = Blueprint("ventas", __name__, url_prefix="/ventas")


# Decorador login_required
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if g.usuario is None:
            flash("Debe iniciar sesión para acceder.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated


@ventas_bp.route("/agregar", methods=["GET", "POST"])
@login_required
def agregar_venta_view():
    """Registra una venta con validaciones completas."""
    if request.method == "POST":
        productos_json = request.form.get("productos")

        # Validación 1: JSON está presente
        if not productos_json or productos_json.strip() == "":
            flash("Debe agregar al menos un producto a la venta.", "error")
            return redirect(url_for("ventas.agregar_venta_view"))

        try:
            productos_cantidades = json.loads(productos_json)
        except json.JSONDecodeError:
            flash("Error: formato de datos inválido.", "error")
            return redirect(url_for("ventas.agregar_venta_view"))

        # Validación 2: Lista no está vacía
        if not productos_cantidades or len(productos_cantidades) == 0:
            flash("Debe agregar al menos un producto a la venta.", "error")
            return redirect(url_for("ventas.agregar_venta_view"))

        # Validación 3: Validar estructura de cada item
        for idx, item in enumerate(productos_cantidades):
            # Verificar que tenga los campos requeridos
            if "id" not in item or "cantidad" not in item:
                flash(f"Error: producto {idx + 1} tiene estructura inválida.", "error")
                return redirect(url_for("ventas.agregar_venta_view"))

            try:
                producto_id = int(item["id"])
                cantidad = int(item["cantidad"])
            except (ValueError, TypeError):
                flash(
                    f"Error: producto {idx + 1} tiene ID o cantidad inválida.", "error"
                )
                return redirect(url_for("ventas.agregar_venta_view"))

            # Validación 4: Cantidad > 0
            if cantidad <= 0:
                flash(
                    f"Error: la cantidad del producto {idx + 1} debe ser mayor a 0.",
                    "error",
                )
                return redirect(url_for("ventas.agregar_venta_view"))

            # Validación 5: Producto existe
            from models.producto import obtener_producto_por_id

            producto = obtener_producto_por_id(producto_id)
            if not producto:
                flash(f"Error: el producto con ID {producto_id} no existe.", "error")
                return redirect(url_for("ventas.agregar_venta_view"))

            # Validación 6: Stock disponible
            if producto["stock"] < cantidad:
                flash(
                    f"Stock insuficiente para '{producto['nombre']}'. "
                    f"Disponible: {producto['stock']}, solicitado: {cantidad}",
                    "error",
                )
                return redirect(url_for("ventas.agregar_venta_view"))

        # Si todas las validaciones pasaron, registrar venta
        exito, mensaje = registrar_venta(
            productos_cantidades, usuario_id=g.usuario["id"]
        )

        if exito:
            cantidad_productos = len(productos_cantidades)
            logger.info(
                f"Venta registrada - Usuario: {g.usuario['username']}, "
                f"Productos: {cantidad_productos}, Mensaje: {mensaje}"
            )
            flash("Venta registrada correctamente.", "success")
        else:
            logger.error(
                f"Fallo al registrar venta para usuario {g.usuario['username']}: {mensaje}"
            )
            flash(f"Error al registrar la venta: {mensaje}", "error")

        return redirect(url_for("ventas.agregar_venta_view"))

    return render_template("agregar_venta.html")


@ventas_bp.route("/buscar/<codigo_barras>")
@login_required
def buscar_producto(codigo_barras):
    producto = obtener_producto_por_codigo(codigo_barras)
    if producto:
        logger.debug(
            f"Producto encontrado - Usuario: {g.usuario['username']}, "
            f"Código: {codigo_barras}, ID: {producto['id']}"
        )
        return jsonify({"success": True, "producto": producto})
    logger.debug(
        f"Producto no encontrado - Usuario: {g.usuario['username']}, "
        f"Código: {codigo_barras}"
    )
    return jsonify({"success": False, "mensaje": "Producto no encontrado"})


@ventas_bp.route("/")
@login_required
def listado_ventas():
    """Lista ventas con filtros avanzados."""
    logger.info(f"Usuario {g.usuario['username']} accedió a listado de ventas")

    # Obtener todas las ventas
    ventas_list = obtener_ventas()

    # Obtener parámetros de filtro
    search_query = request.args.get("search", "").strip().lower()
    fecha_desde = request.args.get("fecha_desde", "").strip()
    fecha_hasta = request.args.get("fecha_hasta", "").strip()
    usuario_filtro = request.args.get("usuario", "").strip()
    monto_minimo = request.args.get("monto_minimo", "").strip()

    # Aplicar filtros
    ventas_filtradas = ventas_list

    # Búsqueda por ID, usuario o producto
    if search_query:
        ventas_filtradas = [
            v
            for v in ventas_filtradas
            if search_query in str(v["id"]).lower()
            or search_query in v.get("username", "").lower()
            or any(
                search_query in detalle.get("nombre", "").lower()
                for detalle in obtener_detalle_venta(v["id"])
            )
        ]
        logger.debug(
            f"Búsqueda - Usuario: {g.usuario['username']}, Query: {search_query}, "
            f"Resultados: {len(ventas_filtradas)}"
        )

    # Filtro por rango de fechas
    if fecha_desde:
        from datetime import datetime

        try:
            fecha_desde_obj = datetime.strptime(fecha_desde, "%Y-%m-%d")
            ventas_filtradas = [
                v
                for v in ventas_filtradas
                if datetime.strptime(v["fecha"][:10], "%Y-%m-%d") >= fecha_desde_obj
            ]
        except ValueError:
            pass

    if fecha_hasta:
        from datetime import datetime

        try:
            fecha_hasta_obj = datetime.strptime(fecha_hasta, "%Y-%m-%d")
            ventas_filtradas = [
                v
                for v in ventas_filtradas
                if datetime.strptime(v["fecha"][:10], "%Y-%m-%d") <= fecha_hasta_obj
            ]
        except ValueError:
            pass

    # Filtro por usuario
    if usuario_filtro:
        ventas_filtradas = [
            v
            for v in ventas_filtradas
            if usuario_filtro.lower() in v.get("username", "").lower()
        ]

    # Filtro por monto mínimo
    if monto_minimo:
        try:
            monto_min_num = float(monto_minimo)
            ventas_filtradas = [
                v for v in ventas_filtradas if v["total"] >= monto_min_num
            ]
        except ValueError:
            pass

    # Obtener lista única de usuarios para el filtro dropdown
    usuarios_unicos = sorted(
        {v.get("username", "-") for v in ventas_list if v.get("username")}
    )

    # Calcular estadísticas del día
    from datetime import date, datetime

    hoy = date.today()
    ventas_hoy = [
        v
        for v in ventas_list
        if datetime.strptime(v["fecha"][:10], "%Y-%m-%d").date() == hoy
    ]

    estadisticas = {
        "cantidad_ventas_hoy": len(ventas_hoy),
        "total_recaudado_hoy": sum(v["total"] for v in ventas_hoy),
        "venta_mas_grande_hoy": max((v["total"] for v in ventas_hoy), default=0),
        "promedio_por_venta_hoy": (
            sum(v["total"] for v in ventas_hoy) / len(ventas_hoy) if ventas_hoy else 0
        ),
    }

    logger.info(
        f"Listado de ventas - Usuario: {g.usuario['username']}, "
        f"Total: {len(ventas_list)}, Filtradas: {len(ventas_filtradas)}"
    )

    # --- Paginación ---
    # Parámetros: page (1-indexed) y per_page
    try:
        page = int(request.args.get("page", 1))
        if page < 1:
            page = 1
    except (ValueError, TypeError):
        page = 1

    try:
        per_page = int(request.args.get("per_page", 10))
        if per_page <= 0:
            per_page = 10
    except (ValueError, TypeError):
        per_page = 10

    total_items = len(ventas_filtradas)
    total_pages = ceil(total_items / per_page) if total_items > 0 else 1

    # Ajustar page si excede
    if page > total_pages:
        page = total_pages

    start = (page - 1) * per_page
    end = start + per_page
    ventas_pagina = ventas_filtradas[start:end]

    # Query params para mantener filtros en los links de paginación
    query_params = request.args.to_dict()

    return render_template(
        "ventas.html",
        ventas=ventas_pagina,
        ventas_total=ventas_list,
        obtener_detalle_venta=obtener_detalle_venta,
        search_query=search_query,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        usuario_filtro=usuario_filtro,
        monto_minimo=monto_minimo,
        usuarios_unicos=usuarios_unicos,
        estadisticas=estadisticas,
        # Paginación
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        total_items=total_items,
        query_params=query_params,
    )

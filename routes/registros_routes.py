"""Rutas para el listado y visualización de registros de ventas."""

import csv
import io
from datetime import datetime
from functools import wraps
from urllib.parse import urlencode

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)

from models.venta import obtener_detalle_venta, obtener_ventas
from services.ventas_service import (
    estadisticas_del_dia,
    estadisticas_generales,
    filter_ventas,
    paginate,
    productos_mas_vendidos,
    usuarios_unicos,
    ventas_por_mes,
    ventas_por_semana,
)
from utils.logging_config import get_logger

logger = get_logger(__name__)
registros_bp = Blueprint("registros", __name__, url_prefix="/registros")


# Decorador login_required
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if g.usuario is None:
            flash("Debe iniciar sesión para acceder.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated


# Decorador admin_required
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if g.usuario is None:
            flash("Debe iniciar sesión para acceder.", "error")
            return redirect(url_for("auth.login"))
        if g.usuario["rol"] != "admin":
            flash("Acceso denegado. Se requieren permisos de administrador.", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated


@registros_bp.route("/")
@login_required
@admin_required
def listado_registros():
    """Lista registros de ventas con filtros avanzados."""
    logger.info(f"Usuario {g.usuario['username']} accedió a listado de registros")

    # Obtener todas las ventas
    ventas_list = obtener_ventas()

    # Obtener parámetros de filtro
    search_query = request.args.get("search", "").strip().lower()
    fecha_desde = request.args.get("fecha_desde", "").strip()
    fecha_hasta = request.args.get("fecha_hasta", "").strip()
    usuario_filtro = request.args.get("usuario", "").strip()
    monto_minimo = request.args.get("monto_minimo", "").strip()

    # Aplicar filtros (delegado a servicio)
    ventas_filtradas = filter_ventas(
        ventas_list,
        obtener_detalle_venta,
        search_query=search_query,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        usuario_filtro=usuario_filtro,
        monto_minimo=monto_minimo,
    )

    # Lista única de usuarios para el dropdown
    usuarios_unicos_list = usuarios_unicos(ventas_list)

    # Estadísticas del día (delegado a servicio)
    estadisticas = estadisticas_del_dia(ventas_list)

    # Estadísticas generales para dashboard
    estadisticas_general = estadisticas_generales(ventas_list)

    # Datos para gráficos
    ventas_mensuales = ventas_por_mes(ventas_list, meses_atras=6)
    ventas_semanales = ventas_por_semana(ventas_list, semanas_atras=8)
    top_productos = productos_mas_vendidos(ventas_list, obtener_detalle_venta, top_n=5)

    # Fecha actual para el template
    now = datetime.now()

    logger.info(
        f"Listado de registros - Usuario: {g.usuario['username']}, "
        f"Total: {len(ventas_list)}, Filtradas: {len(ventas_filtradas)}"
    )

    # --- Paginación --- (delegado al servicio)
    page_arg = request.args.get("page", 1)
    per_page_arg = request.args.get("per_page", 10)
    ventas_pagina, page, per_page, total_items, total_pages = paginate(
        ventas_filtradas, page=page_arg, per_page=per_page_arg
    )

    # Query params para mantener filtros en los links de paginación
    query_params = request.args.to_dict()

    # Construir query string sin los parámetros de paginación (page, per_page)
    qp_no_page = {
        k: v for k, v in query_params.items() if k not in ("page", "per_page")
    }
    query_string = urlencode(qp_no_page)

    return render_template(
        "registros.html",
        ventas=ventas_pagina,
        ventas_total=ventas_list,
        obtener_detalle_venta=obtener_detalle_venta,
        search_query=search_query,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        usuario_filtro=usuario_filtro,
        monto_minimo=monto_minimo,
        usuarios_unicos=usuarios_unicos_list,
        estadisticas=estadisticas,
        estadisticas_general=estadisticas_general,
        ventas_mensuales=ventas_mensuales,
        ventas_semanales=ventas_semanales,
        top_productos=top_productos,
        now=now,
        # Paginación
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        total_items=total_items,
        query_params=query_params,
        query_string=query_string,
    )


@registros_bp.route("/exportar-csv", methods=["POST"])
@login_required
@admin_required
def exportar_csv():
    """Exporta registros de ventas filtrados a CSV."""
    logger.info(f"Usuario {g.usuario['username']} inició exportación a CSV")

    # Obtener todas las ventas
    ventas_list = obtener_ventas()

    # Obtener parámetros de filtro del request JSON
    data = request.get_json() or {}
    search_query = data.get("search", "").strip().lower()
    fecha_desde = data.get("fecha_desde", "").strip()
    fecha_hasta = data.get("fecha_hasta", "").strip()
    usuario_filtro = data.get("usuario", "").strip()
    monto_minimo = data.get("monto_minimo", "").strip()

    # Aplicar filtros
    ventas_filtradas = filter_ventas(
        ventas_list,
        obtener_detalle_venta,
        search_query=search_query,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        usuario_filtro=usuario_filtro,
        monto_minimo=monto_minimo,
    )

    logger.info(
        f"CSV - Usuario: {g.usuario['username']}, "
        f"Total: {len(ventas_list)}, Exportadas: {len(ventas_filtradas)}"
    )

    # Crear CSV en memoria
    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer, lineterminator="\n")

    # Headers
    headers = [
        "ID Venta",
        "Fecha",
        "Usuario",
        "Cantidad Items",
        "Total (₲)",
        "Productos",
    ]
    writer.writerow(headers)

    # Filas de datos
    for venta in ventas_filtradas:
        detalles = obtener_detalle_venta(venta["id"])
        productos = ", ".join([d.get("nombre", "N/A") for d in detalles])
        cantidad_items = sum([d.get("cantidad", 0) for d in detalles])

        row = [
            venta.get("id", ""),
            venta.get("fecha", ""),
            venta.get("username", ""),
            cantidad_items,
            venta.get("total", ""),
            productos,
        ]
        writer.writerow(row)

    # Convertir StringIO a BytesIO
    csv_buffer.seek(0)
    bytes_buffer = io.BytesIO(csv_buffer.getvalue().encode("utf-8-sig"))
    bytes_buffer.seek(0)

    # Generar nombre de archivo con fecha/filtros
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"registros_ventas_{timestamp}.csv"

    return send_file(
        bytes_buffer,
        mimetype="text/csv; charset=utf-8",
        as_attachment=True,
        download_name=filename,
    )

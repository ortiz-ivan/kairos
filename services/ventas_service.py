from datetime import date, datetime
from math import ceil


def filter_ventas(
    ventas,
    obtener_detalle_fn,
    search_query="",
    fecha_desde="",
    fecha_hasta="",
    usuario_filtro="",
    monto_minimo="",
):
    """Aplica filtros a la lista de ventas y devuelve la lista filtrada.

    Args:
        ventas: lista de dicts de ventas
        obtener_detalle_fn: función que recibe venta_id y devuelve detalles
    """
    ventas_filtradas = ventas

    q = (search_query or "").strip().lower()
    if q:
        ventas_filtradas = [
            v
            for v in ventas_filtradas
            if q in str(v["id"]).lower()
            or q in v.get("username", "").lower()
            or any(
                q in d.get("nombre", "").lower() for d in obtener_detalle_fn(v["id"])
            )
        ]

    # Rangos de fecha
    if fecha_desde:
        try:
            fecha_desde_obj = datetime.strptime(fecha_desde, "%Y-%m-%d")
            ventas_filtradas = [
                v
                for v in ventas_filtradas
                if datetime.strptime(str(v["fecha"])[:10], "%Y-%m-%d")
                >= fecha_desde_obj
            ]
        except ValueError:
            pass

    if fecha_hasta:
        try:
            fecha_hasta_obj = datetime.strptime(fecha_hasta, "%Y-%m-%d")
            ventas_filtradas = [
                v
                for v in ventas_filtradas
                if datetime.strptime(str(v["fecha"])[:10], "%Y-%m-%d")
                <= fecha_hasta_obj
            ]
        except ValueError:
            pass

    if usuario_filtro:
        uf = usuario_filtro.strip().lower()
        ventas_filtradas = [
            v for v in ventas_filtradas if uf in v.get("username", "").lower()
        ]

    if monto_minimo:
        try:
            monto_min = float(monto_minimo)
            ventas_filtradas = [
                v for v in ventas_filtradas if v.get("total", 0) >= monto_min
            ]
        except (ValueError, TypeError):
            pass

    return ventas_filtradas


def paginate(ventas, page=1, per_page=10):
    try:
        page = int(page)
        if page < 1:
            page = 1
    except (ValueError, TypeError):
        page = 1

    try:
        per_page = int(per_page)
        if per_page <= 0:
            per_page = 10
    except (ValueError, TypeError):
        per_page = 10

    total_items = len(ventas)
    total_pages = ceil(total_items / per_page) if total_items > 0 else 1

    if page > total_pages:
        page = total_pages

    start = (page - 1) * per_page
    end = start + per_page
    return ventas[start:end], page, per_page, total_items, total_pages


def usuarios_unicos(ventas):
    return sorted({v.get("username", "-") for v in ventas if v.get("username")})


def estadisticas_del_dia(ventas, target_date=None):
    if target_date is None:
        target_date = date.today()

    ventas_hoy = [
        v
        for v in ventas
        if datetime.strptime(str(v["fecha"])[:10], "%Y-%m-%d").date() == target_date
    ]

    total = sum(v.get("total", 0) for v in ventas_hoy)
    cantidad = len(ventas_hoy)
    mayor = max((v.get("total", 0) for v in ventas_hoy), default=0)
    promedio = total / cantidad if cantidad else 0

    return {
        "cantidad_ventas_hoy": cantidad,
        "total_recaudado_hoy": total,
        "venta_mas_grande_hoy": mayor,
        "promedio_por_venta_hoy": promedio,
    }

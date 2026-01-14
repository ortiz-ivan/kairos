from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
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


def ventas_por_mes(ventas, meses_atras=12):
    """Devuelve ventas agrupadas por mes para los últimos N meses."""
    hoy = date.today()
    inicio = hoy.replace(day=1) - timedelta(days=30 * (meses_atras - 1))

    ventas_mensuales = defaultdict(lambda: {"cantidad": 0, "total": 0})

    for venta in ventas:
        try:
            fecha_venta = datetime.strptime(str(venta["fecha"])[:10], "%Y-%m-%d").date()
            if fecha_venta >= inicio:
                mes_key = fecha_venta.strftime("%Y-%m")
                ventas_mensuales[mes_key]["cantidad"] += 1
                ventas_mensuales[mes_key]["total"] += venta.get("total", 0)
        except (ValueError, KeyError):
            continue

    # Completar meses faltantes con ceros
    resultado = []
    for i in range(meses_atras):
        mes_actual = (inicio + timedelta(days=30 * i)).replace(day=1)
        mes_key = mes_actual.strftime("%Y-%m")
        if mes_key in ventas_mensuales:
            resultado.append(
                {
                    "mes": mes_key,
                    "cantidad": ventas_mensuales[mes_key]["cantidad"],
                    "total": ventas_mensuales[mes_key]["total"],
                }
            )
        else:
            resultado.append({"mes": mes_key, "cantidad": 0, "total": 0})

    return resultado


def ventas_por_semana(ventas, semanas_atras=12):
    """Devuelve ventas agrupadas por semana para las últimas N semanas."""
    hoy = date.today()
    inicio = hoy - timedelta(weeks=semanas_atras - 1)

    # Ajustar al inicio de semana (lunes)
    inicio = inicio - timedelta(days=inicio.weekday())

    ventas_semanales = defaultdict(lambda: {"cantidad": 0, "total": 0})

    for venta in ventas:
        try:
            fecha_venta = datetime.strptime(str(venta["fecha"])[:10], "%Y-%m-%d").date()
            if fecha_venta >= inicio:
                # Calcular semana del año
                semana_key = f"{fecha_venta.year}-W{fecha_venta.isocalendar()[1]:02d}"
                ventas_semanales[semana_key]["cantidad"] += 1
                ventas_semanales[semana_key]["total"] += venta.get("total", 0)
        except (ValueError, KeyError):
            continue

    # Completar semanas faltantes con ceros
    resultado = []
    for i in range(semanas_atras):
        semana_actual = inicio + timedelta(weeks=i)
        semana_key = f"{semana_actual.year}-W{semana_actual.isocalendar()[1]:02d}"
        if semana_key in ventas_semanales:
            resultado.append(
                {
                    "semana": semana_key,
                    "cantidad": ventas_semanales[semana_key]["cantidad"],
                    "total": ventas_semanales[semana_key]["total"],
                }
            )
        else:
            resultado.append({"semana": semana_key, "cantidad": 0, "total": 0})

    return resultado


def productos_mas_vendidos(ventas, obtener_detalle_fn, top_n=10):
    """Devuelve los productos más vendidos con sus estadísticas."""
    contador_productos = Counter()
    productos_info = {}

    for venta in ventas:
        detalles = obtener_detalle_fn(venta["id"])
        for detalle in detalles:
            nombre = detalle.get("nombre", "Desconocido")
            cantidad = detalle.get("cantidad", 0)
            subtotal = detalle.get("subtotal", 0)

            contador_productos[nombre] += cantidad
            if nombre not in productos_info:
                productos_info[nombre] = {
                    "cantidad_total": 0,
                    "ventas_total": 0,
                    "precio_promedio": 0,
                }
            productos_info[nombre]["cantidad_total"] += cantidad
            productos_info[nombre]["ventas_total"] += subtotal

    # Calcular precio promedio por producto
    for nombre, info in productos_info.items():
        if info["cantidad_total"] > 0:
            info["precio_promedio"] = info["ventas_total"] / info["cantidad_total"]

    # Obtener top N productos
    top_productos = contador_productos.most_common(top_n)

    resultado = []
    for nombre, cantidad in top_productos:
        info = productos_info.get(nombre, {})
        resultado.append(
            {
                "nombre": nombre,
                "cantidad_vendida": cantidad,
                "ventas_total": info.get("ventas_total", 0),
                "precio_promedio": info.get("precio_promedio", 0),
            }
        )

    return resultado


def estadisticas_generales(ventas):
    """Devuelve estadísticas generales de todas las ventas."""
    if not ventas:
        return {
            "total_ventas": 0,
            "total_recaudado": 0,
            "venta_promedio": 0,
            "venta_mas_grande": 0,
            "venta_mas_pequena": 0,
            "dias_con_ventas": 0,
        }

    totales = [v.get("total", 0) for v in ventas]
    fechas = []

    for v in ventas:
        try:
            fecha = datetime.strptime(str(v["fecha"])[:10], "%Y-%m-%d").date()
            fechas.append(fecha)
        except (ValueError, KeyError):
            continue

    dias_unicos = len(set(fechas)) if fechas else 0

    return {
        "total_ventas": len(ventas),
        "total_recaudado": sum(totales),
        "venta_promedio": sum(totales) / len(ventas),
        "venta_mas_grande": max(totales),
        "venta_mas_pequena": min(totales) if totales else 0,
        "dias_con_ventas": dias_unicos,
    }

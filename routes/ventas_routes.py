import json
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

from models.producto import obtener_producto_por_codigo, obtener_productos
from models.venta import guardar_pendiente, obtener_pendiente_por_id, registrar_venta
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
        pendiente_flag = request.form.get("pendiente") == "1"

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
        if pendiente_flag:
            # Guardar como pendiente: no validar stock ni descontar
            exito, mensaje = guardar_pendiente(
                productos_cantidades, usuario_id=g.usuario["id"]
            )
            if exito:
                logger.info(
                    "Venta guardada como pendiente - Usuario: %s, Productos: %d",
                    g.usuario["username"],
                    len(productos_cantidades),
                )
                flash("Venta guardada como pendiente.", "success")
            else:
                logger.error(f"Fallo al guardar pendiente: {mensaje}")
                flash(f"Error al guardar pendiente: {mensaje}", "error")
            return redirect(url_for("ventas.agregar_venta_view"))

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

    # Si se solicita retomar un pendiente, obtenerlo y pasarlo a la plantilla
    pendiente_id = request.args.get("pendiente_id")
    pendiente_data = None
    if pendiente_id:
        pendiente_data = obtener_pendiente_por_id(pendiente_id)

    return render_template("agregar_venta.html", pendiente=pendiente_data)


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


@ventas_bp.route("/productos/buscar")
@login_required
def buscar_productos_nombre():
    """Busca productos por nombre. Parámetro: ?q=nombre"""
    q = request.args.get("q", "").strip().lower()

    if not q or len(q) < 2:
        return jsonify({"productos": []})

    productos = obtener_productos()

    # Filtrar productos por nombre, código de barras o categoría
    resultados = [
        p
        for p in productos
        if q in p["nombre"].lower()
        or q in p.get("codigo_barras", "").lower()
        or q in p.get("categoria", "").lower()
    ][
        :20
    ]  # Limitar a 20 resultados

    logger.debug(
        f"Búsqueda de productos - Usuario: {g.usuario['username']}, "
        f"Query: '{q}', Resultados: {len(resultados)}"
    )

    return jsonify({"productos": resultados})

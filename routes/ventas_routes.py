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

from models.producto import obtener_producto_por_codigo
from models.venta import registrar_venta
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

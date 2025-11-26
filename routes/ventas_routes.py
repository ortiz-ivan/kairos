from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from functools import wraps
from flask import g
import json
from models.venta import registrar_venta, obtener_ventas, obtener_detalle_venta
from models.producto import obtener_producto_por_codigo

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
    if request.method == "POST":
        productos_json = request.form.get("productos")
        if productos_json:
            try:
                productos_cantidades = json.loads(productos_json)
                exito = registrar_venta(
                    productos_cantidades, usuario_id=g.usuario["id"]
                )
                flash(
                    (
                        "Venta registrada correctamente."
                        if exito
                        else "Error al registrar la venta."
                    ),
                    "success" if exito else "error",
                )
            except Exception as e:
                flash(f"Error procesando venta: {e}", "error")

        return redirect(url_for("ventas.agregar_venta_view"))

    return render_template("agregar_venta.html")


@ventas_bp.route("/buscar/<codigo_barras>")
@login_required
def buscar_producto(codigo_barras):
    producto = obtener_producto_por_codigo(codigo_barras)
    if producto:
        return jsonify({"success": True, "producto": producto})
    return jsonify({"success": False, "mensaje": "Producto no encontrado"})


@ventas_bp.route("/")
@login_required
def listado_ventas():
    ventas_list = obtener_ventas()
    return render_template(
        "ventas.html",
        ventas=ventas_list,
        obtener_detalle_venta=obtener_detalle_venta,
    )

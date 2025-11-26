from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from functools import wraps
from flask import g
from models.producto import obtener_productos

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
    productos_list = obtener_productos()
    categorias = sorted({p["categoria"] for p in productos_list})
    return render_template(
        "inventario.html",
        productos=productos_list,
        stock_bajo=5,
        categorias=categorias,
    )


@inventario_bp.route("/sugerencias")
@login_required
@admin_required
def sugerencias_producto():
    q = request.args.get("q", "")
    productos = obtener_productos()

    resultados = [
        {"id": p["id"], "codigo_barras": p["codigo_barras"], "nombre": p["nombre"]}
        for p in productos
        if q in p["codigo_barras"]
    ][:10]

    return jsonify(resultados)

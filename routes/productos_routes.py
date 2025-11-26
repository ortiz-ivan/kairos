from flask import Blueprint, render_template, request, redirect, url_for, flash
from functools import wraps
from flask import g
from models.producto import (
    obtener_productos,
    obtener_producto_por_id,
    agregar_producto,
    editar_producto,
    eliminar_producto,
)

productos_bp = Blueprint("productos", __name__, url_prefix="/productos")


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if g.usuario is None:
            flash("Debe iniciar sesión.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated


def roles_requeridos(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if g.usuario is None or g.usuario["rol"] not in roles:
                flash("No tiene permisos para acceder.", "error")
                return redirect(url_for("productos.productos_list"))
            return f(*args, **kwargs)

        return decorated

    return decorator


@productos_bp.route("/")
@login_required
def productos_list():
    return render_template("productos.html", productos=obtener_productos())


@productos_bp.route("/agregar", methods=["GET", "POST"])
@login_required
@roles_requeridos("admin")
def agregar_producto_view():
    if request.method == "POST":
        agregar_producto(
            request.form["nombre"],
            float(request.form["precio"]),
            int(request.form["stock"]),
            request.form["categoria"],
            request.form["codigo_barras"],
        )
        return redirect(url_for("productos.productos_list"))
    return render_template("agregar_producto.html")


@productos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
@roles_requeridos("admin")
def editar_producto_view(id):
    producto = obtener_producto_por_id(id)
    if request.method == "POST":
        editar_producto(
            id,
            request.form["nombre"],
            float(request.form["precio"]),
            int(request.form["stock"]),
            request.form["categoria"],
            request.form["codigo_barras"],
        )
        return redirect(url_for("productos.productos_list"))

    return render_template("editar_producto.html", producto=producto)


@productos_bp.route("/eliminar/<int:id>")
@login_required
@roles_requeridos("admin")
def eliminar_producto_view(id):
    eliminar_producto(id)
    return redirect(url_for("productos.productos_list"))

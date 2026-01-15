"""
Rutas de productos para gestión de inventario.

Proporciona endpoints para operaciones CRUD de productos con
autorización basada en roles.
"""

from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from models.producto import obtener_producto_por_id, obtener_productos
from services.productos_service import (
    crear_producto,
    editar_producto_servicio,
    eliminar_producto_servicio,
    filtrar_productos,
    obtener_categorias,
)
from utils.decorators import login_required, roles_requeridos
from utils.logging_config import get_logger

logger = get_logger(__name__)

productos_bp = Blueprint("productos", __name__, url_prefix="/productos")


@productos_bp.route("/")
@login_required
def productos_list():
    """Lista productos con filtros opcionales."""
    logger.info(f"Usuario {g.usuario['username']} accedió a listado de productos")

    productos = obtener_productos()

    # Aplicar filtros
    categoria_filtro = request.args.get("categoria", "").strip()
    codigo_filtro = request.args.get("codigo", "").strip()
    productos_filtrados = filtrar_productos(productos, categoria_filtro, codigo_filtro)

    # Obtener categorías para el select
    categorias = obtener_categorias()

    return render_template(
        "productos.html",
        productos=productos_filtrados,
        categorias=categorias,
        categoria_filtro=categoria_filtro,
        codigo_filtro=codigo_filtro,
    )


@productos_bp.route("/agregar", methods=["GET", "POST"])
@login_required
@roles_requeridos("admin")
def agregar_producto_view():
    """Agrega un nuevo producto con validaciones."""
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        precio = request.form["precio"]
        stock = request.form["stock"]
        categoria = request.form["categoria"].strip()
        codigo_barras = request.form["codigo_barras"].strip()

        exito, mensaje = crear_producto(
            nombre, precio, stock, categoria, codigo_barras, g.usuario["username"]
        )

        if exito:
            flash(mensaje, "success")
            return redirect(url_for("productos.productos_list"))
        else:
            flash(mensaje, "error")
            return render_template("agregar_producto.html")

    return render_template("agregar_producto.html")


@productos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
@roles_requeridos("admin")
def editar_producto_view(id):
    """Edita un producto existente con validaciones."""
    producto = obtener_producto_por_id(id)

    if not producto:
        flash("Producto no encontrado.", "error")
        return redirect(url_for("productos.productos_list"))

    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        precio = request.form["precio"]
        stock = request.form["stock"]
        categoria = request.form["categoria"].strip()
        codigo_barras = request.form["codigo_barras"].strip()

        exito, mensaje = editar_producto_servicio(
            id, nombre, precio, stock, categoria, codigo_barras, g.usuario["username"]
        )

        if exito:
            flash(mensaje, "success")
            return redirect(url_for("productos.productos_list"))
        else:
            flash(mensaje, "error")
            return render_template("editar_producto.html", producto=producto)

    return render_template("editar_producto.html", producto=producto)


@productos_bp.route("/eliminar/<int:id>")
@login_required
@roles_requeridos("admin")
def eliminar_producto_view(id):
    """Elimina un producto."""
    exito, mensaje = eliminar_producto_servicio(id, g.usuario["username"])
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("productos.productos_list"))

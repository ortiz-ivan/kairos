from functools import wraps

from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from models.producto import (
    agregar_producto,
    editar_producto,
    eliminar_producto,
    obtener_producto_por_id,
    obtener_productos,
)
from utils.logging_config import get_logger

logger = get_logger(__name__)

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
    logger.info(f"Usuario {g.usuario['username']} accedió a listado de productos")
    productos = obtener_productos()

    # Filtrar por categoría si se proporciona en query string
    categoria_filtro = request.args.get("categoria", "").strip()
    if categoria_filtro:
        productos = [
            p
            for p in productos
            if p["categoria"] and categoria_filtro.lower() in p["categoria"].lower()
        ]

    # Filtrar por código de barras si se proporciona en query string
    codigo_filtro = request.args.get("codigo", "").strip()
    if codigo_filtro:
        productos = [
            p
            for p in productos
            if p["codigo_barras"]
            and codigo_filtro.lower() in p["codigo_barras"].lower()
        ]

    # Obtener lista de categorías únicas para el select
    categorias = sorted({p["categoria"] for p in obtener_productos() if p["categoria"]})

    return render_template(
        "productos.html",
        productos=productos,
        categorias=categorias,
        categoria_filtro=categoria_filtro,
        codigo_filtro=codigo_filtro,
    )


@productos_bp.route("/agregar", methods=["GET", "POST"])
@login_required
@roles_requeridos("admin")
def agregar_producto_view():
    if request.method == "POST":
        codigo_barras = request.form["codigo_barras"].strip()
        nombre = request.form["nombre"].strip()

        # Validar que el código de barras no esté vacío
        if not codigo_barras:
            flash("El código de barras no puede estar vacío.", "error")
            return render_template("agregar_producto.html")

        # Validar que no exista un producto con el mismo código de barras
        productos_existentes = obtener_productos()
        codigo_duplicado = any(
            p["codigo_barras"] == codigo_barras for p in productos_existentes
        )

        if codigo_duplicado:
            flash(
                f"Error: Ya existe un producto con el código de barras '{codigo_barras}'.",
                "error",
            )
            return render_template("agregar_producto.html")

        # Validar que el nombre no esté vacío
        if not nombre:
            flash("El nombre del producto no puede estar vacío.", "error")
            return render_template("agregar_producto.html")

        try:
            agregar_producto(
                nombre,
                float(request.form["precio"]),
                int(request.form["stock"]),
                request.form["categoria"].strip(),
                codigo_barras,
            )
            mensaje = "Producto agregado correctamente."
            flash(mensaje, "success")
            logger.info(
                f"Producto agregado - Usuario: {g.usuario['username']}, "
                f"Nombre: {nombre}, Código: {codigo_barras}"
            )
            return redirect(url_for("productos.productos_list"))
        except ValueError as e:
            mensaje = "Error: Precio y stock deben ser números válidos."
            flash(mensaje, "error")
            logger.error(
                f"Error de validación al agregar producto - Usuario: {g.usuario['username']}, "
                f"Nombre: {nombre}: {e}"
            )
            return render_template("agregar_producto.html")
        except Exception as e:
            mensaje = f"Error al agregar producto: {e}"
            flash(mensaje, "error")
            logger.error(
                f"Error al agregar producto - Usuario: {g.usuario['username']}, "
                f"Nombre: {nombre}: {e}"
            )
            return render_template("agregar_producto.html")
    return render_template("agregar_producto.html")


@productos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
@roles_requeridos("admin")
def editar_producto_view(id):
    """Edita un producto existente con validaciones completas."""
    producto = obtener_producto_por_id(id)

    # Validar que el producto exista
    if not producto:
        flash("Producto no encontrado.", "error")
        return redirect(url_for("productos.productos_list"))

    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        precio_str = request.form["precio"].strip()
        stock_str = request.form["stock"].strip()
        categoria = request.form["categoria"].strip()
        codigo_barras = request.form["codigo_barras"].strip()

        # Validar que el nombre no esté vacío
        if not nombre:
            flash("El nombre del producto no puede estar vacío.", "error")
            return render_template("editar_producto.html", producto=producto)

        # Validar longitud del nombre (máximo 20 caracteres)
        if len(nombre) > 20:
            flash("El nombre del producto no puede exceder 20 caracteres.", "error")
            return render_template("editar_producto.html", producto=producto)

        # Validar que el código de barras no esté vacío
        if not codigo_barras:
            flash("El código de barras no puede estar vacío.", "error")
            return render_template("editar_producto.html", producto=producto)

        # Validar longitud del código de barras (máximo 50 caracteres)
        if len(codigo_barras) > 50:
            flash("El código de barras no puede exceder 50 caracteres.", "error")
            return render_template("editar_producto.html", producto=producto)

        # Validar que no exista otro producto con el mismo código (excepto el actual)
        productos_existentes = obtener_productos()
        codigo_duplicado = any(
            p["codigo_barras"] == codigo_barras and p["id"] != id
            for p in productos_existentes
        )

        if codigo_duplicado:
            flash(
                f"Error: Ya existe otro producto con el código de barras '{codigo_barras}'.",
                "error",
            )
            return render_template("editar_producto.html", producto=producto)

        # Validar precio
        try:
            precio = float(precio_str)
            if precio < 0:
                flash("El precio no puede ser negativo.", "error")
                return render_template("editar_producto.html", producto=producto)
            if precio == 0:
                flash("El precio debe ser mayor a 0.", "error")
                return render_template("editar_producto.html", producto=producto)
        except ValueError:
            flash("El precio debe ser un número válido.", "error")
            return render_template("editar_producto.html", producto=producto)

        # Validar stock
        try:
            stock = int(stock_str)
            if stock < 0:
                flash("El stock no puede ser negativo.", "error")
                return render_template("editar_producto.html", producto=producto)
        except ValueError:
            flash("El stock debe ser un número entero válido.", "error")
            return render_template("editar_producto.html", producto=producto)

        # Validar categoría (máximo 50 caracteres)
        if len(categoria) > 50:
            flash("La categoría no puede exceder 50 caracteres.", "error")
            return render_template("editar_producto.html", producto=producto)

        try:
            exito = editar_producto(
                id,
                nombre,
                precio,
                stock,
                categoria,
                codigo_barras,
            )

            if exito:
                mensaje = "Producto actualizado correctamente."
                flash(mensaje, "success")
                logger.info(
                    f"Producto editado - Usuario: {g.usuario['username']}, "
                    f"ID: {id}, Nombre: {nombre}, Código: {codigo_barras}"
                )
                return redirect(url_for("productos.productos_list"))
            else:
                flash("Error al actualizar el producto.", "error")
                logger.error(
                    f"Fallo al editar producto - Usuario: {g.usuario['username']}, "
                    f"ID: {id}, Nombre: {nombre}"
                )
                return render_template("editar_producto.html", producto=producto)
        except Exception as e:
            flash(f"Error al actualizar producto: {e}", "error")
            logger.error(
                f"Error al editar producto - Usuario: {g.usuario['username']}, "
                f"ID: {id}, Nombre: {nombre}: {e}"
            )
            return render_template("editar_producto.html", producto=producto)

    return render_template("editar_producto.html", producto=producto)


@productos_bp.route("/eliminar/<int:id>")
@login_required
@roles_requeridos("admin")
def eliminar_producto_view(id):
    producto = obtener_producto_por_id(id)
    if producto:
        nombre = producto["nombre"]
        eliminar_producto(id)
        logger.info(
            f"Producto eliminado - Usuario: {g.usuario['username']}, "
            f"ID: {id}, Nombre: {nombre}"
        )
    return redirect(url_for("productos.productos_list"))

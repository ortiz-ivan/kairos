"""
Rutas de administración para gestión de usuarios.

Proporciona endpoints para operaciones CRUD de usuarios con
autorización de administrador.
"""

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

from models_alchemy import User, db
from services.admin_service import (
    crear_usuario,
    editar_usuario,
    eliminar_usuario,
    obtener_usuarios,
    verificar_username_disponible,
)
from utils.decorators import admin_required
from utils.logging_config import get_logger

logger = get_logger(__name__)

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/usuarios", methods=["GET"])
@admin_required
def admin_usuarios():
    """Lista todos los usuarios de la aplicación."""
    logger.info(f"Admin {g.usuario['username']} accedió a listado de usuarios")
    usuarios = obtener_usuarios()
    return render_template("admin_usuarios.html", usuarios=usuarios)


@admin_bp.route("/usuarios/nuevo", methods=["GET", "POST"])
@admin_required
def admin_usuario_nuevo():
    """Crea un nuevo usuario con validaciones completas."""
    if request.method == "POST":
        nombre = request.form["nombre"].strip() if request.form.get("nombre") else ""
        username = (
            request.form["username"].strip() if request.form.get("username") else ""
        )
        password = request.form["password"] if request.form.get("password") else ""
        rol = request.form["rol"] if request.form.get("rol") else ""

        exito, mensaje = crear_usuario(
            nombre, username, password, rol, g.usuario["username"]
        )

        if exito:
            flash(mensaje, "success")
            return redirect(url_for("admin.admin_usuarios"))
        else:
            flash(mensaje, "error")
            return render_template(
                "admin_usuario_form.html",
                action="Crear",
                usuario=None,
                form_data={"nombre": nombre, "username": username, "rol": rol},
            )

    return render_template("admin_usuario_form.html", action="Crear", usuario=None)


@admin_bp.route("/usuarios/editar/<int:id>", methods=["GET", "POST"])
@admin_required
def admin_usuario_editar(id):
    """Edita un usuario existente con validaciones completas."""
    usuario_orm = db.session.get(User, id)
    if not usuario_orm:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("admin.admin_usuarios"))

    # Convertir a dict para el template
    usuario_dict = {
        "id": usuario_orm.id,
        "nombre": usuario_orm.nombre,
        "username": usuario_orm.username,
        "rol": usuario_orm.rol,
    }

    if request.method == "POST":
        nombre = request.form["nombre"].strip() if request.form.get("nombre") else ""
        username = (
            request.form["username"].strip() if request.form.get("username") else ""
        )
        password = request.form["password"] if request.form.get("password") else ""
        rol = request.form["rol"] if request.form.get("rol") else ""

        exito, mensaje, _ = editar_usuario(
            id, nombre, username, password, rol, g.usuario["username"]
        )

        if exito:
            flash(mensaje, "success")
            return redirect(url_for("admin.admin_usuarios"))
        else:
            flash(mensaje, "error")
            return render_template(
                "admin_usuario_form.html",
                action="Editar",
                usuario=usuario_dict,
                form_data={"nombre": nombre, "username": username, "rol": rol},
            )

    return render_template(
        "admin_usuario_form.html", action="Editar", usuario=usuario_dict
    )


@admin_bp.route("/usuarios/eliminar/<int:id>", methods=["POST"])
@admin_required
def admin_usuario_eliminar(id):
    """Elimina un usuario."""
    exito, mensaje = eliminar_usuario(id, g.usuario["username"])
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("admin.admin_usuarios"))


@admin_bp.route("/usuarios/verificar/<username>", methods=["GET"])
@admin_required
def verificar_username(username):
    """Verifica si un username está disponible (AJAX)."""
    disponible = verificar_username_disponible(username, g.usuario["username"])
    return jsonify({"disponible": disponible})

from flask import Blueprint, render_template, request, redirect, url_for, flash
from functools import wraps
from flask import g
from werkzeug.security import generate_password_hash, check_password_hash
from models_alchemy import db, User

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if g.usuario is None or g.usuario["rol"] != "admin":
            flash("Acceso denegado.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated


@admin_bp.route("/usuarios", methods=["GET"])
@admin_required
def admin_usuarios():
    """Lista todos los usuarios de la aplicación."""
    usuarios = User.query.all()
    # Convertir a dicts para compatibilidad con template
    usuarios_dicts = [
        {
            "id": u.id,
            "nombre": u.nombre,
            "username": u.username,
            "rol": u.rol,
        }
        for u in usuarios
    ]
    return render_template("admin_usuarios.html", usuarios=usuarios_dicts)


@admin_bp.route("/usuarios/nuevo", methods=["GET", "POST"])
@admin_required
def admin_usuario_nuevo():
    """Crea un nuevo usuario."""
    if request.method == "POST":
        nombre = request.form["nombre"]
        username = request.form["username"]
        password = request.form["password"]
        rol = request.form["rol"]

        try:
            # Hashear la contraseña
            hashed = generate_password_hash(password)

            # Crear usuario con ORM
            usuario = User(
                nombre=nombre,
                username=username,
                password=hashed,
                rol=rol,
            )
            db.session.add(usuario)
            db.session.commit()
            flash("Usuario creado correctamente.", "success")
            return redirect(url_for("admin.admin_usuarios"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al crear usuario: {e}", "error")

    return render_template("admin_usuario_form.html", action="Crear", usuario=None)


@admin_bp.route("/usuarios/editar/<int:id>", methods=["GET", "POST"])
@admin_required
def admin_usuario_editar(id):
    """Edita un usuario existente."""
    usuario_orm = User.query.get(id)
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
        nombre = request.form["nombre"]
        username = request.form["username"]
        password = request.form["password"]
        rol = request.form["rol"]

        try:
            # Actualizar campos
            usuario_orm.nombre = nombre
            usuario_orm.username = username
            usuario_orm.rol = rol

            # Si el campo de contraseña está vacío, no modificarla
            if password:
                usuario_orm.password = generate_password_hash(password)

            db.session.commit()
            flash("Usuario actualizado correctamente.", "success")
            return redirect(url_for("admin.admin_usuarios"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar usuario: {e}", "error")

    return render_template(
        "admin_usuario_form.html", action="Editar", usuario=usuario_dict
    )


@admin_bp.route("/usuarios/eliminar/<int:id>", methods=["POST"])
@admin_required
def admin_usuario_eliminar(id):
    """Elimina un usuario."""
    usuario = User.query.get(id)
    if not usuario:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("admin.admin_usuarios"))

    try:
        db.session.delete(usuario)
        db.session.commit()
        flash("Usuario eliminado correctamente.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar usuario: {e}", "error")

    return redirect(url_for("admin.admin_usuarios"))

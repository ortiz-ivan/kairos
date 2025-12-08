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
from werkzeug.security import generate_password_hash

from models_alchemy import User, db
from utils.logging_config import get_logger

logger = get_logger(__name__)

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
    from sqlalchemy import select

    logger.info(f"Admin {g.usuario['username']} accedió a listado de usuarios")
    stmt = select(User)
    usuarios = db.session.execute(stmt).scalars().all()
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
    """Crea un nuevo usuario con validaciones completas."""
    if request.method == "POST":
        nombre = request.form["nombre"].strip() if request.form.get("nombre") else ""
        username = (
            request.form["username"].strip() if request.form.get("username") else ""
        )
        password = request.form["password"] if request.form.get("password") else ""
        rol = request.form["rol"] if request.form.get("rol") else ""

        # Validaciones
        # 1. Nombre vacío
        if not nombre:
            flash("El nombre completo es requerido.", "error")
            return render_template(
                "admin_usuario_form.html",
                action="Crear",
                usuario=None,
                form_data={"nombre": nombre, "username": username, "rol": rol},
            )

        # 2. Nombre - longitud máxima
        if len(nombre) > 20:
            flash("El nombre no puede exceder 20 caracteres.", "error")
            return render_template(
                "admin_usuario_form.html",
                action="Crear",
                usuario=None,
                form_data={"nombre": nombre, "username": username, "rol": rol},
            )

        # 3. Username vacío
        if not username:
            flash("El nombre de usuario es requerido.", "error")
            return render_template(
                "admin_usuario_form.html",
                action="Crear",
                usuario=None,
                form_data={"nombre": nombre, "username": username, "rol": rol},
            )

        # 4. Username - longitud mínima
        if len(username) < 3:
            flash("El nombre de usuario debe tener al menos 3 caracteres.", "error")
            return render_template(
                "admin_usuario_form.html",
                action="Crear",
                usuario=None,
                form_data={"nombre": nombre, "username": username, "rol": rol},
            )

        # 5. Username - longitud máxima
        if len(username) > 20:
            flash("El nombre de usuario no puede exceder 20 caracteres.", "error")
            return render_template(
                "admin_usuario_form.html",
                action="Crear",
                usuario=None,
                form_data={"nombre": nombre, "username": username, "rol": rol},
            )

        # 6. Username - unicidad
        from sqlalchemy import select

        stmt = select(User).where(User.username == username)
        usuario_existente = db.session.execute(stmt).scalars().first()
        if usuario_existente:
            flash(
                f"El nombre de usuario '{username}' ya está en uso. Por favor, elige otro.",
                "error",
            )
            return render_template(
                "admin_usuario_form.html",
                action="Crear",
                usuario=None,
                form_data={"nombre": nombre, "username": username, "rol": rol},
            )

        # 7. Contraseña vacía
        if not password:
            flash("La contraseña es requerida.", "error")
            return render_template(
                "admin_usuario_form.html",
                action="Crear",
                usuario=None,
                form_data={"nombre": nombre, "username": username, "rol": rol},
            )

        # 8. Contraseña - longitud mínima
        if len(password) < 6:
            flash("La contraseña debe tener al menos 6 caracteres.", "error")
            return render_template(
                "admin_usuario_form.html",
                action="Crear",
                usuario=None,
                form_data={"nombre": nombre, "username": username, "rol": rol},
            )

        # 9. Rol válido
        if rol not in ["admin", "usuario"]:
            flash("El rol seleccionado no es válido.", "error")
            return render_template(
                "admin_usuario_form.html",
                action="Crear",
                usuario=None,
                form_data={"nombre": nombre, "username": username, "rol": rol},
            )

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
            mensaje = f"Usuario '{username}' creado correctamente."
            flash(mensaje, "success")
            logger.info(
                f"Usuario creado - Admin: {g.usuario['username']}, "
                f"Nuevo usuario: {username}, Rol: {rol}"
            )
            return redirect(url_for("admin.admin_usuarios"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al crear usuario: {e}", "error")
            logger.error(
                f"Error al crear usuario - Admin: {g.usuario['username']}, "
                f"Username: {username}: {e}"
            )
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
        username_original = usuario_orm.username

        # Validaciones
        # 1. Nombre vacío
        if not nombre:
            flash("El nombre completo es requerido.", "error")
            return render_template(
                "admin_usuario_form.html",
                action="Editar",
                usuario=usuario_dict,
                form_data={"nombre": nombre, "username": username, "rol": rol},
            )

        # 2. Nombre - longitud máxima
        if len(nombre) > 100:
            flash("El nombre no puede exceder 100 caracteres.", "error")
            return render_template(
                "admin_usuario_form.html",
                action="Editar",
                usuario=usuario_dict,
                form_data={"nombre": nombre, "username": username, "rol": rol},
            )

        # 3. Username vacío
        if not username:
            flash("El nombre de usuario es requerido.", "error")
            return render_template(
                "admin_usuario_form.html",
                action="Editar",
                usuario=usuario_dict,
                form_data={"nombre": nombre, "username": username, "rol": rol},
            )

        # 4. Username - longitud mínima
        if len(username) < 3:
            flash("El nombre de usuario debe tener al menos 3 caracteres.", "error")
            return render_template(
                "admin_usuario_form.html",
                action="Editar",
                usuario=usuario_dict,
                form_data={"nombre": nombre, "username": username, "rol": rol},
            )

        # 5. Username - longitud máxima
        if len(username) > 20:
            flash("El nombre de usuario no puede exceder 20 caracteres.", "error")
            return render_template(
                "admin_usuario_form.html",
                action="Editar",
                usuario=usuario_dict,
                form_data={"nombre": nombre, "username": username, "rol": rol},
            )

        # 6. Username - unicidad (permitir el mismo username actual)
        if username != username_original:
            from sqlalchemy import select

            stmt = select(User).where(User.username == username)
            usuario_existente = db.session.execute(stmt).scalars().first()
            if usuario_existente:
                flash(
                    f"El nombre de usuario '{username}' ya está en uso. Por favor, elige otro.",
                    "error",
                )
                return render_template(
                    "admin_usuario_form.html",
                    action="Editar",
                    usuario=usuario_dict,
                    form_data={"nombre": nombre, "username": username, "rol": rol},
                )

        # 7. Contraseña - validar si se intenta cambiar
        if password and len(password) < 6:
            flash("La contraseña debe tener al menos 6 caracteres.", "error")
            return render_template(
                "admin_usuario_form.html",
                action="Editar",
                usuario=usuario_dict,
                form_data={"nombre": nombre, "username": username, "rol": rol},
            )

        # 8. Rol válido
        if rol not in ["admin", "usuario"]:
            flash("El rol seleccionado no es válido.", "error")
            return render_template(
                "admin_usuario_form.html",
                action="Editar",
                usuario=usuario_dict,
                form_data={"nombre": nombre, "username": username, "rol": rol},
            )

        try:
            # Actualizar campos
            usuario_orm.nombre = nombre
            usuario_orm.username = username
            usuario_orm.rol = rol

            # Si el campo de contraseña está vacío, no modificarla
            if password:
                usuario_orm.password = generate_password_hash(password)

            db.session.commit()
            mensaje = f"Usuario '{username}' actualizado correctamente."
            flash(mensaje, "success")
            logger.info(
                f"Usuario editado - Admin: {g.usuario['username']}, "
                f"ID: {id}, Username: {username}, Rol: {rol}"
            )
            return redirect(url_for("admin.admin_usuarios"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar usuario: {e}", "error")
            logger.error(
                f"Error al editar usuario - Admin: {g.usuario['username']}, "
                f"ID: {id}, Username: {username}: {e}"
            )
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
    usuario = db.session.get(User, id)
    if not usuario:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("admin.admin_usuarios"))

    username = usuario.username
    try:
        db.session.delete(usuario)
        db.session.commit()
        flash("Usuario eliminado correctamente.", "success")
        logger.info(
            f"Usuario eliminado - Admin: {g.usuario['username']}, "
            f"ID: {id}, Username: {username}"
        )
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar usuario: {e}", "error")
        logger.error(
            f"Error al eliminar usuario - Admin: {g.usuario['username']}, "
            f"ID: {id}, Username: {username}: {e}"
        )

    return redirect(url_for("admin.admin_usuarios"))


@admin_bp.route("/usuarios/verificar/<username>", methods=["GET"])
@admin_required
def verificar_username(username):
    """Verifica si un username está disponible (AJAX)."""
    from sqlalchemy import select

    stmt = select(User).where(User.username == username)
    usuario = db.session.execute(stmt).scalars().first()
    disponible = usuario is None
    logger.debug(
        f"Verificación de username - Admin: {g.usuario['username']}, "
        f"Username: {username}, Disponible: {disponible}"
    )
    return jsonify({"disponible": disponible})

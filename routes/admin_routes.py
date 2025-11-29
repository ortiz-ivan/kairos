from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
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
        if len(nombre) > 100:
            flash("El nombre no puede exceder 100 caracteres.", "error")
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
        usuario_existente = User.query.filter_by(username=username).first()
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
            flash(f"Usuario '{username}' creado correctamente.", "success")
            return redirect(url_for("admin.admin_usuarios"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al crear usuario: {e}", "error")
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
            usuario_existente = User.query.filter_by(username=username).first()
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
            flash(f"Usuario '{username}' actualizado correctamente.", "success")
            return redirect(url_for("admin.admin_usuarios"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar usuario: {e}", "error")
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


@admin_bp.route("/usuarios/verificar/<username>", methods=["GET"])
@admin_required
def verificar_username(username):
    """Verifica si un username está disponible (AJAX)."""
    usuario = User.query.filter_by(username=username).first()
    return jsonify({"disponible": usuario is None})

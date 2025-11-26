from flask import Blueprint, render_template, request, redirect, url_for, flash
from functools import wraps
from flask import g
from database import get_connection
from werkzeug.security import generate_password_hash

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
    conn = get_connection()
    usuarios = conn.execute("SELECT id, nombre, username, rol FROM usuarios").fetchall()
    conn.close()
    return render_template("admin_usuarios.html", usuarios=usuarios)


@admin_bp.route("/usuarios/nuevo", methods=["GET", "POST"])
@admin_required
def admin_usuario_nuevo():
    if request.method == "POST":
        nombre = request.form["nombre"]
        username = request.form["username"]
        password = request.form["password"]
        rol = request.form["rol"]

        # Hashear la contraseña
        hashed = generate_password_hash(password)

        conn = get_connection()
        conn.execute(
            "INSERT INTO usuarios (nombre, username, password, rol) VALUES (?, ?, ?, ?)",
            (nombre, username, hashed, rol),
        )
        conn.commit()
        conn.close()
        flash("Usuario creado correctamente.", "success")
        return redirect(url_for("admin.admin_usuarios"))

    return render_template("admin_usuario_form.html", action="Crear", usuario=None)


@admin_bp.route("/usuarios/editar/<int:id>", methods=["GET", "POST"])
@admin_required
def admin_usuario_editar(id):
    conn = get_connection()
    usuario = conn.execute("SELECT * FROM usuarios WHERE id=?", (id,)).fetchone()
    if not usuario:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("admin.admin_usuarios"))

    if request.method == "POST":
        nombre = request.form["nombre"]
        username = request.form["username"]
        password = request.form["password"]
        rol = request.form["rol"]

        # Si el campo de contraseña está vacío, no modificarla
        if password:
            hashed = generate_password_hash(password)
            conn.execute(
                "UPDATE usuarios SET nombre=?, username=?, password=?, rol=? WHERE id=?",
                (nombre, username, hashed, rol, id),
            )
        else:
            conn.execute(
                "UPDATE usuarios SET nombre=?, username=?, rol=? WHERE id=?",
                (nombre, username, rol, id),
            )
        conn.commit()
        conn.close()
        flash("Usuario actualizado correctamente.", "success")
        return redirect(url_for("admin.admin_usuarios"))

    conn.close()
    return render_template("admin_usuario_form.html", action="Editar", usuario=usuario)


@admin_bp.route("/usuarios/eliminar/<int:id>", methods=["POST"])
@admin_required
def admin_usuario_eliminar(id):
    conn = get_connection()
    conn.execute("DELETE FROM usuarios WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("Usuario eliminado correctamente.", "success")
    return redirect(url_for("admin.admin_usuarios"))

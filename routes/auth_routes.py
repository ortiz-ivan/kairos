from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.usuario import verificar_usuario
from utils.logging_config import get_logger

logger = get_logger(__name__)
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        usuario = verificar_usuario(username, password)
        if usuario:
            session["user_id"] = usuario["id"]
            session["rol"] = usuario["rol"]
            logger.info(f"Login exitoso para usuario: {username}")
            flash("Bienvenido", "success")
            return redirect(url_for("ventas.agregar_venta_view"))
        else:
            logger.warning(f"Intento de login fallido para usuario: {username}")
            flash("Usuario o contraseña incorrectos", "error")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    username = session.get("user_id", "unknown")
    session.clear()
    logger.info(f"Logout para usuario ID: {username}")
    flash("Sesión cerrada", "success")
    return redirect(url_for("auth.login"))

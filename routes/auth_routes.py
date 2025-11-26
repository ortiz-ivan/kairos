from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.usuario import verificar_usuario

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        usuario = verificar_usuario(username, password)
        if usuario:
            session["user_id"] = usuario["id"]
            session["rol"] = usuario["rol"]
            flash("Bienvenido", "success")
            return redirect(url_for("ventas.agregar_venta_view"))
        else:
            flash("Usuario o contraseña incorrectos", "error")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada", "success")
    return redirect(url_for("auth.login"))

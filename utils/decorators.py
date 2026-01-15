"""
Decoradores comunes para la aplicación Kairos.

Proporciona decoradores para autenticación y autorización.
"""

from functools import wraps

from flask import flash, g, redirect, url_for


def login_required(f):
    """
    Decorador que requiere que el usuario esté autenticado.

    Redirige al login si no está autenticado.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        if g.usuario is None:
            flash("Debe iniciar sesión.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    """
    Decorador que requiere que el usuario sea administrador.

    Redirige al login si no está autenticado o no es admin.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        if g.usuario is None or g.usuario["rol"] != "admin":
            flash("Acceso denegado.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated


def roles_requeridos(*roles):
    """
    Decorador que requiere que el usuario tenga uno de los roles especificados.

    Args:
        *roles: Roles permitidos (ej: "admin", "usuario")

    Redirige a productos si no tiene permisos.
    """

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if g.usuario is None or g.usuario["rol"] not in roles:
                flash("No tiene permisos para acceder.", "error")
                return redirect(url_for("productos.productos_list"))
            return f(*args, **kwargs)

        return decorated

    return decorator

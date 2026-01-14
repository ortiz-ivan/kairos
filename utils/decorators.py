"""
Decoradores comunes para la aplicación Kairos.

Proporciona decoradores para autenticación y autorización.
"""

from functools import wraps

from flask import flash, g, redirect, url_for


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

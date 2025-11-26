import os
from flask import Flask, session, g, redirect, url_for, request
from models.usuario import obtener_usuario_por_id
from routes.auth_routes import auth_bp
from routes.ventas_routes import ventas_bp
from routes.productos_routes import productos_bp
from routes.inventario_routes import inventario_bp
from routes.admin_routes import admin_bp


def create_app():
    app = Flask(__name__)
    # Leer secret key desde variable de entorno; usar valor por defecto en desarrollo
    secret = os.environ.get("SECRET_KEY")
    is_production = (
        os.environ.get("FLASK_ENV") == "production"
        or os.environ.get("PRODUCTION") == "1"
    )
    if not secret:
        app.logger.warning(
            "No SECRET_KEY en entorno: usando clave por defecto (NO usar en producción)"
        )
        secret = "dev_secret_change_me"
    app.secret_key = secret

    # Cookies de sesión seguras
    app.config.update(
        SESSION_COOKIE_SECURE=True if is_production else False,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_HTTPONLY=True,
        PREFERRED_URL_SCHEME="https" if is_production else "http",
    )

    # Forzar HTTPS en producción (simple redirect). Si se usa proxy/reverse-proxy, asegúrate de
    # configurar X-Forwarded-Proto y ProxyFix en producción.
    @app.before_request
    def _enforce_https_in_production():
        if is_production:
            forwarded_proto = request.headers.get("X-Forwarded-Proto", "")
            secure = forwarded_proto == "https" or request.is_secure
            host = request.host.split(":")[0]
            if not secure and host not in ("127.0.0.1", "localhost"):
                return redirect(request.url.replace("http://", "https://"), code=301)

    # -------------------------
    # Cargar usuario logueado
    # -------------------------
    @app.before_request
    def cargar_usuario():
        g.usuario = None
        if "user_id" in session:
            g.usuario = obtener_usuario_por_id(session["user_id"])

    # -------------------------
    # Ruta raíz
    # -------------------------
    @app.route("/")
    def index():
        """Redirige según autenticación: si está logueado va a ventas, sino a login."""
        if g.usuario:
            return redirect(url_for("ventas.agregar_venta_view"))
        return redirect(url_for("auth.login"))

    # -------------------------
    # Registro de Blueprints
    # -------------------------
    app.register_blueprint(auth_bp)
    app.register_blueprint(ventas_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(inventario_bp)
    app.register_blueprint(admin_bp)

    return app


# Lanzar aplicación
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

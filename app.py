import os

from flask import Flask, g, redirect, request, session, url_for

from config import get_config
from models.usuario import obtener_usuario_por_id
from models_alchemy import db
from routes.admin_routes import admin_bp
from routes.auth_routes import auth_bp
from routes.inventario_routes import inventario_bp
from routes.productos_routes import productos_bp
from routes.registros_routes import registros_bp
from routes.ventas_routes import ventas_bp
from utils import register_error_handlers, setup_logging


def create_app():
    app = Flask(__name__)

    # -------------------------
    # Cargar configuración según entorno
    # -------------------------
    config = get_config(os.environ.get("FLASK_ENV"))
    app.config.from_object(config)
    is_production = config.ENV == "production"

    # -------------------------
    # Configurar SQLAlchemy
    # -------------------------
    db.init_app(app)

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
    # Health Check
    # -------------------------
    @app.route("/health")
    def health():
        """Endpoint para Docker healthcheck y load balancers."""
        try:
            # Verificar conexión a base de datos
            db.session.execute("SELECT 1")
            return {"status": "ok", "database": "connected"}, 200
        except Exception as e:
            app.logger.error(f"Health check failed: {e}")
            return {"status": "error", "database": "disconnected"}, 503

    # -------------------------
    # Configurar Logging y Error Handlers
    # -------------------------
    logger = setup_logging(app)
    logger.info("=== Iniciando aplicación Kairos ===")
    register_error_handlers(app)

    # -------------------------
    # Registro de Blueprints
    # -------------------------
    app.register_blueprint(auth_bp)
    app.register_blueprint(registros_bp)
    app.register_blueprint(ventas_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(inventario_bp)
    app.register_blueprint(admin_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

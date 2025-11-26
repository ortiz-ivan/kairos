from flask import Flask, session, g, redirect, url_for
from models.usuario import obtener_usuario_por_id
from routes.auth_routes import auth_bp
from routes.ventas_routes import ventas_bp
from routes.productos_routes import productos_bp
from routes.inventario_routes import inventario_bp
from routes.admin_routes import admin_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = "clave_secreta_para_flash"

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

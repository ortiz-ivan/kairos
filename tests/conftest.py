import os
import sys

import pytest
from flask import Flask

# Asegurar que el proyecto esté en sys.path para imports en tests
sys.path.insert(0, os.getcwd())

# Importar después de insertar en sys.path
from models_alchemy import db as _db  # noqa: E402
from routes.admin_routes import admin_bp  # noqa: E402
from routes.auth_routes import auth_bp  # noqa: E402
from routes.inventario_routes import inventario_bp  # noqa: E402
from routes.productos_routes import productos_bp  # noqa: E402
from routes.ventas_routes import ventas_bp  # noqa: E402
from utils.error_handlers import register_error_handlers  # noqa: E402
from utils.logging_config import setup_logging  # noqa: E402


def create_test_app(tmp_path):
    """Crea una app de Flask para testing con una DB SQLite temporal.

    Registra blueprints, handlers y configura logging para replicar
    el entorno mínimo necesario en tests.
    """
    app = Flask(
        __name__,
        template_folder=os.path.join(os.getcwd(), "templates"),
        static_folder=os.path.join(os.getcwd(), "static"),
    )

    db_file = tmp_path / "test_kairos.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_file}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "test-secret"

    # Configurar logging (crea logs/)
    try:
        setup_logging(app)
    except Exception:
        # Si falla el setup de logging no debe romper los tests
        pass

    # Registrar blueprints y manejadores de error
    app.register_blueprint(auth_bp)
    app.register_blueprint(ventas_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(inventario_bp)
    app.register_blueprint(admin_bp)

    register_error_handlers(app)

    _db.init_app(app)
    with app.app_context():
        _db.create_all()

    return app


@pytest.fixture
def app(tmp_path):
    app = create_test_app(tmp_path)
    yield app
    # Teardown: intentar eliminar archivo de DB temporal
    try:
        db_path = tmp_path / "test_kairos.db"
        if db_path.exists():
            os.remove(str(db_path))
    except Exception:
        pass


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    """Fixture que provee el objeto `db` y limpia la sesión después del test."""
    from models_alchemy import db as _db2

    with app.app_context():
        yield _db2
        try:
            _db2.session.remove()
            _db2.drop_all()
        except Exception:
            pass

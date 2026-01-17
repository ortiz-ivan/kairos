"""
Configuración de la aplicación Kairos.

Proporciona classes de configuración para diferentes ambientes:
- DevelopmentConfig: desarrollo local (SQLite, debug=True)
- ProductionConfig: producción (Postgres, debug=False, secure cookies)
- TestingConfig: testing (SQLite in-memory, testing mode)

Las variables de entorno se leen con os.environ.get() con valores por defecto.

IMPORTANTE: Para que la persistencia de datos funcione en el ejecutable PyInstaller,
la URI de la BD se evalúa dinámicamente en tiempo de ejecución, no en tiempo
de compilación.
"""

import os
from datetime import timedelta


def get_database_uri():
    """Obtiene la URI de la BD de forma dinámica en tiempo de ejecución.

    Esto es crítico para que PyInstaller funcione correctamente con datos persistentes.
    """
    # Primero revisar si hay DATABASE_URL en el entorno (producción)
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        return database_url

    # Luego revisar si estamos en ejecutable compilado (KAIROS_DATA_DIR existente)
    kairos_data_dir = os.environ.get("KAIROS_DATA_DIR")
    if kairos_data_dir:
        db_path = os.path.join(kairos_data_dir, "kairos.db")
        return f"sqlite:///{db_path}"

    # Por defecto, usar kairos.db en el directorio del proyecto (desarrollo)
    base_dir = os.path.dirname(__file__)
    db_path = os.path.join(base_dir, "kairos.db")
    return f"sqlite:///{db_path}"


class Config:
    """Configuración base compartida por todos los ambientes."""

    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-key-change-in-production"
    PREFERRED_URL_SCHEME = os.environ.get("PREFERRED_URL_SCHEME", "http")

    # SQLAlchemy - Evaluar dinámicamente en tiempo de ejecución
    SQLALCHEMY_DATABASE_URI = None  # Se establecerá en __init__
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Logging
    LOG_LEVEL = "DEBUG"

    def __init__(self):
        """Inicializa la configuración y establece la BD de forma dinámica."""
        # Evaluar SQLALCHEMY_DATABASE_URI en tiempo de ejecución
        self.SQLALCHEMY_DATABASE_URI = get_database_uri()


class DevelopmentConfig(Config):
    """Configuración para desarrollo local."""

    ENV = "development"
    DEBUG = True
    TESTING = False

    # Session
    SESSION_COOKIE_SECURE = False

    # Logging
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Configuración para producción."""

    ENV = "production"
    DEBUG = False
    TESTING = False

    # Base de datos Postgres (requerida en producción)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "postgresql://user:password@db:5432/kairos"
    )

    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL environment variable must be set in production")

    # Session segura
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Strict"

    # Logging
    LOG_LEVEL = "INFO"


class TestingConfig(Config):
    """Configuración para testing."""

    ENV = "testing"
    DEBUG = True
    TESTING = True

    # SQLite en memoria para tests
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    # Session
    SESSION_COOKIE_SECURE = False

    # Logging
    LOG_LEVEL = "WARNING"


def get_config(env=None):
    """Obtiene la configuración según el ambiente.

    Args:
        env: nombre del ambiente ("development", "production", "testing")
             Si es None, lee FLASK_ENV del environment.

    Returns:
        Instancia de la clase de configuración apropiada.
    """
    if env is None:
        env = os.environ.get("FLASK_ENV", "development")

    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }

    config_class = config_map.get(env, DevelopmentConfig)
    return config_class()  # ← Retornar instancia, no clase

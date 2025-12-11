"""
Configuración de la aplicación Kairos.

Proporciona classes de configuración para diferentes ambientes:
- DevelopmentConfig: desarrollo local (SQLite, debug=True)
- ProductionConfig: producción (Postgres, debug=False, secure cookies)
- TestingConfig: testing (SQLite in-memory, testing mode)

Las variables de entorno se leen con os.environ.get() con valores por defecto.
"""

import os
from datetime import timedelta


class Config:
    """Configuración base compartida por todos los ambientes."""

    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-key-change-in-production"
    PREFERRED_URL_SCHEME = os.environ.get("PREFERRED_URL_SCHEME", "http")

    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Logging
    LOG_LEVEL = "DEBUG"


class DevelopmentConfig(Config):
    """Configuración para desarrollo local."""

    ENV = "development"
    DEBUG = True
    TESTING = False

    # SQLite local
    base_dir = os.path.dirname(__file__)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(base_dir, 'kairos.db')}"
    )

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
    """Obtiene la clase de configuración según el ambiente.

    Args:
        env: nombre del ambiente ("development", "production", "testing")
             Si es None, lee FLASK_ENV del environment.

    Returns:
        Clase de configuración apropiada.
    """
    if env is None:
        env = os.environ.get("FLASK_ENV", "development")

    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }

    return config_map.get(env, DevelopmentConfig)

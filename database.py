"""
Módulo de configuración y utilidades de base de datos.

NOTA: La definición de esquema está centralizada en models_alchemy.py (modelos ORM).
Este módulo solo proporciona funciones de conexión para compatibilidad con código legacy.
A futuro, migrar completamente a ORM desde models/.
"""

import sqlite3

DB_NAME = "kairos.db"


def get_connection():
    """Devuelve una conexión raw a SQLite (para código legacy).

    Para código nuevo, usa los modelos ORM en models_alchemy.py directamente.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    """Wrapper para compatibilidad: equivalente a get_connection()."""
    return get_connection()

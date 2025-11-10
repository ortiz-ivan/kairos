import sqlite3
from werkzeug.security import generate_password_hash

DB_NAME = "kairos.db"


def get_connection():
    """Crea y devuelve una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Para acceder a las columnas por nombre
    return conn


def get_db():
    """Compat wrapper: función usada en algunos módulos que esperan get_db().

    Devuelve una conexión a la base de datos (equivalente a get_connection).
    """
    return get_connection()


def init_db():
    """Crea las tablas necesarias si no existen."""
    conn = get_connection()
    cursor = conn.cursor()

    # Tabla productos
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio INTEGER NOT NULL,
            stock INTEGER NOT NULL,
            categoria TEXT,
            codigo_barras TEXT UNIQUE
        )
        """
    )

    # Tabla ventas
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            total REAL NOT NULL
        )
        """
    )

    # Tabla detalle de ventas
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS detalle_ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venta_id INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY(venta_id) REFERENCES ventas(id),
            FOREIGN KEY(producto_id) REFERENCES productos(id)
        )
        """
    )

    # Tabla usuarios
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol TEXT NOT NULL
        )
        """
    )

    conn.commit()

    # Crear usuario admin inicial si no existe
    cursor.execute("SELECT * FROM usuarios WHERE username = ?", ("admin",))
    if not cursor.fetchone():
        hashed_password = generate_password_hash("admin123")
        cursor.execute(
            "INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)",
            ("admin", hashed_password, "admin"),
        )
        conn.commit()

    conn.close()


# Inicializa la base de datos al importar este módulo
init_db()

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
            ,
                usuario_id INTEGER NOT NULL,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
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
            nombre TEXT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol TEXT NOT NULL
        )
        """
    )

    conn.commit()

    # Verificar si la columna 'nombre' existe en usuarios, sino crearla
    cursor.execute("PRAGMA table_info(usuarios)")
    columns = [column[1] for column in cursor.fetchall()]
    if "nombre" not in columns:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN nombre TEXT")
        print("Columna 'nombre' agregada a la tabla usuarios")
        conn.commit()

    # Verificar si la columna 'usuario_id' existe en ventas, sino crearla
    cursor.execute("PRAGMA table_info(ventas)")
    columns = [column[1] for column in cursor.fetchall()]
    if "usuario_id" not in columns:
        cursor.execute("ALTER TABLE ventas ADD COLUMN usuario_id INTEGER")
        print("Columna 'usuario_id' agregada a la tabla ventas")
        conn.commit()

    # Crear usuario admin inicial si no existe
    cursor.execute("SELECT * FROM usuarios WHERE username = ?", ("admin",))
    if not cursor.fetchone():
        hashed_password = generate_password_hash("admin123")
        cursor.execute(
            "INSERT INTO usuarios (nombre, username, password, rol) VALUES (?, ?, ?, ?)",
            ("Administrador", "admin", hashed_password, "admin"),
        )
        conn.commit()

    conn.close()


# Inicializa la base de datos al importar este módulo
init_db()

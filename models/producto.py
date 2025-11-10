from database import get_connection

# ------------------------------
# FUNCIONES CRUD PARA PRODUCTOS
# ------------------------------


def agregar_producto(nombre, precio, stock, categoria, codigo_barras):
    """Agrega un nuevo producto a la base de datos."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO productos (nombre, precio, stock, categoria, codigo_barras)
            VALUES (?, ?, ?, ?, ?)
            """,
            (nombre, precio, stock, categoria, codigo_barras),
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al agregar producto: {e}")
        return False
    finally:
        conn.close()


def obtener_productos():
    """Devuelve todos los productos como lista de diccionarios."""
    conn = get_connection()
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos


def obtener_producto_por_id(producto_id, conn=None):
    """Devuelve un producto por su ID."""
    should_close = False
    if conn is None:
        conn = get_connection()
        should_close = True

    original_factory = conn.row_factory
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
    producto = cursor.fetchone()

    # Restaurar el row_factory original
    conn.row_factory = original_factory

    if should_close:
        conn.close()
    return producto


def obtener_producto_por_codigo(codigo_barras):
    """Devuelve un producto por su código de barras."""
    conn = get_connection()
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE codigo_barras = ?", (codigo_barras,))
    producto = cursor.fetchone()
    conn.close()

    # 🔍 Validar y limpiar datos antes de devolverlos
    if producto:
        return {
            "id": producto.get("id"),
            "nombre": producto.get("nombre", "").strip(),
            "precio": float(producto.get("precio", 0)),
            "stock": int(producto.get("stock", 0)),
            "categoria": producto.get("categoria", ""),
            "codigo_barras": producto.get("codigo_barras", ""),
        }
    return None


def editar_producto(
    producto_id, nombre, precio, stock, categoria, codigo_barras, conn=None
):
    """Edita un producto existente."""
    should_close = False
    if conn is None:
        conn = get_connection()
        should_close = True

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE productos
            SET nombre = ?, precio = ?, stock = ?, categoria = ?, codigo_barras = ?
            WHERE id = ?
            """,
            (nombre, precio, stock, categoria, codigo_barras, producto_id),
        )
        if should_close:
            conn.commit()
        return True
    except Exception as e:
        print(f"Error al editar producto: {e}")
        return False
    finally:
        if should_close:
            conn.close()


def eliminar_producto(producto_id):
    """Elimina un producto por su ID."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al eliminar producto: {e}")
        return False
    finally:
        conn.close()


# ------------------------------
# FUNCIONES AUXILIARES
# ------------------------------


def dict_factory(cursor, row):
    """Convierte los resultados del cursor en diccionarios."""
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

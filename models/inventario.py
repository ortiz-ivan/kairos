from database import get_connection


def obtener_inventario():
    """Devuelve todos los productos con su stock actual."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos ORDER BY nombre")
    productos = cursor.fetchall()
    conn.close()
    return productos


def obtener_stock_bajo(limite=5):
    """Devuelve productos con stock menor o igual al límite."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM productos WHERE stock <= ? ORDER BY nombre", (limite,)
    )
    productos = cursor.fetchall()
    conn.close()
    return productos

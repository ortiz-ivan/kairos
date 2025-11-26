from database import get_connection
from models.producto import obtener_producto_por_id, editar_producto
from datetime import datetime

# ------------------------------
# FUNCIONES DE VENTAS
# ------------------------------


def registrar_venta(productos_cantidades, usuario_id=None):
    """
    Registra una venta.
    productos_cantidades: lista de dicts [{"id": 1, "cantidad": 2}, ...]
    usuario_id: ID del usuario que realiza la venta
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        total = 0

        # Calcular total general de la venta
        for item in productos_cantidades:
            producto_id = item["id"]
            cantidad = item["cantidad"]

            producto = obtener_producto_por_id(producto_id, conn=conn)
            if not producto:
                raise ValueError(f"Producto con ID {producto_id} no encontrado.")

            if producto["stock"] < cantidad:
                raise ValueError(
                    f"Stock insuficiente para '{producto['nombre']}'. Disponible: {producto['stock']}"
                )

            subtotal = producto["precio"] * cantidad
            total += subtotal

        # Insertar venta
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO ventas (fecha, total, usuario_id) VALUES (?, ?, ?)",
            (fecha, total, usuario_id),
        )
        venta_id = cursor.lastrowid

        # Insertar detalles y actualizar stock
        for item in productos_cantidades:
            producto_id = item["id"]
            cantidad = item["cantidad"]
            producto = obtener_producto_por_id(producto_id, conn=conn)
            subtotal = producto["precio"] * cantidad

            # Insertar detalle
            cursor.execute(
                """
                INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, subtotal)
                VALUES (?, ?, ?, ?)
                """,
                (venta_id, producto_id, cantidad, subtotal),
            )

            # Actualizar stock sin que baje de 0
            nuevo_stock = max(producto["stock"] - cantidad, 0)
            # Actualizar el stock del producto usando la misma conexión
            resultado = editar_producto(
                producto_id,
                producto["nombre"],
                producto["precio"],
                nuevo_stock,
                producto["categoria"],
                producto["codigo_barras"],
                conn=conn,
            )

            if not resultado:
                raise Exception(
                    f"Error al actualizar el stock del producto {producto['nombre']}"
                )

        conn.commit()
        print("Venta registrada y stock actualizado correctamente.")
        return True

    except Exception as e:
        conn.rollback()
        print(f"Error al registrar venta: {e}")
        return False

    finally:
        conn.close()


def obtener_ventas():
    """Devuelve todas las ventas."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT v.id, v.fecha, v.total, v.usuario_id, u.username
        FROM ventas v
        LEFT JOIN usuarios u ON v.usuario_id = u.id
        ORDER BY v.fecha DESC
    """
    )
    ventas = cursor.fetchall()
    conn.close()
    return ventas


def obtener_detalle_venta(venta_id):
    """Devuelve los productos de una venta específica."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT dv.id, p.nombre, dv.cantidad, dv.subtotal
        FROM detalle_ventas dv
        JOIN productos p ON dv.producto_id = p.id
        WHERE dv.venta_id = ?
        """,
        (venta_id,),
    )
    detalles = cursor.fetchall()
    conn.close()
    return detalles

"""Modelo de Venta con SQLAlchemy ORM."""

from models_alchemy import db, Venta, DetalleVenta, Producto, User
from models.producto import obtener_producto_por_id
from datetime import datetime


def registrar_venta(productos_cantidades, usuario_id=None):
    """Registra una venta con sus detalles y actualiza stock.

    Args:
        productos_cantidades: lista de dicts [{"id": 1, "cantidad": 2}, ...]
        usuario_id: ID del usuario que realiza la venta
    """
    try:
        total = 0

        # Validar y calcular total
        for item in productos_cantidades:
            producto_id = item["id"]
            cantidad = item["cantidad"]
            producto = obtener_producto_por_id(producto_id)

            if not producto:
                raise ValueError(f"Producto con ID {producto_id} no encontrado.")

            if producto["stock"] < cantidad:
                raise ValueError(
                    f"Stock insuficiente para '{producto['nombre']}'. Disponible: {producto['stock']}"
                )

            total += producto["precio"] * cantidad

        # Crear venta
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        venta = Venta(fecha=fecha, total=total, usuario_id=usuario_id)
        db.session.add(venta)
        db.session.flush()  # Obtener el ID de la venta
        venta_id = venta.id

        # Insertar detalles y actualizar stock
        for item in productos_cantidades:
            producto_id = item["id"]
            cantidad = item["cantidad"]
            producto = obtener_producto_por_id(producto_id)
            subtotal = producto["precio"] * cantidad

            # Crear detalle de venta
            detalle = DetalleVenta(
                venta_id=venta_id,
                producto_id=producto_id,
                cantidad=cantidad,
                subtotal=subtotal,
            )
            db.session.add(detalle)

            # Actualizar stock del producto
            prod_obj = Producto.query.get(producto_id)
            if prod_obj:
                prod_obj.stock = max(prod_obj.stock - cantidad, 0)

        db.session.commit()
        print("Venta registrada y stock actualizado correctamente.")
        return True

    except Exception as e:
        db.session.rollback()
        print(f"Error al registrar venta: {e}")
        return False


def obtener_ventas():
    """Devuelve todas las ventas con información del usuario."""
    ventas = (
        db.session.query(Venta, User.username)
        .outerjoin(User, Venta.usuario_id == User.id)
        .order_by(Venta.fecha.desc())
        .all()
    )

    return [
        {
            "id": v[0].id,
            "fecha": v[0].fecha,
            "total": v[0].total,
            "usuario_id": v[0].usuario_id,
            "username": v[1] or "-",
        }
        for v in ventas
    ]


def obtener_detalle_venta(venta_id):
    """Devuelve los productos de una venta específica."""
    detalles = (
        db.session.query(DetalleVenta, Producto.nombre)
        .join(Producto, DetalleVenta.producto_id == Producto.id)
        .filter(DetalleVenta.venta_id == venta_id)
        .all()
    )

    return [
        {
            "id": d[0].id,
            "nombre": d[1],
            "cantidad": d[0].cantidad,
            "subtotal": d[0].subtotal,
        }
        for d in detalles
    ]

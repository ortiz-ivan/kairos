"""Modelo de Venta con SQLAlchemy ORM."""

from models_alchemy import db, Venta, DetalleVenta, Producto, User
from models.producto import obtener_producto_por_id
from datetime import datetime


def registrar_venta(productos_cantidades, usuario_id=None):
    """Registra una venta con sus detalles y actualiza stock.

    Args:
        productos_cantidades: lista de dicts [{"id": 1, "cantidad": 2}, ...]
        usuario_id: ID del usuario que realiza la venta

    Returns:
        tuple: (exito: bool, mensaje: str)
    """
    try:
        # Validación adicional: lista no vacía
        if not productos_cantidades or len(productos_cantidades) == 0:
            return False, "La venta debe contener al menos un producto."

        total = 0

        # Validar y calcular total
        for item in productos_cantidades:
            try:
                producto_id = int(item["id"])
                cantidad = int(item["cantidad"])
            except (KeyError, ValueError, TypeError):
                return False, "Estructura de datos de productos inválida."

            # Validar cantidad
            if cantidad <= 0:
                return False, "La cantidad de cada producto debe ser mayor a 0."

            producto = obtener_producto_por_id(producto_id)

            if not producto:
                return False, f"Producto con ID {producto_id} no encontrado."

            if producto["stock"] < cantidad:
                return False, (
                    f"Stock insuficiente para '{producto['nombre']}'. "
                    f"Disponible: {producto['stock']}, solicitado: {cantidad}"
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
            producto_id = int(item["id"])
            cantidad = int(item["cantidad"])
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
            prod_obj = db.session.get(Producto, producto_id)
            if prod_obj:
                prod_obj.stock = max(prod_obj.stock - cantidad, 0)

        db.session.commit()
        return True, "Venta registrada exitosamente."

    except Exception as e:
        db.session.rollback()
        return False, str(e)


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

"""Modelo de Venta con SQLAlchemy ORM."""

from datetime import datetime

from models.producto import obtener_producto_por_id
from models_alchemy import (
    DetalleVenta,
    Pendiente,
    PendienteDetalle,
    Producto,
    User,
    Venta,
    db,
)


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


def _pendientes_file_path():
    # no longer used (pendientes now persisted in DB)
    return None


def guardar_pendiente(productos_cantidades, usuario_id=None):
    """Guarda una venta como pendiente en archivo JSON (no modifica stock)."""
    try:
        # Calcular total (tomando precio actual de productos)
        total = 0
        detalles_data = []
        for item in productos_cantidades:
            producto_id = int(item["id"])
            cantidad = int(item["cantidad"])
            producto = obtener_producto_por_id(producto_id)
            precio = producto["precio"] if producto else 0
            subtotal = precio * cantidad
            total += subtotal
            detalles_data.append(
                {
                    "producto_id": producto_id,
                    "nombre": producto["nombre"] if producto else "-",
                    "cantidad": cantidad,
                    "precio": precio,
                    "subtotal": subtotal,
                }
            )

        # Persistir pendiente y sus detalles en la base de datos
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pendiente = Pendiente(fecha=fecha, usuario_id=usuario_id, total=total)
        db.session.add(pendiente)
        db.session.flush()  # obtener id
        for d in detalles_data:
            pd = PendienteDetalle(
                pendiente_id=pendiente.id,
                producto_id=d.get("producto_id"),
                nombre=d.get("nombre"),
                cantidad=d.get("cantidad"),
                precio=d.get("precio"),
                subtotal=d.get("subtotal"),
            )
            db.session.add(pd)

        db.session.commit()
        return True, "Pendiente guardado exitosamente."
    except Exception as e:
        db.session.rollback()
        return False, str(e)


def obtener_pendientes():
    # Obtener pendientes desde la base de datos
    try:
        pendientes = db.session.query(Pendiente).order_by(Pendiente.id.desc()).all()
        resultados = []
        for p in pendientes:
            detalles = (
                db.session.query(PendienteDetalle).filter_by(pendiente_id=p.id).all()
            )
            detalles_list = [
                {
                    "id": d.producto_id,
                    "nombre": d.nombre,
                    "cantidad": d.cantidad,
                    "precio": d.precio,
                    "subtotal": d.subtotal,
                }
                for d in detalles
            ]
            resultados.append(
                {
                    "id": p.id,
                    "fecha": p.fecha,
                    "usuario_id": p.usuario_id,
                    "total": p.total,
                    "detalles": detalles_list,
                }
            )
        return resultados
    except Exception:
        return []


def obtener_pendiente_por_id(pendiente_id):
    try:
        p = db.session.get(Pendiente, int(pendiente_id))
        if not p:
            return None
        detalles = db.session.query(PendienteDetalle).filter_by(pendiente_id=p.id).all()
        detalles_list = [
            {
                "id": d.producto_id,
                "nombre": d.nombre,
                "cantidad": d.cantidad,
                "precio": d.precio,
                "subtotal": d.subtotal,
            }
            for d in detalles
        ]
        return {
            "id": p.id,
            "fecha": p.fecha,
            "usuario_id": p.usuario_id,
            "total": p.total,
            "detalles": detalles_list,
        }
    except Exception:
        return None


def obtener_ventas():
    """Devuelve todas las ventas con información del usuario."""
    from sqlalchemy import desc, select

    stmt = (
        select(Venta, User.username)
        .outerjoin(User, Venta.usuario_id == User.id)
        .order_by(desc(Venta.fecha))
    )
    ventas = db.session.execute(stmt).all()

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
    from sqlalchemy import select

    stmt = (
        select(DetalleVenta, Producto.nombre)
        .join(Producto, DetalleVenta.producto_id == Producto.id)
        .where(DetalleVenta.venta_id == venta_id)
    )
    detalles = db.session.execute(stmt).all()

    return [
        {
            "id": d[0].id,
            "nombre": d[1],
            "cantidad": d[0].cantidad,
            "subtotal": d[0].subtotal,
        }
        for d in detalles
    ]


def eliminar_pendiente(pendiente_id):
    """Elimina un pendiente por ID del archivo JSON.

    Retorna: (True, mensaje) o (False, mensaje)
    """
    try:
        p = db.session.get(Pendiente, int(pendiente_id))
        if not p:
            return False, "Pendiente no encontrado."

        # Eliminar detalles y el pendiente
        db.session.query(PendienteDetalle).filter_by(pendiente_id=p.id).delete()
        db.session.delete(p)
        db.session.commit()
        return True, "Pendiente eliminado correctamente."
    except Exception as e:
        db.session.rollback()
        return False, str(e)

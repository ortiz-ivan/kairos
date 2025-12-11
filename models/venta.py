"""Modelo de Venta con SQLAlchemy ORM."""

import json
import os
from datetime import datetime

from models.producto import obtener_producto_por_id
from models_alchemy import DetalleVenta, Producto, User, Venta, db


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
    base = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base, "pendientes.json")


def guardar_pendiente(productos_cantidades, usuario_id=None):
    """Guarda una venta como pendiente en archivo JSON (no modifica stock)."""
    try:
        path = _pendientes_file_path()
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as fh:
                json.dump([], fh, ensure_ascii=False)

        with open(path, "r", encoding="utf-8") as fh:
            pendientes = json.load(fh)

        # Calcular total aproximado (tomando precio actual de productos)
        total = 0
        detalles = []
        for item in productos_cantidades:
            producto_id = int(item["id"])
            cantidad = int(item["cantidad"])
            producto = obtener_producto_por_id(producto_id)
            precio = producto["precio"] if producto else 0
            subtotal = precio * cantidad
            total += subtotal
            detalles.append(
                {
                    "id": producto_id,
                    "nombre": producto["nombre"] if producto else "-",
                    "cantidad": cantidad,
                    "precio": precio,
                    "subtotal": subtotal,
                }
            )

        pendiente = {
            "id": int(datetime.utcnow().timestamp()),
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "usuario_id": usuario_id,
            "total": total,
            "detalles": detalles,
        }

        pendientes.append(pendiente)

        with open(path, "w", encoding="utf-8") as fh:
            json.dump(pendientes, fh, ensure_ascii=False, indent=2)

        return True, "Pendiente guardado exitosamente."
    except Exception as e:
        return False, str(e)


def obtener_pendientes():
    path = _pendientes_file_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return []


def obtener_pendiente_por_id(pendiente_id):
    pendientes = obtener_pendientes()
    for p in pendientes:
        if str(p.get("id")) == str(pendiente_id):
            return p
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
        path = _pendientes_file_path()
        if not os.path.exists(path):
            return False, "No hay pendientes guardados."

        with open(path, "r", encoding="utf-8") as fh:
            pendientes = json.load(fh)

        nuevos = [p for p in pendientes if str(p.get("id")) != str(pendiente_id)]

        if len(nuevos) == len(pendientes):
            return False, "Pendiente no encontrado."

        with open(path, "w", encoding="utf-8") as fh:
            json.dump(nuevos, fh, ensure_ascii=False, indent=2)

        return True, "Pendiente eliminado correctamente."
    except Exception as e:
        return False, str(e)

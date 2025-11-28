"""Modelo de Inventario con SQLAlchemy ORM."""

from models_alchemy import db, Producto


def obtener_inventario():
    """Devuelve todos los productos con su stock actual."""
    productos = Producto.query.order_by(Producto.nombre).all()
    return [
        {
            "id": p.id,
            "nombre": p.nombre,
            "precio": p.precio,
            "stock": p.stock,
            "categoria": p.categoria,
            "codigo_barras": p.codigo_barras,
        }
        for p in productos
    ]


def obtener_stock_bajo(limite=5):
    """Devuelve productos con stock menor o igual al límite."""
    productos = (
        Producto.query.filter(Producto.stock <= limite).order_by(Producto.nombre).all()
    )
    return [
        {
            "id": p.id,
            "nombre": p.nombre,
            "precio": p.precio,
            "stock": p.stock,
            "categoria": p.categoria,
            "codigo_barras": p.codigo_barras,
        }
        for p in productos
    ]

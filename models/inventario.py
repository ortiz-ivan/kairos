"""Modelo de Inventario con SQLAlchemy ORM."""

from models_alchemy import Producto, db


def obtener_inventario():
    """Devuelve todos los productos con su stock actual."""
    from sqlalchemy import asc, select

    stmt = select(Producto).order_by(asc(Producto.nombre))
    productos = db.session.execute(stmt).scalars().all()
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
    from sqlalchemy import asc, select

    stmt = (
        select(Producto).where(Producto.stock <= limite).order_by(asc(Producto.nombre))
    )
    productos = db.session.execute(stmt).scalars().all()
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

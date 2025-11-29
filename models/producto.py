"""Modelo de Producto con SQLAlchemy ORM."""

from models_alchemy import db, Producto


def agregar_producto(nombre, precio, stock, categoria, codigo_barras):
    """Agrega un nuevo producto a la base de datos."""
    try:
        producto = Producto(
            nombre=nombre,
            precio=precio,
            stock=stock,
            categoria=categoria,
            codigo_barras=codigo_barras,
        )
        db.session.add(producto)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error al agregar producto: {e}")
        db.session.rollback()
        return False


def obtener_productos():
    """Devuelve todos los productos como lista de diccionarios."""
    productos = Producto.query.all()
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


def obtener_producto_por_id(producto_id, conn=None):
    """Devuelve un producto por su ID. Parámetro 'conn' ignorado (compatibilidad legacy)."""
    producto = db.session.get(Producto, producto_id)
    if producto:
        return {
            "id": producto.id,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "stock": producto.stock,
            "categoria": producto.categoria,
            "codigo_barras": producto.codigo_barras,
        }
    return None


def obtener_producto_por_codigo(codigo_barras):
    """Devuelve un producto por su código de barras."""
    producto = Producto.query.filter_by(codigo_barras=codigo_barras).first()
    if producto:
        return {
            "id": producto.id,
            "nombre": producto.nombre.strip(),
            "precio": float(producto.precio),
            "stock": int(producto.stock),
            "categoria": producto.categoria or "",
            "codigo_barras": producto.codigo_barras or "",
        }
    return None


def editar_producto(
    producto_id, nombre, precio, stock, categoria, codigo_barras, conn=None
):
    """Edita un producto existente. Parámetro 'conn' ignorado (compatibilidad legacy)."""
    try:
        producto = db.session.get(Producto, producto_id)
        if not producto:
            return False
        producto.nombre = nombre
        producto.precio = precio
        producto.stock = stock
        producto.categoria = categoria
        producto.codigo_barras = codigo_barras
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error al editar producto: {e}")
        db.session.rollback()
        return False


def eliminar_producto(producto_id):
    """Elimina un producto por su ID."""
    try:
        producto = db.session.get(Producto, producto_id)
        if producto:
            db.session.delete(producto)
            db.session.commit()
            return True
        return False
    except Exception as e:
        print(f"Error al eliminar producto: {e}")
        db.session.rollback()
        return False

from models.producto import (
    agregar_producto,
    editar_producto,
    eliminar_producto,
    obtener_producto_por_id,
    obtener_productos,
)


def test_products_crud(app):
    # Usar la app de test proporcionada por la fixture (DB temporal)
    with app.app_context():
        # Crear producto
        res = agregar_producto("Producto Test", 123.45, 10, "CategoriaX", "CODE-001")
        assert res is True or res is None or res is not False

        productos = obtener_productos()
        assert len(productos) == 1
        p = productos[0]
        assert p["nombre"] == "Producto Test"
        pid = p["id"]

        # Editar producto
        editar_producto(pid, "Producto Mod", 150.0, 5, "CategoriaY", "CODE-001")
        p2 = obtener_producto_por_id(pid)
        assert p2 is not None
        assert p2["nombre"] == "Producto Mod"
        assert p2["precio"] == 150.0
        assert p2["stock"] == 5

        # Eliminar producto
        eliminar_producto(pid)
        assert obtener_producto_por_id(pid) is None

from models.producto import agregar_producto, obtener_producto_por_id
from models.venta import registrar_venta


def test_registrar_venta_y_actualiza_stock(app):
    # Usar la app de test proporcionada por la fixture (DB temporal)
    with app.app_context():
        # Crear producto con stock 10
        agregar_producto("Prod Venta", 200.0, 10, "VentaCat", "VEND-001")

        # Obtener el producto creado
        from models.producto import obtener_productos

        prods = obtener_productos()
        assert len(prods) == 1
        pid = prods[0]["id"]

        # Registrar venta por cantidad 3
        items = [{"id": pid, "cantidad": 3}]
        exito, mensaje = registrar_venta(items, usuario_id=None)
        assert exito is True

        # Verificar stock reducido (10 - 3 = 7)
        p_after = obtener_producto_por_id(pid)
        assert p_after is not None
        assert p_after["stock"] == 7

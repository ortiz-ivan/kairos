"""
Servicio de productos para gestión de inventario.

Proporciona funciones de negocio para operaciones CRUD de productos,
validaciones, filtrado y lógica relacionada con el inventario.
"""

from models.producto import agregar_producto as modelo_agregar
from models.producto import editar_producto as modelo_editar
from models.producto import eliminar_producto as modelo_eliminar
from models.producto import obtener_producto_por_id, obtener_productos
from utils.logging_config import get_logger

logger = get_logger(__name__)


def validar_datos_producto(
    nombre, precio, stock, categoria, codigo_barras, producto_id=None
):
    """
    Valida los datos de un producto.

    Args:
        nombre (str): Nombre del producto.
        precio (float): Precio del producto.
        stock (int): Stock del producto.
        categoria (str): Categoría del producto.
        codigo_barras (str): Código de barras.
        producto_id (int, optional): ID del producto para edición.

    Returns:
        tuple: (es_valido: bool, mensaje_error: str or None)
    """
    # Validar nombre
    if not nombre:
        return False, "El nombre del producto no puede estar vacío."
    if len(nombre) > 50:
        return False, "El nombre del producto no puede exceder 50 caracteres."

    # Validar código de barras
    if not codigo_barras:
        return False, "El código de barras no puede estar vacío."
    if len(codigo_barras) > 50:
        return False, "El código de barras no puede exceder 50 caracteres."

    # Validar unicidad del código de barras
    productos_existentes = obtener_productos()
    codigo_duplicado = any(
        p["codigo_barras"] == codigo_barras and p["id"] != (producto_id or 0)
        for p in productos_existentes
    )
    if codigo_duplicado:
        return (
            False,
            f"Ya existe un producto con el código de barras '{codigo_barras}'.",
        )

    # Validar precio
    try:
        precio_float = float(precio)
        if precio_float < 0:
            return False, "El precio no puede ser negativo."
        if precio_float == 0:
            return False, "El precio debe ser mayor a 0."
    except ValueError:
        return False, "El precio debe ser un número válido."

    # Validar stock
    try:
        stock_int = int(stock)
        if stock_int < 0:
            return False, "El stock no puede ser negativo."
    except ValueError:
        return False, "El stock debe ser un número entero válido."

    # Validar categoría
    if len(categoria) > 50:
        return False, "La categoría no puede exceder 50 caracteres."

    return True, None


def crear_producto(nombre, precio, stock, categoria, codigo_barras, admin_username):
    """
    Crea un nuevo producto con validaciones.

    Args:
        nombre (str): Nombre del producto.
        precio (float): Precio.
        stock (int): Stock inicial.
        categoria (str): Categoría.
        codigo_barras (str): Código de barras.
        admin_username (str): Username del admin que crea.

    Returns:
        tuple: (exito: bool, mensaje: str)
    """
    # Validar datos
    valido, error_msg = validar_datos_producto(
        nombre, precio, stock, categoria, codigo_barras
    )
    if not valido:
        return False, error_msg

    try:
        modelo_agregar(
            nombre,
            float(precio),
            int(stock),
            categoria.strip(),
            codigo_barras,
        )

        logger.info(
            f"Producto creado - Admin: {admin_username}, "
            f"Nombre: {nombre}, Código: {codigo_barras}"
        )
        return True, "Producto agregado correctamente."

    except Exception as e:
        logger.error(
            f"Error al crear producto - Admin: {admin_username}, "
            f"Nombre: {nombre}: {e}"
        )
        return False, f"Error al agregar producto: {e}"


def editar_producto_servicio(
    producto_id, nombre, precio, stock, categoria, codigo_barras, admin_username
):
    """
    Edita un producto existente.

    Args:
        producto_id (int): ID del producto.
        nombre (str): Nuevo nombre.
        precio (float): Nuevo precio.
        stock (int): Nuevo stock.
        categoria (str): Nueva categoría.
        codigo_barras (str): Nuevo código de barras.
        admin_username (str): Username del admin que edita.

    Returns:
        tuple: (exito: bool, mensaje: str)
    """
    # Validar que el producto exista
    producto = obtener_producto_por_id(producto_id)
    if not producto:
        return False, "Producto no encontrado."

    # Validar datos
    valido, error_msg = validar_datos_producto(
        nombre, precio, stock, categoria, codigo_barras, producto_id
    )
    if not valido:
        return False, error_msg

    try:
        exito = modelo_editar(
            producto_id,
            nombre,
            float(precio),
            int(stock),
            categoria.strip(),
            codigo_barras,
        )

        if exito:
            logger.info(
                f"Producto editado - Admin: {admin_username}, "
                f"ID: {producto_id}, Nombre: {nombre}, Código: {codigo_barras}"
            )
            return True, "Producto actualizado correctamente."
        else:
            logger.error(
                f"Fallo al editar producto - Admin: {admin_username}, "
                f"ID: {producto_id}, Nombre: {nombre}"
            )
            return False, "Error al actualizar el producto."

    except Exception as e:
        logger.error(
            f"Error al editar producto - Admin: {admin_username}, "
            f"ID: {producto_id}, Nombre: {nombre}: {e}"
        )
        return False, f"Error al actualizar producto: {e}"


def eliminar_producto_servicio(producto_id, admin_username):
    """
    Elimina un producto.

    Args:
        producto_id (int): ID del producto a eliminar.
        admin_username (str): Username del admin que elimina.

    Returns:
        tuple: (exito: bool, mensaje: str)
    """
    producto = obtener_producto_por_id(producto_id)
    if not producto:
        return False, "Producto no encontrado."

    nombre = producto["nombre"]

    try:
        modelo_eliminar(producto_id)
        logger.info(
            f"Producto eliminado - Admin: {admin_username}, "
            f"ID: {producto_id}, Nombre: {nombre}"
        )
        return True, "Producto eliminado correctamente."

    except Exception as e:
        logger.error(
            f"Error al eliminar producto - Admin: {admin_username}, "
            f"ID: {producto_id}, Nombre: {nombre}: {e}"
        )
        return False, f"Error al eliminar producto: {e}"


def filtrar_productos(productos, categoria_filtro="", codigo_filtro=""):
    """
    Filtra la lista de productos por categoría y código de barras.

    Args:
        productos (list): Lista de productos.
        categoria_filtro (str): Filtro de categoría.
        codigo_filtro (str): Filtro de código de barras.

    Returns:
        list: Lista filtrada de productos.
    """
    filtrados = productos

    if categoria_filtro:
        filtrados = [
            p
            for p in filtrados
            if p["categoria"] and categoria_filtro.lower() in p["categoria"].lower()
        ]

    if codigo_filtro:
        filtrados = [
            p
            for p in filtrados
            if p["codigo_barras"]
            and codigo_filtro.lower() in p["codigo_barras"].lower()
        ]

    return filtrados


def obtener_categorias():
    """
    Obtiene la lista de categorías únicas ordenadas.

    Returns:
        list: Lista de categorías.
    """
    productos = obtener_productos()
    return sorted({p["categoria"] for p in productos if p["categoria"]})

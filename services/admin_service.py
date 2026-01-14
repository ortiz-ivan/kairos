"""
Servicio de administración para gestión de usuarios.

Proporciona funciones de negocio para operaciones CRUD de usuarios,
validaciones y lógica relacionada con la administración.
"""

from sqlalchemy import select
from werkzeug.security import generate_password_hash

from models_alchemy import User, db
from utils.logging_config import get_logger

logger = get_logger(__name__)


def obtener_usuarios():
    """
    Obtiene todos los usuarios como lista de diccionarios.

    Returns:
        list: Lista de diccionarios con datos de usuarios.
    """
    stmt = select(User)
    usuarios = db.session.execute(stmt).scalars().all()
    return [
        {
            "id": u.id,
            "nombre": u.nombre,
            "username": u.username,
            "rol": u.rol,
        }
        for u in usuarios
    ]


def validar_datos_usuario(
    nombre, username, password=None, rol=None, username_original=None
):
    """
    Valida los datos de un usuario.

    Args:
        nombre (str): Nombre del usuario.
        username (str): Nombre de usuario.
        password (str, optional): Contraseña (requerida para creación).
        rol (str, optional): Rol del usuario.
        username_original (str, optional): Username original para edición.

    Returns:
        tuple: (es_valido: bool, mensaje_error: str or None)
    """
    # 1. Nombre vacío
    if not nombre:
        return False, "El nombre completo es requerido."

    # 2. Nombre - longitud máxima
    if len(nombre) > 100:
        return False, "El nombre no puede exceder 100 caracteres."

    # 3. Username vacío
    if not username:
        return False, "El nombre de usuario es requerido."

    # 4. Username - longitud mínima
    if len(username) < 3:
        return False, "El nombre de usuario debe tener al menos 3 caracteres."

    # 5. Username - longitud máxima
    if len(username) > 20:
        return False, "El nombre de usuario no puede exceder 20 caracteres."

    # 6. Username - unicidad
    if username != username_original:
        stmt = select(User).where(User.username == username)
        usuario_existente = db.session.execute(stmt).scalars().first()
        if usuario_existente:
            return (
                False,
                f"El nombre de usuario '{username}' ya está en uso. Por favor, elige otro.",
            )

    # 7. Contraseña (solo si se proporciona)
    if password is not None and password != "":
        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres."

    # 8. Rol válido
    if rol and rol not in ["admin", "usuario"]:
        return False, "El rol seleccionado no es válido."

    return True, None


def crear_usuario(nombre, username, password, rol, admin_username):
    """
    Crea un nuevo usuario con validaciones.

    Args:
        nombre (str): Nombre del usuario.
        username (str): Nombre de usuario.
        password (str): Contraseña.
        rol (str): Rol del usuario.
        admin_username (str): Username del admin que crea el usuario.

    Returns:
        tuple: (exito: bool, mensaje: str)
    """
    # Validar datos
    valido, error_msg = validar_datos_usuario(nombre, username, password, rol)
    if not valido:
        return False, error_msg

    try:
        # Hashear la contraseña
        hashed = generate_password_hash(password)

        # Crear usuario
        usuario = User(
            nombre=nombre,
            username=username,
            password=hashed,
            rol=rol,
        )
        db.session.add(usuario)
        db.session.commit()

        logger.info(
            f"Usuario creado - Admin: {admin_username}, "
            f"Nuevo usuario: {username}, Rol: {rol}"
        )
        return True, f"Usuario '{username}' creado correctamente."

    except Exception as e:
        db.session.rollback()
        logger.error(
            f"Error al crear usuario - Admin: {admin_username}, "
            f"Username: {username}: {e}"
        )
        return False, f"Error al crear usuario: {e}"


def editar_usuario(user_id, nombre, username, password, rol, admin_username):
    """
    Edita un usuario existente.

    Args:
        user_id (int): ID del usuario a editar.
        nombre (str): Nuevo nombre.
        username (str): Nuevo username.
        password (str): Nueva contraseña (opcional).
        rol (str): Nuevo rol.
        admin_username (str): Username del admin que edita.

    Returns:
        tuple: (exito: bool, mensaje: str, usuario_dict: dict or None)
    """
    usuario_orm = db.session.get(User, user_id)
    if not usuario_orm:
        return False, "Usuario no encontrado.", None

    username_original = usuario_orm.username

    # Validar datos
    valido, error_msg = validar_datos_usuario(
        nombre, username, password if password else None, rol, username_original
    )
    if not valido:
        return False, error_msg, None

    try:
        # Actualizar campos
        usuario_orm.nombre = nombre
        usuario_orm.username = username
        usuario_orm.rol = rol

        # Si se proporciona contraseña, actualizarla
        if password:
            usuario_orm.password = generate_password_hash(password)

        db.session.commit()

        logger.info(
            f"Usuario editado - Admin: {admin_username}, "
            f"ID: {user_id}, Username: {username}, Rol: {rol}"
        )
        return True, f"Usuario '{username}' actualizado correctamente.", None

    except Exception as e:
        db.session.rollback()
        logger.error(
            f"Error al editar usuario - Admin: {admin_username}, "
            f"ID: {user_id}, Username: {username}: {e}"
        )
        return False, f"Error al actualizar usuario: {e}", None


def eliminar_usuario(user_id, admin_username):
    """
    Elimina un usuario.

    Args:
        user_id (int): ID del usuario a eliminar.
        admin_username (str): Username del admin que elimina.

    Returns:
        tuple: (exito: bool, mensaje: str)
    """
    usuario = db.session.get(User, user_id)
    if not usuario:
        return False, "Usuario no encontrado."

    username = usuario.username

    try:
        db.session.delete(usuario)
        db.session.commit()

        logger.info(
            f"Usuario eliminado - Admin: {admin_username}, "
            f"ID: {user_id}, Username: {username}"
        )
        return True, "Usuario eliminado correctamente."

    except Exception as e:
        db.session.rollback()
        logger.error(
            f"Error al eliminar usuario - Admin: {admin_username}, "
            f"ID: {user_id}, Username: {username}: {e}"
        )
        return False, f"Error al eliminar usuario: {e}"


def verificar_username_disponible(username, admin_username):
    """
    Verifica si un username está disponible.

    Args:
        username (str): Username a verificar.
        admin_username (str): Username del admin que verifica.

    Returns:
        bool: True si está disponible.
    """
    stmt = select(User).where(User.username == username)
    usuario = db.session.execute(stmt).scalars().first()
    disponible = usuario is None

    logger.debug(
        f"Verificación de username - Admin: {admin_username}, "
        f"Username: {username}, Disponible: {disponible}"
    )
    return disponible

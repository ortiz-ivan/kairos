"""Modelo de Usuario con SQLAlchemy ORM."""

from werkzeug.security import check_password_hash, generate_password_hash

from models_alchemy import User, db


def crear_usuario(username, password, rol, nombre=None):
    """Crea un nuevo usuario en la DB."""
    hashed = generate_password_hash(password)
    usuario = User(nombre=nombre, username=username, password=hashed, rol=rol)
    db.session.add(usuario)
    db.session.commit()
    return usuario


def verificar_usuario(username, password):
    """Verifica credenciales y devuelve el usuario si es válido."""
    from sqlalchemy import select

    stmt = select(User).where(User.username == username)
    usuario = db.session.execute(stmt).scalars().first()
    if usuario and check_password_hash(usuario.password, password):
        # Retornar como dict para compatibilidad con código legacy
        return {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "username": usuario.username,
            "password": usuario.password,
            "rol": usuario.rol,
        }
    return None


def obtener_usuario_por_id(user_id):
    """Obtiene un usuario por su ID."""
    usuario = db.session.get(User, user_id)
    if usuario:
        return {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "username": usuario.username,
            "password": usuario.password,
            "rol": usuario.rol,
        }
    return None

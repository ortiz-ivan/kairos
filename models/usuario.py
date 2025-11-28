"""Modelo de Usuario con SQLAlchemy ORM."""

from werkzeug.security import generate_password_hash, check_password_hash
from models_alchemy import db, User


def crear_usuario(username, password, rol, nombre=None):
    """Crea un nuevo usuario en la DB."""
    hashed = generate_password_hash(password)
    usuario = User(nombre=nombre, username=username, password=hashed, rol=rol)
    db.session.add(usuario)
    db.session.commit()
    return usuario


def verificar_usuario(username, password):
    """Verifica credenciales y devuelve el usuario si es válido."""
    usuario = User.query.filter_by(username=username).first()
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
    usuario = User.query.get(user_id)
    if usuario:
        return {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "username": usuario.username,
            "password": usuario.password,
            "rol": usuario.rol,
        }
    return None

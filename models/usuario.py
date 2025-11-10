from werkzeug.security import generate_password_hash, check_password_hash
from database import get_connection  # usar get_connection de forma consistente


def crear_usuario(username, password, rol):
    db = get_connection()
    hashed = generate_password_hash(password)
    db.execute(
        "INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)",
        (username, hashed, rol),
    )
    db.commit()


def verificar_usuario(username, password):
    db = get_connection()
    usuario = db.execute(
        "SELECT * FROM usuarios WHERE username = ?", (username,)
    ).fetchone()
    if usuario and check_password_hash(usuario["password"], password):
        return usuario
    return None


def obtener_usuario_por_id(user_id):
    db = get_connection()
    usuario = db.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,)).fetchone()
    db.close()
    return usuario

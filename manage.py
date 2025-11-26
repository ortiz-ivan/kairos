import os
from app import create_app
from werkzeug.security import generate_password_hash

from models_alchemy import db, User
from flask_migrate import Migrate


def get_sqlite_uri():
    # Usa kairos.db en el directorio del proyecto por defecto
    base = os.path.dirname(__file__)
    path = os.path.join(base, "kairos.db")
    return f"sqlite:///{path}"


app = create_app()

# Configurar SQLAlchemy para uso con Flask-Migrate (solo para migraciones/seed)
app.config.setdefault("SQLALCHEMY_DATABASE_URI", get_sqlite_uri())
app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)

db.init_app(app)
migrate = Migrate(app, db)


@app.cli.command("seed")
def seed():
    """Crea las tablas (si hacen falta) y siembra un usuario admin de ejemplo.

    Usar: `flask seed` (asegúrate de exportar FLASK_APP=manage.py)
    """
    with app.app_context():
        db.create_all()
        admin = User.query.filter_by(username="admin").first()
        if admin:
            print("Usuario admin ya existe, omitiendo creación.")
            return
        pwd = os.environ.get("ADMIN_PASSWORD", "admin123")
        admin = User(
            nombre="Administrador",
            username="admin",
            password=generate_password_hash(pwd),
            rol="admin",
        )
        db.session.add(admin)
        db.session.commit()
        print(
            "Usuario admin creado. Usuario: admin, contraseña: (ver ADMIN_PASSWORD o 'admin123')"
        )


if __name__ == "__main__":
    # Ejecutar solo para desarrollo rápido
    app.run(debug=True)

"""
Gestor de migraciones y seeding para la aplicación Kairos.

Uso:
    flask db init          # Inicializar migraciones (primera vez)
    flask db migrate -m "message"  # Generar migración
    flask db upgrade       # Aplicar migraciones
    flask seed            # Sembrar datos iniciales (admin)
"""

import os

from flask_migrate import Migrate
from werkzeug.security import generate_password_hash

from app import create_app
from models_alchemy import User, db


def get_sqlite_uri():
    """Obtiene la URI de SQLite basada en el directorio del proyecto."""
    base = os.path.dirname(__file__)
    path = os.path.join(base, "kairos.db")
    return f"sqlite:///{path}"


app = create_app()

# Configurar SQLAlchemy (ya lo hace create_app, pero lo dejamos para claridad)
app.config.setdefault("SQLALCHEMY_DATABASE_URI", get_sqlite_uri())
app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)

migrate = Migrate(app, db)


@app.cli.command("seed")
def seed():
    """Siembra datos iniciales: crea un usuario admin de prueba."""
    with app.app_context():
        # Crear todas las tablas si no existen
        db.create_all()

        # Verificar si admin ya existe
        from sqlalchemy import select

        stmt = select(User).where(User.username == "admin")
        admin = db.session.execute(stmt).scalars().first()
        if admin:
            print("Usuario admin ya existe, omitiendo creación.")
            return

        # Crear admin
        pwd = os.environ.get("ADMIN_PASSWORD", "admin123")
        admin_user = User(
            nombre="Administrador",
            username="admin",
            password=generate_password_hash(pwd),
            rol="admin",
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Usuario admin creado.")
        print("  Username: admin")
        print(f"  Password: {pwd} (o usar ADMIN_PASSWORD)")


if __name__ == "__main__":
    app.run(debug=True)

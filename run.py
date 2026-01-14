"""
Script de punto de entrada para Kairos (para PyInstaller).
Gestiona la ruta de la aplicación y el contexto de Flask.
Inicializa la BD automáticamente si no existe.
Guarda los datos en una ubicación persistente.
"""

import os
import sys
from pathlib import Path

from werkzeug.security import generate_password_hash

# Importar módulos de la aplicación
from app import create_app
from models_alchemy import User, db

# Obtener la ruta base y configurar directorio de datos persistente
if getattr(sys, "frozen", False):
    # Ejecutable compilado - guardar datos en AppData (persistente entre actualizaciones)
    appdata_dir = os.environ.get("APPDATA", os.path.expanduser("~"))
    DATA_DIR = Path(appdata_dir) / "Kairos" / "datos"
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    BASE_DIR = Path(sys.executable).parent
else:
    # Ejecución desde código fuente
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR

# Establecer variable de entorno para la ruta de la BD
os.environ["KAIROS_DATA_DIR"] = str(DATA_DIR)

# Cambiar al directorio base
os.chdir(BASE_DIR)

# Asegurar que los módulos locales se cargan primero
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


def init_database(app):
    """Inicializa la base de datos y crea usuario admin si es necesario."""
    with app.app_context():
        # Crear todas las tablas
        print("📊 Inicializando base de datos...")
        print(f"📁 Ubicación: {DATA_DIR / 'kairos.db'}")
        db.create_all()
        print("✅ Tablas creadas/verificadas")

        # Crear usuario admin si no existe
        admin_exists = db.session.query(User).filter_by(username="admin").first()
        if not admin_exists:
            print("👤 Creando usuario administrador...")
            admin = User(
                username="admin",
                password=generate_password_hash("admin123"),
                nombre="Administrador",
                rol="admin",
            )
            db.session.add(admin)
            db.session.commit()
        else:
            print("✅ Usuario admin ya existe")


if __name__ == "__main__":
    app = create_app()

    # Inicializar la BD
    init_database(app)

    print("\n" + "=" * 70)
    print("🚀 KAIROS - Sistema de Ventas")
    print("=" * 70)
    print("📍 Accede a: http://localhost:5000")
    print("🔑 Credenciales por defecto:")
    print(f"💾 Base de datos: {DATA_DIR / 'kairos.db'}")
    print("� Ubicación datos: persistente (AppData)")
    print("�🛑 Presiona CTRL+C para detener la aplicación")
    print("=" * 70 + "\n")

    # Ejecutar en modo desarrollo
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False,  # No usar reloader en ejecutable
    )

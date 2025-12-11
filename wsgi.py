"""
Entry point para Gunicorn y servidores WSGI en producción.

Uso:
    gunicorn --bind 0.0.0.0:8000 --workers 4 wsgi:app
"""

import os

from app import create_app

# Configurar Flask con la clase apropiada según el ambiente
os.environ.setdefault("FLASK_ENV", "development")

app = create_app()

if __name__ == "__main__":
    app.run()

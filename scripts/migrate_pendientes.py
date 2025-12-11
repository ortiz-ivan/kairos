import json
import os
import sys
from pathlib import Path

from app import create_app
from models_alchemy import Pendiente, PendienteDetalle, db

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

app = create_app()

with app.app_context():
    path = ROOT / "pendientes.json"
    if not os.path.exists(path):
        print("No existe pendientes.json, nada que migrar")
        exit(0)

    with open(path, "r", encoding="utf-8") as fh:
        pendientes = json.load(fh)

    if not pendientes:
        print("Archivo vacío, nada que migrar")
        exit(0)

    migrated = 0
    for p in pendientes:
        try:
            pendiente = Pendiente(
                fecha=p.get("fecha") or "",
                usuario_id=p.get("usuario_id"),
                total=p.get("total") or 0,
            )
            db.session.add(pendiente)
            db.session.flush()
            for d in p.get("detalles", []):
                pd = PendienteDetalle(
                    pendiente_id=pendiente.id,
                    producto_id=d.get("id"),
                    nombre=d.get("nombre"),
                    cantidad=d.get("cantidad"),
                    precio=d.get("precio"),
                    subtotal=d.get("subtotal"),
                )
                db.session.add(pd)
            migrated += 1
        except Exception as e:
            print("Error migrando pendiente", p.get("id"), e)
            db.session.rollback()
    db.session.commit()
    print(f"Migrados {migrated} pendientes a la base de datos")

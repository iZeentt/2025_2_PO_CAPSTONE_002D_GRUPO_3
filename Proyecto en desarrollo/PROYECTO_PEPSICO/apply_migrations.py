"""
Script para aplicar migraciones de base de datos
"""
from app import create_app
from extensions import db
from flask_migrate import Migrate, upgrade
import os

app = create_app()
migrations_dir = os.path.join(os.path.dirname(__file__), 'migrations')
migrate = Migrate(app, db, directory=migrations_dir)

with app.app_context():
    # Aplicar todas las migraciones pendientes
    upgrade(directory=migrations_dir)
    print("✓ Migraciones aplicadas exitosamente")

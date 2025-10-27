#!/usr/bin/env python3
"""
Script de utilidades para inspección y administración de la base de datos.
Uso:
    python db_utils.py --list-users        # Listar todos los usuarios
    python db_utils.py --inspect-table vehicle  # Inspeccionar estructura de tabla
    python db_utils.py --list-tables       # Listar todas las tablas
"""
import argparse
import os
import sys
from sqlalchemy import inspect

# Asegurar que se puede importar desde el directorio raíz
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE)

from app import create_app
from extensions import db
from models import User, Vehicle, Mechanic, Assignment, WorkOrder, AccessEntry


def list_users():
    """Lista todos los usuarios del sistema."""
    app = create_app()
    with app.app_context():
        users = User.query.order_by(User.id).all()
        if not users:
            print('❌ No hay usuarios en la base de datos')
            return
        
        print(f'\n{"ID":<5} {"Usuario":<20} {"Rol":<20}')
        print('-' * 50)
        for u in users:
            print(f'{u.id:<5} {u.username:<20} {u.role:<20}')
        print(f'\nTotal: {len(users)} usuarios')


def list_tables():
    """Lista todas las tablas de la base de datos."""
    app = create_app()
    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print('\n=== Tablas en la base de datos ===')
        for i, table in enumerate(tables, 1):
            print(f'{i}. {table}')
        print(f'\nTotal: {len(tables)} tablas')


def inspect_table(table_name):
    """Inspecciona la estructura de una tabla."""
    app = create_app()
    with app.app_context():
        inspector = inspect(db.engine)
        
        if table_name not in inspector.get_table_names():
            print(f'❌ La tabla "{table_name}" no existe')
            return
        
        columns = inspector.get_columns(table_name)
        foreign_keys = inspector.get_foreign_keys(table_name)
        indexes = inspector.get_indexes(table_name)
        
        print(f'\n=== Tabla: {table_name} ===')
        print(f'\n{"Columna":<25} {"Tipo":<20} {"Nullable":<10} {"Default"}')
        print('-' * 80)
        for col in columns:
            nullable = 'Sí' if col['nullable'] else 'No'
            default = col.get('default', 'NULL')
            print(f"{col['name']:<25} {str(col['type']):<20} {nullable:<10} {default}")
        
        if foreign_keys:
            print('\n--- Foreign Keys ---')
            for fk in foreign_keys:
                print(f"  {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
        
        if indexes:
            print('\n--- Índices ---')
            for idx in indexes:
                print(f"  {idx['name']}: {idx['column_names']}")


def get_db_stats():
    """Muestra estadísticas generales de la base de datos."""
    app = create_app()
    with app.app_context():
        stats = {
            'Usuarios': User.query.count(),
            'Vehículos': Vehicle.query.count(),
            'Mecánicos': Mechanic.query.count(),
            'Asignaciones': Assignment.query.count(),
            'Órdenes de Trabajo': WorkOrder.query.count(),
            'Registros de Acceso': AccessEntry.query.count(),
        }
        
        print('\n=== Estadísticas de la Base de Datos ===')
        for key, value in stats.items():
            print(f'{key:<25}: {value:>6}')


def main():
    parser = argparse.ArgumentParser(
        description='Utilidades para inspección de la base de datos'
    )
    
    parser.add_argument('--list-users', action='store_true',
                       help='Listar todos los usuarios')
    parser.add_argument('--list-tables', action='store_true',
                       help='Listar todas las tablas')
    parser.add_argument('--inspect-table', metavar='TABLE',
                       help='Inspeccionar estructura de una tabla')
    parser.add_argument('--stats', action='store_true',
                       help='Mostrar estadísticas de la base de datos')
    
    args = parser.parse_args()
    
    if args.list_users:
        list_users()
    elif args.list_tables:
        list_tables()
    elif args.inspect_table:
        inspect_table(args.inspect_table)
    elif args.stats:
        get_db_stats()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

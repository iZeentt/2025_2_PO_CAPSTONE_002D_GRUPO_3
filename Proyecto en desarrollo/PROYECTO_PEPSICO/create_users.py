#!/usr/bin/env python3
"""
Script unificado para crear usuarios con diferentes roles en el sistema.
Uso:
    python create_users.py --role admin --username admin --password admin123
    python create_users.py --role mechanic --username juan --password pass123 --name "Juan Pérez" --phone "123456789"
    python create_users.py --role parts_assistant --username asistente --password pass123
    python create_users.py --role key_manager --username encargado --password pass123
"""
import argparse
from app import create_app
from extensions import db
from models import User, UserProfile, Mechanic


def create_user_with_role(username, password, role, full_name=None, phone=None, function=None):
    """Crea un usuario con el rol especificado y sus datos asociados."""
    app = create_app()
    with app.app_context():
        db.create_all()
        
        # Verificar si el usuario ya existe
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f'❌ El usuario "{username}" ya existe')
            print(f'   ID: {existing_user.id}, Rol: {existing_user.role}')
            return False
        
        # Crear usuario
        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        print(f'✓ Usuario creado: {username}')
        print(f'  ID: {user.id}')
        print(f'  Rol: {role}')
        
        # Crear perfil de mecánico si es necesario
        if role == 'mechanic':
            mechanic = Mechanic(
                name=(full_name or username),
                phone=phone,
                user_id=user.id
            )
            db.session.add(mechanic)
            db.session.commit()
            print(f'  Mechanic ID: {mechanic.id}')
        
        # Crear perfil de usuario si se proporcionó información adicional
        if full_name or function:
            profile = UserProfile(
                user_id=user.id,
                full_name=full_name,
                function=function
            )
            db.session.add(profile)
            db.session.commit()
            print(f'  Perfil creado')
            if full_name:
                print(f'    Nombre: {full_name}')
            if function:
                print(f'    Función: {function}')
        
        return True


def main():
    parser = argparse.ArgumentParser(
        description='Crear usuario con rol específico',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Roles disponibles:
  admin             - Administrador del sistema
  mechanic          - Mecánico (requiere --name)
  parts_assistant   - Asistente de repuestos
  key_manager       - Encargado de llaves
  receptionist      - Recepcionista
  guard             - Guardia de acceso
  operator          - Operador general
        """
    )
    
    parser.add_argument('--username', required=True, help='Nombre de usuario')
    parser.add_argument('--password', required=True, help='Contraseña')
    parser.add_argument('--role', required=True, 
                       choices=['admin', 'mechanic', 'parts_assistant', 'key_manager', 
                               'receptionist', 'guard', 'operator'],
                       help='Rol del usuario')
    parser.add_argument('--name', help='Nombre completo (requerido para mechanic)')
    parser.add_argument('--phone', help='Teléfono (opcional, para mechanic)')
    parser.add_argument('--function', help='Función del usuario (opcional)')
    
    args = parser.parse_args()
    
    # Validar que mechanic tenga nombre
    if args.role == 'mechanic' and not args.name:
        parser.error('El rol "mechanic" requiere --name')
    
    create_user_with_role(
        username=args.username,
        password=args.password,
        role=args.role,
        full_name=args.name,
        phone=args.phone,
        function=args.function
    )


if __name__ == '__main__':
    main()

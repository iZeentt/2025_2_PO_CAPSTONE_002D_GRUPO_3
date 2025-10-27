import os
from app import create_app
from extensions import db
from models import User, Mechanic


def create_default_mechanic(username='Mecanico', password='mecanico123', name='Mecanico', phone=None):
    app = create_app()
    with app.app_context():
        db.create_all()
        u = User.query.filter_by(username=username).first()
        if u:
            print(f"El usuario '{username}' ya existe (id={u.id})")
            # ensure there is a Mechanic profile linked to this user
            m = Mechanic.query.filter_by(user_id=u.id).first()
            if m:
                print(f"Perfil de Mechanic ya enlazado (mechanic_id={m.id})")
                # return a fresh user instance attached to the session
                return User.query.get(u.id)
            # try to find a mechanic by name to link instead
            m_by_name = Mechanic.query.filter_by(name=name).first()
            if m_by_name:
                m_by_name.user_id = u.id
                db.session.add(m_by_name)
                db.session.commit()
                print(f"Perfil de Mechanic existente enlazado al usuario (mechanic_id={m_by_name.id})")
                return User.query.get(u.id)
            # otherwise create a new mechanic profile and link it
            m = Mechanic(name=name, phone=phone, user_id=u.id)
            db.session.add(m)
            db.session.commit()
            print(f"Perfil de Mechanic creado y enlazado (mechanic_id={m.id})")
            return User.query.get(u.id)
        u = User(username=username, role='mechanic')
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        m = Mechanic(name=name, phone=phone, user_id=u.id)
        db.session.add(m)
        db.session.commit()
    print(f"Usuario mecanico creado: {username} (user_id={u.id}, mechanic_id={m.id})")
    return User.query.get(u.id)


if __name__ == '__main__':
    # Allow overriding via environment variables
    username = os.environ.get('MECH_USERNAME', 'Mecanico')
    password = os.environ.get('MECH_PASSWORD', 'mecanico123')
    name = os.environ.get('MECH_NAME', 'Mecanico')
    phone = os.environ.get('MECH_PHONE')
    create_default_mechanic(username=username, password=password, name=name, phone=phone)

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(32), nullable=False, default='operator')
    # optional profile relationship
    profile = db.relationship('UserProfile', backref='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(32), nullable=False)
    driver_name = db.Column(db.String(120))
    driver_rut = db.Column(db.String(64))
    company = db.Column(db.String(120))
    status = db.Column(db.String(32), default='pending')
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    approved_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    approved_at = db.Column(db.DateTime, nullable=True)
    # assignments relationship
    assignment_set = db.relationship('Assignment', backref='vehicle', order_by='Assignment.assigned_at')


class UserProfile(db.Model):
    __tablename__ = 'user_profile'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(200))
    function = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Mechanic(db.Model):
    __tablename__ = 'mechanic'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(50))
    # optional link to a User account (for mechanic users)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    # relationship to the User record (if this mechanic has a linked user account)
    user = db.relationship('User', foreign_keys=[user_id])
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Assignment(db.Model):
    __tablename__ = 'assignment'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanic.id'), nullable=False)
    assigned_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    note = db.Column(db.Text)

    # relationships
    mechanic = db.relationship('Mechanic')
    # 'vehicle' backref is provided by Vehicle.assignment_set


class Progress(db.Model):
    __tablename__ = 'progress'
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanic.id'), nullable=False)
    note = db.Column(db.Text)
    status = db.Column(db.String(32), default='in_progress')  # in_progress, paused, rejected, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    mechanic = db.relationship('Mechanic')
    assignment = db.relationship('Assignment')


class WorkOrder(db.Model):
    __tablename__ = 'work_order'
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(64), nullable=False, index=True)
    driver_name = db.Column(db.String(200), nullable=True)
    driver_rut = db.Column(db.String(64), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    docs_valid = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(32), default='open')  # open | blocked | duplicate | closed
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # convenience relationship to show creator username in templates
    created_user = db.relationship('User', foreign_keys=[created_by])


class AccessEntry(db.Model):
    """Registro de ingreso realizado por un guardia de acceso.
    Contiene la patente, usuario que registró y marca de tiempo.
    """
    __tablename__ = 'access_entry'
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(64), nullable=False)
    driver_name = db.Column(db.String(200), nullable=True)
    driver_rut = db.Column(db.String(64), nullable=True)
    region = db.Column(db.String(100), nullable=True)
    comuna = db.Column(db.String(100), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    photos = db.relationship('AccessPhoto', backref='entry', cascade='all, delete-orphan')


class AccessPhoto(db.Model):
    __tablename__ = 'access_photo'
    id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('access_entry.id'), nullable=False)
    filename = db.Column(db.String(260), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ReturnRecord(db.Model):
    """Registro de devolución realizado por un Ejecutivo de ventas.
    Guarda referencia al vehículo, kilometraje, comentarios y fecha.
    """
    __tablename__ = 'return_record'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    returned_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mileage = db.Column(db.Integer, nullable=True)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    photos = db.relationship('ReturnPhoto', backref='record', cascade='all, delete-orphan')


class ReturnPhoto(db.Model):
    __tablename__ = 'return_photo'
    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer, db.ForeignKey('return_record.id'), nullable=False)
    filename = db.Column(db.String(260), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class KeyAssignment(db.Model):
    """Asignación activa de llave por patente."""
    __tablename__ = 'key_assignment'
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(64), nullable=False, index=True)
    holder = db.Column(db.String(200), nullable=True)
    assigned_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    returned_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    returned_at = db.Column(db.DateTime, nullable=True)
    active = db.Column(db.Boolean, default=True)
    
    # Relationships
    assigned_user = db.relationship('User', foreign_keys=[assigned_by])
    returned_user = db.relationship('User', foreign_keys=[returned_by])


class KeyLog(db.Model):
    """Historial de entregas y devoluciones de llaves."""
    __tablename__ = 'key_log'
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(64), nullable=False, index=True)
    action = db.Column(db.String(32), nullable=False)  # 'delivery' | 'return'
    performed_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # relationship to access performer username in templates
    performed_user = db.relationship('User', foreign_keys=[performed_by])


class Part(db.Model):
    """Repuesto/Pieza con control de stock."""
    __tablename__ = 'part'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    stock = db.Column(db.Integer, default=0, nullable=False)
    min_stock = db.Column(db.Integer, default=0)  # Alerta de stock mínimo
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    created_user = db.relationship('User', foreign_keys=[created_by])
    deliveries = db.relationship('PartDelivery', backref='part', order_by='PartDelivery.created_at.desc()')


class PartDelivery(db.Model):
    """Registro de entrega de repuestos a un mecánico."""
    __tablename__ = 'part_delivery'
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('part.id'), nullable=False)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanic.id'), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    delivered_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    mechanic = db.relationship('Mechanic')
    assignment = db.relationship('Assignment')
    delivered_user = db.relationship('User', foreign_keys=[delivered_by])


class PartRequest(db.Model):
    """Solicitud de repuesto realizada por un mecánico."""
    __tablename__ = 'part_request'
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('part.id'), nullable=False)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanic.id'), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(32), default='pending', nullable=False)  # pending, approved, rejected, delivered
    note = db.Column(db.Text)
    requested_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    processed_at = db.Column(db.DateTime, nullable=True)
    response_note = db.Column(db.Text)
    
    # Relationships
    part = db.relationship('Part')
    mechanic = db.relationship('Mechanic')
    assignment = db.relationship('Assignment')
    requester = db.relationship('User', foreign_keys=[requested_by])
    processor = db.relationship('User', foreign_keys=[processed_by])






import os
from datetime import datetime
from functools import wraps
from secrets import token_urlsafe

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user

from extensions import db, login_manager
from models import (
    User, Vehicle, Mechanic, Assignment, Progress, AccessEntry, AccessPhoto,
    Part, PartDelivery, PartRequest, WorkOrder, UserProfile
)

BASE_DIR = os.path.dirname(__file__)

# ==================== REGIONES Y COMUNAS DE CHILE ====================
REGIONES_COMUNAS = {
    "Región de Arica y Parinacota": ["Arica", "Camarones", "Putre", "General Lagos"],
    "Región de Tarapacá": ["Iquique", "Alto Hospicio", "Pozo Almonte", "Camiña", "Colchane", "Huara", "Pica"],
    "Región de Antofagasta": ["Antofagasta", "Mejillones", "Sierra Gorda", "Taltal", "Calama", "Ollagüe", "San Pedro de Atacama", "Tocopilla", "María Elena"],
    "Región de Atacama": ["Copiapó", "Caldera", "Tierra Amarilla", "Chañaral", "Diego de Almagro", "Vallenar", "Alto del Carmen", "Freirina", "Huasco"],
    "Región de Coquimbo": ["La Serena", "Coquimbo", "Andacollo", "La Higuera", "Paiguano", "Vicuña", "Illapel", "Canela", "Los Vilos", "Salamanca", "Ovalle", "Combarbalá", "Monte Patria", "Punitaqui", "Río Hurtado"],
    "Región de Valparaíso": ["Valparaíso", "Casablanca", "Concón", "Juan Fernández", "Puchuncaví", "Quintero", "Viña del Mar", "Isla de Pascua", "Los Andes", "Calle Larga", "Rinconada", "San Esteban", "La Ligua", "Cabildo", "Papudo", "Petorca", "Zapallar", "Quillota", "Calera", "Hijuelas", "La Cruz", "Nogales", "San Antonio", "Algarrobo", "Cartagena", "El Quisco", "El Tabo", "Santo Domingo", "San Felipe", "Catemu", "Llaillay", "Panquehue", "Putaendo", "Santa María", "Quilpué", "Limache", "Olmué", "Villa Alemana"],
    "Región Metropolitana de Santiago": ["Cerrillos", "Cerro Navia", "Conchalí", "El Bosque", "Estación Central", "Huechuraba", "Independencia", "La Cisterna", "La Florida", "La Granja", "La Pintana", "La Reina", "Las Condes", "Lo Barnechea", "Lo Espejo", "Lo Prado", "Macul", "Maipú", "Ñuñoa", "Pedro Aguirre Cerda", "Peñalolén", "Providencia", "Pudahuel", "Quilicura", "Quinta Normal", "Recoleta", "Renca", "Santiago", "San Joaquín", "San Miguel", "San Ramón", "Vitacura", "Puente Alto", "Pirque", "San José de Maipo", "Colina", "Lampa", "Tiltil", "San Bernardo", "Buin", "Calera de Tango", "Paine", "Melipilla", "Alhué", "Curacaví", "María Pinto", "San Pedro", "Talagante", "El Monte", "Isla de Maipo", "Padre Hurtado", "Peñaflor"],
    "Región del Libertador Gral. Bernardo O'Higgins": ["Rancagua", "Codegua", "Coinco", "Coltauco", "Doñihue", "Graneros", "Las Cabras", "Machalí", "Malloa", "Mostazal", "Olivar", "Peumo", "Pichidegua", "Quinta de Tilcoco", "Rengo", "Requínoa", "San Vicente", "Pichilemu", "La Estrella", "Litueche", "Marchihue", "Navidad", "Paredones", "San Fernando", "Chépica", "Chimbarongo", "Lolol", "Nancagua", "Palmilla", "Peralillo", "Placilla", "Pumanque", "Santa Cruz"],
    "Región del Maule": ["Talca", "ConsVitución", "Curepto", "Empedrado", "Maule", "Pelarco", "Pencahue", "Río Claro", "San Clemente", "San Rafael", "Cauquenes", "Chanco", "Pelluhue", "Curicó", "Hualañé", "Licantén", "Molina", "Rauco", "Romeral", "Sagrada Familia", "Teno", "Vichuquén", "Linares", "Colbún", "Longaví", "Parral", "Retiro", "San Javier", "Villa Alegre", "Yerbas Buenas"],
    "Región de Ñuble": ["Chillán", "Bulnes", "Cobquecura", "Coelemu", "Coihueco", "Chillán Viejo", "El Carmen", "Ninhue", "Ñiquén", "Pemuco", "Pinto", "Portezuelo", "Quillón", "Quirihue", "Ránquil", "San Carlos", "San Fabián", "San Ignacio", "San Nicolás", "Treguaco", "Yungay"],
    "Región del Biobío": ["Concepción", "Coronel", "Chiguayante", "Florida", "Hualqui", "Lota", "Penco", "San Pedro de la Paz", "Santa Juana", "Talcahuano", "Tomé", "Hualpén", "Lebu", "Arauco", "Cañete", "Contulmo", "Curanilahue", "Los Álamos", "Tirúa", "Los Ángeles", "Antuco", "Cabrero", "Laja", "Mulchén", "Nacimiento", "Negrete", "Quilaco", "Quilleco", "San Rosendo", "Santa Bárbara", "Tucapel", "Yumbel", "Alto Biobío"],
    "Región de La Araucanía": ["Temuco", "Carahue", "Cunco", "Curarrehue", "Freire", "Galvarino", "Gorbea", "Lautaro", "Loncoche", "Melipeuco", "Nueva Imperial", "Padre las Casas", "Perquenco", "Pitrufquén", "Pucón", "Saavedra", "Teodoro Schmidt", "Toltén", "Vilcún", "Villarrica", "Cholchol", "Angol", "Collipulli", "Curacautín", "Ercilla", "Lonquimay", "Los Sauces", "Lumaco", "Purén", "Renaico", "Traiguén", "Victoria"],
    "Región de Los Ríos": ["Valdivia", "Corral", "Lanco", "Los Lagos", "Máfil", "Mariquina", "Paillaco", "Panguipulli", "La Unión", "Futrono", "Lago Ranco", "Río Bueno"],
    "Región de Los Lagos": ["Puerto Montt", "Calbuco", "Cochamó", "Fresia", "Frutillar", "Los Muermos", "Llanquihue", "Maullín", "Puerto Varas", "Castro", "Ancud", "Chonchi", "Curaco de Vélez", "Dalcahue", "Puqueldón", "Queilén", "Quellón", "Quemchi", "Quinchao", "Osorno", "Puerto Octay", "Purranque", "Puyehue", "Río Negro", "San Juan de la Costa", "San Pablo", "Chaitén", "Futaleufú", "Hualaihué", "Palena"],
    "Región Aysén del Gral. Carlos Ibáñez del Campo": ["Coyhaique", "Lago Verde", "Aysén", "Cisnes", "Guaitecas", "Cochrane", "O'Higgins", "Tortel", "Chile Chico", "Río Ibáñez"],
    "Región de Magallanes y de la Antártica Chilena": ["Punta Arenas", "Laguna Blanca", "Río Verde", "San Gregorio", "Cabo de Hornos (Ex Navarino)", "Antártica", "Porvenir", "Primavera", "Timaukel", "Natales", "Torres del Paine"]
}

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # uploads for access guard photos
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    # allowed image extensions
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

    db.init_app(app)
    login_manager.init_app(app)

    # ==================== USER LOADER ====================
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ==================== DECORATORS ====================

    def role_required(*roles):
        def decorator(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                if not current_user.is_authenticated:
                    return login_manager.unauthorized()
                if current_user.role not in roles:
                    flash('Acceso denegado: rol insuficiente', 'danger')
                    return redirect(url_for('index'))
                return f(*args, **kwargs)
            return wrapped
        return decorator

    def exclude_roles(*roles):
        """Decorator to deny access to specific roles."""
        def decorator(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                if not current_user.is_authenticated:
                    return login_manager.unauthorized()
                if current_user.role in roles:
                    flash('Acceso denegado para su rol', 'danger')
                    return redirect(url_for('index'))
                return f(*args, **kwargs)
            return wrapped
        return decorator

    # ==================== PUBLIC & AUTH ROUTES ====================
    
    @app.route('/')
    def index():
        return render_template('index.html')

    # NOTE: /login route removed. Use POST /auth/login from the homepage login form.
    @app.route('/auth/login', methods=['POST'])
    def auth_login():
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            remember = bool(request.form.get('remember'))
            login_user(user, remember=remember)
            # Redirect mechanics and guards to their specific dashboards
            if user.role == 'mechanic':
                return redirect(url_for('mechanic_dashboard'))
            if user.role == 'guard':
                return redirect(url_for('guard_entry_create'))
            # Key manager should land on their dashboard
            if user.role == 'key_manager':
                return redirect(url_for('keys_dashboard'))
            # Parts assistant should land on parts dashboard
            if user.role == 'parts_assistant':
                return redirect(url_for('parts_dashboard'))
            # Sales executive should land on sales return form
            if user.role == 'sales':
                return redirect(url_for('sales_return_create'))
            # Receptionist should land on work orders
            if user.role == 'receptionist':
                return redirect(url_for('reception_workorders'))
            return redirect(url_for('dashboard'))
        flash('Usuario o contraseña inválidos', 'danger')
        return redirect(url_for('index'))

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    # ==================== DASHBOARD ROUTES ====================
    
    @app.route('/dashboard')
    @login_required
    @exclude_roles('guard','sales','key_manager','parts_assistant')
    def dashboard():
        return render_template('dashboard.html')

    # ==================== VEHICLE MANAGEMENT ====================
    
    @app.route('/vehicles')
    @login_required
    # Vehicles management is exclusive to the workshop supervisor (jefe de taller).
    # Exclude mechanics so they cannot access the vehicles list.
    @exclude_roles('guard','sales','key_manager','mechanic','receptionist')
    def vehicles_list():
        try:
            vehicles = Vehicle.query.order_by(Vehicle.id).all()
        except Exception as e:
            # If missing column on legacy DB, attempt to add it and retry once
            try:
                msg = str(e)
                if 'vehicle.driver_rut' in msg or 'no such column' in msg:
                    conn = db.engine.connect()
                    try:
                        conn.execute("ALTER TABLE vehicle ADD COLUMN driver_rut VARCHAR(64)")
                    except Exception:
                        pass
                    conn.close()
                    vehicles = Vehicle.query.order_by(Vehicle.id).all()
                else:
                    raise
            except Exception:
                raise
        # build a map vehicle_id -> assigned display name (prefer linked User.username)
        assigned_names = {}
        try:
            for v in vehicles:
                last = v.assignment_set[-1] if v.assignment_set else None
                if not last:
                    assigned_names[v.id] = None
                    continue
                mech = last.mechanic
                # prefer mechanic linked user username if available
                assigned_username = None
                if getattr(mech, 'user_id', None):
                    u = User.query.get(mech.user_id)
                    if u:
                        assigned_username = u.username
                # fallback to mechanic.name
                assigned_names[v.id] = assigned_username or mech.name
        except Exception:
            # on any error, leave mapping empty so template can fallback
            assigned_names = {}

        return render_template('vehicles.html', vehicles=vehicles, assigned_names=assigned_names)

    # ==================== MECHANIC MANAGEMENT ====================
    
    @app.route('/mechanics')
    @login_required
    @exclude_roles('guard','sales','key_manager')
    def mechanics_list():
        mechanics = Mechanic.query.order_by(Mechanic.created_at.desc()).all()
        return render_template('mechanics.html', mechanics=mechanics)

    @app.route('/mechanics/new', methods=['GET','POST'])
    @login_required
    @exclude_roles('guard','sales','key_manager')
    def mechanic_create():
        if request.method == 'POST':
            name = request.form['name']
            phone = request.form.get('phone')
            m = Mechanic(name=name, phone=phone)
            db.session.add(m)
            db.session.commit()
            flash('Mecánico agregado', 'success')
            return redirect(url_for('mechanics_list'))
        return render_template('mechanic_form.html')

    @app.route('/vehicles/<int:vehicle_id>/assign', methods=['GET','POST'])
    @login_required
    # Only supervisors should assign mechanics to vehicles (no admins/mechanics).
    @role_required('supervisor')
    def assign_mechanic(vehicle_id):
        v = Vehicle.query.get_or_404(vehicle_id)
        mechanics = Mechanic.query.order_by(Mechanic.name).all()
        if request.method == 'POST':
            mech_id = int(request.form['mechanic_id'])
            note = request.form.get('note')
            a = Assignment(vehicle_id=v.id, mechanic_id=mech_id, assigned_by=current_user.id, note=note)
            db.session.add(a)
            db.session.commit()
            flash('Mecánico asignado', 'success')
            return redirect(url_for('vehicles_list'))
        return render_template('assign_form.html', vehicle=v, mechanics=mechanics)

    @app.route('/supervisor/assignments')
    @login_required
    @role_required('supervisor', 'admin')
    def supervisor_assignments():
        """Vista para que el supervisor vea todas las asignaciones con sus estados y progresos"""
        assignments = Assignment.query.order_by(Assignment.assigned_at.desc()).all()
        
        # Obtener el último progreso de cada asignación
        assignment_data = []
        for a in assignments:
            last_progress = Progress.query.filter_by(assignment_id=a.id).order_by(Progress.created_at.desc()).first()
            assignment_data.append({
                'assignment': a,
                'last_progress': last_progress,
                'all_progress': Progress.query.filter_by(assignment_id=a.id).order_by(Progress.created_at.desc()).all()
            })
        
        return render_template('supervisor_assignments.html', assignment_data=assignment_data)

    # Mechanic-specific views
    @app.route('/me/dashboard')
    @login_required
    @role_required('mechanic')
    def mechanic_dashboard():
        # find mechanic linked to current_user
        mech = Mechanic.query.filter_by(user_id=current_user.id).first()
        # If the logged-in user has role 'mechanic' but there's no linked Mechanic profile,
        # create a minimal Mechanic record automatically so the user can access their dashboard.
        if not mech:
            if getattr(current_user, 'role', None) == 'mechanic':
                try:
                    mech = Mechanic(name=current_user.username, user_id=current_user.id)
                    db.session.add(mech)
                    db.session.commit()
                    flash('Perfil de mecánico creado automáticamente', 'info')
                except Exception:
                    db.session.rollback()
                    flash('No existe un perfil de mecánico asociado a este usuario', 'warning')
                    return redirect(url_for('index'))
            else:
                flash('No existe un perfil de mecánico asociado a este usuario', 'warning')
                return redirect(url_for('index'))
        # get latest assignments for this mechanic, but only those assigned
        # by users with the role 'supervisor' (Jefe de Taller). This ensures
        # mechanics only see orders that a supervisor assigned.
        try:
            assignments = (
                Assignment.query
                .join(User, Assignment.assigned_by == User.id)
                .filter(Assignment.mechanic_id == mech.id, User.role == 'supervisor')
                .order_by(Assignment.assigned_at.desc())
                .all()
            )
        except Exception:
            # on error, return an empty list to avoid exposing assignments
            assignments = []

        return render_template('mechanic_dashboard.html', mechanic=mech, assignments=assignments)

    @app.route('/assignments/<int:assignment_id>/progress', methods=['GET','POST'])
    @login_required
    @role_required('mechanic')
    def add_progress(assignment_id):
        mech = Mechanic.query.filter_by(user_id=current_user.id).first()
        if not mech:
            flash('Perfil de mecánico no encontrado', 'warning')
            return redirect(url_for('index'))
        a = Assignment.query.get_or_404(assignment_id)
        if a.mechanic_id != mech.id:
            flash('Acceso denegado a esta orden', 'danger')
            return redirect(url_for('mechanic_dashboard'))
        if request.method == 'POST':
            note = request.form.get('note')
            status = request.form.get('status', 'in_progress')  # Obtener estado seleccionado
            p = Progress(assignment_id=a.id, mechanic_id=mech.id, note=note, status=status)
            db.session.add(p)
            
            # Actualizar el estado de la asignación si es necesario
            if status in ['completed', 'rejected']:
                a.status = status
            
            db.session.commit()
            flash('Avance registrado exitosamente', 'success')
            return redirect(url_for('mechanic_dashboard'))
        return render_template('progress_form.html', assignment=a)

    # ==================== MECHANIC PART REQUESTS ====================
    
    @app.route('/mechanic/part-requests/new', methods=['GET', 'POST'])
    @login_required
    @role_required('mechanic')
    def mechanic_part_request_create():
        """Crear solicitud de repuesto"""
        mech = Mechanic.query.filter_by(user_id=current_user.id).first()
        if not mech:
            flash('Perfil de mecánico no encontrado', 'warning')
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            part_id = int(request.form['part_id'])
            quantity = int(request.form['quantity'])
            assignment_id = request.form.get('assignment_id')
            note = request.form.get('note', '').strip()
            
            # Crear solicitud
            part_request = PartRequest(
                part_id=part_id,
                mechanic_id=mech.id,
                assignment_id=int(assignment_id) if assignment_id else None,
                quantity=quantity,
                note=note,
                requested_by=current_user.id,
                status='pending'
            )
            
            db.session.add(part_request)
            db.session.commit()
            
            flash('Solicitud de repuesto enviada exitosamente', 'success')
            return redirect(url_for('mechanic_part_requests'))
        
        # GET: Mostrar formulario
        parts = Part.query.order_by(Part.code).all()
        # Solo mostrar asignaciones del mecánico actual
        assignments = Assignment.query.filter_by(mechanic_id=mech.id).order_by(Assignment.assigned_at.desc()).all()
        
        return render_template('mechanic_part_request_form.html', 
                             parts=parts, 
                             assignments=assignments)
    
    @app.route('/mechanic/part-requests')
    @login_required
    @role_required('mechanic')
    def mechanic_part_requests():
        """Historial de solicitudes del mecánico"""
        mech = Mechanic.query.filter_by(user_id=current_user.id).first()
        if not mech:
            flash('Perfil de mecánico no encontrado', 'warning')
            return redirect(url_for('index'))
        
        requests = PartRequest.query.filter_by(mechanic_id=mech.id).order_by(PartRequest.requested_at.desc()).all()
        return render_template('mechanic_part_requests.html', requests=requests)

    @app.route('/vehicles/new', methods=['GET','POST'])
    @login_required
    # Only supervisors can create vehicles (mechanics must not access this).
    @exclude_roles('guard','sales','key_manager','mechanic','receptionist')
    def vehicle_create():
        from models import WorkOrder

        # gather plates from workorders validated by reception
        validated_orders = WorkOrder.query.filter_by(docs_valid=True).order_by(WorkOrder.created_at.desc()).all()
        # unique plates from validated workorders. Include even if already registered
        validated_plates = []
        seen = set()
        for wo in validated_orders:
            p = (wo.plate or '').strip()
            if not p or p in seen:
                continue
            # determine if already registered as Vehicle
            registered = True if Vehicle.query.filter_by(plate=p).first() else False
            # try to find the latest AccessEntry for this plate to get driver info
            ae = AccessEntry.query.filter_by(plate=p).order_by(AccessEntry.created_at.desc()).first()
            driver_name = ae.driver_name if ae else None
            driver_rut = ae.driver_rut if ae else None
            seen.add(p)
            validated_plates.append({'plate': p, 'workorder_id': wo.id, 'driver_name': driver_name, 'driver_rut': driver_rut, 'registered': registered})

        if request.method == 'POST':
            # plate must be chosen from validated list
            plate = (request.form.get('plate') or '').strip()
            company = request.form.get('company')

            if not plate:
                flash('Debe seleccionar una placa validada por recepción', 'danger')
                return render_template('vehicle_form.html', validated_plates=validated_plates)

            # ensure plate is indeed validated
            if not WorkOrder.query.filter_by(plate=plate, docs_valid=True).first():
                flash('La placa seleccionada no está validada por recepción', 'danger')
                return render_template('vehicle_form.html', validated_plates=validated_plates)

            # try to get driver info from latest AccessEntry first, fallback to WorkOrder
            ae = AccessEntry.query.filter_by(plate=plate).order_by(AccessEntry.created_at.desc()).first()
            driver_name = ae.driver_name if ae else None
            driver_rut = ae.driver_rut if ae else None
            if not driver_name or not driver_rut:
                wo0 = WorkOrder.query.filter_by(plate=plate, docs_valid=True).order_by(WorkOrder.created_at.desc()).first()
                if wo0:
                    driver_name = driver_name or wo0.driver_name
                    driver_rut = driver_rut or wo0.driver_rut

            # If the plate is already registered as a Vehicle, update its driver info and go to assign
            existing_v = Vehicle.query.filter_by(plate=plate).first()
            if existing_v:
                existing_v.driver_name = driver_name
                # also set a driver_rut attribute if model had one; Vehicle currently stores driver_name and company
                # We'll store driver_rut inside driver_name field if needed or extend model; for now attach to driver_name display
                db.session.add(existing_v)
                db.session.commit()
                flash('Vehículo actualizado con información del conductor. Redirigiendo a Asignar mecánico.', 'info')
                return redirect(url_for('assign_mechanic', vehicle_id=existing_v.id))

            # create new vehicle with driver info so it appears in the vehicles table
            v = Vehicle(plate=plate, driver_name=driver_name, company=company, created_by=current_user.id)
            db.session.add(v)
            db.session.commit()
            flash('Vehículo registrado', 'success')
            return redirect(url_for('vehicles_list'))

        return render_template('vehicle_form.html', validated_plates=validated_plates)

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    @app.route('/guard/entry/new', methods=['GET','POST'])
    @login_required
    @role_required('guard')
    def guard_entry_create():
        if request.method == 'POST':
            plate = (request.form.get('plate') or '').strip()
            driver_name = (request.form.get('driver_name') or '').strip()
            driver_rut = (request.form.get('driver_rut') or '').strip()
            region = (request.form.get('region') or '').strip()
            comuna = (request.form.get('comuna') or '').strip()
            files = request.files.getlist('photos')

            # Validación obligatoria: plate y al menos una foto
            if not plate:
                flash('Patente obligatoria', 'danger')
                return render_template('guard_entry_form.html')
            if not files or all(f.filename == '' for f in files):
                flash('Se requiere al menos una foto', 'danger')
                return render_template('guard_entry_form.html')

            saved_filenames = []
            for f in files:
                if f and f.filename:
                    if not allowed_file(f.filename):
                        flash(f'Formato de archivo no válido: {f.filename}', 'danger')
                        return render_template('guard_entry_form.html')
                    # secure filename: simple approach
                    fname = f"{int(__import__('time').time())}_{f.filename}"
                    dest = os.path.join(app.config['UPLOAD_FOLDER'], fname)
                    f.save(dest)
                    saved_filenames.append(fname)

            # create entry
            e = AccessEntry(
                plate=plate, 
                driver_name=driver_name or None, 
                driver_rut=driver_rut or None,
                region=region or None,
                comuna=comuna or None,
                created_by=current_user.id
            )
            db.session.add(e)
            db.session.commit()
            for fname in saved_filenames:
                p = AccessPhoto(entry_id=e.id, filename=fname)
                db.session.add(p)
            # commit photos
            db.session.commit()
            # create notifications to receptionists so they can see driver info
            try:
                from models import Notification, User
                recps = User.query.filter_by(role='receptionist').all()
                for r in recps:
                    msg = f"Ingreso: {plate} - Conductor: {driver_name or 'N/A'} - RUT: {driver_rut or 'N/A'} (registrado por {current_user.username})"
                    n = Notification(recipient_id=r.id, message=msg)
                    db.session.add(n)
                db.session.commit()
            except Exception:
                db.session.rollback()

            flash('Registro guardado correctamente y notificado a recepción', 'success')
            # Redirect back to form so guard can continue registering more entries
            return redirect(url_for('guard_entry_create'))
        return render_template('guard_entry_form.html')

    @app.route('/api/comunas/<region>')
    def get_comunas(region):
        """API endpoint para obtener comunas de una región específica"""
        from flask import jsonify
        comunas = REGIONES_COMUNAS.get(region, [])
        return jsonify(comunas)

    @app.route('/guard/entries/<int:entry_id>')
    @login_required
    @role_required('supervisor','admin','receptionist')
    def guard_entry_detail(entry_id):
        # supervisor, admin o receptionist consulta el ingreso
        from models import AccessEntry
        e = AccessEntry.query.get_or_404(entry_id)
        return render_template('guard_entry_detail.html', entry=e)

    @app.route('/guard/entries')
    @login_required
    @role_required('supervisor','admin','receptionist')
    def guard_entries_list():
        """Lista de todos los registros de ingreso del guardia"""
        from models import AccessEntry
        plate = request.args.get('plate')
        region = request.args.get('region')
        q = AccessEntry.query
        if plate:
            q = q.filter_by(plate=plate)
        if region:
            q = q.filter_by(region=region)
        entries = q.order_by(AccessEntry.created_at.desc()).all()
        return render_template('guard_entries_list.html', entries=entries, search_plate=plate, search_region=region, regiones=list(REGIONES_COMUNAS.keys()))

    # --- Ejecutivos de ventas: registrar devoluciones ---
    @app.route('/sales/return/new', methods=['GET','POST'])
    @login_required
    @role_required('sales')
    def sales_return_create():
        from models import Vehicle, ReturnRecord, ReturnPhoto, Notification, User
        if request.method == 'POST':
            vehicle_id = int(request.form.get('vehicle_id'))
            mileage = request.form.get('mileage')
            comment = request.form.get('comment')
            files = request.files.getlist('photos')

            # validation: vehicle must exist
            v = Vehicle.query.get_or_404(vehicle_id)

            # save record
            rr = ReturnRecord(vehicle_id=v.id, returned_by=current_user.id, mileage=(int(mileage) if mileage else None), comment=comment)
            db.session.add(rr)
            db.session.commit()

            saved = []
            for f in files:
                if f and f.filename:
                    if not allowed_file(f.filename):
                        flash(f'Formato de archivo no válido: {f.filename}', 'danger')
                        return render_template('sales_return_form.html')
                    fname = f"ret_{int(__import__('time').time())}_{f.filename}"
                    dest = os.path.join(app.config['UPLOAD_FOLDER'], fname)
                    f.save(dest)
                    p = ReturnPhoto(record_id=rr.id, filename=fname)
                    db.session.add(p)
                    saved.append(fname)
            # mark vehicle as available
            v.status = 'available'
            # optionally record mileage in a simple history field — here we use vehicle.updated_at and a notification
            db.session.commit()

            # If there is an active key assignment for this vehicle, close it and log the return
            try:
                from models import KeyAssignment, KeyLog
                ka = KeyAssignment.query.filter_by(plate=v.plate, active=True).first()
                if ka:
                    from datetime import datetime
                    ka.active = False
                    ka.returned_by = current_user.id
                    ka.returned_at = datetime.utcnow()
                    db.session.add(ka)
                    kl = KeyLog(plate=v.plate, action='return', performed_by=current_user.id, note='Closed due to vehicle return')
                    db.session.add(kl)
                    db.session.commit()
            except Exception:
                # don't block the main flow if logging fails
                db.session.rollback()

            # create notifications to supervisor and key manager
            sup_list = User.query.filter(User.role.in_(['supervisor','key_manager'])).all()
            for sup in sup_list:
                msg = f"Vehículo {v.plate} devuelto y disponible (registrado por {current_user.username})"
                n = Notification(recipient_id=sup.id, message=msg)
                db.session.add(n)
            db.session.commit()

            flash('Devolución registrada y vehículo marcado como Disponible', 'success')
            return redirect(url_for('sales_return_detail', record_id=rr.id))
        vehicles = Vehicle.query.order_by(Vehicle.plate).all()
        return render_template('sales_return_form.html', vehicles=vehicles)

    @app.route('/sales/return/<int:record_id>')
    @login_required
    @role_required('sales','supervisor','admin')
    def sales_return_detail(record_id):
        from models import ReturnRecord
        rr = ReturnRecord.query.get_or_404(record_id)
        return render_template('sales_return_detail.html', record=rr)

    # --- Encargado de llaves y documentos ---
    @app.route('/keys/dashboard')
    @login_required
    @role_required('key_manager', 'supervisor', 'admin')
    def keys_dashboard():
        from models import KeyAssignment, KeyLog, Vehicle
        from datetime import datetime, timedelta
        
        # Obtener estadísticas
        total_vehicles = Vehicle.query.count()
        active_assignments = KeyAssignment.query.filter_by(active=True).count()
        
        # Obtener devoluciones y entregas de hoy
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_returns = KeyLog.query.filter(
            KeyLog.action == 'return',
            KeyLog.created_at >= today_start
        ).count()
        
        today_deliveries = KeyLog.query.filter(
            KeyLog.action == 'delivery',
            KeyLog.created_at >= today_start
        ).count()
        
        # Obtener llaves actualmente asignadas
        active_keys = KeyAssignment.query.filter_by(active=True).order_by(KeyAssignment.assigned_at.desc()).all()
        
        # Obtener actividad reciente (últimos 10 registros)
        recent_logs = KeyLog.query.order_by(KeyLog.created_at.desc()).limit(10).all()
        
        return render_template('keys_dashboard.html',
                             total_vehicles=total_vehicles,
                             active_assignments=active_assignments,
                             today_returns=today_returns,
                             today_deliveries=today_deliveries,
                             active_keys=active_keys,
                             recent_logs=recent_logs,
                             now=datetime.utcnow())

    @app.route('/keys/assign', methods=['GET','POST'])
    @login_required
    @role_required('key_manager')
    def keys_assign():
        # La funcionalidad de registrar entrega fue removida para el encargado de llaves.
        # Redirigimos al dashboard de llaves para que use las opciones disponibles.
        flash('La entrega de llaves ya no se registra aquí. Utilice el Dashboard para gestionar llaves.', 'info')
        return redirect(url_for('keys_dashboard'))

    @app.route('/keys/return', methods=['GET','POST'])
    @login_required
    @role_required('key_manager')
    def keys_return():
        from models import KeyAssignment, KeyLog, Vehicle
        if request.method == 'POST':
            plate = (request.form.get('plate') or '').strip()
            if not plate:
                flash('Patente obligatoria', 'danger')
                return render_template('key_return_form.html')
            # ensure plate exists
            if not Vehicle.query.filter_by(plate=plate).first():
                flash('La patente no existe en el sistema', 'danger')
                return render_template('key_return_form.html')
            existing = KeyAssignment.query.filter_by(plate=plate, active=True).first()
            if not existing:
                flash('No hay llave asignada para esta patente', 'warning')
                return render_template('key_return_form.html')
            existing.active = False
            existing.returned_by = current_user.id
            from datetime import datetime
            existing.returned_at = datetime.utcnow()
            kl = KeyLog(plate=plate, action='return', performed_by=current_user.id, note='Returned')
            db.session.add(kl)
            db.session.commit()
            flash('Devolución registrada y ciclo cerrado', 'success')
            return redirect(url_for('keys_history', plate=plate))
        vehicles = Vehicle.query.order_by(Vehicle.plate).all()
        return render_template('key_return_form.html', vehicles=vehicles)

    @app.route('/keys/history')
    @login_required
    @role_required('key_manager','supervisor','admin')
    def keys_history():
        from models import KeyLog
        plate = request.args.get('plate')
        query = KeyLog.query
        if plate:
            query = query.filter_by(plate=plate)
        logs = query.order_by(KeyLog.created_at.desc()).all()
        return render_template('key_history.html', logs=logs, plate=plate)

    # --- Receptionist: work order management ---
    @app.route('/reception/workorders')
    @login_required
    @role_required('receptionist')
    def reception_workorders():
        from models import WorkOrder
        plate = request.args.get('plate')
        q = WorkOrder.query
        if plate:
            q = q.filter_by(plate=plate)
        orders = q.order_by(WorkOrder.created_at.desc()).all()
        # build map plate -> latest access entry (driver info)
        plates = {o.plate for o in orders}
        plate_driver_info = {}
        for p in plates:
            ae = AccessEntry.query.filter_by(plate=p).order_by(AccessEntry.created_at.desc()).first()
            if ae:
                plate_driver_info[p] = {'driver_name': ae.driver_name, 'driver_rut': ae.driver_rut}
            else:
                plate_driver_info[p] = {'driver_name': None, 'driver_rut': None}

        return render_template('receptionist_workorders.html', orders=orders, plate_driver_info=plate_driver_info)

    @app.route('/reception/workorders/new', methods=['GET','POST'])
    @login_required
    @role_required('receptionist')
    def reception_workorder_create():
        from models import WorkOrder, AccessEntry

        # collect recent access entries recorded by guards (most recent first)
        guard_entries = AccessEntry.query.order_by(AccessEntry.created_at.desc()).limit(200).all()

        if request.method == 'POST':
            # receptionist may select an access_entry (preferred) or enter a raw plate
            access_entry_id = request.form.get('access_entry_id')
            plate = None
            driver_name = None
            driver_rut = None
            if access_entry_id:
                ae = AccessEntry.query.get(int(access_entry_id))
                if not ae:
                    flash('Registro de guardia no válido', 'danger')
                    return render_template('receptionist_form.html', guard_entries=guard_entries)
                plate = (ae.plate or '').strip()
                driver_name = ae.driver_name
                driver_rut = ae.driver_rut
            else:
                plate = (request.form.get('plate') or '').strip()

            docs_valid = bool(request.form.get('docs_valid'))
            notes = request.form.get('notes')

            if not plate:
                flash('Patente obligatoria', 'danger')
                return render_template('receptionist_form.html', guard_entries=guard_entries, plate=plate)

            # simple duplicate check: existing open or blocked order for same plate
            existing = WorkOrder.query.filter(WorkOrder.plate==plate, WorkOrder.status.in_(['open','blocked'])).first()
            if existing:
                flash('Existe un registro activo/pendiente para esta patente (posible duplicado)', 'warning')
                return redirect(url_for('reception_workorder_detail', order_id=existing.id))

            wo = WorkOrder(plate=plate, created_by=current_user.id, docs_valid=docs_valid, status=('open' if docs_valid else 'blocked'), notes=notes, driver_name=driver_name, driver_rut=driver_rut)
            db.session.add(wo)
            db.session.commit()
            flash('OT creada', 'success')
            return redirect(url_for('reception_workorders'))

        return render_template('receptionist_form.html', guard_entries=guard_entries)

    @app.route('/reception/workorders/<int:order_id>')
    @login_required
    @role_required('receptionist')
    def reception_workorder_detail(order_id):
        from models import WorkOrder
        wo = WorkOrder.query.get_or_404(order_id)
        return render_template('workorder_detail.html', order=wo)

    @app.route('/reception/workorders/<int:order_id>/mark_duplicate')
    @login_required
    @role_required('receptionist')
    def reception_mark_duplicate(order_id):
        from models import WorkOrder
        wo = WorkOrder.query.get_or_404(order_id)
        wo.status = 'duplicate'
        db.session.commit()
        flash('OT marcada como duplicada', 'info')
        return redirect(url_for('reception_workorder_detail', order_id=order_id))

    @app.route('/reception/workorders/<int:order_id>/unblock')
    @login_required
    @role_required('receptionist')
    def reception_unblock(order_id):
        from models import WorkOrder
        wo = WorkOrder.query.get_or_404(order_id)
        wo.status = 'open'
        wo.docs_valid = True
        db.session.commit()
        flash('OT desbloqueada y documentos validados', 'success')
        return redirect(url_for('reception_workorder_detail', order_id=order_id))

    @app.route('/vehicles/<int:vehicle_id>/approve')
    @login_required
    @role_required('admin','supervisor','gatekeeper')
    def vehicle_approve(vehicle_id):
        v = Vehicle.query.get_or_404(vehicle_id)
        v.status = 'approved'
        v.approved_by = current_user.id
        from datetime import datetime
        v.approved_at = datetime.utcnow()
        db.session.commit()
        flash('Vehículo aprobado', 'success')
        return redirect(url_for('vehicles_list'))

    @app.route('/vehicles/<int:vehicle_id>/reject')
    @login_required
    @role_required('admin','supervisor')
    def vehicle_reject(vehicle_id):
        v = Vehicle.query.get_or_404(vehicle_id)
        v.status = 'rejected'
        v.approved_by = current_user.id
        from datetime import datetime
        v.approved_at = datetime.utcnow()
        db.session.commit()
        flash('Vehículo rechazado', 'warning')
        return redirect(url_for('vehicles_list'))

    @app.route('/health')
    def health():
        # simple health endpoint for local connectivity checks
        return 'ok', 200

    # Compute average background color from a static image at startup (optional)
    def _compute_average_color(image_path):
        try:
            from PIL import Image
            img = Image.open(image_path).convert('RGBA')
            # downscale for speed
            img.thumbnail((100,100))
            px = list(img.getdata())
            r=g=b=count=0
            for pr,pg,pb,pa in px:
                if pa==0: continue
                r += pr; g += pg; b += pb; count += 1
            if count==0: return None
            r = int(r/count); g = int(g/count); b = int(b/count)
            return '#%02x%02x%02x' % (r,g,b)
        except Exception:
            return None

    # Attempt to compute color for brand image
    try:
        brand_img = os.path.join(BASE_DIR, 'static', 'brand_images', 'camion.png')
        app.config['BG_COLOR'] = _compute_average_color(brand_img) or None
    except Exception:
        app.config['BG_COLOR'] = None

    @app.context_processor
    def inject_bg_color():
        return {'bg_color': app.config.get('BG_COLOR')}

    # --- Admin: create users from the web UI ---
    @app.route('/admin/users/new', methods=['GET', 'POST'])
    @login_required
    @role_required('admin')
    def admin_user_create():
        from models import User, UserProfile
        if request.method == 'POST':
            username = (request.form.get('username') or '').strip()
            password = request.form.get('password')
            role = request.form.get('role') or 'operator'
            full_name = request.form.get('full_name')
            function = request.form.get('function')

            if not username or not password:
                flash('Usuario y contraseña son obligatorios', 'danger')
                return render_template('user_form.html')

            if User.query.filter_by(username=username).first():
                flash('Usuario ya existe', 'warning')
                return render_template('user_form.html')

            u = User(username=username, role=role)
            u.set_password(password)
            db.session.add(u)
            db.session.commit()

            # If creating a mechanic user, create the Mechanic profile and link it
            if role == 'mechanic':
                try:
                    m = Mechanic(name=(full_name or username), phone=None, user_id=u.id)
                    db.session.add(m)
                    db.session.commit()
                except Exception:
                    db.session.rollback()

            if full_name or function:
                p = UserProfile(user_id=u.id, full_name=full_name, function=function)
                db.session.add(p)
                db.session.commit()

            flash(f'Usuario {username} creado con rol {role}', 'success')
            return redirect(url_for('dashboard'))

        return render_template('user_form.html')

    @app.route('/admin/users')
    @login_required
    @role_required('admin')
    def admin_users_list():
        # Mostrar todos los usuarios al admin (passwords se muestran como hashes)
        users = User.query.order_by(User.username).all()
        return render_template('admin_users.html', users=users)

    @app.route('/admin/users/<int:user_id>/reset_password', methods=['POST'])
    @login_required
    @role_required('admin')
    def admin_user_reset_password(user_id):
        # Genera una contraseña temporal segura, la guarda (como hash) y la muestra una sola vez.
        from secrets import token_urlsafe
        u = User.query.get_or_404(user_id)
        # token_urlsafe(9) produce ~12 caracteres URL-safe; suficiente para un password temporal
        new_pw = token_urlsafe(9)
        u.set_password(new_pw)
        db.session.add(u)
        db.session.commit()
        return render_template('admin_show_password.html', user=u, new_password=new_pw)

    @app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
    @login_required
    @role_required('admin')
    def admin_user_delete(user_id):
        # Prevent self-deletion
        if current_user.id == user_id:
            flash('No puedes eliminar tu propio usuario mientras estés logueado', 'warning')
            return redirect(url_for('admin_users_list'))
        u = User.query.get_or_404(user_id)
        try:
            # If user has linked mechanic or profile records, attempt to remove or detach safely
            from models import Mechanic, UserProfile
            mech = Mechanic.query.filter_by(user_id=u.id).first()
            if mech:
                db.session.delete(mech)
            prof = UserProfile.query.filter_by(user_id=u.id).first()
            if prof:
                db.session.delete(prof)
            db.session.delete(u)
            db.session.commit()
            flash(f'Usuario {u.username} eliminado', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error al eliminar usuario: '+str(e), 'danger')
        return redirect(url_for('admin_users_list'))

    # ==================== PARTS MANAGEMENT (Asistente de Repuestos) ====================
    
    @app.route('/parts/dashboard')
    @login_required
    @role_required('parts_assistant')
    def parts_dashboard():
        """Dashboard principal del asistente de repuestos"""
        parts = Part.query.order_by(Part.code).all()
        # Alertas de stock bajo
        low_stock_parts = [p for p in parts if p.stock <= p.min_stock]
        recent_deliveries = PartDelivery.query.order_by(PartDelivery.created_at.desc()).limit(10).all()
        # Contar solicitudes pendientes
        pending_requests_count = PartRequest.query.filter_by(status='pending').count()
        return render_template('parts_dashboard.html', 
                             parts=parts, 
                             low_stock_parts=low_stock_parts,
                             recent_deliveries=recent_deliveries,
                             pending_requests_count=pending_requests_count)
    
    @app.route('/parts/list')
    @login_required
    @role_required('parts_assistant')
    def parts_list():
        """Lista completa de repuestos"""
        parts = Part.query.order_by(Part.code).all()
        return render_template('parts_list.html', parts=parts)
    
    @app.route('/parts/new', methods=['GET', 'POST'])
    @login_required
    @role_required('parts_assistant')
    def part_create():
        """Crear nuevo repuesto"""
        if request.method == 'POST':
            code = request.form['code'].strip()
            name = request.form['name'].strip()
            description = request.form.get('description', '').strip()
            stock = int(request.form.get('stock', 0))
            min_stock = int(request.form.get('min_stock', 0))
            
            # Verificar si el código ya existe
            existing = Part.query.filter_by(code=code).first()
            if existing:
                flash(f'Ya existe un repuesto con código {code}', 'danger')
                return redirect(url_for('part_create'))
            
            part = Part(
                code=code,
                name=name,
                description=description,
                stock=stock,
                min_stock=min_stock,
                created_by=current_user.id
            )
            db.session.add(part)
            db.session.commit()
            flash(f'Repuesto {code} - {name} agregado exitosamente', 'success')
            return redirect(url_for('parts_dashboard'))
        
        return render_template('part_form.html')
    
    @app.route('/parts/<int:part_id>/edit', methods=['GET', 'POST'])
    @login_required
    @role_required('parts_assistant')
    def part_edit(part_id):
        """Editar repuesto existente"""
        part = Part.query.get_or_404(part_id)
        
        if request.method == 'POST':
            part.name = request.form['name'].strip()
            part.description = request.form.get('description', '').strip()
            part.stock = int(request.form.get('stock', 0))
            part.min_stock = int(request.form.get('min_stock', 0))
            
            db.session.commit()
            flash(f'Repuesto {part.code} actualizado', 'success')
            return redirect(url_for('parts_dashboard'))
        
        return render_template('part_form.html', part=part)
    
    @app.route('/parts/delivery/new', methods=['GET', 'POST'])
    @login_required
    @role_required('parts_assistant')
    def part_delivery_create():
        """Registrar entrega de repuesto a mecánico"""
        if request.method == 'POST':
            try:
                part_id = int(request.form['part_id'])
                mechanic_id = int(request.form['mechanic_id'])
                quantity = int(request.form['quantity'])
            except (ValueError, KeyError):
                flash('Datos inválidos en el formulario', 'danger')
                parts = Part.query.filter(Part.stock > 0).order_by(Part.code).all()
                mechanics = Mechanic.query.order_by(Mechanic.name).all()
                assignments = Assignment.query.order_by(Assignment.assigned_at.desc()).limit(50).all()
                return render_template('part_delivery_form.html', 
                                     parts=parts, 
                                     mechanics=mechanics,
                                     assignments=assignments)
            
            assignment_id = request.form.get('assignment_id')
            note = request.form.get('note', '').strip()
            
            part = Part.query.get_or_404(part_id)
            
            # Verificar que la cantidad sea positiva
            if quantity <= 0:
                flash('La cantidad debe ser mayor a 0', 'danger')
                parts = Part.query.filter(Part.stock > 0).order_by(Part.code).all()
                mechanics = Mechanic.query.order_by(Mechanic.name).all()
                assignments = Assignment.query.order_by(Assignment.assigned_at.desc()).limit(50).all()
                return render_template('part_delivery_form.html', 
                                     parts=parts, 
                                     mechanics=mechanics,
                                     assignments=assignments)
            
            # Verificar stock disponible
            if part.stock < quantity:
                flash(f'Stock insuficiente. Disponible: {part.stock}, Solicitado: {quantity}', 'danger')
                parts = Part.query.filter(Part.stock > 0).order_by(Part.code).all()
                mechanics = Mechanic.query.order_by(Mechanic.name).all()
                assignments = Assignment.query.order_by(Assignment.assigned_at.desc()).limit(50).all()
                return render_template('part_delivery_form.html', 
                                     parts=parts, 
                                     mechanics=mechanics,
                                     assignments=assignments)
            
            # Crear registro de entrega
            delivery = PartDelivery(
                part_id=part_id,
                mechanic_id=mechanic_id,
                assignment_id=int(assignment_id) if assignment_id else None,
                quantity=quantity,
                delivered_by=current_user.id,
                note=note
            )
            
            # Actualizar stock
            part.stock -= quantity
            
            db.session.add(delivery)
            db.session.commit()
            
            flash(f'Entrega registrada: {quantity} unidades de {part.code} - {part.name}', 'success')
            return redirect(url_for('parts_dashboard'))
        
        # GET: Mostrar formulario
        parts = Part.query.filter(Part.stock > 0).order_by(Part.code).all()
        mechanics = Mechanic.query.order_by(Mechanic.name).all()
        assignments = Assignment.query.order_by(Assignment.assigned_at.desc()).limit(50).all()
        
        return render_template('part_delivery_form.html', 
                             parts=parts, 
                             mechanics=mechanics,
                             assignments=assignments)
    
    @app.route('/parts/delivery/history')
    @login_required
    @role_required('parts_assistant')
    def part_delivery_history():
        """Historial completo de entregas"""
        deliveries = PartDelivery.query.order_by(PartDelivery.created_at.desc()).all()
        return render_template('part_delivery_history.html', deliveries=deliveries)
    
    @app.route('/parts/requests')
    @login_required
    @role_required('parts_assistant')
    def parts_requests_list():
        """Lista de solicitudes de repuestos pendientes y procesadas"""
        pending_requests = PartRequest.query.filter_by(status='pending').order_by(PartRequest.requested_at.desc()).all()
        processed_requests = PartRequest.query.filter(PartRequest.status != 'pending').order_by(PartRequest.processed_at.desc()).limit(50).all()
        return render_template('parts_requests_list.html', 
                             pending_requests=pending_requests,
                             processed_requests=processed_requests)
    
    @app.route('/parts/requests/<int:request_id>/process', methods=['POST'])
    @login_required
    @role_required('parts_assistant')
    def parts_request_process(request_id):
        """Procesar solicitud (aprobar/rechazar)"""
        part_request = PartRequest.query.get_or_404(request_id)
        
        action = request.form.get('action')  # 'approve' or 'reject'
        response_note = request.form.get('response_note', '').strip()
        
        if action == 'approve':
            part = Part.query.get(part_request.part_id)
            
            # Verificar stock disponible
            if part.stock < part_request.quantity:
                flash(f'Stock insuficiente. Disponible: {part.stock}, Solicitado: {part_request.quantity}', 'danger')
                return redirect(url_for('parts_requests_list'))
            
            # Aprobar y crear entrega automáticamente
            part_request.status = 'approved'
            part_request.processed_by = current_user.id
            from datetime import datetime
            part_request.processed_at = datetime.utcnow()
            part_request.response_note = response_note
            
            # Crear entrega
            delivery = PartDelivery(
                part_id=part_request.part_id,
                mechanic_id=part_request.mechanic_id,
                assignment_id=part_request.assignment_id,
                quantity=part_request.quantity,
                delivered_by=current_user.id,
                note=f"Entrega de solicitud #{part_request.id}: {part_request.note or ''}"
            )
            
            # Actualizar stock
            part.stock -= part_request.quantity
            
            # Cambiar estado a delivered
            part_request.status = 'delivered'
            
            db.session.add(delivery)
            db.session.commit()
            
            flash(f'Solicitud aprobada y entregada: {part_request.quantity} unidades de {part.code}', 'success')
        
        elif action == 'reject':
            part_request.status = 'rejected'
            part_request.processed_by = current_user.id
            from datetime import datetime
            part_request.processed_at = datetime.utcnow()
            part_request.response_note = response_note
            db.session.commit()
            
            flash('Solicitud rechazada', 'info')
        
        return redirect(url_for('parts_requests_list'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

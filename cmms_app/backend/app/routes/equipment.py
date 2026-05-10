"""
Equipment management routes - CRUD operations
"""

from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from werkzeug.utils import secure_filename
import os
from ..models import (
    db, Equipment, AssetCategory, Department, Building, Floor, Room,
    ChecklistTemplate, ChecklistItem, PMSchedule, Attachment, AuditLog, User
)

equipment_bp = Blueprint('equipment', __name__)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@equipment_bp.route('', methods=['GET'])
@jwt_required()
def get_equipment_list():
    """Get all equipment with filters and pagination"""
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category_id = request.args.get('category_id', type=int)
    department_id = request.args.get('department_id', type=int)
    status = request.args.get('status')
    search = request.args.get('search')
    location = request.args.get('location')
    
    # Build query
    query = Equipment.query
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if department_id:
        query = query.filter_by(department_id=department_id)
    
    if status:
        query = query.filter_by(status=status)
    
    if search:
        query = query.filter(
            (Equipment.name.ilike(f'%{search}%')) |
            (Equipment.brand.ilike(f'%{search}%')) |
            (Equipment.model.ilike(f'%{search}%')) |
            (Equipment.serial_number.ilike(f'%{search}%'))
        )
    
    if location:
        query = query.filter(
            (Equipment.location.ilike(f'%{location}%')) |
            (Equipment.sub_location.ilike(f'%{location}%'))
        )
    
    # Order by name
    query = query.order_by(Equipment.name)
    
    # Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    equipment_list = pagination.items
    
    return jsonify({
        'equipment': [eq.to_dict() for eq in equipment_list],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    }), 200


@equipment_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_equipment(id):
    """Get single equipment by ID"""
    equipment = Equipment.query.get_or_404(id)
    
    # Get related data
    checklist_templates = ChecklistTemplate.query.filter_by(equipment_id=id).all()
    pm_schedules = PMSchedule.query.filter_by(equipment_id=id).all()
    work_orders = equipment.work_orders.order_by(db.desc('created_at')).limit(10).all()
    attachments = Attachment.query.filter_by(equipment_id=id).all()
    
    return jsonify({
        'equipment': equipment.to_dict(),
        'checklist_templates': [t.to_dict() for t in checklist_templates],
        'pm_schedules': [s.to_dict() for s in pm_schedules],
        'recent_work_orders': [wo.to_dict() for wo in work_orders],
        'attachments': [a.to_dict() for a in attachments]
    }), 200


@equipment_bp.route('', methods=['POST'])
@jwt_required()
def create_equipment():
    """Create new equipment"""
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    
    # Check permission
    if claims.get('role') not in ['super_admin', 'maintenance_engineer']:
        return jsonify({'error': 'Unauthorized - Engineer or Admin access required'}), 403
    
    data = request.get_json()
    
    # Required fields
    required_fields = ['name', 'category_id']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    # Check for duplicate asset tag
    if data.get('asset_tag') and Equipment.query.filter_by(asset_tag=data['asset_tag']).first():
        return jsonify({'error': 'Asset tag already exists'}), 400
    
    # Parse dates
    purchase_date = None
    if data.get('purchase_date'):
        try:
            purchase_date = datetime.fromisoformat(data['purchase_date']).date()
        except:
            return jsonify({'error': 'Invalid purchase_date format'}), 400
    
    warranty_expiry_date = None
    if data.get('warranty_expiry_date'):
        try:
            warranty_expiry_date = datetime.fromisoformat(data['warranty_expiry_date']).date()
        except:
            return jsonify({'error': 'Invalid warranty_expiry_date format'}), 400
    
    next_pm_date = None
    if data.get('next_pm_date'):
        try:
            next_pm_date = datetime.fromisoformat(data['next_pm_date']).date()
        except:
            return jsonify({'error': 'Invalid next_pm_date format'}), 400
    
    # Create equipment
    equipment = Equipment(
        name=data['name'],
        category_id=data['category_id'],
        department_id=data.get('department_id'),
        location=data.get('location'),
        sub_location=data.get('sub_location'),
        building_id=data.get('building_id'),
        floor_id=data.get('floor_id'),
        room_id=data.get('room_id'),
        brand=data.get('brand'),
        model=data.get('model'),
        serial_number=data.get('serial_number'),
        asset_tag=data.get('asset_tag'),
        purchase_date=purchase_date,
        warranty_expiry_date=warranty_expiry_date,
        installation_date=data.get('installation_date'),
        expected_lifetime_years=data.get('expected_lifetime_years'),
        pm_frequency=data.get('pm_frequency'),
        last_pm_date=data.get('last_pm_date'),
        next_pm_date=next_pm_date,
        pm_duration_minutes=data.get('pm_duration_minutes', 60),
        status=data.get('status', 'active'),
        condition=data.get('condition', 'good'),
        specifications=data.get('specifications'),
        notes=data.get('notes'),
        created_by=current_user_id
    )
    
    db.session.add(equipment)
    db.session.commit()
    
    # Log action
    audit_log = AuditLog(
        user_id=current_user_id,
        action='CREATE',
        entity_type='Equipment',
        entity_id=equipment.id,
        new_values=f'Created equipment: {equipment.name}',
        ip_address=request.remote_addr
    )
    db.session.add(audit_log)
    db.session.commit()
    
    return jsonify({
        'message': 'Equipment created successfully',
        'equipment': equipment.to_dict()
    }), 201


@equipment_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_equipment(id):
    """Update existing equipment"""
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    
    # Check permission
    if claims.get('role') not in ['super_admin', 'maintenance_engineer']:
        return jsonify({'error': 'Unauthorized - Engineer or Admin access required'}), 403
    
    equipment = Equipment.query.get_or_404(id)
    data = request.get_json()
    
    # Update fields
    updatable_fields = [
        'name', 'category_id', 'department_id', 'location', 'sub_location',
        'building_id', 'floor_id', 'room_id', 'brand', 'model', 'serial_number',
        'purchase_date', 'warranty_expiry_date', 'installation_date',
        'expected_lifetime_years', 'pm_frequency', 'last_pm_date', 'next_pm_date',
        'pm_duration_minutes', 'status', 'condition', 'specifications', 'notes'
    ]
    
    old_values = equipment.to_dict()
    
    for field in updatable_fields:
        if field in data:
            setattr(equipment, field, data[field])
    
    # Handle asset_tag separately (must be unique)
    if 'asset_tag' in data and data['asset_tag'] != equipment.asset_tag:
        if Equipment.query.filter_by(asset_tag=data['asset_tag']).first():
            return jsonify({'error': 'Asset tag already exists'}), 400
        equipment.asset_tag = data['asset_tag']
    
    db.session.commit()
    
    # Log action
    audit_log = AuditLog(
        user_id=current_user_id,
        action='UPDATE',
        entity_type='Equipment',
        entity_id=equipment.id,
        old_values=str(old_values),
        new_values=str(equipment.to_dict()),
        ip_address=request.remote_addr
    )
    db.session.add(audit_log)
    db.session.commit()
    
    return jsonify({
        'message': 'Equipment updated successfully',
        'equipment': equipment.to_dict()
    }), 200


@equipment_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_equipment(id):
    """Delete equipment (soft delete by setting status)"""
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    
    # Check permission
    if claims.get('role') != 'super_admin':
        return jsonify({'error': 'Unauthorized - Admin access required'}), 403
    
    equipment = Equipment.query.get_or_404(id)
    
    # Soft delete - set status to decommissioned
    old_status = equipment.status
    equipment.status = 'decommissioned'
    db.session.commit()
    
    # Log action
    audit_log = AuditLog(
        user_id=current_user_id,
        action='DELETE',
        entity_type='Equipment',
        entity_id=equipment.id,
        old_values=f'Status: {old_status}',
        new_values='Status: decommissioned',
        ip_address=request.remote_addr
    )
    db.session.add(audit_log)
    db.session.commit()
    
    return jsonify({'message': 'Equipment decommissioned successfully'}), 200


@equipment_bp.route('/<int:id>/upload-photo', methods=['POST'])
@jwt_required()
def upload_equipment_photo(id):
    """Upload equipment photo"""
    current_user_id = get_jwt_identity()
    equipment = Equipment.query.get_or_404(id)
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    # Save file
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
    filename = f"{timestamp}{filename}"
    
    upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'equipment')
    os.makedirs(upload_folder, exist_ok=True)
    
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    
    # Update equipment
    equipment.photo_path = file_path
    db.session.commit()
    
    # Create attachment record
    attachment = Attachment(
        equipment_id=equipment.id,
        file_path=file_path,
        file_name=filename,
        file_type='image',
        file_size=os.path.getsize(file_path),
        uploaded_by=current_user_id
    )
    db.session.add(attachment)
    db.session.commit()
    
    return jsonify({
        'message': 'Photo uploaded successfully',
        'photo_path': file_path
    }), 200


@equipment_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """Get all asset categories"""
    categories = AssetCategory.query.order_by(AssetCategory.name).all()
    return jsonify({
        'categories': [cat.to_dict() for cat in categories]
    }), 200


@equipment_bp.route('/departments', methods=['GET'])
@jwt_required()
def get_departments():
    """Get all departments"""
    departments = Department.query.order_by(Department.name).all()
    return jsonify({
        'departments': [dept.to_dict() for dept in departments]
    }), 200


@equipment_bp.route('/<int:id>/history', methods=['GET'])
@jwt_required()
def get_equipment_history(id):
    """Get full maintenance history for equipment"""
    equipment = Equipment.query.get_or_404(id)
    
    # Get all work orders
    work_orders = equipment.work_orders.order_by(db.desc('scheduled_date')).all()
    
    history = []
    for wo in work_orders:
        checklist_results = wo.checklist_results.all()
        spare_parts = wo.spare_parts.all()
        
        history.append({
            'work_order': wo.to_dict(),
            'checklist_results': [r.to_dict() for r in checklist_results],
            'spare_parts': [sp.to_dict() for sp in spare_parts]
        })
    
    return jsonify({
        'equipment': equipment.to_dict(),
        'history': history,
        'total_work_orders': len(work_orders)
    }), 200

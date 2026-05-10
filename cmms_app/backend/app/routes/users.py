"""
User management routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ..models import db, User, Department, AuditLog

users_bp = Blueprint('users', __name__)


@users_bp.route('', methods=['GET'])
@jwt_required()
def get_users():
    """Get all users"""
    claims = get_jwt()
    
    if claims.get('role') not in ['super_admin', 'maintenance_engineer']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    department_id = request.args.get('department_id', type=int)
    role = request.args.get('role')
    
    query = User.query
    if department_id:
        query = query.filter_by(department_id=department_id)
    if role:
        query = query.filter_by(role=role)
    
    users = query.order_by(User.name).all()
    return jsonify({'users': [u.to_dict() for u in users]}), 200


@users_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    """Get single user"""
    claims = get_jwt()
    if claims.get('role') not in ['super_admin', 'maintenance_engineer']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get_or_404(id)
    return jsonify({'user': user.to_dict()}), 200


@users_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    """Update user"""
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    
    if claims.get('role') != 'super_admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    user = User.query.get_or_404(id)
    data = request.get_json()
    
    updatable = ['name', 'role', 'department_id', 'whatsapp', 'is_active']
    for field in updatable:
        if field in data:
            setattr(user, field, data[field])
    
    db.session.commit()
    
    audit_log = AuditLog(
        user_id=current_user_id,
        action='UPDATE',
        entity_type='User',
        entity_id=user.id,
        ip_address=request.remote_addr
    )
    db.session.add(audit_log)
    db.session.commit()
    
    return jsonify({'message': 'User updated', 'user': user.to_dict()}), 200


@users_bp.route('/technicians', methods=['GET'])
@jwt_required()
def get_technicians():
    """Get all technicians"""
    technicians = User.query.filter_by(role='technician', is_active=True).all()
    return jsonify({
        'technicians': [t.to_dict() for t in technicians]
    }), 200


@users_bp.route('/<int:id>/signature', methods=['POST'])
@jwt_required()
def upload_signature(id):
    """Upload user signature"""
    from werkzeug.utils import secure_filename
    from datetime import datetime
    import os
    from flask import current_app
    
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    
    # Only allow updating own signature or admin
    if current_user_id != id and claims.get('role') != 'super_admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get_or_404(id)
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
    filename = f"{timestamp}{filename}"
    
    upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'signatures')
    os.makedirs(upload_folder, exist_ok=True)
    
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    
    # Update or create signature record
    from ..models import Signature
    sig = Signature.query.filter_by(user_id=id, is_active=True).first()
    if sig:
        sig.signature_image_path = file_path
    else:
        sig = Signature(
            user_id=id,
            signature_image_path=file_path,
            signature_text=user.name
        )
        db.session.add(sig)
    
    db.session.commit()
    
    return jsonify({'message': 'Signature uploaded', 'path': file_path}), 200

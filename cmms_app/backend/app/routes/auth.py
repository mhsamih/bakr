"""
Authentication routes - Login, Logout, Token refresh
"""

from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from ..models import db, User, AuditLog

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    # Find user
    user = User.query.filter_by(email=email).first()
    
    if not user or not user.check_password(password):
        # Log failed attempt
        audit_log = AuditLog(
            action='LOGIN_FAILED',
            entity_type='User',
            entity_id=None,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(audit_log)
        db.session.commit()
        
        return jsonify({'error': 'Invalid email or password'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Account is deactivated'}), 403
    
    # Create tokens
    additional_claims = {'role': user.role}
    access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=user.id)
    
    # Log successful login
    audit_log = AuditLog(
        user_id=user.id,
        action='LOGIN',
        entity_type='User',
        entity_id=user.id,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent')
    )
    db.session.add(audit_log)
    db.session.commit()
    
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict(),
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer'
    }), 200


@auth_bp.route('/register', methods=['POST'])
@jwt_required()
def register():
    """Register new user (Admin only)"""
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    
    if claims.get('role') not in ['super_admin']:
        return jsonify({'error': 'Unauthorized - Admin access required'}), 403
    
    data = request.get_json()
    
    required_fields = ['name', 'email', 'password', 'role']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create new user
    user = User(
        name=data['name'],
        email=data['email'],
        role=data['role'],
        department_id=data.get('department_id'),
        whatsapp=data.get('whatsapp')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    
    # Log action
    audit_log = AuditLog(
        user_id=current_user_id,
        action='CREATE',
        entity_type='User',
        entity_id=None,
        new_values=f'Created user: {data["email"]}',
        ip_address=request.remote_addr
    )
    db.session.add(audit_log)
    db.session.commit()
    
    return jsonify({
        'message': 'User created successfully',
        'user': user.to_dict()
    }), 201


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_active:
        return jsonify({'error': 'User not found or inactive'}), 401
    
    additional_claims = {'role': user.role}
    new_access_token = create_access_token(identity=current_user_id, additional_claims=additional_claims)
    
    return jsonify({
        'access_token': new_access_token,
        'token_type': 'Bearer'
    }), 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """User logout"""
    current_user_id = get_jwt_identity()
    
    # Log logout
    audit_log = AuditLog(
        user_id=current_user_id,
        action='LOGOUT',
        entity_type='User',
        entity_id=current_user_id,
        ip_address=request.remote_addr
    )
    db.session.add(audit_log)
    db.session.commit()
    
    return jsonify({'message': 'Logout successful'}), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current logged-in user info"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'user': user.to_dict()
    }), 200


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    if not current_password or not new_password:
        return jsonify({'error': 'Current and new password are required'}), 400
    
    if not user.check_password(current_password):
        return jsonify({'error': 'Current password is incorrect'}), 401
    
    if len(new_password) < 6:
        return jsonify({'error': 'New password must be at least 6 characters'}), 400
    
    user.set_password(new_password)
    db.session.commit()
    
    # Log action
    audit_log = AuditLog(
        user_id=current_user_id,
        action='PASSWORD_CHANGE',
        entity_type='User',
        entity_id=current_user_id,
        ip_address=request.remote_addr
    )
    db.session.add(audit_log)
    db.session.commit()
    
    return jsonify({'message': 'Password changed successfully'}), 200

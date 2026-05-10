"""
Work Orders management routes
"""

from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ..models import (
    db, WorkOrder, Equipment, ChecklistTemplate, ChecklistItem, ChecklistResult,
    SparePartUsed, Notification, User, AuditLog
)

work_orders_bp = Blueprint('work_orders', __name__)


@work_orders_bp.route('', methods=['GET'])
@jwt_required()
def get_work_orders():
    """Get all work orders with filters"""
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    equipment_id = request.args.get('equipment_id', type=int)
    assigned_to = request.args.get('assigned_to', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    wo_type = request.args.get('type')
    
    query = WorkOrder.query
    
    # Role-based filtering
    if claims.get('role') == 'technician':
        query = query.filter_by(assigned_to=current_user_id)
    elif assigned_to:
        query = query.filter_by(assigned_to=assigned_to)
    
    if status:
        query = query.filter_by(status=status)
    
    if equipment_id:
        query = query.filter_by(equipment_id=equipment_id)
    
    if wo_type:
        query = query.filter_by(wo_type=wo_type)
    
    if start_date:
        try:
            start = datetime.fromisoformat(start_date).date()
            query = query.filter(WorkOrder.scheduled_date >= start)
        except:
            pass
    
    if end_date:
        try:
            end = datetime.fromisoformat(end_date).date()
            query = query.filter(WorkOrder.scheduled_date <= end)
        except:
            pass
    
    query = query.order_by(db.desc(WorkOrder.scheduled_date))
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'work_orders': [wo.to_dict() for wo in pagination.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages
        }
    }), 200


@work_orders_bp.route('/today', methods=['GET'])
@jwt_required()
def get_todays_work_orders():
    """Get today's work orders"""
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    today = datetime.now().date()
    
    query = WorkOrder.query.filter_by(scheduled_date=today)
    
    if claims.get('role') == 'technician':
        query = query.filter_by(assigned_to=current_user_id)
    
    work_orders = query.order_by(WorkOrder.scheduled_date).all()
    
    return jsonify({
        'work_orders': [wo.to_dict() for wo in work_orders],
        'count': len(work_orders)
    }), 200


@work_orders_bp.route('', methods=['POST'])
@jwt_required()
def create_work_order():
    """Create new work order"""
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    
    if claims.get('role') not in ['super_admin', 'maintenance_engineer']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    required = ['equipment_id', 'scheduled_date']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'{field} required'}), 400
    
    # Generate order number
    year = datetime.now().year
    last_wo = WorkOrder.query.filter(WorkOrder.order_number.like(f'PPM-{year}-%')).order_by(db.desc(WorkOrder.id)).first()
    next_num = int(last_wo.order_number.split('-')[-1]) + 1 if last_wo else 1
    order_number = f'PPM-{year}-{next_num:04d}'
    
    scheduled_date = datetime.fromisoformat(data['scheduled_date']).date()
    
    wo = WorkOrder(
        order_number=order_number,
        equipment_id=data['equipment_id'],
        assigned_to=data.get('assigned_to'),
        scheduled_date=scheduled_date,
        estimated_duration_minutes=data.get('estimated_duration_minutes', 60),
        priority=data.get('priority', 'medium'),
        wo_type=data.get('wo_type', 'preventive'),
        problem_description=data.get('problem_description'),
        notes=data.get('notes'),
        created_by=current_user_id
    )
    
    db.session.add(wo)
    db.session.commit()
    
    # Auto-populate checklist from template
    equipment = Equipment.query.get(data['equipment_id'])
    if equipment:
        templates = ChecklistTemplate.query.filter_by(category_id=equipment.category_id, is_active=True).all()
        for template in templates:
            items = ChecklistItem.query.filter_by(template_id=template.id).order_by(ChecklistItem.item_order).all()
            for item in items:
                result = ChecklistResult(
                    work_order_id=wo.id,
                    checklist_item_id=item.id,
                    item_description=item.description,
                    item_order=item.item_order,
                    is_required=item.is_required
                )
                db.session.add(result)
    
    db.session.commit()
    
    # Notify assigned technician
    if wo.assigned_to:
        notification = Notification(
            user_id=wo.assigned_to,
            work_order_id=wo.id,
            title='New Task Assigned',
            message=f'Work Order {order_number} assigned to you',
            notification_type='task_assigned'
        )
        db.session.add(notification)
        db.session.commit()
    
    return jsonify({'message': 'Work order created', 'work_order': wo.to_dict()}), 201


@work_orders_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_work_order(id):
    """Get single work order"""
    wo = WorkOrder.query.get_or_404(id)
    
    checklist_results = ChecklistResult.query.filter_by(work_order_id=id).order_by(ChecklistResult.item_order).all()
    spare_parts = SparePartUsed.query.filter_by(work_order_id=id).all()
    
    return jsonify({
        'work_order': wo.to_dict(),
        'checklist_results': [r.to_dict() for r in checklist_results],
        'spare_parts': [sp.to_dict() for sp in spare_parts]
    }), 200


@work_orders_bp.route('/<int:id>/start', methods=['POST'])
@jwt_required()
def start_work_order(id):
    """Start a work order"""
    current_user_id = get_jwt_identity()
    wo = WorkOrder.query.get_or_404(id)
    
    if wo.assigned_to != current_user_id:
        claims = get_jwt()
        if claims.get('role') not in ['super_admin', 'maintenance_engineer']:
            return jsonify({'error': 'Unauthorized'}), 403
    
    wo.status = 'in_progress'
    wo.start_time = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'message': 'Work order started', 'work_order': wo.to_dict()}), 200


@work_orders_bp.route('/<int:id>/complete', methods=['POST'])
@jwt_required()
def complete_work_order(id):
    """Complete a work order"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    wo = WorkOrder.query.get_or_404(id)
    
    wo.status = 'completed'
    wo.end_time = datetime.utcnow()
    if wo.start_time:
        wo.actual_duration_minutes = int((wo.end_time - wo.start_time).total_seconds() / 60)
    
    if data.get('notes'):
        wo.notes = data['notes']
    if data.get('recommendations'):
        wo.recommendations = data['recommendations']
    if data.get('technician_signature'):
        wo.technician_signature = data['technician_signature']
        wo.technician_sign_date = datetime.utcnow()
    
    wo.completed_at = datetime.utcnow()
    db.session.commit()
    
    # Notify engineer
    notification = Notification(
        user_id=wo.created_by,
        work_order_id=wo.id,
        title='Task Completed',
        message=f'Work Order {wo.order_number} completed',
        notification_type='task_completed'
    )
    db.session.add(notification)
    db.session.commit()
    
    return jsonify({'message': 'Work order completed', 'work_order': wo.to_dict()}), 200


@work_orders_bp.route('/<int:id>/checklist', methods=['POST'])
@jwt_required()
def update_checklist(id):
    """Update checklist results"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    wo = WorkOrder.query.get_or_404(id)
    
    items = data.get('items', [])
    for item_data in items:
        result = ChecklistResult.query.get(item_data['id'])
        if result:
            result.is_done = item_data.get('is_done', False)
            if item_data.get('action_taken'):
                result.action_taken = item_data['action_taken']
            if item_data.get('notes'):
                result.notes = item_data['notes']
            result.checked_by = current_user_id
            result.checked_at = datetime.utcnow()
    
    db.session.commit()
    return jsonify({'message': 'Checklist updated'}), 200


@work_orders_bp.route('/<int:id>/spare-parts', methods=['POST'])
@jwt_required()
def add_spare_part(id):
    """Add spare part used"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    sp = SparePartUsed(
        work_order_id=id,
        description=data['description'],
        quantity=data.get('quantity', 1),
        part_number=data.get('part_number'),
        unit_cost=data.get('unit_cost'),
        total_cost=data.get('total_cost'),
        used_by=current_user_id
    )
    db.session.add(sp)
    db.session.commit()
    
    return jsonify({'message': 'Spare part added', 'spare_part': sp.to_dict()}), 201

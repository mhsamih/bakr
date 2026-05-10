"""
Dashboard routes - KPIs, statistics, charts data
"""

from datetime import datetime, timedelta
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from sqlalchemy import func
from ..models import (
    db, Equipment, WorkOrder, User, Notification, Department, AssetCategory
)

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/kpi', methods=['GET'])
@jwt_required()
def get_kpi():
    """Get dashboard KPI cards data"""
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    month_start = today.replace(day=1)
    
    # Base queries
    equipment_query = Equipment.query.filter_by(status='active')
    wo_query = WorkOrder.query
    
    # Role-based filtering for technicians
    if claims.get('role') == 'technician':
        wo_query = wo_query.filter_by(assigned_to=current_user_id)
    
    # Calculate KPIs
    total_equipment = equipment_query.count()
    
    tasks_due_today = wo_query.filter(
        WorkOrder.scheduled_date == today,
        WorkOrder.status.in_(['pending', 'in_progress'])
    ).count()
    
    overdue_tasks = wo_query.filter(
        WorkOrder.scheduled_date < today,
        WorkOrder.status.in_(['pending', 'in_progress'])
    ).count()
    
    completed_this_month = wo_query.filter(
        WorkOrder.status == 'completed',
        WorkOrder.completed_at >= month_start
    ).count()
    
    completed_this_week = wo_query.filter(
        WorkOrder.status == 'completed',
        WorkOrder.completed_at >= week_ago
    ).count()
    
    # Warranty expiring in 30 days
    warranty_expiry_date = today + timedelta(days=30)
    warranty_expiring = equipment_query.filter(
        Equipment.warranty_expiry_date != None,
        Equipment.warranty_expiry_date <= warranty_expiry_date,
        Equipment.warranty_expiry_date >= today
    ).count()
    
    # Pending approvals
    pending_approval = wo_query.filter(
        WorkOrder.status == 'completed',
        WorkOrder.engineer_signature == None
    ).count() if claims.get('role') in ['super_admin', 'maintenance_engineer'] else 0
    
    return jsonify({
        'kpi': {
            'total_equipment': total_equipment,
            'tasks_due_today': tasks_due_today,
            'overdue_tasks': overdue_tasks,
            'completed_this_month': completed_this_month,
            'completed_this_week': completed_this_week,
            'warranty_expiring': warranty_expiring,
            'pending_approval': pending_approval
        }
    }), 200


@dashboard_bp.route('/today', methods=['GET'])
def get_today_summary():
    """Get today's work orders summary"""
    today = datetime.now().date()
    
    work_orders = WorkOrder.query.filter_by(scheduled_date=today).all()
    
    by_status = {}
    by_department = {}
    
    for wo in work_orders:
        # By status
        status = wo.status
        by_status[status] = by_status.get(status, 0) + 1
        
        # By department
        if wo.equipment and wo.equipment.department:
            dept_name = wo.equipment.department.name
            by_department[dept_name] = by_department.get(dept_name, 0) + 1
    
    return jsonify({
        'date': today.isoformat(),
        'total': len(work_orders),
        'by_status': by_status,
        'by_department': by_department,
        'work_orders': [wo.to_dict() for wo in work_orders[:10]]  # Limit to 10
    }), 200


@dashboard_bp.route('/charts/work-orders-by-status', methods=['GET'])
@jwt_required()
def get_wo_by_status():
    """Get work orders grouped by status for chart"""
    results = db.session.query(
        WorkOrder.status, func.count(WorkOrder.id)
    ).group_by(WorkOrder.status).all()
    
    return jsonify({
        'labels': [r[0] for r in results],
        'values': [r[1] for r in results]
    }), 200


@dashboard_bp.route('/charts/work-orders-by-category', methods=['GET'])
@jwt_required()
def get_wo_by_category():
    """Get work orders grouped by equipment category"""
    results = db.session.query(
        AssetCategory.name, func.count(WorkOrder.id)
    ).join(Equipment, WorkOrder.equipment_id == Equipment.id)\
     .join(AssetCategory, Equipment.category_id == AssetCategory.id)\
     .group_by(AssetCategory.name).all()
    
    return jsonify({
        'labels': [r[0] for r in results],
        'values': [r[1] for r in results]
    }), 200


@dashboard_bp.route('/charts/completion-trend', methods=['GET'])
@jwt_required()
def get_completion_trend():
    """Get completion trend for last 30 days"""
    thirty_days_ago = datetime.now().date() - timedelta(days=30)
    
    results = db.session.query(
        func.date(WorkOrder.completed_at), func.count(WorkOrder.id)
    ).filter(
        WorkOrder.status == 'completed',
        WorkOrder.completed_at >= thirty_days_ago
    ).group_by(func.date(WorkOrder.completed_at)).order_by(func.date(WorkOrder.completed_at)).all()
    
    return jsonify({
        'labels': [str(r[0]) for r in results],
        'values': [r[1] for r in results]
    }), 200


@dashboard_bp.route('/alerts', methods=['GET'])
@jwt_required()
def get_alerts():
    """Get system alerts"""
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    today = datetime.now().date()
    
    alerts = []
    
    # Overdue tasks (Red)
    overdue = WorkOrder.query.filter(
        WorkOrder.scheduled_date < today,
        WorkOrder.status.in_(['pending', 'in_progress'])
    ).count()
    if overdue > 0:
        alerts.append({
            'type': 'error',
            'priority': 'high',
            'title': 'Overdue Tasks',
            'message': f'{overdue} tasks are overdue',
            'icon': 'alert-circle'
        })
    
    # Due in 3 days (Orange)
    three_days = today + timedelta(days=3)
    due_soon = WorkOrder.query.filter(
        WorkOrder.scheduled_date > today,
        WorkOrder.scheduled_date <= three_days,
        WorkOrder.status == 'pending'
    ).count()
    if due_soon > 0:
        alerts.append({
            'type': 'warning',
            'priority': 'medium',
            'title': 'Tasks Due Soon',
            'message': f'{due_soon} tasks due in next 3 days',
            'icon': 'clock'
        })
    
    # Warranty expiring (Yellow)
    warranty_expiry = today + timedelta(days=30)
    expiring = Equipment.query.filter(
        Equipment.warranty_expiry_date != None,
        Equipment.warranty_expiry_date <= warranty_expiry,
        Equipment.warranty_expiry_date >= today
    ).count()
    if expiring > 0:
        alerts.append({
            'type': 'info',
            'priority': 'low',
            'title': 'Warranty Expiring',
            'message': f'{expiring} equipment warranties expiring in 30 days',
            'icon': 'shield'
        })
    
    return jsonify({'alerts': alerts}), 200


@dashboard_bp.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    """Get user notifications"""
    current_user_id = get_jwt_identity()
    
    notifications = Notification.query.filter_by(
        user_id=current_user_id,
        is_read=False
    ).order_by(db.desc(Notification.created_at)).limit(20).all()
    
    unread_count = Notification.query.filter_by(
        user_id=current_user_id,
        is_read=False
    ).count()
    
    return jsonify({
        'notifications': [n.to_dict() for n in notifications],
        'unread_count': unread_count
    }), 200


@dashboard_bp.route('/notifications/<int:id>/read', methods=['POST'])
@jwt_required()
def mark_notification_read(id):
    """Mark notification as read"""
    current_user_id = get_jwt_identity()
    notification = Notification.query.get_or_404(id)
    
    if notification.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    notification.is_read = True
    notification.read_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'message': 'Notification marked as read'}), 200

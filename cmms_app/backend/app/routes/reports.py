"""
Reports routes - PDF generation, exports
"""

from datetime import datetime
from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
import io
from ..models import db, WorkOrder, Equipment, User

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/work-order/<int:id>/pdf', methods=['GET'])
@jwt_required()
def generate_wo_pdf(id):
    """Generate PDF report for a work order"""
    wo = WorkOrder.query.get_or_404(id)
    
    # In production, use ReportLab or similar
    # For now, return JSON that frontend can use with jsPDF
    
    checklist_results = wo.checklist_results.order_by(ChecklistResult.item_order).all()
    spare_parts = wo.spare_parts.all()
    
    report_data = {
        'work_order': {
            'order_number': wo.order_number,
            'equipment': wo.equipment.name if wo.equipment else 'N/A',
            'location': wo.equipment.location if wo.equipment else 'N/A',
            'scheduled_date': wo.scheduled_date.isoformat(),
            'status': wo.status,
            'assigned_to': wo.assigned_to.name if wo.assigned_to else 'Unassigned'
        },
        'checklist': [
            {
                'item': r.item_order,
                'description': r.item_description,
                'status': 'Completed' if r.is_done else 'Pending',
                'action': r.action_taken,
                'notes': r.notes
            }
            for r in checklist_results
        ],
        'spare_parts': [
            {
                'description': sp.description,
                'quantity': sp.quantity,
                'part_number': sp.part_number
            }
            for sp in spare_parts
        ],
        'notes': wo.notes,
        'recommendations': wo.recommendations,
        'signatures': {
            'technician': wo.technician_signature,
            'engineer': wo.engineer_signature,
            'manager': wo.manager_signature
        }
    }
    
    return jsonify({
        'message': 'Report data generated',
        'report': report_data
    }), 200


@reports_bp.route('/monthly-summary', methods=['GET'])
@jwt_required()
def monthly_summary():
    """Generate monthly summary report"""
    year = request.args.get('year', datetime.now().year, type=int)
    month = request.args.get('month', datetime.now().month, type=int)
    
    from sqlalchemy import func
    
    # Get date range
    from datetime import date
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)
    
    # Total planned vs completed
    total_planned = WorkOrder.query.filter(
        WorkOrder.scheduled_date >= start_date,
        WorkOrder.scheduled_date < end_date
    ).count()
    
    total_completed = WorkOrder.query.filter(
        WorkOrder.status == 'completed',
        WorkOrder.completed_at >= start_date,
        WorkOrder.completed_at < end_date
    ).count()
    
    completion_rate = (total_completed / total_planned * 100) if total_planned > 0 else 0
    
    # Overdue
    overdue = WorkOrder.query.filter(
        WorkOrder.scheduled_date < start_date,
        WorkOrder.status.in_(['pending', 'in_progress'])
    ).count()
    
    # By technician
    tech_performance = db.session.query(
        User.name,
        func.count(WorkOrder.id),
        func.sum(WorkOrder.actual_duration_minutes)
    ).join(WorkOrder, User.id == WorkOrder.assigned_to)\
     .filter(
         WorkOrder.status == 'completed',
         WorkOrder.completed_at >= start_date,
         WorkOrder.completed_at < end_date
     ).group_by(User.name).all()
    
    return jsonify({
        'period': f'{year}-{month:02d}',
        'total_planned': total_planned,
        'total_completed': total_completed,
        'completion_rate': round(completion_rate, 2),
        'overdue': overdue,
        'technician_performance': [
            {'name': r[0], 'tasks': r[1], 'total_minutes': r[2] or 0}
            for r in tech_performance
        ]
    }), 200


@reports_bp.route('/equipment-history/<int:id>', methods=['GET'])
@jwt_required()
def equipment_history_report(id):
    """Get equipment history report"""
    equipment = Equipment.query.get_or_404(id)
    
    work_orders = WorkOrder.query.filter_by(equipment_id=id)\
        .order_by(db.desc(WorkOrder.scheduled_date)).all()
    
    total_maintenance = len(work_orders)
    total_cost = sum(sp.total_cost or 0 for wo in work_orders for sp in wo.spare_parts)
    
    return jsonify({
        'equipment': equipment.to_dict(),
        'total_work_orders': total_maintenance,
        'total_cost': total_cost,
        'history': [wo.to_dict() for wo in work_orders]
    }), 200


@reports_bp.route('/worker-performance', methods=['GET'])
@jwt_required()
def worker_performance():
    """Get worker performance report"""
    technicians = User.query.filter_by(role='technician', is_active=True).all()
    
    performance = []
    for tech in technicians:
        completed = WorkOrder.query.filter_by(
            assigned_to=tech.id,
            status='completed'
        ).all()
        
        total_tasks = len(completed)
        avg_time = sum(wo.actual_duration_minutes or 0 for wo in completed) / total_tasks if total_tasks > 0 else 0
        
        # On-time rate
        on_time = sum(1 for wo in completed if wo.completed_at and wo.completed_at.date() <= wo.scheduled_date)
        on_time_rate = (on_time / total_tasks * 100) if total_tasks > 0 else 0
        
        performance.append({
            'technician': tech.to_dict(),
            'total_tasks': total_tasks,
            'avg_completion_time_minutes': round(avg_time, 2),
            'on_time_rate': round(on_time_rate, 2)
        })
    
    return jsonify({'performance': performance}), 200

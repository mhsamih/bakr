"""
Database Models for CMMS Application
Using SQLAlchemy ORM with SQLite/PostgreSQL support
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Association tables
work_order_checklist_items = db.Table('work_order_checklist_items',
    db.Column('work_order_id', db.Integer, db.ForeignKey('work_orders.id'), primary_key=True),
    db.Column('checklist_item_id', db.Integer, db.ForeignKey('checklist_items.id'), primary_key=True),
    db.Column('is_done', db.Boolean, default=False),
    db.Column('action_taken', db.Text),
    db.Column('notes', db.Text)
)

class User(db.Model):
    """User model with role-based access control"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum('super_admin', 'maintenance_engineer', 'technician', 'viewer', name='user_roles'), nullable=False, default='viewer')
    whatsapp = db.Column(db.String(20))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    department = db.relationship('Department', backref='users')
    assigned_work_orders = db.relationship('WorkOrder', backref='assigned_to', lazy='dynamic')
    created_work_orders = db.relationship('WorkOrder', foreign_keys='WorkOrder.created_by', backref='creator', lazy='dynamic')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')
    signatures = db.relationship('Signature', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'department': self.department.name if self.department else None,
            'whatsapp': self.whatsapp,
            'is_active': self.is_active
        }


class Facility(db.Model):
    """Facility/Location model (e.g., Hospital, School, Factory)"""
    __tablename__ = 'facilities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(100))  # Hospital, School, Hotel, Factory, etc.
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    country = db.Column(db.String(100), default='Saudi Arabia')
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    logo_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    departments = db.relationship('Department', backref='facility', lazy='dynamic')
    buildings = db.relationship('Building', backref='facility', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'address': self.address,
            'city': self.city,
            'country': self.country
        }


class Department(db.Model):
    """Department model (HVAC, Electrical, Mechanical, Civil, etc.)"""
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True)
    description = db.Column(db.Text)
    facility_id = db.Column(db.Integer, db.ForeignKey('facilities.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    parent = db.relationship('Department', remote_side=[id], backref='sub_departments')
    equipment = db.relationship('Equipment', backref='department', lazy='dynamic')
    buildings = db.relationship('Building', backref='department', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'facility': self.facility.name if self.facility else None
        }


class Building(db.Model):
    """Building model within a facility"""
    __tablename__ = 'buildings'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20))
    facility_id = db.Column(db.Integer, db.ForeignKey('facilities.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    floors = db.relationship('Floor', backref='building', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'facility': self.facility.name if self.facility else None
        }


class Floor(db.Model):
    """Floor model within a building"""
    __tablename__ = 'floors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    floor_number = db.Column(db.Integer)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    rooms = db.relationship('Room', backref='floor', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'floor_number': self.floor_number,
            'building': self.building.name if self.building else None
        }


class Room(db.Model):
    """Room model within a floor"""
    __tablename__ = 'rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    room_number = db.Column(db.String(20))
    floor_id = db.Column(db.Integer, db.ForeignKey('floors.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    equipment = db.relationship('Equipment', backref='room', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'room_number': self.room_number,
            'floor': self.floor.name if self.floor else None
        }


class AssetCategory(db.Model):
    """Asset Category (HVAC, Electrical, Mechanical, Civil, Communication, etc.)"""
    __tablename__ = 'asset_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))  # Icon class for UI
    color = db.Column(db.String(7))  # Hex color for UI
    parent_id = db.Column(db.Integer, db.ForeignKey('asset_categories.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    parent = db.relationship('AssetCategory', remote_side=[id], backref='sub_categories')
    equipment = db.relationship('Equipment', backref='category', lazy='dynamic')
    checklist_templates = db.relationship('ChecklistTemplate', backref='category', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'icon': self.icon,
            'color': self.color,
            'parent': self.parent.name if self.parent else None
        }


class Equipment(db.Model):
    """Main Equipment model - core of the CMMS"""
    __tablename__ = 'equipment'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('asset_categories.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    
    # Location details
    location = db.Column(db.String(200))  # General location
    sub_location = db.Column(db.String(200))  # Specific location (room, zone)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'))
    floor_id = db.Column(db.Integer, db.ForeignKey('floors.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    
    # Equipment specifications
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    serial_number = db.Column(db.String(100), index=True)
    asset_tag = db.Column(db.String(50), unique=True, index=True)
    
    # Purchase and warranty info
    purchase_date = db.Column(db.Date)
    warranty_expiry_date = db.Column(db.Date)
    installation_date = db.Column(db.Date)
    expected_lifetime_years = db.Column(db.Integer)
    
    # PM Schedule
    pm_frequency = db.Column(db.Enum('daily', 'weekly', 'monthly', 'quarterly', 'semi_annual', 'annual', name='pm_frequencies'))
    last_pm_date = db.Column(db.Date)
    next_pm_date = db.Column(db.Date, index=True)
    pm_duration_minutes = db.Column(db.Integer, default=60)
    
    # Status
    status = db.Column(db.Enum('active', 'inactive', 'under_maintenance', 'decommissioned', name='equipment_status'), default='active')
    condition = db.Column(db.Enum('excellent', 'good', 'fair', 'poor', 'critical', name='equipment_condition'), default='good')
    
    # Additional info
    specifications = db.Column(db.Text)  # JSON or text for custom specs
    manual_path = db.Column(db.String(255))
    photo_path = db.Column(db.String(255))
    notes = db.Column(db.Text)
    
    # Tracking
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    work_orders = db.relationship('WorkOrder', backref='equipment', lazy='dynamic')
    checklist_templates = db.relationship('ChecklistTemplate', backref='equipment', lazy='dynamic')
    pm_schedules = db.relationship('PMSchedule', backref='equipment', lazy='dynamic')
    attachments = db.relationship('Attachment', backref='equipment', lazy='dynamic')
    creator = db.relationship('User', foreign_keys=[created_by])
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category.name if self.category else None,
            'department': self.department.name if self.department else None,
            'location': self.location,
            'sub_location': self.sub_location,
            'brand': self.brand,
            'model': self.model,
            'serial_number': self.serial_number,
            'asset_tag': self.asset_tag,
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None,
            'warranty_expiry_date': self.warranty_expiry_date.isoformat() if self.warranty_expiry_date else None,
            'pm_frequency': self.pm_frequency,
            'last_pm_date': self.last_pm_date.isoformat() if self.last_pm_date else None,
            'next_pm_date': self.next_pm_date.isoformat() if self.next_pm_date else None,
            'status': self.status,
            'condition': self.condition
        }


class ChecklistTemplate(db.Model):
    """Template for checklists per equipment type"""
    __tablename__ = 'checklist_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('asset_categories.id'))
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    version = db.Column(db.String(20), default='1.0')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('ChecklistItem', backref='template', lazy='dynamic', order_by='ChecklistItem.item_order')
    creator = db.relationship('User', foreign_keys=[created_by])
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'equipment': self.equipment.name if self.equipment else None,
            'category': self.category.name if self.category else None,
            'description': self.description,
            'is_active': self.is_active,
            'version': self.version,
            'items': [item.to_dict() for item in self.items]
        }


class ChecklistItem(db.Model):
    """Individual checklist items"""
    __tablename__ = 'checklist_items'
    
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('checklist_templates.id'), nullable=False)
    item_order = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    action_required = db.Column(db.Text)  # Expected action
    is_required = db.Column(db.Boolean, default=True)
    category = db.Column(db.String(50))  # Inspection, Cleaning, Testing, etc.
    estimated_time_minutes = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'item_order': self.item_order,
            'description': self.description,
            'action_required': self.action_required,
            'is_required': self.is_required,
            'category': self.category,
            'estimated_time_minutes': self.estimated_time_minutes
        }


class WorkOrder(db.Model):
    """Work Order - core operational unit"""
    __tablename__ = 'work_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    
    # Assignment
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Scheduling
    scheduled_date = db.Column(db.Date, nullable=False, index=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    estimated_duration_minutes = db.Column(db.Integer)
    actual_duration_minutes = db.Column(db.Integer)
    
    # Status tracking
    status = db.Column(db.Enum('pending', 'in_progress', 'completed', 'needs_followup', 'cancelled', name='wo_status'), default='pending')
    priority = db.Column(db.Enum('low', 'medium', 'high', 'critical', name='wo_priority'), default='medium')
    wo_type = db.Column(db.Enum('preventive', 'corrective', 'emergency', 'inspection', name='wo_types'), default='preventive')
    
    # Content
    problem_description = db.Column(db.Text)
    notes = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    
    # Signatures (3-signature system)
    technician_signature = db.Column(db.String(255))
    technician_sign_date = db.Column(db.DateTime)
    engineer_signature = db.Column(db.String(255))
    engineer_sign_date = db.Column(db.DateTime)
    manager_signature = db.Column(db.String(255))
    manager_sign_date = db.Column(db.DateTime)
    
    # Tracking
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    checklist_results = db.relationship('ChecklistResult', backref='work_order', lazy='dynamic')
    spare_parts = db.relationship('SparePartUsed', backref='work_order', lazy='dynamic')
    attachments = db.relationship('Attachment', backref='work_order', lazy='dynamic')
    notifications = db.relationship('Notification', backref='work_order', lazy='dynamic')
    creator = db.relationship('User', foreign_keys=[created_by])
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'equipment': self.equipment.name if self.equipment else None,
            'equipment_id': self.equipment_id,
            'assigned_to': self.assigned_to.name if self.assigned_to else None,
            'scheduled_date': self.scheduled_date.isoformat(),
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'status': self.status,
            'priority': self.priority,
            'wo_type': self.wo_type,
            'problem_description': self.problem_description,
            'notes': self.notes,
            'recommendations': self.recommendations,
            'has_technician_signature': bool(self.technician_signature),
            'has_engineer_signature': bool(self.engineer_signature),
            'has_manager_signature': bool(self.manager_signature),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }


class ChecklistResult(db.Model):
    """Results of checklist items for a work order"""
    __tablename__ = 'checklist_results'
    
    id = db.Column(db.Integer, primary_key=True)
    work_order_id = db.Column(db.Integer, db.ForeignKey('work_orders.id'), nullable=False)
    checklist_item_id = db.Column(db.Integer, db.ForeignKey('checklist_items.id'), nullable=False)
    item_description = db.Column(db.Text, nullable=False)  # Snapshot of description
    item_order = db.Column(db.Integer, nullable=False)
    
    # Result
    is_done = db.Column(db.Boolean, default=False)
    action_taken = db.Column(db.Text)
    notes = db.Column(db.Text)
    photo_before_path = db.Column(db.String(255))
    photo_after_path = db.Column(db.String(255))
    
    # Tracking
    checked_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    checked_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'item_order': self.item_order,
            'item_description': self.item_description,
            'is_done': self.is_done,
            'action_taken': self.action_taken,
            'notes': self.notes,
            'checked_at': self.checked_at.isoformat() if self.checked_at else None
        }


class SparePartUsed(db.Model):
    """Spare parts used in work orders"""
    __tablename__ = 'spare_parts_used'
    
    id = db.Column(db.Integer, primary_key=True)
    work_order_id = db.Column(db.Integer, db.ForeignKey('work_orders.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    part_number = db.Column(db.String(100))
    unit_cost = db.Column(db.Numeric(10, 2))
    total_cost = db.Column(db.Numeric(10, 2))
    inventory_item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.id'))
    notes = db.Column(db.Text)
    used_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    used_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'quantity': self.quantity,
            'part_number': self.part_number,
            'unit_cost': float(self.unit_cost) if self.unit_cost else None,
            'total_cost': float(self.total_cost) if self.total_cost else None
        }


class Attachment(db.Model):
    """File attachments for work orders and equipment"""
    __tablename__ = 'attachments'
    
    id = db.Column(db.Integer, primary_key=True)
    work_order_id = db.Column(db.Integer, db.ForeignKey('work_orders.id'))
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))
    file_path = db.Column(db.String(255), nullable=False)
    file_name = db.Column(db.String(200), nullable=False)
    file_type = db.Column(db.String(50))  # image, document, pdf, etc.
    file_size = db.Column(db.Integer)  # in bytes
    description = db.Column(db.Text)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }


class PMSchedule(db.Model):
    """Preventive Maintenance Schedule generator"""
    __tablename__ = 'pm_schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('checklist_templates.id'))
    
    # Schedule details
    frequency = db.Column(db.Enum('daily', 'weekly', 'monthly', 'quarterly', 'semi_annual', 'annual', name='pm_freqs'))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)  # Optional end date
    day_of_week = db.Column(db.Integer)  # 0-6 for weekly
    day_of_month = db.Column(db.Integer)  # 1-31 for monthly
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    auto_generate = db.Column(db.Boolean, default=True)
    generate_days_ahead = db.Column(db.Integer, default=7)  # Generate WOs this many days before due
    
    # Tracking
    last_generated_date = db.Column(db.Date)
    next_generation_date = db.Column(db.Date)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'equipment': self.equipment.name if self.equipment else None,
            'frequency': self.frequency,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_active': self.is_active,
            'auto_generate': self.auto_generate,
            'next_generation_date': self.next_generation_date.isoformat() if self.next_generation_date else None
        }


class Notification(db.Model):
    """System notifications"""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    work_order_id = db.Column(db.Integer, db.ForeignKey('work_orders.id'))
    
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.Enum('task_assigned', 'task_due', 'task_overdue', 'task_completed', 'problem_reported', 'warranty_expiring', 'system', name='notif_types'))
    priority = db.Column(db.Enum('low', 'medium', 'high', name='notif_priority'), default='medium')
    
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime)
    sent_via_whatsapp = db.Column(db.Boolean, default=False)
    whatsapp_sent_at = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'type': self.notification_type,
            'priority': self.priority,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class WhatsAppLog(db.Model):
    """WhatsApp notification logs"""
    __tablename__ = 'whatsapp_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    recipient_number = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum('pending', 'sent', 'delivered', 'failed', name='wa_status'), default='pending')
    error_message = db.Column(db.Text)
    provider = db.Column(db.String(50))  # twilio, callmebot, etc.
    message_id = db.Column(db.String(100))
    sent_at = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'recipient_number': self.recipient_number,
            'message': self.message,
            'status': self.status,
            'provider': self.provider,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None
        }


class InventoryItem(db.Model):
    """Inventory/Spare Parts management"""
    __tablename__ = 'inventory_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    part_number = db.Column(db.String(100), index=True)
    category = db.Column(db.String(100))
    description = db.Column(db.Text)
    
    # Stock info
    current_stock = db.Column(db.Integer, default=0)
    min_stock_level = db.Column(db.Integer, default=0)
    max_stock_level = db.Column(db.Integer)
    unit_of_measure = db.Column(db.String(20), default='piece')
    unit_cost = db.Column(db.Numeric(10, 2))
    
    # Location
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'))
    shelf_location = db.Column(db.String(50))
    
    # Supplier
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    
    # Tracking
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'part_number': self.part_number,
            'category': self.category,
            'current_stock': self.current_stock,
            'min_stock_level': self.min_stock_level,
            'unit_cost': float(self.unit_cost) if self.unit_cost else None,
            'is_active': self.is_active
        }


class Warehouse(db.Model):
    """Warehouse/Storage locations"""
    __tablename__ = 'warehouses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True)
    location = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'location': self.location
        }


class Supplier(db.Model):
    """Suppliers for spare parts"""
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    contact_person = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'contact_person': self.contact_person,
            'phone': self.phone,
            'email': self.email
        }


class Signature(db.Model):
    """Digital signatures for users"""
    __tablename__ = 'signatures'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    signature_image_path = db.Column(db.String(255), nullable=False)
    signature_text = db.Column(db.String(100))  # Typed name
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'signature_text': self.signature_text,
            'is_active': self.is_active
        }


class AuditLog(db.Model):
    """Audit trail for security and compliance"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(100), nullable=False)  # CREATE, UPDATE, DELETE, LOGIN, LOGOUT
    entity_type = db.Column(db.String(50), nullable=False)  # User, Equipment, WorkOrder, etc.
    entity_id = db.Column(db.Integer)
    old_values = db.Column(db.Text)  # JSON string
    new_values = db.Column(db.Text)  # JSON string
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'action': self.action,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class SystemSetting(db.Model):
    """System-wide settings"""
    __tablename__ = 'system_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    value_type = db.Column(db.String(20), default='string')  # string, int, bool, json
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'key': self.key,
            'value': self.value,
            'value_type': self.value_type,
            'description': self.description,
            'category': self.category
        }


class ImportLog(db.Model):
    """Logs for Excel/data imports"""
    __tablename__ = 'import_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    import_type = db.Column(db.String(50), nullable=False)  # equipment, work_orders, etc.
    total_records = db.Column(db.Integer)
    success_count = db.Column(db.Integer, default=0)
    error_count = db.Column(db.Integer, default=0)
    skipped_count = db.Column(db.Integer, default=0)
    errors = db.Column(db.Text)  # JSON string of errors
    status = db.Column(db.Enum('pending', 'processing', 'completed', 'failed', name='import_status'), default='pending')
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    imported_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'file_name': self.file_name,
            'import_type': self.import_type,
            'total_records': self.total_records,
            'success_count': self.success_count,
            'error_count': self.error_count,
            'status': self.status,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

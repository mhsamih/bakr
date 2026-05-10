"""
Routes blueprints initialization
"""

from .auth import auth_bp
from .equipment import equipment_bp
from .work_orders import work_orders_bp
from .users import users_bp
from .dashboard import dashboard_bp
from .reports import reports_bp

__all__ = [
    'auth_bp',
    'equipment_bp',
    'work_orders_bp',
    'users_bp',
    'dashboard_bp',
    'reports_bp'
]

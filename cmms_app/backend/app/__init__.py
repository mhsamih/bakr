"""
CMMS - Preventive Maintenance Web Application
Flask Application Factory
"""

import os
from datetime import timedelta
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from .models import db


def create_app(config_name='development'):
    """Application factory for creating Flask app instances"""
    
    app = Flask(__name__)
    
    # Configuration
    app.config.from_object(f'config.{config_name.title()}Config')
    
    # Ensure upload folders exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'equipment'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'work_orders'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'signatures'), exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    
    # JWT configuration
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=8)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    
    # Register blueprints
    from .routes import auth_bp, equipment_bp, work_orders_bp, users_bp, dashboard_bp, reports_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(equipment_bp, url_prefix='/api/equipment')
    app.register_blueprint(work_orders_bp, url_prefix='/api/work-orders')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return jsonify({'status': 'healthy', 'message': 'CMMS API is running'})
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'name': 'CMMS - Preventive Maintenance System',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'equipment': '/api/equipment',
                'work_orders': '/api/work-orders',
                'users': '/api/users',
                'dashboard': '/api/dashboard',
                'reports': '/api/reports'
            }
        })
    
    return app

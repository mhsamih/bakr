"""
CMMS - Preventive Maintenance Web Application
Run script for development
"""

from backend.app import create_app
from backend.app.models import db

app = create_app('development')


if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)

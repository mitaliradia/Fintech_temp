from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta
from app.models import db

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    
    # Ensure the instance folder exists and is writable
    try:
        os.makedirs(app.instance_path, exist_ok=True)
        print(f"Instance path: {app.instance_path}")
    except OSError as e:
        print(f"Error creating instance path: {e}")
    
    # Configure SQLite to use the standard Flask instance folder
    db_path = os.path.join(app.instance_path, 'fintech.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-for-development')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    
    # Import and register blueprints
    from app.routes.pay import pay_bp
    from app.routes.auth import auth_bp
    from app.routes.station import station_bp
    from app.routes.vehicle import vehicle_bp
    from app.routes.rental import rental_bp

    from app.routes.test import test_bp
    app.register_blueprint(test_bp, url_prefix='/test')
    
    app.register_blueprint(pay_bp, url_prefix="/pay")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(station_bp, url_prefix="/api/station")
    app.register_blueprint(vehicle_bp, url_prefix="/api/vehicle")
    app.register_blueprint(rental_bp, url_prefix="/api/rentals")
    
    # Import all models before creating tables
    from app.models.user import User
    from app.models.station import Station  # Import Station first
    from app.models.admin import Admin      # Then import Admin
    from app.models.vehicle import Vehicle
    from app.models.rental import Rental
    
    with app.app_context():
        db.create_all()
        
    @app.route("/")
    def home():
        return "Hello, Babes!"
        
    return app
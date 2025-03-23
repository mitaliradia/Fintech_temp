from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta
from app.models import db

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # Setup CORS with more specific configuration
    CORS(app, 
     resources={r"/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}}, 
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    
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
    
    # Add diagnostic routes
    @app.route("/debug", methods=["GET", "POST", "OPTIONS"])
    def debug():
        if request.method == "OPTIONS":
            response = jsonify({"success": True})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
            return response
            
        return jsonify({
            "success": True, 
            "message": "Debug endpoint reached successfully",
            "method": request.method,
            "headers": dict(request.headers)
        })
    
    @app.route("/test-register", methods=["POST", "OPTIONS"])
    def test_register():
        if request.method == "OPTIONS":
            response = jsonify({"success": True})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
            return response
            
        try:
            data = request.get_json()
            print("Received test registration data:", data)
            return jsonify({
                "success": True,
                "message": "Test registration endpoint reached",
                "received_data": data
            })
        except Exception as e:
            print(f"Error in test registration: {str(e)}")
            return jsonify({
                "success": False,
                "message": f"Error: {str(e)}"
            }), 500
    
    # Import and register blueprints
    from app.routes.pay import pay_bp
    from app.routes.auth import auth_bp
    from app.routes.station import station_bp
    from app.routes.vehicle import vehicle_bp
    from app.routes.rental import rental_bp
<<<<<<< HEAD
    from app.routes.kyc import kyc_bp

=======
>>>>>>> f76d352 (push for deployment)
    from app.routes.test import test_bp
    
    app.register_blueprint(test_bp, url_prefix='/test')
    app.register_blueprint(pay_bp, url_prefix="/pay")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(station_bp, url_prefix="/api/station")
    app.register_blueprint(vehicle_bp, url_prefix="/api/vehicle")
    app.register_blueprint(rental_bp, url_prefix="/api/rentals")
    app.register_blueprint(kyc_bp, url_prefix="/api/kyc")
    
    # Import all models before creating tables
    from app.models.user import User
    from app.models.station import Station # Import Station first
    from app.models.admin import Admin # Then import Admin
    from app.models.vehicle import Vehicle
    from app.models.rental import Rental
    
    with app.app_context():
        db.create_all()
<<<<<<< HEAD

    # from app.routes.vehicle import vehicle_bp
    # app.register_blueprint(vehicle_bp)
        
=======
    
>>>>>>> f76d352 (push for deployment)
    @app.route("/")
    def home():
        return "Hello, Babes!"
    
    # Add another test route below to ensure routes are registered properly
    @app.route("/ping")
    def ping():
        return jsonify({"message": "pong"})
    
    return app
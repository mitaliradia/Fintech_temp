from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta
from app.models import db

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance/fintech.db")}'
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
    app.register_blueprint(pay_bp, url_prefix="/pay")
    app.register_blueprint(auth_bp)
    
    # Import all models before creating tables
    from app.models.user import User
    from app.models.station import Station  # Import Station first
    from app.models.admin import Admin      # Then import Admin
    # from app.models.rental import Rental
    # from app.models.vehicle import Vehicle
    
    with app.app_context():
        db.create_all()
        
    @app.route("/")
    def home():
        return "Hello, Babes!"
        
    return app
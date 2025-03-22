from flask import Flask
from flask_cors import CORS
import os
from app.models import db

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance/fintech.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
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
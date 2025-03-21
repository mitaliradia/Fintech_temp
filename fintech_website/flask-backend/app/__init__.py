from flask import Flask
from flask_cors import CORS



def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/fintech.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from app.models.user import db
    db.init_app(app)

    # Import and register blueprints
    from app.routes.pay import pay_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(pay_bp, url_prefix="/pay")
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        return "Hello, Babes!"

    return app
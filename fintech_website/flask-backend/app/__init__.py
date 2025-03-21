from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Import and register blueprints
    from app.routes.pay import pay_bp
    app.register_blueprint(pay_bp, url_prefix="/pay")

    @app.route("/")
    def home():
        return "Hello, Babes!"

    return app
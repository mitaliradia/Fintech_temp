from flask import Blueprint, jsonify, request
from ..models.user import User
from app.app__init__ import db  
from flask_jwt_extended import create_access_token
from flask_cors import cross_origin

auth_bp = Blueprint('auth', __name__, url_prefix='/api')


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "No JSON payload provided", "status": "error"}), 400

        required_fields = ["name", "email", "password", "confirm_password"]
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"Missing {field}", "status": "error"}), 400

        if data["password"] != data["confirm_password"]:
            return jsonify({"message": "Passwords do not match", "status": "error"}), 400

        if User.query.filter_by(email=data['email']).first():
            return jsonify({"message": "Email already exists", "status": "error"}), 400

        new_user = User(
            name=data['name'],
            email=data['email']
        )
        new_user.set_password(data['password'])  
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully", "status": "success"}), 201

    except Exception as e:
        print(f"Error occurred: {e}") 
        return jsonify({"message": "Internal server error", "status": "error"}), 500

@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 204
        
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "No input data provided"}), 400
        
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"message": "Missing email or password"}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "user_id": user.id
        }), 200
    
    return jsonify({"message": "Invalid email or password"}), 401
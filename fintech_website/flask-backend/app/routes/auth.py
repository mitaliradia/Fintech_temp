from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import datetime, date
from ..models.user import db, User
from ..models.admin import Admin, RoleEnum
import uuid
import re
import jwt
import os
from flask_cors import CORS
# from datetime import timedelta
import datetime
#  datetime

from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, jwt_required, get_jwt

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
CORS(auth_bp, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Store blacklisted tokens (Use Redis or database for production)
blacklisted_tokens = set()

# SECRET KEY (Ensure this is set as an environment variable in production)
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-secret-key')
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

@auth_bp.route('/test-simple', methods=['GET', 'POST'])
def test_simple():
    return jsonify({'message': 'This is a simple test route'})

@auth_bp.route('/simple-register', methods=['POST'])
def simple_register():
    print("Simple register endpoint called")
    
    try:
        data = request.get_json()
        print("Received data:", data)
        
        # Just echo back the data without database operations
        return jsonify({
            'success': True,
            'message': 'Simple register test successful',
            'received_data': data
        }), 200
        
    except Exception as e:
        print(f"Error in simple register: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500



@auth_bp.route('/register', methods=['POST', 'OPTIONS'])
def register():
    # Handle OPTIONS request for CORS preflight
    if request.method == 'OPTIONS':
        response = jsonify({'success': True})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    print("Register endpoint called")
    print("Request headers:", dict(request.headers))
    print("Request data:", request.get_data(as_text=True))
    
    try:
        data = request.get_json()
        print("Parsed JSON data:", data)
        
        # Validate required fields
        required_fields = ['email', 'phone', 'first_name', 'last_name', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'success': False, 'message': f'Missing required field: {field}'}), 400
        
        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, data['email']):
            return jsonify({'success': False, 'message': 'Invalid email format'}), 400
        
        # Validate phone format (simple validation, can be enhanced)
        phone_pattern = r'^\+?[0-9]{10,15}$'
        if not re.match(phone_pattern, data['phone']):
            return jsonify({'success': False, 'message': 'Invalid phone number format'}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'message': 'Email already registered'}), 409
        
        if User.query.filter_by(phone=data['phone']).first():
            return jsonify({'success': False, 'message': 'Phone number already registered'}), 409
        
        # Process date of birth if provided
        dob = None
        if 'date_of_birth' in data and data['date_of_birth']:
            try:
                dob = datetime.datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'success': False, 'message': 'Invalid date format for date_of_birth. Use YYYY-MM-DD'}), 400
        
        # Create new user
        new_user = User(
            id=uuid.uuid4(),
            email=data['email'],
            phone=data['phone'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            password_hash=generate_password_hash(data['password']),
            date_of_birth=dob,
            # Optional fields
            street=data.get('street'),
            city=data.get('city'),
            state=data.get('state'),
            postal_code=data.get('postal_code'),
            country=data.get('country'),
            preferred_language=data.get('preferred_language', 'en'),
            marketing_consent=data.get('marketing_consent', False),
            created_at=datetime.datetime.now(datetime.timezone.utc),
            updated_at=datetime.datetime.now(datetime.timezone.utc)
        )
        
        # Save to database
        try:
            db.session.add(new_user)
            db.session.commit()
            
            # Generate JWT token
            token_payload = {
                'user_id': str(new_user.id),
                'email': new_user.email,
                'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)  # Token expires in 1 day
            }
            
            token = jwt.encode(
                token_payload,
                os.environ.get('JWT_SECRET_KEY', 'dev-secret-key'),
                algorithm='HS256'
            )
            
            # Prepare response
            response_data = {
                'success': True,
                'message': 'User registered successfully',
                'user': {
                    'id': str(new_user.id),
                    'email': new_user.email,
                    'first_name': new_user.first_name,
                    'last_name': new_user.last_name,
                    'phone': new_user.phone
                },
                'token': token
            }
            
            response = jsonify(response_data)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 201
            
        except Exception as e:
            db.session.rollback()
            print(f"Database error: {str(e)}")
            return jsonify({'success': False, 'message': f'Registration failed: {str(e)}'}), 500
            
    except Exception as e:
        print(f"Error in register function: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Error processing request: {str(e)}'}), 500 

# Helper function to generate JWT tokens
def generate_token(user, expires_in=1):
    payload = {
        'user_id': str(user.id),
        'email': user.email,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=expires_in)  # Token expiry
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')


# -------------------- LOGIN ROUTE --------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validate input
    if not data.get('email') or not data.get('password'):
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400
    
    # Find user
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    
    # Generate tokens
    access_token = generate_token(user, expires_in=1)  # 1-day expiry
    refresh_token = generate_token(user, expires_in=7)  # 7-day expiry

    return jsonify({
        'success': True,
        'message': 'Login successful',
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200

# -------------------- LOGOUT ROUTE --------------------
@auth_bp.route('/logout', methods=['POST'])
def logout():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'success': False, 'message': 'No token provided'}), 400

    token = auth_header.split(" ")[1]  # Extract token from "Bearer <token>"
    blacklisted_tokens.add(token)  # Add to blacklist (for production, use Redis or DB)

    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200

# -------------------- REFRESH TOKEN ROUTE --------------------
@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'success': False, 'message': 'No refresh token provided'}), 400

    token = auth_header.split(" ")[1]  # Extract token from "Bearer <token>"

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        
        # Check if token is blacklisted
        if token in blacklisted_tokens:
            return jsonify({'success': False, 'message': 'Token is blacklisted'}), 401
        
        # Generate new access token
        user = User.query.get(payload['user_id'])
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404

        new_access_token = generate_token(user, expires_in=1)  # 1-day expiry
        return jsonify({
            'success': True,
            'message': 'Token refreshed successfully',
            'access_token': new_access_token
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({'success': False, 'message': 'Refresh token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'success': False, 'message': 'Invalid refresh token'}), 401


# Admin Registration
@auth_bp.route("/admin/register", methods=["POST"])
def register_admin():
    data = request.get_json()
    
    # Extract details
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    phone_number = data.get("phone_number")
    password = data.get("password")
    role = data.get("role", "SUPPORT_STAFF")  # Default to SUPPORT_STAFF
    station_id = data.get("station_id")
    
    # Check if email already exists
    if Admin.query.filter_by(email=email).first():
        return jsonify({"error": "Admin with this email already exists"}), 400
    
    # Validate role
    if role not in RoleEnum.__members__:
        return jsonify({"error": "Invalid role"}), 400
    
    # Hash the password
    hashed_password = generate_password_hash(password)
    
    # Create new admin - with string UUID instead of UUID object
    new_admin = Admin(
        id=str(uuid.uuid4()),  # Convert UUID to string
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        password_hash=hashed_password,
        role=RoleEnum[role],
        permissions="",  # Empty string for permissions
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow(),
    )
    
    # Convert station_id to string if it exists
    if station_id:
        new_admin.station_id = str(station_id)
    
    db.session.add(new_admin)
    db.session.commit()
    
    return jsonify({"message": "Admin registered successfully", "admin_id": str(new_admin.id)}), 201

# Admin Login
@auth_bp.route("/admin/login", methods=["POST"])
def login_admin():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    # Find admin by email
    admin = Admin.query.filter_by(email=email).first()
    
    if not admin or not check_password_hash(admin.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401
    
    # Update last login timestamp
    admin.last_login_at = datetime.datetime.utcnow()
    db.session.commit()
    
    # Generate JWT tokens - admin.id is already a string in SQLite
    access_token = create_access_token(
        identity=admin.id, 
        additional_claims={
            "role": admin.role.value,
            "email": admin.email,
            "name": f"{admin.first_name} {admin.last_name}"
        }
    )
    
    refresh_token = create_refresh_token(identity=admin.id)
    
    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "admin": {
            "id": admin.id,  # Already a string in SQLite
            "email": admin.email,
            "first_name": admin.first_name,
            "last_name": admin.last_name,
            "role": admin.role.value
        }
    }), 200

@auth_bp.route("/admin/logout", methods=["POST"])
@jwt_required()
def logout_admin():
    # Get the JWT token from the request
    jwt_token = get_jwt()["jti"]
    
    # Add to blacklist (for production, use Redis or DB)
    # In a real implementation, you would store this in a persistent storage
    blacklisted_tokens.add(jwt_token)
    
    return jsonify({"success": True, "message": "Admin logged out successfully"}), 200
# Add to your main app.py file:
# from routes.auth import auth_bp
# app.register_blueprint(auth_bp)
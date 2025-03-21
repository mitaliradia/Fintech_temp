from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import datetime, date
from ..models.user import db, User
import uuid
import re
import jwt
import os
# from datetime import timedelta
import datetime
#  datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Store blacklisted tokens (Use Redis or database for production)
blacklisted_tokens = set()

# SECRET KEY (Ensure this is set as an environment variable in production)
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-secret-key')
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
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
        response = {
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
        
        return jsonify(response), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Registration failed: {str(e)}'}), 500
    

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

# Add to your main app.py file:
# from routes.auth import auth_bp
# app.register_blueprint(auth_bp)
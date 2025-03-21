from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from app.models import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date)
    
    # Address fields
    street = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100))
    
    # Driver license fields
    license_number = db.Column(db.String(100))
    license_issue_date = db.Column(db.Date)
    license_expiry_date = db.Column(db.Date)
    license_issuing_country = db.Column(db.String(100))
    license_verified = db.Column(db.Boolean, default=False)
    license_verification_date = db.Column(db.DateTime)
    
    # KYC and status fields
    kyc_status = db.Column(db.Enum('PENDING', 'LEVEL1', 'LEVEL2', 'LEVEL3', 'REJECTED', 
                                   name='kyc_status_enum'), default='PENDING')
    kyc_rejection_reason = db.Column(db.Text)
    account_status = db.Column(db.Enum('ACTIVE', 'SUSPENDED', 'DEACTIVATED', 
                                       name='account_status_enum'), default='ACTIVE')
    
    # Security and tracking fields
    login_attempts = db.Column(db.Integer, default=0)
    last_login_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Loyalty program fields
    loyalty_tier = db.Column(db.Enum('BASIC', 'SILVER', 'GOLD', 'PLATINUM', 
                                     name='loyalty_tier_enum'), default='BASIC')
    loyalty_points = db.Column(db.Integer, default=0)
    wallet_address = db.Column(db.String(255))
    
    # Risk and fraud prevention
    risk_score = db.Column(db.Integer, default=0)  # 0-100
    
    # Preferences and consent
    preferred_language = db.Column(db.String(10), default='en')
    marketing_consent = db.Column(db.Boolean, default=False)
    
    # Referral relationship
    referred_by_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    referred_users = db.relationship('User', backref=db.backref('referred_by', remote_side=[id]))
    
    def __repr__(self):
        return f'<User {self.email}>'
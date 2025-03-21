from app import db
from datetime import datetime
import uuid

class Loyalty(db.Model):
    __tablename__ = 'loyalty'
    
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, unique=True)
    
    total_points = db.Column(db.Integer, default=0)
    available_points = db.Column(db.Integer, default=0)
    redeemed_points = db.Column(db.Integer, default=0)
    
    current_tier = db.Column(db.String(20), default='BASIC')  # BASIC, SILVER, GOLD, PLATINUM
    tier_expiry_date = db.Column(db.Date)
    tier_start_date = db.Column(db.Date)
    
    points_to_next_tier = db.Column(db.Integer)
    lifetime_points = db.Column(db.Integer, default=0)
    
    last_points_earned_date = db.Column(db.DateTime)
    last_points_redeemed_date = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    transactions = db.relationship('LoyaltyTransaction', backref='loyalty', lazy=True)

class LoyaltyTransaction(db.Model):
    __tablename__ = 'loyalty_transactions'
    
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    loyalty_id = db.Column(db.String(36), db.ForeignKey('loyalty.id'), nullable=False)
    
    transaction_type = db.Column(db.String(20), nullable=False)  # EARNED, REDEEMED, EXPIRED, ADJUSTED, BONUS
    points = db.Column(db.Integer, nullable=False)
    balance_before = db.Column(db.Integer, nullable=False)
    balance_after = db.Column(db.Integer, nullable=False)
    
    description = db.Column(db.String(255))
    source = db.Column(db.String(30))  # RENTAL, REFERRAL, PROMOTION, SUPPORT_ADJUSTMENT
    source_id = db.Column(db.String(36))  # Reference to the source (e.g., Rental ID)
    
    expiry_date = db.Column(db.Date)  # When these points expire
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(36))  # User or Admin who created this transaction

class LoyaltyReward(db.Model):
    __tablename__ = 'loyalty_rewards'
    
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    points_cost = db.Column(db.Integer, nullable=False)
    
    reward_type = db.Column(db.String(30), nullable=False)  # DISCOUNT, FREE_RENTAL, UPGRADE, PARTNER_REWARD, MERCHANDISE
    discount_percentage = db.Column(db.Float)
    discount_amount = db.Column(db.Float)
    
    valid_from = db.Column(db.DateTime)
    valid_until = db.Column(db.DateTime)
    
    minimum_tier = db.Column(db.String(20), default='BASIC')  # BASIC, SILVER, GOLD, PLATINUM
    is_active = db.Column(db.Boolean, default=True)
    
    image_url = db.Column(db.String(255))
    terms_and_conditions = db.Column(db.Text)
    
    limit_per_user = db.Column(db.Integer)
    total_available = db.Column(db.Integer)
    redeemed_count = db.Column(db.Integer, default=0)
    
    partner_name = db.Column(db.String(100))  # For partner rewards
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
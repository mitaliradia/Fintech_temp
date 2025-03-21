from app import db
from datetime import datetime
import uuid

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    rental_id = db.Column(db.String(36), db.ForeignKey('rentals.id'))
    payment_method_id = db.Column(db.String(36), db.ForeignKey('payment_methods.id'), nullable=False)
    authorization_id = db.Column(db.String(36), db.ForeignKey('payment_authorizations.id'))
    
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    status = db.Column(db.String(30), default='PENDING')  # PENDING, COMPLETED, FAILED, REFUNDED, PARTIALLY_REFUNDED, DISPUTED
    
    payment_intent_id = db.Column(db.String(100))  # Payment processor's ID
    payment_date = db.Column(db.DateTime)
    transaction_reference = db.Column(db.String(100))
    receipt_url = db.Column(db.String(255))
    
    refunded_amount = db.Column(db.Float, default=0)
    refund_reason = db.Column(db.String(255))
    
    payment_processor = db.Column(db.String(50), default='STRIPE')
    payment_type = db.Column(db.String(30), default='RENTAL_CHARGE')  # RENTAL_CHARGE, ADDITIONAL_CHARGE, DAMAGE_CHARGE, REFUND
    
    metadata = db.Column(db.JSON)  # Additional metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    rentals = db.relationship('Rental', backref='payment', lazy=True)

class PaymentAuthorization(db.Model):
    __tablename__ = 'payment_authorizations'
    
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    rental_id = db.Column(db.String(36), db.ForeignKey('rentals.id'))
    payment_method_id = db.Column(db.String(36), db.ForeignKey('payment_methods.id'), nullable=False)
    
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    status = db.Column(db.String(20), default='PENDING')  # PENDING, AUTHORIZED, CAPTURED, VOIDED, FAILED
    
    authorization_code = db.Column(db.String(100))
    authorization_reference = db.Column(db.String(100))
    processor_response = db.Column(db.String(255))
    
    authorization_date = db.Column(db.DateTime)
    expiration_date = db.Column(db.DateTime)  # When authorization expires
    
    captured_amount = db.Column(db.Float, default=0)
    refunded_amount = db.Column(db.Float, default=0)
    
    metadata = db.Column(db.JSON)  # Additional metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    rentals = db.relationship('Rental', backref='authorization', lazy=True)
    payments = db.relationship('Payment', backref='authorization', lazy=True)

class PaymentMethod(db.Model):
    __tablename__ = 'payment_methods'
    
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    type = db.Column(db.String(30), nullable=False)  # CREDIT_CARD, DEBIT_CARD, BANK_ACCOUNT, DIGITAL_WALLET, CRYPTOCURRENCY
    is_default = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='ACTIVE')  # ACTIVE, EXPIRED, INVALID, REMOVED
    
    # For credit/debit card
    card_type = db.Column(db.String(20))
    last4 = db.Column(db.String(4))
    expiry_month = db.Column(db.Integer)
    expiry_year = db.Column(db.Integer)
    cardholder_name = db.Column(db.String(100))
    
    # Billing address
    billing_street = db.Column(db.String(100))
    billing_city = db.Column(db.String(50))
    billing_state = db.Column(db.String(50))
    billing_zip_code = db.Column(db.String(20))
    billing_country = db.Column(db.String(50))
    
    # Tokenized payment info
    tokenized = db.Column(db.String(255))
    payment_processor_id = db.Column(db.String(100))
    
    validation_status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
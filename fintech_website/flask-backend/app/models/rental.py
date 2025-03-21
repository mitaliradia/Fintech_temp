from app import db
# from datetime import datetime
import datetime
import uuid

class Rental(db.Model):
    __tablename__ = 'rentals'
    
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    vehicle_id = db.Column(db.String(36), db.ForeignKey('vehicles.id'), nullable=False)
    pickup_station_id = db.Column(db.String(36), db.ForeignKey('stations.id'), nullable=False)
    return_station_id = db.Column(db.String(36), db.ForeignKey('stations.id'), nullable=False)
    
    booking_date = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    actual_start_date = db.Column(db.DateTime)
    actual_end_date = db.Column(db.DateTime)
    
    status = db.Column(db.String(30), default='PENDING_APPROVAL')  # PENDING_APPROVAL, APPROVED, ACTIVE, COMPLETED, CANCELLED, DECLINED
    approved_by = db.Column(db.String(36), db.ForeignKey('admins.id'))
    approval_date = db.Column(db.DateTime)
    cancellation_reason = db.Column(db.String(255))
    
    initial_charge_level = db.Column(db.Float)  # At pickup
    final_charge_level = db.Column(db.Float)  # At return
    initial_odometer = db.Column(db.Float)
    final_odometer = db.Column(db.Float)
    
    pre_rental_inspection = db.Column(db.JSON)
    post_rental_inspection = db.Column(db.JSON)
    
    total_cost = db.Column(db.Float)
    rental_cost = db.Column(db.Float)
    additional_charges = db.Column(db.JSON)  # Array of additional charges
    discount = db.Column(db.Float, default=0)
    discount_code = db.Column(db.String(50))
    tax_amount = db.Column(db.Float, default=0)
    
    payment_status = db.Column(db.String(20), default='PENDING')  # PENDING, AUTHORIZED, PAID, REFUNDED, DISPUTED, FAILED
    payment_id = db.Column(db.String(36), db.ForeignKey('payments.id'))
    pre_authorization_id = db.Column(db.String(36), db.ForeignKey('payment_authorizations.id'))
    
    loyalty_points_earned = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
    notes = db.Column(db.Text)
    tracking_data = db.Column(db.JSON)  # Array of tracking data points
    
    # Relationships
    pickup_station = db.relationship('Station', foreign_keys=[pickup_station_id])
    return_station = db.relationship('Station', foreign_keys=[return_station_id])
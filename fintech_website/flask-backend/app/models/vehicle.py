from app.models import db
# from datetime import datetime
import datetime
import uuid

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    model = db.Column(db.String(100), nullable=False)
    # manufacturer = db.Column(db.String(100), nullable=False)
    # year = db.Column(db.Integer)
    # color = db.Column(db.String(50))
    # registration_number = db.Column(db.String(50), unique=True, nullable=False)
    vin_number = db.Column(db.String(50), unique=True, nullable=False)
    vehicle_type = db.Column(db.String(20), nullable=False)  # CAR, SCOOTER, BIKE, MOTORCYCLE
    battery_capacity = db.Column(db.Float)  # kWh
    range = db.Column(db.Float)  # km on full charge
    # current_charge_level = db.Column(db.Float)  # Percentage
    status = db.Column(db.String(20), default='AVAILABLE')  # AVAILABLE, RENTED, MAINTENANCE, CHARGING, OUT_OF_SERVICE
    
    # Current location
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    station_id = db.Column(db.String(36), db.ForeignKey('stations.id'))
    
    # Pricing
    hourly_rate = db.Column(db.Float, nullable=False)
    daily_rate = db.Column(db.Float, nullable=False)
    weekly_rate = db.Column(db.Float)
    security_deposit_amount = db.Column(db.Float, nullable=False)
    
    # JSON fields
    # features = db.Column(db.JSON)  # Array of features
    # maintenance_history = db.Column(db.JSON)  # Array of maintenance events
    image_urls = db.Column(db.JSON)  # Array of image URLs
    
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
    # last_maintenance_date = db.Column(db.Date)
    # next_maintenance_date = db.Column(db.Date)
    total_rentals = db.Column(db.Integer, default=0)
    total_distance = db.Column(db.Float, default=0)
    min_loyalty_tier = db.Column(db.String(20), default='BASIC')  # BASIC, SILVER, GOLD, PLATINUM
    
    # Relationships
    # rentals = db.relationship('Rental', backref='vehicle', lazy=True)


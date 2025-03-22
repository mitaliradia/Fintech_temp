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
    rentals = db.relationship('Rental', backref='vehicle', lazy=True)

class Station(db.Model):
    __tablename__ = 'stations'
    
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    
    # Address
    street = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(20))
    country = db.Column(db.String(50))
    
    # Location
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    contact_phone = db.Column(db.String(20))
    contact_email = db.Column(db.String(120))
    operating_hours = db.Column(db.JSON)  # Operating hours for each day
    capacity = db.Column(db.Integer)  # Total parking spots
    available_spots = db.Column(db.Integer)  # Currently available spots
    charging_stations = db.Column(db.Integer)  # Number of charging points
    
    station_master_id = db.Column(db.String(36), db.ForeignKey('admins.id'))
    # amenities = db.Column(db.JSON)  # Array of amenities available
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
    
    # Relationships
    vehicles = db.relationship('Vehicle', backref='station', lazy=True)
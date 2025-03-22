from app.models import db
from datetime import datetime
import uuid

class Station(db.Model):
    __tablename__ = 'stations'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
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
    
    # Contact
    contact_phone = db.Column(db.String(20))
    contact_email = db.Column(db.String(120))
    
    # Operating Hours
    operating_hours = db.Column(db.JSON)  # JSON format for opening and closing times
    
    # Capacity and Availability
    capacity = db.Column(db.Integer)  # Total parking spots
    available_spots = db.Column(db.Integer)  # Currently available spots
    charging_stations = db.Column(db.Integer)  # Number of charging points
    
    # Relationships - Note we're removing the bidirectional relationship that was causing problems
    station_master_id = db.Column(db.String(36), db.ForeignKey('admins.id', deferrable=True))
    
    # Status and Metadata
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Station {self.name}>"
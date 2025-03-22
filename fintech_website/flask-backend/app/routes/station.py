from flask import Blueprint, request, jsonify
from app.models import db
from app.models.station import Station
from app.models.admin import Admin, RoleEnum
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import uuid
from datetime import datetime
import json

# Create blueprint
station_bp = Blueprint('station', __name__, url_prefix='/api/station')

# Helper function to check if the current user has admin permissions
def is_admin_authorized(required_roles=None):
    jwt_data = get_jwt()
    role = jwt_data.get("role", None)
    
    # If no specific roles required, just check if user has any admin role
    if not required_roles:
        return role in [r.value for r in RoleEnum]
    
    # Check if user's role is in the required roles list
    return role in [r.value for r in required_roles]

@station_bp.route("/create", methods=["POST"])
@jwt_required()
def create_station():
    """Create a new charging station"""
    # Check if user has permission (only SUPER_ADMIN or STATION_MASTER can create stations)
    if not is_admin_authorized([RoleEnum.SUPER_ADMIN, RoleEnum.STATION_MASTER]):
        return jsonify({"error": "Unauthorized. Insufficient permissions."}), 403
    
    data = request.get_json()
    
    # Validate required fields
    if not data.get("name"):
        return jsonify({"error": "Station name is required"}), 400
    
    if not data.get("latitude") or not data.get("longitude"):
        return jsonify({"error": "Latitude and longitude are required"}), 400
    
    # Get current admin from JWT token
    admin_id = get_jwt_identity()
    
    # Create new station
    new_station = Station(
        id=str(uuid.uuid4()),
        name=data.get("name"),
        street=data.get("street"),
        city=data.get("city"),
        state=data.get("state"),
        zip_code=data.get("zip_code"),
        country=data.get("country"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        contact_phone=data.get("contact_phone"),
        contact_email=data.get("contact_email"),
        operating_hours=data.get("operating_hours"),
        capacity=data.get("capacity"),
        available_spots=data.get("available_spots", data.get("capacity")),
        charging_stations=data.get("charging_stations", 0),
        is_active=data.get("is_active", True),
        created_at=datetime.utcnow()
    )
    
    # Assign station master if provided
    if data.get("station_master_id"):
        # Validate that the assigned station master exists
        station_master = Admin.query.filter_by(id=data.get("station_master_id")).first()
        if not station_master:
            return jsonify({"error": "Station master not found"}), 404
        new_station.station_master_id = data.get("station_master_id")
    
    db.session.add(new_station)
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Station created successfully", 
        "station_id": new_station.id
    }), 201

@station_bp.route("/list", methods=["GET"])
@jwt_required()
def list_stations():
    """Get a list of all stations"""
    # Get query parameters for filtering and pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Base query
    query = Station.query
    
    # Apply filters if provided
    name = request.args.get('name')
    if name:
        query = query.filter(Station.name.ilike(f"%{name}%"))
    
    is_active = request.args.get('is_active')
    if is_active is not None:
        is_active = is_active.lower() == 'true'
        query = query.filter(Station.is_active == is_active)
    
    # Check if the user is a station master, if so, show only their stations
    admin_id = get_jwt_identity()
    jwt_data = get_jwt()
    role = jwt_data.get("role")
    
    if role == RoleEnum.STATION_MASTER.value:
        query = query.filter(Station.station_master_id == admin_id)
    
    # Paginate results
    stations_page = query.paginate(page=page, per_page=per_page)
    
    # Format response
    stations = []
    for station in stations_page.items:
        stations.append({
            "id": station.id,
            "name": station.name,
            "address": {
                "street": station.street,
                "city": station.city,
                "state": station.state,
                "zip_code": station.zip_code,
                "country": station.country
            },
            "location": {
                "latitude": station.latitude,
                "longitude": station.longitude
            },
            "contact": {
                "phone": station.contact_phone,
                "email": station.contact_email
            },
            "capacity": station.capacity,
            "available_spots": station.available_spots,
            "charging_stations": station.charging_stations,
            "is_active": station.is_active,
            "created_at": station.created_at.isoformat() if station.created_at else None
        })
    
    return jsonify({
        "success": True,
        "stations": stations,
        "pagination": {
            "total": stations_page.total,
            "pages": stations_page.pages,
            "current_page": page,
            "per_page": per_page,
            "has_next": stations_page.has_next,
            "has_prev": stations_page.has_prev
        }
    }), 200

@station_bp.route("/<station_id>", methods=["GET"])
@jwt_required()
def get_station(station_id):
    """Get a specific station by ID"""
    station = Station.query.get(station_id)
    
    if not station:
        return jsonify({"error": "Station not found"}), 404
    
    # Check if user has permission to view this station
    admin_id = get_jwt_identity()
    jwt_data = get_jwt()
    role = jwt_data.get("role")
    
    # If user is a station master, they can only view their own stations
    if role == RoleEnum.STATION_MASTER.value and station.station_master_id != admin_id:
        return jsonify({"error": "Unauthorized. You can only view your assigned stations."}), 403
    
    # Format the station data
    station_data = {
        "id": station.id,
        "name": station.name,
        "address": {
            "street": station.street,
            "city": station.city,
            "state": station.state,
            "zip_code": station.zip_code,
            "country": station.country
        },
        "location": {
            "latitude": station.latitude,
            "longitude": station.longitude
        },
        "contact": {
            "phone": station.contact_phone,
            "email": station.contact_email
        },
        "operating_hours": station.operating_hours,
        "capacity": station.capacity,
        "available_spots": station.available_spots,
        "charging_stations": station.charging_stations,
        "station_master_id": station.station_master_id,
        "is_active": station.is_active,
        "created_at": station.created_at.isoformat() if station.created_at else None,
        "updated_at": station.updated_at.isoformat() if station.updated_at else None
    }
    
    # If station has a station master, include their basic info
    if station.station_master_id:
        station_master = Admin.query.get(station.station_master_id)
        if station_master:
            station_data["station_master"] = {
                "id": station_master.id,
                "name": f"{station_master.first_name} {station_master.last_name}",
                "email": station_master.email
            }
    
    return jsonify({
        "success": True,
        "station": station_data
    }), 200

@station_bp.route("/<station_id>", methods=["PUT"])
@jwt_required()
def update_station(station_id):
    """Update a specific station"""
    station = Station.query.get(station_id)
    
    if not station:
        return jsonify({"error": "Station not found"}), 404
    
    # Check if user has permission to update this station
    admin_id = get_jwt_identity()
    jwt_data = get_jwt()
    role = jwt_data.get("role")
    
    # Only SUPER_ADMIN can update any station
    # STATION_MASTER can only update their assigned stations
    if role == RoleEnum.STATION_MASTER.value and station.station_master_id != admin_id:
        return jsonify({"error": "Unauthorized. You can only update your assigned stations."}), 403
    
    # For other roles than SUPER_ADMIN/STATION_MASTER, deny access
    if role not in [RoleEnum.SUPER_ADMIN.value, RoleEnum.STATION_MASTER.value]:
        return jsonify({"error": "Unauthorized. Insufficient permissions."}), 403
    
    data = request.get_json()
    
    # Update fields if provided
    if "name" in data:
        station.name = data["name"]
    
    # Address fields
    if "street" in data:
        station.street = data["street"]
    if "city" in data:
        station.city = data["city"]
    if "state" in data:
        station.state = data["state"]
    if "zip_code" in data:
        station.zip_code = data["zip_code"]
    if "country" in data:
        station.country = data["country"]
    
    # Location fields
    if "latitude" in data:
        station.latitude = data["latitude"]
    if "longitude" in data:
        station.longitude = data["longitude"]
    
    # Contact fields
    if "contact_phone" in data:
        station.contact_phone = data["contact_phone"]
    if "contact_email" in data:
        station.contact_email = data["contact_email"]
    
    # Capacity fields
    if "capacity" in data:
        station.capacity = data["capacity"]
    if "available_spots" in data:
        station.available_spots = data["available_spots"]
    if "charging_stations" in data:
        station.charging_stations = data["charging_stations"]
    
    # Operating hours
    if "operating_hours" in data:
        station.operating_hours = data["operating_hours"]
    
    # Status
    if "is_active" in data:
        station.is_active = data["is_active"]
    
    # Only SUPER_ADMIN can change the station master
    if "station_master_id" in data and role == RoleEnum.SUPER_ADMIN.value:
        # Validate that the assigned station master exists
        if data["station_master_id"]:
            station_master = Admin.query.filter_by(id=data["station_master_id"]).first()
            if not station_master:
                return jsonify({"error": "Station master not found"}), 404
        station.station_master_id = data["station_master_id"]
    
    # Update timestamp
    station.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Station updated successfully", 
        "station_id": station.id
    }), 200

@station_bp.route("/<station_id>", methods=["DELETE"])
@jwt_required()
def delete_station(station_id):
    """Delete a station (soft delete by setting is_active to False)"""
    # Only SUPER_ADMIN can delete stations
    if not is_admin_authorized([RoleEnum.SUPER_ADMIN]):
        return jsonify({"error": "Unauthorized. Only SUPER_ADMIN can delete stations."}), 403
    
    station = Station.query.get(station_id)
    
    if not station:
        return jsonify({"error": "Station not found"}), 404
    
    # Soft delete - set is_active to False
    station.is_active = False
    station.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Station deleted successfully"
    }), 200

@station_bp.route("/<station_id>/update-availability", methods=["PATCH"])
@jwt_required()
def update_availability(station_id):
    """Update station availability (available parking spots)"""
    station = Station.query.get(station_id)
    
    if not station:
        return jsonify({"error": "Station not found"}), 404
    
    # Check if user has permission to update this station
    admin_id = get_jwt_identity()
    jwt_data = get_jwt()
    role = jwt_data.get("role")
    
    # SUPER_ADMIN, STATION_MASTER of this station, and SUPPORT_STAFF can update availability
    if (role == RoleEnum.STATION_MASTER.value and station.station_master_id != admin_id and 
        role not in [RoleEnum.SUPER_ADMIN.value, RoleEnum.SUPPORT_STAFF.value]):
        return jsonify({"error": "Unauthorized. You can only update availability for your assigned stations."}), 403
    
    data = request.get_json()
    
    if "available_spots" not in data:
        return jsonify({"error": "available_spots is required"}), 400
    
    # Validate the available spots doesn't exceed capacity
    if data["available_spots"] > station.capacity:
        return jsonify({"error": f"Available spots cannot exceed capacity ({station.capacity})"}), 400
    
    station.available_spots = data["available_spots"]
    station.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Station availability updated successfully",
        "available_spots": station.available_spots,
        "capacity": station.capacity
    }), 200
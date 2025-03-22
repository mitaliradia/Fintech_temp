from flask import Blueprint, request, jsonify
from sqlalchemy import func
from app.models import db
from app.models.vehicle import Vehicle
from app.models.station import Station
from app.models.admin import Admin, RoleEnum
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import uuid
from datetime import datetime
import json
import math

# Create blueprint
vehicle_bp = Blueprint('vehicle', __name__,url_prefix='/api/vehicle')



# Helper function to check if the current user has admin permissions
def is_admin_authorized(required_roles=None):
    jwt_data = get_jwt()
    role = jwt_data.get("role", None)
    
    # If no specific roles required, just check if user has any admin role
    if not required_roles:
        return role in [r.value for r in RoleEnum]
    
    # Check if user's role is in the required roles list
    return role in [r.value for r in required_roles]

@vehicle_bp.route("/", methods=["GET"])
def test_vehicle_route():
    return jsonify({"message": "Vehicle routes are working!"}), 200

# Calculate distance between two coordinates using Haversine formula
def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert coordinates from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r

# Format vehicle data for response
def format_vehicle_data(vehicle, include_station=False):
    vehicle_data = {
        "id": vehicle.id,
        "model": vehicle.model,
        "vin_number": vehicle.vin_number,
        "vehicle_type": vehicle.vehicle_type,
        "battery_capacity": vehicle.battery_capacity,
        "range": vehicle.range,
        "status": vehicle.status,
        "location": {
            "latitude": vehicle.latitude,
            "longitude": vehicle.longitude,
        },
        "station_id": vehicle.station_id,
        "pricing": {
            "hourly_rate": vehicle.hourly_rate,
            "daily_rate": vehicle.daily_rate,
            "weekly_rate": vehicle.weekly_rate,
            "security_deposit": vehicle.security_deposit_amount
        },
        "image_urls": vehicle.image_urls,
        "stats": {
            "total_rentals": vehicle.total_rentals,
            "total_distance": vehicle.total_distance
        },
        "min_loyalty_tier": vehicle.min_loyalty_tier,
        "created_at": vehicle.created_at.isoformat() if vehicle.created_at else None,
        "updated_at": vehicle.updated_at.isoformat() if vehicle.updated_at else None
    }
    
    # Include station details if requested
    if include_station and vehicle.station_id:
        station = Station.query.get(vehicle.station_id)
        if station:
            vehicle_data["station"] = {
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
                }
            }
    
    return vehicle_data

@vehicle_bp.route("/create", methods=["POST"])
@jwt_required()
def create_vehicle():
    """Create a new vehicle"""
    # Only SUPER_ADMIN and STATION_MASTER can add vehicles
    if not is_admin_authorized([RoleEnum.SUPER_ADMIN, RoleEnum.STATION_MASTER]):
        return jsonify({"error": "Unauthorized. Insufficient permissions."}), 403
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ["model", "vin_number", "vehicle_type", "hourly_rate", "daily_rate", "security_deposit_amount"]
    for field in required_fields:
        if field not in data or data[field] is None:
            return jsonify({"error": f"Field '{field}' is required"}), 400
    
    # Validate VIN number is unique
    if Vehicle.query.filter_by(vin_number=data.get("vin_number")).first():
        return jsonify({"error": "Vehicle with this VIN number already exists"}), 400
    
    # Validate vehicle_type is valid
    valid_types = ["CAR", "SCOOTER", "BIKE", "MOTORCYCLE"]
    if data.get("vehicle_type") not in valid_types:
        return jsonify({"error": f"Invalid vehicle_type. Must be one of: {', '.join(valid_types)}"}), 400
    
    # Validate station_id if provided
    if data.get("station_id"):
        station = Station.query.get(data.get("station_id"))
        if not station:
            return jsonify({"error": "Station not found"}), 404
            
        # If user is a STATION_MASTER, they can only add vehicles to their own station
        admin_id = get_jwt_identity()
        jwt_data = get_jwt()
        role = jwt_data.get("role")
        
        if role == RoleEnum.STATION_MASTER.value and station.station_master_id != admin_id:
            return jsonify({"error": "Unauthorized. You can only add vehicles to your assigned station."}), 403
    
    # Create new vehicle
    new_vehicle = Vehicle(
        id=str(uuid.uuid4()),
        model=data.get("model"),
        vin_number=data.get("vin_number"),
        vehicle_type=data.get("vehicle_type"),
        battery_capacity=data.get("battery_capacity"),
        range=data.get("range"),
        status=data.get("status", "AVAILABLE"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        station_id=data.get("station_id"),
        hourly_rate=data.get("hourly_rate"),
        daily_rate=data.get("daily_rate"),
        weekly_rate=data.get("weekly_rate"),
        security_deposit_amount=data.get("security_deposit_amount"),
        image_urls=data.get("image_urls", []),
        min_loyalty_tier=data.get("min_loyalty_tier", "BASIC"),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    db.session.add(new_vehicle)
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Vehicle created successfully",
        "vehicle": format_vehicle_data(new_vehicle)
    }), 201

@vehicle_bp.route("", methods=["GET"])
@jwt_required()
def list_vehicles():
    """Get a list of vehicles with filtering options"""
    # Get query parameters for filtering and pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Base query
    query = Vehicle.query
    
    # Apply filters if provided
    vehicle_type = request.args.get('type')
    if vehicle_type:
        query = query.filter(Vehicle.vehicle_type == vehicle_type.upper())
    
    status = request.args.get('status')
    if status:
        query = query.filter(Vehicle.status == status.upper())
    
    station_id = request.args.get('station_id')
    if station_id:
        query = query.filter(Vehicle.station_id == station_id)
    
    min_range = request.args.get('min_range', type=float)
    if min_range:
        query = query.filter(Vehicle.range >= min_range)
    
    max_hourly_rate = request.args.get('max_hourly_rate', type=float)
    if max_hourly_rate:
        query = query.filter(Vehicle.hourly_rate <= max_hourly_rate)
    
    min_loyalty_tier = request.args.get('min_loyalty_tier')
    if min_loyalty_tier:
        query = query.filter(Vehicle.min_loyalty_tier == min_loyalty_tier.upper())
    
    # Check if the user is a station master, if so, only show vehicles at their station
    admin_id = get_jwt_identity()
    jwt_data = get_jwt()
    role = jwt_data.get("role")
    
    if role == RoleEnum.STATION_MASTER.value:
        # Get the station managed by this admin
        station = Station.query.filter_by(station_master_id=admin_id).first()
        if station:
            query = query.filter(Vehicle.station_id == station.id)
    
    # Paginate results
    vehicles_page = query.paginate(page=page, per_page=per_page)
    
    # Format response
    vehicles = []
    for vehicle in vehicles_page.items:
        vehicles.append(format_vehicle_data(vehicle))
    
    return jsonify({
        "success": True,
        "vehicles": vehicles,
        "pagination": {
            "total": vehicles_page.total,
            "pages": vehicles_page.pages,
            "current_page": page,
            "per_page": per_page,
            "has_next": vehicles_page.has_next,
            "has_prev": vehicles_page.has_prev
        }
    }), 200

@vehicle_bp.route("/<vehicle_id>", methods=["GET"])
@jwt_required()
def get_vehicle(vehicle_id):
    """Get details of a specific vehicle"""
    vehicle = Vehicle.query.get(vehicle_id)
    
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    
    # If user is a station master, they can only view vehicles at their station
    admin_id = get_jwt_identity()
    jwt_data = get_jwt()
    role = jwt_data.get("role")
    
    if role == RoleEnum.STATION_MASTER.value:
        # Get the station managed by this admin
        station = Station.query.filter_by(station_master_id=admin_id).first()
        if not station or vehicle.station_id != station.id:
            return jsonify({"error": "Unauthorized. You can only view vehicles at your assigned station."}), 403
    
    return jsonify({
        "success": True,
        "vehicle": format_vehicle_data(vehicle, include_station=True)
    }), 200

@vehicle_bp.route("/nearby", methods=["GET"])
@jwt_required()
def nearby_vehicles():
    """Find vehicles near a given location"""
    # Get location parameters
    latitude = request.args.get('latitude', type=float)
    longitude = request.args.get('longitude', type=float)
    radius = request.args.get('radius', 5.0, type=float)  # Default 5km radius
    
    if not latitude or not longitude:
        return jsonify({"error": "Latitude and longitude are required"}), 400
    
    # Get additional filters
    vehicle_type = request.args.get('type')
    status = request.args.get('status', 'AVAILABLE')  # Default to available vehicles
    
    # Base query
    query = Vehicle.query
    
    # Apply filters
    if vehicle_type:
        query = query.filter(Vehicle.vehicle_type == vehicle_type.upper())
    
    if status:
        query = query.filter(Vehicle.status == status.upper())
    
    # Get all vehicles that match filters
    vehicles = query.all()
    
    # Filter by distance (would be more efficient with PostGIS or similar, but this works for SQLite)
    nearby_vehicles = []
    for vehicle in vehicles:
        if vehicle.latitude and vehicle.longitude:
            distance = calculate_distance(latitude, longitude, vehicle.latitude, vehicle.longitude)
            if distance <= radius:
                vehicle_data = format_vehicle_data(vehicle)
                vehicle_data['distance'] = round(distance, 2)  # Add distance in km
                nearby_vehicles.append(vehicle_data)
    
    # Sort by distance
    nearby_vehicles.sort(key=lambda x: x['distance'])
    
    return jsonify({
        "success": True,
        "count": len(nearby_vehicles),
        "vehicles": nearby_vehicles
    }), 200

@vehicle_bp.route("/types", methods=["GET"])
def vehicle_types():
    """Get available vehicle types and counts"""
    # Query for vehicle types and counts
    types_query = db.session.query(
        Vehicle.vehicle_type,
        func.count(Vehicle.id).label('count')
    ).group_by(Vehicle.vehicle_type).all()
    
    # Format response
    vehicle_types = []
    for type_name, count in types_query:
        vehicle_types.append({
            "type": type_name,
            "count": count
        })
    
    return jsonify({
        "success": True,
        "vehicle_types": vehicle_types
    }), 200

@vehicle_bp.route("/<vehicle_id>", methods=["PUT"])
@jwt_required()
def update_vehicle(vehicle_id):
    """Update a vehicle's information"""
    vehicle = Vehicle.query.get(vehicle_id)
    
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    
    # Check permissions
    admin_id = get_jwt_identity()
    jwt_data = get_jwt()
    role = jwt_data.get("role")
    
    # SUPER_ADMIN can update any vehicle
    # STATION_MASTER can only update vehicles at their station
    if role == RoleEnum.STATION_MASTER.value:
        station = Station.query.filter_by(station_master_id=admin_id).first()
        if not station or vehicle.station_id != station.id:
            return jsonify({"error": "Unauthorized. You can only update vehicles at your assigned station."}), 403
    elif role not in [RoleEnum.SUPER_ADMIN.value]:
        return jsonify({"error": "Unauthorized. Insufficient permissions."}), 403
    
    data = request.get_json()
    
    # Update fields if provided
    if "model" in data:
        vehicle.model = data["model"]
    
    if "vin_number" in data:
        # Check if VIN is being changed and is unique
        if data["vin_number"] != vehicle.vin_number:
            existing = Vehicle.query.filter_by(vin_number=data["vin_number"]).first()
            if existing:
                return jsonify({"error": "Vehicle with this VIN number already exists"}), 400
        vehicle.vin_number = data["vin_number"]
    
    if "vehicle_type" in data:
        valid_types = ["CAR", "SCOOTER", "BIKE", "MOTORCYCLE"]
        if data["vehicle_type"] not in valid_types:
            return jsonify({"error": f"Invalid vehicle_type. Must be one of: {', '.join(valid_types)}"}), 400
        vehicle.vehicle_type = data["vehicle_type"]
    
    if "battery_capacity" in data:
        vehicle.battery_capacity = data["battery_capacity"]
    
    if "range" in data:
        vehicle.range = data["range"]
    
    if "status" in data:
        valid_statuses = ["AVAILABLE", "RENTED", "MAINTENANCE", "CHARGING", "OUT_OF_SERVICE"]
        if data["status"] not in valid_statuses:
            return jsonify({"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}), 400
        vehicle.status = data["status"]
    
    if "latitude" in data:
        vehicle.latitude = data["latitude"]
    
    if "longitude" in data:
        vehicle.longitude = data["longitude"]
    
    # Only SUPER_ADMIN can change which station a vehicle belongs to
    if "station_id" in data and role == RoleEnum.SUPER_ADMIN.value:
        if data["station_id"]:
            station = Station.query.get(data["station_id"])
            if not station:
                return jsonify({"error": "Station not found"}), 404
        vehicle.station_id = data["station_id"]
    
    if "hourly_rate" in data:
        vehicle.hourly_rate = data["hourly_rate"]
    
    if "daily_rate" in data:
        vehicle.daily_rate = data["daily_rate"]
    
    if "weekly_rate" in data:
        vehicle.weekly_rate = data["weekly_rate"]
    
    if "security_deposit_amount" in data:
        vehicle.security_deposit_amount = data["security_deposit_amount"]
    
    if "image_urls" in data:
        vehicle.image_urls = data["image_urls"]
    
    if "min_loyalty_tier" in data:
        valid_tiers = ["BASIC", "SILVER", "GOLD", "PLATINUM"]
        if data["min_loyalty_tier"] not in valid_tiers:
            return jsonify({"error": f"Invalid min_loyalty_tier. Must be one of: {', '.join(valid_tiers)}"}), 400
        vehicle.min_loyalty_tier = data["min_loyalty_tier"]
    
    # Update timestamp
    vehicle.updated_at = datetime.now()
    
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Vehicle updated successfully",
        "vehicle": format_vehicle_data(vehicle)
    }), 200

@vehicle_bp.route("/<vehicle_id>/status", methods=["PATCH"])
@jwt_required()
def update_vehicle_status(vehicle_id):
    """Update a vehicle's status"""
    vehicle = Vehicle.query.get(vehicle_id)
    
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    
    # Check permissions
    admin_id = get_jwt_identity()
    jwt_data = get_jwt()
    role = jwt_data.get("role")
    
    # SUPER_ADMIN, STATION_MASTER of this station, and SUPPORT_STAFF can update vehicle status
    if role == RoleEnum.STATION_MASTER.value:
        station = Station.query.filter_by(station_master_id=admin_id).first()
        if not station or vehicle.station_id != station.id:
            return jsonify({"error": "Unauthorized. You can only update vehicles at your assigned station."}), 403
    elif role not in [RoleEnum.SUPER_ADMIN.value, RoleEnum.SUPPORT_STAFF.value]:
        return jsonify({"error": "Unauthorized. Insufficient permissions."}), 403
    
    data = request.get_json()
    
    if "status" not in data:
        return jsonify({"error": "status is required"}), 400
    
    valid_statuses = ["AVAILABLE", "RENTED", "MAINTENANCE", "CHARGING", "OUT_OF_SERVICE"]
    if data["status"] not in valid_statuses:
        return jsonify({"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}), 400
    
    # Update status and timestamp
    vehicle.status = data["status"]
    vehicle.updated_at = datetime.now()
    
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": f"Vehicle status updated to {data['status']}",
        "vehicle_id": vehicle.id,
        "status": vehicle.status
    }), 200

@vehicle_bp.route("/<vehicle_id>", methods=["DELETE"])
@jwt_required()
def delete_vehicle(vehicle_id):
    """Delete a vehicle (soft delete by setting status to OUT_OF_SERVICE)"""
    # Only SUPER_ADMIN can delete vehicles
    if not is_admin_authorized([RoleEnum.SUPER_ADMIN]):
        return jsonify({"error": "Unauthorized. Only SUPER_ADMIN can delete vehicles."}), 403
    
    vehicle = Vehicle.query.get(vehicle_id)
    
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    
    # Soft delete - set status to OUT_OF_SERVICE
    vehicle.status = "OUT_OF_SERVICE"
    vehicle.updated_at = datetime.now()
    
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Vehicle removed from service"
    }), 200
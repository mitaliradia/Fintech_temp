from flask import Blueprint, request, jsonify
from app import db
from models import Vehicle  # Import your model
from sqlalchemy import func

vehicles_bp = Blueprint("vehicles", __name__, url_prefix="/api/vehicles")


# 1. GET /api/vehicles - Get all available vehicles (with filters)
@vehicles_bp.route("/", methods=["GET"])
def get_vehicles():
    query = Vehicle.query

    # Filtering parameters
    vehicle_type = request.args.get("vehicle_type")
    min_range = request.args.get("min_range", type=float)
    max_hourly_rate = request.args.get("max_hourly_rate", type=float)
    status = request.args.get("status", default="AVAILABLE")

    # Apply filters
    if vehicle_type:
        query = query.filter(Vehicle.vehicle_type == vehicle_type)
    if min_range is not None:
        query = query.filter(Vehicle.range >= min_range)
    if max_hourly_rate is not None:
        query = query.filter(Vehicle.hourly_rate <= max_hourly_rate)
    if status:
        query = query.filter(Vehicle.status == status)

    vehicles = query.all()
    
    return jsonify([{
        "id": v.id,
        "model": v.model,
        "vin_number": v.vin_number,
        "vehicle_type": v.vehicle_type,
        "battery_capacity": v.battery_capacity,
        "range": v.range,
        "hourly_rate": v.hourly_rate,
        "daily_rate": v.daily_rate,
        "weekly_rate": v.weekly_rate,
        "security_deposit_amount": v.security_deposit_amount,
        "status": v.status,
        "latitude": v.latitude,
        "longitude": v.longitude,
        "image_urls": v.image_urls
    } for v in vehicles]), 200


# 2. GET /api/vehicles/<id> - Get vehicle details
@vehicles_bp.route("/<string:vehicle_id>", methods=["GET"])
def get_vehicle_by_id(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404

    return jsonify({
        "id": vehicle.id,
        "model": vehicle.model,
        "vin_number": vehicle.vin_number,
        "vehicle_type": vehicle.vehicle_type,
        "battery_capacity": vehicle.battery_capacity,
        "range": vehicle.range,
        "hourly_rate": vehicle.hourly_rate,
        "daily_rate": vehicle.daily_rate,
        "weekly_rate": vehicle.weekly_rate,
        "security_deposit_amount": vehicle.security_deposit_amount,
        "status": vehicle.status,
        "latitude": vehicle.latitude,
        "longitude": vehicle.longitude,
        "image_urls": vehicle.image_urls
    }), 200


# 3. GET /api/vehicles/nearby - Get vehicles near a location
@vehicles_bp.route("/nearby", methods=["GET"])
def get_nearby_vehicles():
    latitude = request.args.get("latitude", type=float)
    longitude = request.args.get("longitude", type=float)
    radius_km = request.args.get("radius", type=float, default=5.0)  # Default: 5km

    if latitude is None or longitude is None:
        return jsonify({"error": "Latitude and longitude are required"}), 400

    # Approximate filtering using simple bounding box
    lat_range = 0.009 * radius_km  # Approx. 1 km = 0.009 degrees latitude
    lon_range = 0.011 * radius_km  # Approx. adjustment for longitude

    vehicles = Vehicle.query.filter(
        Vehicle.latitude.between(latitude - lat_range, latitude + lat_range),
        Vehicle.longitude.between(longitude - lon_range, longitude + lon_range),
        Vehicle.status == "AVAILABLE"
    ).all()

    return jsonify([{
        "id": v.id,
        "model": v.model,
        "vehicle_type": v.vehicle_type,
        "latitude": v.latitude,
        "longitude": v.longitude,
        "status": v.status
    } for v in vehicles]), 200


# 4. GET /api/vehicles/types - Get vehicle types and categories
@vehicles_bp.route("/types", methods=["GET"])
def get_vehicle_types():
    vehicle_types = db.session.query(Vehicle.vehicle_type).distinct().all()
    return jsonify({"vehicle_types": [t[0] for t in vehicle_types]}), 200

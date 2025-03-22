from flask import Blueprint, request, jsonify
from sqlalchemy import func, and_, or_
from app.models import db
from app.models.rental import Rental
from app.models.vehicle import Vehicle
from app.models.station import Station
from app.models.user import User
from app.models.admin import Admin, RoleEnum
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import uuid
from datetime import datetime, timezone, timedelta
import json

# Create blueprint
rental_bp = Blueprint('rental', __name__, url_prefix='/api/rentals')

# Helper function to check if the current user has admin permissions
def is_admin_authorized(required_roles=None):
    jwt_data = get_jwt()
    role = jwt_data.get("role", None)
    
    # If no specific roles required, just check if user has any admin role
    if not required_roles:
        return role in [r.value for r in RoleEnum]
    
    # Check if user's role is in the required roles list
    return role in [r.value for r in required_roles]

# Helper function to format rental data for response
def format_rental_data(rental, include_vehicle_details=False, include_station_details=False):
    rental_data = {
        "id": rental.id,
        "user_id": rental.user_id,
        "vehicle_id": rental.vehicle_id,
        "pickup_station_id": rental.pickup_station_id,
        "return_station_id": rental.return_station_id,
        "booking_date": rental.booking_date.isoformat() if rental.booking_date else None,
        "start_date": rental.start_date.isoformat() if rental.start_date else None,
        "end_date": rental.end_date.isoformat() if rental.end_date else None,
        "actual_start_date": rental.actual_start_date.isoformat() if rental.actual_start_date else None,
        "actual_end_date": rental.actual_end_date.isoformat() if rental.actual_end_date else None,
        "status": rental.status,
        "approved_by": rental.approved_by,
        "approval_date": rental.approval_date.isoformat() if rental.approval_date else None,
        "cancellation_reason": rental.cancellation_reason,
        "total_cost": rental.total_cost,
        "rental_cost": rental.rental_cost,
        "additional_charges": rental.additional_charges,
        "discount": rental.discount,
        "discount_code": rental.discount_code,
        "tax_amount": rental.tax_amount,
        "payment_status": rental.payment_status,
        "payment_id": rental.payment_id,
        "pre_authorization_id": rental.pre_authorization_id,
        "loyalty_points_earned": rental.loyalty_points_earned,
        "created_at": rental.created_at.isoformat() if rental.created_at else None,
        "updated_at": rental.updated_at.isoformat() if rental.updated_at else None
    }
    
    # Include vehicle details if requested
    if include_vehicle_details:
        vehicle = Vehicle.query.get(rental.vehicle_id)
        if vehicle:
            rental_data["vehicle"] = {
                "id": vehicle.id,
                "model": vehicle.model,
                "vehicle_type": vehicle.vehicle_type,
                "image_urls": vehicle.image_urls
            }
    
    # Include station details if requested
    if include_station_details:
        pickup_station = Station.query.get(rental.pickup_station_id)
        return_station = Station.query.get(rental.return_station_id)
        
        if pickup_station:
            rental_data["pickup_station"] = {
                "id": pickup_station.id,
                "name": pickup_station.name,
                "address": {
                    "street": pickup_station.street,
                    "city": pickup_station.city,
                    "state": pickup_station.state,
                    "zip_code": pickup_station.zip_code,
                    "country": pickup_station.country
                },
                "location": {
                    "latitude": pickup_station.latitude,
                    "longitude": pickup_station.longitude
                }
            }
        
        if return_station:
            rental_data["return_station"] = {
                "id": return_station.id,
                "name": return_station.name,
                "address": {
                    "street": return_station.street,
                    "city": return_station.city,
                    "state": return_station.state,
                    "zip_code": return_station.zip_code,
                    "country": return_station.country
                },
                "location": {
                    "latitude": return_station.latitude,
                    "longitude": return_station.longitude
                }
            }
    
    return rental_data

# Helper function to format rental list items (simplified version for lists)
def format_rental_list_item(rental):
    vehicle = Vehicle.query.get(rental.vehicle_id)
    pickup_station = Station.query.get(rental.pickup_station_id)
    return_station = Station.query.get(rental.return_station_id)
    
    return {
        "id": rental.id,
        "vehicle": {
            "id": vehicle.id,
            "model": vehicle.model,
            "vehicle_type": vehicle.vehicle_type,
            "image_urls": vehicle.image_urls[0] if vehicle.image_urls and len(vehicle.image_urls) > 0 else None
        },
        "start_date": rental.start_date.isoformat() if rental.start_date else None,
        "end_date": rental.end_date.isoformat() if rental.end_date else None,
        "actual_start_date": rental.actual_start_date.isoformat() if rental.actual_start_date else None,
        "actual_end_date": rental.actual_end_date.isoformat() if rental.actual_end_date else None,
        "status": rental.status,
        "pickup_station_name": pickup_station.name if pickup_station else None,
        "return_station_name": return_station.name if return_station else None,
        "total_cost": rental.total_cost,
        "loyalty_points_earned": rental.loyalty_points_earned
    }

# Calculate rental cost based on vehicle rates and rental duration
def calculate_rental_cost(vehicle, start_date, end_date):
    # Calculate the rental duration in hours
    duration = (end_date - start_date).total_seconds() / 3600
    
    # Determine if hourly, daily, or weekly rate applies
    hourly_rate = vehicle.hourly_rate or 0
    daily_rate = vehicle.daily_rate or 0
    weekly_rate = vehicle.weekly_rate or 0
    
    # Calculate costs for different durations
    if duration <= 24:
        # Hourly rate (minimum 1 hour)
        hours = max(1, int(duration))
        return hourly_rate * hours
    elif duration <= 168:  # 7 days * 24 hours
        # Daily rate (minimum 1 day)
        days = max(1, int(duration / 24))
        return daily_rate * days
    else:
        # Weekly rate plus daily rate for extra days
        weeks = int(duration / 168)
        remaining_days = int((duration % 168) / 24)
        return (weekly_rate * weeks) + (daily_rate * remaining_days)

@rental_bp.route("/", methods=["GET"])
def test_rental_route():
    return jsonify({"message": "Rental routes are working!"}), 200

@rental_bp.route("", methods=["POST"])
@jwt_required()
def create_rental():
    """Create a new rental booking"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    required_fields = ["vehicle_id", "pickup_station_id", "return_station_id", "start_date", "end_date"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Field '{field}' is required"}), 400
    
    # Parse dates
    try:
        start_date = datetime.fromisoformat(data["start_date"].replace('Z', '+00:00'))
        end_date = datetime.fromisoformat(data["end_date"].replace('Z', '+00:00'))
    except ValueError:
        return jsonify({"error": "Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SSZ)"}), 400
    
    # Validate dates
    now = datetime.now(timezone.utc)
    if start_date < now:
        return jsonify({"error": "Start date must be in the future"}), 400
    
    if end_date <= start_date:
        return jsonify({"error": "End date must be after start date"}), 400
    
    # Verify vehicle exists and is available
    vehicle = Vehicle.query.get(data["vehicle_id"])
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    
    if vehicle.status != "AVAILABLE":
        return jsonify({"error": f"Vehicle is not available (current status: {vehicle.status})"}), 400
    
    # Check if there are any overlapping rentals for this vehicle
    overlapping_rentals = Rental.query.filter(
        Rental.vehicle_id == data["vehicle_id"],
        Rental.status.in_(["PENDING_APPROVAL", "APPROVED", "ACTIVE"]),
        or_(
            and_(Rental.start_date <= start_date, Rental.end_date >= start_date),
            and_(Rental.start_date <= end_date, Rental.end_date >= end_date),
            and_(Rental.start_date >= start_date, Rental.end_date <= end_date)
        )
    ).all()
    
    if overlapping_rentals:
        return jsonify({"error": "Vehicle is already booked for part or all of the requested time period"}), 409
    
    # Verify stations exist
    pickup_station = Station.query.get(data["pickup_station_id"])
    if not pickup_station:
        return jsonify({"error": "Pickup station not found"}), 404
    
    return_station = Station.query.get(data["return_station_id"])
    if not return_station:
        return jsonify({"error": "Return station not found"}), 404
    
    # Get user for loyalty tier check
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Check loyalty tier requirements
    user_tier = user.loyalty_tier if hasattr(user, 'loyalty_tier') else "BASIC"
    vehicle_min_tier = vehicle.min_loyalty_tier
    
    tier_levels = {"BASIC": 0, "SILVER": 1, "GOLD": 2, "PLATINUM": 3}
    if tier_levels.get(user_tier, 0) < tier_levels.get(vehicle_min_tier, 0):
        return jsonify({
            "error": f"This vehicle requires a minimum loyalty tier of {vehicle_min_tier}. Your current tier is {user_tier}."
        }), 403
    
    # Calculate rental cost
    rental_cost = calculate_rental_cost(vehicle, start_date, end_date)
    
    # Apply discount if code provided
    discount = 0
    discount_code = data.get("discount_code")
    # In real implementation, validate discount code and calculate discount
    # This is a simplified example
    if discount_code:
        # Apply a simple 10% discount for demonstration
        discount = rental_cost * 0.1
    
    # Calculate tax (example: 10%)
    tax_amount = (rental_cost - discount) * 0.1
    
    # Calculate total cost
    total_cost = rental_cost - discount + tax_amount
    
    # Create new rental
    new_rental = Rental(
        id=str(uuid.uuid4()),
        user_id=user_id,
        vehicle_id=data["vehicle_id"],
        pickup_station_id=data["pickup_station_id"],
        return_station_id=data["return_station_id"],
        booking_date=datetime.now(timezone.utc),
        start_date=start_date,
        end_date=end_date,
        status="PENDING_APPROVAL",
        rental_cost=rental_cost,
        discount=discount,
        discount_code=discount_code,
        tax_amount=tax_amount,
        total_cost=total_cost,
        payment_status="PENDING",
        additional_charges=data.get("additional_charges", []),
        notes=data.get("notes"),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    
    db.session.add(new_rental)
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Rental booking created successfully",
        "rental": format_rental_data(new_rental)
    }), 201

@rental_bp.route("/<rental_id>", methods=["GET"])
@jwt_required()
def get_rental(rental_id):
    """Get details of a specific rental"""
    user_id = get_jwt_identity()
    
    # Check if rental exists
    rental = Rental.query.get(rental_id)
    if not rental:
        return jsonify({"error": "Rental not found"}), 404
    
    # Check if user is authorized to view this rental
    is_admin = is_admin_authorized()
    if not is_admin and rental.user_id != user_id:
        return jsonify({"error": "Unauthorized to view this rental"}), 403
    
    return jsonify({
        "success": True,
        "rental": format_rental_data(rental, include_vehicle_details=True, include_station_details=True)
    }), 200

@rental_bp.route("/<rental_id>/cancel", methods=["PUT"])
@jwt_required()
def cancel_rental(rental_id):
    """Cancel a rental booking"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Check if rental exists
    rental = Rental.query.get(rental_id)
    if not rental:
        return jsonify({"error": "Rental not found"}), 404
    
    # Check if user is authorized to cancel this rental
    is_admin = is_admin_authorized()
    if not is_admin and rental.user_id != user_id:
        return jsonify({"error": "Unauthorized to cancel this rental"}), 403
    
    # Check if rental can be cancelled
    if rental.status not in ["PENDING_APPROVAL", "APPROVED"]:
        return jsonify({"error": f"Cannot cancel rental with status: {rental.status}"}), 400
    
    # If the rental is already active, only admins can cancel it
    if rental.status == "ACTIVE" and not is_admin:
        return jsonify({"error": "Cannot cancel an active rental. Please contact customer support."}), 400
    
    # Update rental status
    rental.status = "CANCELLED"
    rental.cancellation_reason = data.get("cancellation_reason")
    rental.updated_at = datetime.now(timezone.utc)
    
    # In a real implementation, handle refund if payment was made
    refund_amount = 0
    refund_status = "NONE"
    
    if rental.payment_status == "PAID":
        # Calculate refund based on cancellation policy and time until rental
        time_until_rental = rental.start_date - datetime.now(timezone.utc)
        
        if time_until_rental > timedelta(days=7):
            # Full refund if cancelled more than 7 days in advance
            refund_amount = rental.total_cost
            refund_status = "PROCESSING"
        elif time_until_rental > timedelta(days=2):
            # 50% refund if cancelled 2-7 days in advance
            refund_amount = rental.total_cost * 0.5
            refund_status = "PROCESSING"
        else:
            # No refund if cancelled less than 2 days in advance
            refund_amount = 0
            refund_status = "NONE"
    
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Rental successfully cancelled",
        "rental_id": rental.id,
        "status": rental.status,
        "refund_amount": refund_amount,
        "refund_status": refund_status
    }), 200

@rental_bp.route("/active", methods=["GET"])
@jwt_required()
def get_active_rentals():
    """Get user's active rentals"""
    user_id = get_jwt_identity()
    
    # Get query parameters for pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Query for active rentals
    query = Rental.query.filter_by(
        user_id=user_id,
        status="ACTIVE"
    ).order_by(Rental.start_date.desc())
    
    # Paginate results
    rentals_page = query.paginate(page=page, per_page=per_page)
    
    # Format response
    rentals = []
    for rental in rentals_page.items:
        rentals.append(format_rental_list_item(rental))
    
    return jsonify({
        "success": True,
        "rentals": rentals,
        "pagination": {
            "total": rentals_page.total,
            "pages": rentals_page.pages,
            "current_page": page,
            "per_page": per_page,
            "has_next": rentals_page.has_next,
            "has_prev": rentals_page.has_prev
        }
    }), 200

@rental_bp.route("/upcoming", methods=["GET"])
@jwt_required()
def get_upcoming_rentals():
    """Get user's upcoming rentals"""
    user_id = get_jwt_identity()
    
    # Get query parameters for pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Current date
    now = datetime.now(timezone.utc)
    
    # Query for upcoming rentals (approved but not yet started)
    query = Rental.query.filter(
        Rental.user_id == user_id,
        Rental.status == "APPROVED",
        Rental.start_date > now
    ).order_by(Rental.start_date.asc())
    
    # Paginate results
    rentals_page = query.paginate(page=page, per_page=per_page)
    
    # Format response
    rentals = []
    for rental in rentals_page.items:
        rentals.append(format_rental_list_item(rental))
    
    return jsonify({
        "success": True,
        "rentals": rentals,
        "pagination": {
            "total": rentals_page.total,
            "pages": rentals_page.pages,
            "current_page": page,
            "per_page": per_page,
            "has_next": rentals_page.has_next,
            "has_prev": rentals_page.has_prev
        }
    }), 200

@rental_bp.route("/past", methods=["GET"])
@jwt_required()
def get_past_rentals():
    """Get user's past rentals"""
    user_id = get_jwt_identity()
    
    # Get query parameters for pagination and sorting
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_field = request.args.get('sort', 'end_date')
    sort_order = request.args.get('order', 'desc')
    
    # Validate sort field
    valid_sort_fields = ['start_date', 'end_date', 'created_at', 'total_cost']
    if sort_field not in valid_sort_fields:
        sort_field = 'end_date'
    
    # Build query for past rentals (completed or cancelled)
    query = Rental.query.filter(
        Rental.user_id == user_id,
        Rental.status.in_(["COMPLETED", "CANCELLED"])
    )
    
    # Apply sorting
    if sort_order.lower() == 'asc':
        query = query.order_by(getattr(Rental, sort_field).asc())
    else:
        query = query.order_by(getattr(Rental, sort_field).desc())
    
    # Paginate results
    rentals_page = query.paginate(page=page, per_page=per_page)
    
    # Format response
    rentals = []
    for rental in rentals_page.items:
        rentals.append(format_rental_list_item(rental))
    
    return jsonify({
        "success": True,
        "rentals": rentals,
        "pagination": {
            "total": rentals_page.total,
            "pages": rentals_page.pages,
            "current_page": page,
            "per_page": per_page,
            "has_next": rentals_page.has_next,
            "has_prev": rentals_page.has_prev
        }
    }), 200

# Admin Routes

@rental_bp.route("/admin/pending", methods=["GET"])
@jwt_required()
def get_pending_rentals():
    """Get rentals pending approval (admin only)"""
    # Check if user is admin
    if not is_admin_authorized():
        return jsonify({"error": "Unauthorized. Admin access required."}), 403
    
    # Get query parameters for pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Query for pending rentals
    query = Rental.query.filter_by(status="PENDING_APPROVAL").order_by(Rental.booking_date.asc())
    
    # Check if admin is station master - only show rentals for their station
    user_id = get_jwt_identity()
    jwt_data = get_jwt()
    role = jwt_data.get("role")
    
    if role == RoleEnum.STATION_MASTER.value:
        admin = Admin.query.get(user_id)
        if admin and admin.station_id:
            query = query.filter(
                or_(
                    Rental.pickup_station_id == admin.station_id,
                    Rental.return_station_id == admin.station_id
                )
            )
    
    # Paginate results
    rentals_page = query.paginate(page=page, per_page=per_page)
    
    # Format response
    rentals = []
    for rental in rentals_page.items:
        rental_data = format_rental_list_item(rental)
        
        # Add user info for admin view
        user = User.query.get(rental.user_id)
        if user:
            rental_data["user"] = {
                "id": str(user.id),
                "name": f"{user.first_name} {user.last_name}",
                "email": user.email,
                "phone": user.phone
            }
        
        rentals.append(rental_data)
    
    return jsonify({
        "success": True,
        "rentals": rentals,
        "pagination": {
            "total": rentals_page.total,
            "pages": rentals_page.pages,
            "current_page": page,
            "per_page": per_page,
            "has_next": rentals_page.has_next,
            "has_prev": rentals_page.has_prev
        }
    }), 200

@rental_bp.route("/<rental_id>/approve", methods=["PUT"])
@jwt_required()
def approve_rental(rental_id):
    """Approve a rental (admin only)"""
    # Check if user is admin
    if not is_admin_authorized():
        return jsonify({"error": "Unauthorized. Admin access required."}), 403
    
    admin_id = get_jwt_identity()
    
    # Check if rental exists
    rental = Rental.query.get(rental_id)
    if not rental:
        return jsonify({"error": "Rental not found"}), 404
    
    # Check if rental status is valid for approval
    if rental.status != "PENDING_APPROVAL":
        return jsonify({"error": f"Cannot approve rental with status: {rental.status}"}), 400
    
    # Update rental status
    rental.status = "APPROVED"
    rental.approved_by = admin_id
    rental.approval_date = datetime.now(timezone.utc)
    rental.updated_at = datetime.now(timezone.utc)
    
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Rental approved successfully",
        "rental_id": rental.id,
        "status": rental.status
    }), 200

@rental_bp.route("/<rental_id>/decline", methods=["PUT"])
@jwt_required()
def decline_rental(rental_id):
    """Decline a rental (admin only)"""
    # Check if user is admin
    if not is_admin_authorized():
        return jsonify({"error": "Unauthorized. Admin access required."}), 403
    
    data = request.get_json()
    admin_id = get_jwt_identity()
    
    # Check if rental exists
    rental = Rental.query.get(rental_id)
    if not rental:
        return jsonify({"error": "Rental not found"}), 404
    
    # Check if rental status is valid for declining
    if rental.status != "PENDING_APPROVAL":
        return jsonify({"error": f"Cannot decline rental with status: {rental.status}"}), 400
    
    # Update rental status
    rental.status = "DECLINED"
    rental.approved_by = admin_id
    rental.approval_date = datetime.now(timezone.utc)
    rental.cancellation_reason = data.get("reason", "Declined by admin")
    rental.updated_at = datetime.now(timezone.utc)
    
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Rental declined successfully",
        "rental_id": rental.id,
        "status": rental.status
    }), 200

@rental_bp.route("/<rental_id>/start", methods=["PUT"])
@jwt_required()
def start_rental(rental_id):
    """Start a rental (change status to ACTIVE)"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Check if rental exists
    rental = Rental.query.get(rental_id)
    if not rental:
        return jsonify({"error": "Rental not found"}), 404
    
    # Check authorization
    is_admin = is_admin_authorized()
    if not is_admin and rental.user_id != user_id:
        return jsonify({"error": "Unauthorized to start this rental"}), 403
    
    # Check if rental status is valid for starting
    if rental.status != "APPROVED":
        return jsonify({"error": f"Cannot start rental with status: {rental.status}"}), 400
    
    # Get vehicle
    vehicle = Vehicle.query.get(rental.vehicle_id)
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    
    # Check if vehicle is available
    if vehicle.status != "AVAILABLE":
        return jsonify({"error": f"Vehicle is not available (current status: {vehicle.status})"}), 400
    
    # Update rental
    rental.status = "ACTIVE"
    rental.actual_start_date = datetime.now(timezone.utc)
    rental.initial_charge_level = data.get("initial_charge_level")
    rental.initial_odometer = data.get("initial_odometer")
    rental.pre_rental_inspection = data.get("pre_rental_inspection")
    rental.updated_at = datetime.now(timezone.utc)
    
    # Update vehicle status
    vehicle.status = "RENTED"
    vehicle.updated_at = datetime.now(timezone.utc)
    
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Rental started successfully",
        "rental_id": rental.id,
        "status": rental.status,
        "actual_start_date": rental.actual_start_date.isoformat() if rental.actual_start_date else None
    }), 200

@rental_bp.route("/<rental_id>/complete", methods=["PUT"])
@jwt_required()
def complete_rental(rental_id):
    """Complete a rental (return vehicle)"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Check if rental exists
    rental = Rental.query.get(rental_id)
    if not rental:
        return jsonify({"error": "Rental not found"}), 404
    
    # Check authorization
    is_admin = is_admin_authorized()
    if not is_admin and rental.user_id != user_id:
        return jsonify({"error": "Unauthorized to complete this rental"}), 403
    
    # Check if rental status is valid for completion
    if rental.status != "ACTIVE":
        return jsonify({"error": f"Cannot complete rental with status: {rental.status}"}), 400
    
    # Get vehicle
    vehicle = Vehicle.query.get(rental.vehicle_id)
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    
    # Calculate additional charges if any
    additional_charges = []
    
    # Check for late return
    now = datetime.now(timezone.utc)
    if now > rental.end_date:
        hours_late = (now - rental.end_date).total_seconds() / 3600
        late_fee = hours_late * vehicle.hourly_rate * 1.5  # 150% of hourly rate
        
        if late_fee > 0:
            additional_charges.append({
                "type": "LATE_RETURN",
                "description": f"Late return fee ({int(hours_late)} hours)",
                "amount": late_fee
            })
    
    # Check for battery charge difference
    final_charge_level = data.get("final_charge_level")
    if final_charge_level is not None and rental.initial_charge_level is not None:
        charge_difference = rental.initial_charge_level - final_charge_level
        if charge_difference > 20:  # More than 20% battery used
            recharge_fee = (charge_difference - 20) * 0.5  # $0.50 per % over 20%
            additional_charges.append({
                "type": "RECHARGE_FEE",
                "description": f"Battery recharge fee ({int(charge_difference)}% used)",
                "amount": recharge_fee
            })
    
    # Calculate distance traveled
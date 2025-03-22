from flask import Blueprint, request, jsonify
from app import db
from models.station import Station
from auth_middleware import token_required

station_bp = Blueprint('station', __name__, url_prefix='/api/stations')

@station_bp.route('', methods=['GET'])
def get_all_stations():
    """
    Get all stations with optional filtering
    Query parameters:
    - is_active: Filter by active status (true/false)
    - city: Filter by city
    - state: Filter by state
    - has_charging: Filter stations with charging points (true/false)
    - limit: Limit the number of results
    - offset: Offset for pagination
    """
    try:
        # Start with a base query
        query = Station.query
        
        # Apply filters from query parameters
        if request.args.get('is_active'):
            is_active = request.args.get('is_active').lower() == 'true'
            query = query.filter(Station.is_active == is_active)
        
        if request.args.get('city'):
            query = query.filter(Station.city.ilike(f"%{request.args.get('city')}%"))
        
        if request.args.get('state'):
            query = query.filter(Station.state.ilike(f"%{request.args.get('state')}%"))
        
        if request.args.get('has_charging'):
            has_charging = request.args.get('has_charging').lower() == 'true'
            if has_charging:
                query = query.filter(Station.charging_stations > 0)
            else:
                query = query.filter(Station.charging_stations == 0)
        
        # Pagination
        limit = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))
        
        # Get results with pagination
        stations = query.limit(limit).offset(offset).all()
        
        # Count total available records for pagination info
        total_count = query.count()
        
        # Format the response
        result = []
        for station in stations:
            result.append({
                'id': station.id,
                'name': station.name,
                'address': {
                    'street': station.street,
                    'city': station.city,
                    'state': station.state,
                    'zip_code': station.zip_code,
                    'country': station.country
                },
                'location': {
                    'latitude': station.latitude,
                    'longitude': station.longitude
                },
                'contact': {
                    'phone': station.contact_phone,
                    'email': station.contact_email
                },
                'capacity': station.capacity,
                'available_spots': station.available_spots,
                'charging_stations': station.charging_stations,
                'operating_hours': station.operating_hours,
                'amenities': station.amenities,
                'is_active': station.is_active,
                'created_at': station.created_at.isoformat() if station.created_at else None,
                'updated_at': station.updated_at.isoformat() if station.updated_at else None
            })
        
        response = {
            'success': True,
            'count': len(result),
            'total': total_count,
            'offset': offset,
            'limit': limit,
            'stations': result
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving stations: {str(e)}'
        }), 500

@station_bp.route('/<string:station_id>', methods=['GET'])
def get_station(station_id):
    """Get a specific station by ID"""
    try:
        station = Station.query.get(station_id)
        
        if not station:
            return jsonify({
                'success': False,
                'message': 'Station not found'
            }), 404
        
        # Format the response
        response = {
            'success': True,
            'station': {
                'id': station.id,
                'name': station.name,
                'address': {
                    'street': station.street,
                    'city': station.city,
                    'state': station.state,
                    'zip_code': station.zip_code,
                    'country': station.country
                },
                'location': {
                    'latitude': station.latitude,
                    'longitude': station.longitude
                },
                'contact': {
                    'phone': station.contact_phone,
                    'email': station.contact_email
                },
                'capacity': station.capacity,
                'available_spots': station.available_spots,
                'charging_stations': station.charging_stations,
                'operating_hours': station.operating_hours,
                'amenities': station.amenities,
                'is_active': station.is_active,
                'created_at': station.created_at.isoformat() if station.created_at else None,
                'updated_at': station.updated_at.isoformat() if station.updated_at else None
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving station: {str(e)}'
        }), 500

@station_bp.route('', methods=['POST'])
@token_required
def create_station(current_user):
    """
    Create a new station
    Requires authentication with admin privileges
    """
    try:
        # Check if user has admin privileges (You may need to adjust this based on your auth system)
        # This is a placeholder for permission checking
        admin_check = hasattr(current_user, 'is_admin') and current_user.is_admin
        if not admin_check:
            return jsonify({
                'success': False,
                'message': 'Unauthorized. Admin privileges required to create stations'
            }), 403
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'latitude', 'longitude']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Create new station
        new_station = Station(
            name=data['name'],
            street=data.get('street'),
            city=data.get('city'),
            state=data.get('state'),
            zip_code=data.get('zip_code'),
            country=data.get('country'),
            latitude=data['latitude'],
            longitude=data['longitude'],
            contact_phone=data.get('contact_phone'),
            contact_email=data.get('contact_email'),
            operating_hours=data.get('operating_hours', {}),
            capacity=data.get('capacity', 0),
            available_spots=data.get('available_spots', 0),
            charging_stations=data.get('charging_stations', 0),
            amenities=data.get('amenities', []),
            is_active=data.get('is_active', True),
            station_master_id=data.get('station_master_id')
        )
        
        db.session.add(new_station)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Station created successfully',
            'station': {
                'id': new_station.id,
                'name': new_station.name,
                'location': {
                    'latitude': new_station.latitude,
                    'longitude': new_station.longitude
                },
                'is_active': new_station.is_active,
                'created_at': new_station.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error creating station: {str(e)}'
        }), 500
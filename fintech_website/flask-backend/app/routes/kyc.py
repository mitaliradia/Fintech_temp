from flask import Blueprint, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

kyc_bp = Blueprint('kyc', __name__, url_prefix='/api/kyc')

# Configuration
SANDBOX_HOST = os.getenv('SANDBOX_HOST', 'https://api.sandbox.co.in')
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
API_VERSION = os.getenv('API_VERSION', '2.0')

def get_access_token():
    url = f"{SANDBOX_HOST}/authenticate"
    headers = {
        'x-api-key': API_KEY,
        'x-api-secret': API_SECRET,
        'x-api-version': API_VERSION
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('access_token')
    return None

@kyc_bp.route('/initiate', methods=['POST'])
def initiate_kyc():
    data = request.json
    aadhaar_number = data.get('aadhaar_number')
    
    if not aadhaar_number:
        return jsonify({'success': False, 'message': 'Aadhaar number is required'}), 400

    access_token = get_access_token()
    if not access_token:
        return jsonify({'success': False, 'message': 'Failed to authenticate with KYC service'}), 500

    url = f"{SANDBOX_HOST}/kyc/aadhaar/okyc/otp"
    headers = {
        'Authorization': access_token,  # Note: No "Bearer" prefix if that's what worked
        'x-api-key': API_KEY,
        'x-api-version': API_VERSION,
        'Content-Type': 'application/json'
    }
    payload = {
        "@entity": "in.co.sandbox.kyc.aadhaar.okyc.otp.request",
        "aadhaar_number": aadhaar_number,
        "consent": "y",
        "reason": "for KYC"
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        data = response_json.get('data', {})
        reference_id = data.get('reference_id')
        
        return jsonify({
            'success': True,
            'message': 'OTP sent successfully',
            'reference_id': reference_id,
            'access_token': access_token,
            'aadhaar_number': aadhaar_number,
            'verify_url': f"/api/kyc/verify/{reference_id}/{access_token}"
        }), 200
    else:
        return jsonify({
            'success': False, 
            'message': 'Failed to send OTP',
            'error': response.text if hasattr(response, 'text') else 'Unknown error'
        }), response.status_code

@kyc_bp.route('/verify/<reference_id>/<path:access_token>', methods=['POST'])
def verify_kyc(reference_id, access_token):
    """
    Verify KYC using the reference ID and access token from the URL path parameters
    """
    data = request.json
    otp = data.get('otp')
    
    if not otp:
        return jsonify({'success': False, 'message': 'OTP is required'}), 400

    url = f"{SANDBOX_HOST}/kyc/aadhaar/okyc/otp/verify"
    headers = {
        'Authorization': access_token,  # Using the access token from URL parameter
        'x-api-key': API_KEY,
        'x-api-version': API_VERSION,
        # 'Content-Type': 'application/json'
    }
    payload = {
        "@entity": "in.co.sandbox.kyc.aadhaar.okyc.request",
        "reference_id": reference_id,
        "otp": otp
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return jsonify({
            'success': True,
            'message': 'KYC verification successful',
            'response_data': response.json()
        }), 200
    else:
        return jsonify({
            'success': False, 
            'message': 'KYC verification failed',
            'error': response.text if hasattr(response, 'text') else 'Unknown error'
        }), response.status_code

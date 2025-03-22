from flask import Blueprint, request, jsonify
import razorpay
import os
from flask_cors import CORS

# Fix the syntax error
pay_bp = Blueprint("pay", __name__)
CORS(pay_bp)  # Enable CORS for this blueprint

# Razorpay credentials - USE REAL VALUES HERE
RAZORPAY_KEY_ID = "rzp_test_SSVqgvkApR03lb"  # Your test key
RAZORPAY_KEY_SECRET = "WWTtpKmJGvzXtj0hyqnJPGk6"  # Replace with your actual secret

# Initialize Razorpay client
try:
    razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
    print(f"Razorpay client initialized successfully with key ID: {RAZORPAY_KEY_ID}")
except Exception as e:
    print(f"Failed to initialize Razorpay client: {str(e)}")

@pay_bp.route("/create_order", methods=["POST"])
def create_order():
    try:
        data = request.json
        print(f"Received order request: {data}")
        
        amount = int(float(data.get("amount", 0))) * 100  # Convert to paise, handle potential string input
        name = data.get("name")
        
        print(f"Processing order for {name}, amount: {amount} paise")
        
        if amount <= 0 or not name:
            print("Invalid input: amount or name is missing/invalid")
            return jsonify({"error": "Invalid input"}), 400
            
        # Create an order with Razorpay
        order_data = {
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        }
        print(f"Creating Razorpay order with data: {order_data}")
        
        order = razorpay_client.order.create(order_data)
        print(f"Created Razorpay order: {order}")
        
        return jsonify(order)
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error creating order: {error_msg}")
        return jsonify({"error": error_msg}), 500
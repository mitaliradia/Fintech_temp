from flask import Blueprint, request, jsonify
import razorpay
import os

pay_bp = Blueprint("pay", __name__)

# # Razorpay credentials (store them in environment variables for security)
# RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "your_razorpay_key_id")
# RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "your_razorpay_key_secret")

razorpay_client = razorpay.Client(auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_KEY_SECRET")))


# razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

@pay_bp.route("/create_order", methods=["POST"])
def create_order():
    data = request.json
    amount = int(data.get("amount", 0)) * 100  # Convert to paise
    name = data.get("name")

    if amount <= 0 or not name:
        return jsonify({"error": "Invalid input"}), 400

    # Create an order with Razorpay
    order = razorpay_client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1  # Auto capture payment
    })

    return jsonify(order)
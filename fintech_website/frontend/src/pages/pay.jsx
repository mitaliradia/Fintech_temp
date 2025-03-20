import { useState, useEffect } from "react";

const PaymentPage = () => {
    const [name, setName] = useState("");
    const [amount, setAmount] = useState("");

    useEffect(() => {
        // Load Razorpay script
        const script = document.createElement("script");
        script.src = "https://checkout.razorpay.com/v1/checkout.js";
        script.async = true;
        document.body.appendChild(script);
    }, []);

    const handlePayment = async (e) => {
        e.preventDefault();

        if (!name || !amount || amount <= 0) {
            alert("Please enter valid details");
            return;
        }

        try {
            let response = await fetch("http://127.0.0.1:5000/pay/create_order", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, amount }),
            });

            let order = await response.json();
            if (order.error) {
                alert(order.error);
                return;
            }

            let options = {
                key: "rzp_test_p61jqL4C4mBo78",  // Replace with actual Razorpay Key ID
                amount: order.amount,
                currency: "INR",
                name: name,
                description: "Test Payment",
                order_id: order.id,
                handler: function (response) {
                    alert("Payment successful! Payment ID: " + response.razorpay_payment_id);
                },
                prefill: {
                    name: name
                }
            };

            let rzp = new window.Razorpay(options);
            rzp.open();
        } catch (error) {
            console.error("Error:", error);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
            <div className="p-6 bg-white shadow-md rounded-xl">
                <h2 className="text-2xl font-semibold mb-4">Make a Payment</h2>
                <form onSubmit={handlePayment} className="flex flex-col gap-4">
                    <input
                        type="text"
                        placeholder="Enter Name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        className="border p-2 rounded-lg"
                        required
                    />
                    <input
                        type="number"
                        placeholder="Enter Amount"
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                        className="border p-2 rounded-lg"
                        required
                    />
                    <button
                        type="submit"
                        className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
                    >
                        Pay Now
                    </button>
                </form>
            </div>
        </div>
    );
};

export default PaymentPage;
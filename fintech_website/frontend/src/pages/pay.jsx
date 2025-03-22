import { useState, useEffect } from "react";

const PaymentPage = () => {
  const [name, setName] = useState("");
  const [amount, setAmount] = useState("");
  const [isScriptLoaded, setIsScriptLoaded] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Check if Razorpay is already loaded
    if (window.Razorpay) {
      console.log("Razorpay already loaded");
      setIsScriptLoaded(true);
      return;
    }

    console.log("Loading Razorpay script...");
    // Load Razorpay script
    const script = document.createElement("script");
    script.src = "https://checkout.razorpay.com/v1/checkout.js";
    script.async = true;
    
    script.onload = () => {
      console.log("✅ Razorpay script loaded successfully");
      setIsScriptLoaded(true);
    };
    
    script.onerror = () => {
      console.error("❌ Failed to load Razorpay script");
      alert("Failed to load payment gateway. Please refresh and try again.");
    };
    
    document.body.appendChild(script);

    return () => {
      // Cleanup
      if (document.body.contains(script)) {
        document.body.removeChild(script);
      }
    };
  }, []);

  const handlePayment = async (e) => {
    e.preventDefault();
    console.log("Payment button clicked");
    
    if (!isScriptLoaded) {
      console.error("Razorpay script not loaded yet");
      alert("Payment system is still loading. Please wait a moment and try again.");
      return;
    }

    if (!name || !amount || amount <= 0) {
      console.error("Invalid input:", { name, amount });
      alert("Please enter valid details");
      return;
    }

    setIsLoading(true);
    console.log(`Attempting payment for ${name}, amount: ${amount}`);

    try {
      // Check if Razorpay is available
      if (typeof window.Razorpay !== 'function') {
        throw new Error("Razorpay is not available");
      }

      console.log("Sending request to create order...");
      const apiUrl = "http://127.0.0.1:5000/pay/create_order";
      console.log(`API URL: ${apiUrl}`);
      
      let response = await fetch(apiUrl, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          // Add this to help with CORS
          "Accept": "application/json" 
        },
        body: JSON.stringify({ name, amount }),
      });

      console.log(`Response status: ${response.status}`);
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`API error (${response.status}): ${errorText}`);
      }

      let order = await response.json();
      console.log("Order created successfully:", order);

      if (order.error) {
        alert(`Error: ${order.error}`);
        return;
      }

      let options = {
        key: "rzp_test_SSVqgvkApR03lb", // Make sure this matches your backend
        amount: order.amount,
        currency: "INR",
        name: "Your Company Name",
        description: "Payment for " + name,
        order_id: order.id,
        handler: function (response) {
          console.log("Payment successful:", response);
          alert("Payment successful! Payment ID: " + response.razorpay_payment_id);
        },
        prefill: {
          name: name
        },
        theme: {
          color: "#3399cc"
        },
        modal: {
          ondismiss: function() {
            console.log("Payment modal dismissed");
          }
        }
      };

      console.log("Opening Razorpay with options:", options);
      
      let rzp = new window.Razorpay(options);
      rzp.on('payment.failed', function(response) {
        console.error("Payment failed:", response.error);
        alert(`Payment failed: ${response.error.description}`);
      });
      
      rzp.open();
      console.log("Razorpay modal opened");
      
    } catch (error) {
      console.error("Error during payment process:", error);
      alert(`Payment process error: ${error.message}`);
    } finally {
      setIsLoading(false);
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
            min="1"
          />
          <button
            type="submit"
            className={`${
              isLoading ? "bg-gray-400" : "bg-blue-500 hover:bg-blue-600"
            } text-white px-4 py-2 rounded-lg`}
            disabled={isLoading}
          >
            {isLoading ? "Processing..." : "Pay Now"}
          </button>
          {!isScriptLoaded && (
            <p className="text-sm text-amber-600">Loading payment system...</p>
          )}
        </form>
      </div>
    </div>
  );
};

export default PaymentPage;
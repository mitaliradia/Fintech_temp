import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Activity() {
  const { isAuthenticated, user } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Mock data for testing
  const [activeRides, setActiveRides] = useState([
    {
      id: 1,
      station: "Central Station",
      startTime: new Date(),
      duration: 2,
      status: "In Progress",
    },
  ]);

  const [pastRides, setPastRides] = useState([
    {
      id: 1,
      station: "North Station",
      date: new Date("2024-03-20"),
      duration: 1,
      cost: 200,
    },
  ]);

  const [transactions, setTransactions] = useState([
    {
      id: "TXN001",
      amount: 200,
      date: new Date("2024-03-20"),
      status: "Completed",
    },
  ]);

  useEffect(() => {
    const loadActivityData = async () => {
      try {
        if (!isAuthenticated) {
          navigate("/login");
          return;
        }

        setLoading(true);
        // Simulate API calls with setTimeout
        setTimeout(() => {
          console.log("Loading activity data for user:", user);
          // Your existing mock data is already set in state
          setLoading(false);
        }, 1000);
      } catch (err) {
        console.error("Error loading activity data:", err);
        setError("Failed to load activity data");
        setLoading(false);
      }
    };

    loadActivityData();
  }, [isAuthenticated, navigate, user]);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="activity-container">
      <h1>My Activity</h1>

      <section className="active-rides">
        <h2>Active Rides</h2>
        <div className="rides-grid">
          {activeRides.length === 0 ? (
            <p>No active rides</p>
          ) : (
            activeRides.map((ride) => (
              <div key={ride.id} className="ride-card">
                <h3>Station: {ride.station}</h3>
                <p>Started: {new Date(ride.startTime).toLocaleString()}</p>
                <p>Duration: {ride.duration} hours</p>
                <p>Status: {ride.status}</p>
              </div>
            ))
          )}
        </div>
      </section>

      <section className="past-rides">
        <h2>Past Rides</h2>
        <div className="rides-grid">
          {pastRides.map((ride) => (
            <div key={ride.id} className="ride-card">
              <h3>Station: {ride.station}</h3>
              <p>Date: {new Date(ride.date).toLocaleDateString()}</p>
              <p>Duration: {ride.duration} hours</p>
              <p>Cost: ₹{ride.cost}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="transactions">
        <h2>Transaction History</h2>
        <div className="transaction-list">
          {transactions.map((transaction) => (
            <div key={transaction.id} className="transaction-item">
              <p>ID: {transaction.id}</p>
              <p>Amount: ₹{transaction.amount}</p>
              <p>Date: {new Date(transaction.date).toLocaleString()}</p>
              <p>Status: {transaction.status}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

"use client"

import { useState, useEffect } from "react"
import "../index.css"

const Activity = () => {
  const [activeTab, setActiveTab] = useState("active")
  const [isLoading, setIsLoading] = useState(true)

  // Mock data for active ride
  const activeRide = {
    bikeId: "BK-2023-789",
    bikeName: "Urban Cruiser",
    startTime: new Date(Date.now() - 45 * 60 * 1000), // 45 minutes ago
    startLocation: "Downtown Station",
    currentLocation: "Central Park",
    estimatedCost: 14.25,
  }

  // Mock data for past rides
  const pastRides = [
    {
      id: "RD-2023-001",
      bikeId: "BK-2023-456",
      bikeName: "City Explorer",
      startTime: new Date(2023, 6, 15, 10, 30),
      endTime: new Date(2023, 6, 15, 11, 45),
      startLocation: "Riverside Park",
      endLocation: "University Campus",
      distance: 5.7,
      cost: 18.75,
      status: "Completed",
    },
    {
      id: "RD-2023-002",
      bikeId: "BK-2023-123",
      bikeName: "Trail Blazer",
      startTime: new Date(2023, 6, 12, 14, 15),
      endTime: new Date(2023, 6, 12, 16, 30),
      startLocation: "Beach Boulevard",
      endLocation: "Downtown Station",
      distance: 8.3,
      cost: 27.5,
      status: "Completed",
    },
    {
      id: "RD-2023-003",
      bikeId: "BK-2023-789",
      bikeName: "Urban Cruiser",
      startTime: new Date(2023, 6, 10, 9, 0),
      endTime: new Date(2023, 6, 10, 9, 45),
      startLocation: "Central Square",
      endLocation: "Riverside Park",
      distance: 3.2,
      cost: 12.0,
      status: "Completed",
    },
    {
      id: "RD-2023-004",
      bikeId: "BK-2023-234",
      bikeName: "City Hopper",
      startTime: new Date(2023, 6, 5, 18, 30),
      endTime: new Date(2023, 6, 5, 19, 15),
      startLocation: "University Campus",
      endLocation: "Central Square",
      distance: 4.1,
      cost: 15.5,
      status: "Completed",
    },
  ]

  // Mock data for transactions
  const transactions = [
    {
      id: "TXN-2023-001",
      date: new Date(2023, 6, 15, 11, 45),
      amount: 18.75,
      type: "Ride Payment",
      status: "Successful",
      method: "Credit Card (**** 4582)",
    },
    {
      id: "TXN-2023-002",
      date: new Date(2023, 6, 12, 16, 30),
      amount: 27.5,
      type: "Ride Payment",
      status: "Successful",
      method: "PayPal",
    },
    {
      id: "TXN-2023-003",
      date: new Date(2023, 6, 10, 9, 45),
      amount: 12.0,
      type: "Ride Payment",
      status: "Successful",
      method: "Credit Card (**** 4582)",
    },
    {
      id: "TXN-2023-004",
      date: new Date(2023, 6, 5, 19, 15),
      amount: 15.5,
      type: "Ride Payment",
      status: "Successful",
      method: "Wallet",
    },
    {
      id: "TXN-2023-005",
      date: new Date(2023, 6, 1, 12, 0),
      amount: 50.0,
      type: "Wallet Recharge",
      status: "Successful",
      method: "Credit Card (**** 4582)",
    },
  ]

  // Calculate ride duration in minutes
  const calculateDuration = (start, end) => {
    const diff = end - start
    return Math.round(diff / (1000 * 60))
  }

  // Format date to readable string
  const formatDate = (date) => {
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })
  }

  // Calculate active ride duration and update it every minute
  const [activeDuration, setActiveDuration] = useState(0)

  useEffect(() => {
    // Simulate loading
    const loadingTimer = setTimeout(() => {
      setIsLoading(false)
    }, 1500)

    // Update active ride duration every minute
    const durationTimer = setInterval(() => {
      const duration = calculateDuration(activeRide.startTime, new Date())
      setActiveDuration(duration)
    }, 60000)

    // Initial calculation
    setActiveDuration(calculateDuration(activeRide.startTime, new Date()))

    return () => {
      clearTimeout(loadingTimer)
      clearInterval(durationTimer)
    }
  }, [])

  // Handle tab switching
  const switchTab = (tab) => {
    setActiveTab(tab)
  }

  if (isLoading) {
    return (
      <div className="activity-loading">
        <div className="spinner"></div>
        <p>Loading your activity...</p>
      </div>
    )
  }

  return (
    <div className="activity-container">
      <h1 className="activity-title">My Activity</h1>

      <div className="activity-tabs">
        <button className={`tab-button ${activeTab === "active" ? "active" : ""}`} onClick={() => switchTab("active")}>
          Active Ride
        </button>
        <button className={`tab-button ${activeTab === "past" ? "active" : ""}`} onClick={() => switchTab("past")}>
          Past Rides
        </button>
        <button
          className={`tab-button ${activeTab === "transactions" ? "active" : ""}`}
          onClick={() => switchTab("transactions")}
        >
          Transaction History
        </button>
      </div>

      <div className="activity-content">
        {/* Active Ride Section */}
        <section className={`active-ride-section ${activeTab === "active" ? "visible" : "hidden"}`}>
          {activeRide ? (
            <div className="active-ride-card">
              <div className="ride-status">
                <span className="status-indicator"></span>
                <span className="status-text">In Progress</span>
              </div>

              <div className="ride-map">
                <img src="/placeholder.svg?height=200&width=400" alt="Ride Map" className="map-image" />
              </div>

              <div className="ride-details">
                <div className="detail-column">
                  <div className="detail-item">
                    <h3>Bike</h3>
                    <p>
                      {activeRide.bikeName} ({activeRide.bikeId})
                    </p>
                  </div>
                  <div className="detail-item">
                    <h3>Start Location</h3>
                    <p>{activeRide.startLocation}</p>
                  </div>
                  <div className="detail-item">
                    <h3>Current Location</h3>
                    <p>{activeRide.currentLocation}</p>
                  </div>
                </div>

                <div className="detail-column">
                  <div className="detail-item">
                    <h3>Start Time</h3>
                    <p>{formatDate(activeRide.startTime)}</p>
                  </div>
                  <div className="detail-item">
                    <h3>Duration</h3>
                    <p className="duration-counter">{activeDuration} minutes</p>
                  </div>
                  <div className="detail-item">
                    <h3>Estimated Cost</h3>
                    <p className="cost-counter">${activeRide.estimatedCost.toFixed(2)}</p>
                  </div>
                </div>
              </div>

              <button className="end-ride-btn">End Ride</button>
            </div>
          ) : (
            <div className="no-active-ride">
              <img src="/placeholder.svg?height=150&width=150" alt="No Active Ride" />
              <h2>No Active Rides</h2>
              <p>You don't have any active rides at the moment.</p>
              <button className="start-ride-btn">Start a New Ride</button>
            </div>
          )}
        </section>

        {/* Past Rides Section */}
        <section className={`past-rides-section ${activeTab === "past" ? "visible" : "hidden"}`}>
          <h2>Your Ride History</h2>

          <div className="past-rides-list">
            {pastRides.map((ride, index) => (
              <div className="past-ride-card" key={ride.id} style={{ animationDelay: `${index * 0.1}s` }}>
                <div className="ride-header">
                  <h3>{ride.bikeName}</h3>
                  <span className="ride-id">{ride.id}</span>
                </div>

                <div className="ride-info">
                  <div className="info-column">
                    <div className="info-item">
                      <span className="info-label">Date:</span>
                      <span className="info-value">{formatDate(ride.startTime).split(",")[0]}</span>
                    </div>
                    <div className="info-item">
                      <span className="info-label">Time:</span>
                      <span className="info-value">
                        {formatDate(ride.startTime).split(",")[1]} -{" "}
                        {ride.endTime.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" })}
                      </span>
                    </div>
                    <div className="info-item">
                      <span className="info-label">Duration:</span>
                      <span className="info-value">{calculateDuration(ride.startTime, ride.endTime)} minutes</span>
                    </div>
                  </div>

                  <div className="info-column">
                    <div className="info-item">
                      <span className="info-label">From:</span>
                      <span className="info-value">{ride.startLocation}</span>
                    </div>
                    <div className="info-item">
                      <span className="info-label">To:</span>
                      <span className="info-value">{ride.endLocation}</span>
                    </div>
                    <div className="info-item">
                      <span className="info-label">Distance:</span>
                      <span className="info-value">{ride.distance} km</span>
                    </div>
                  </div>

                  <div className="info-column">
                    <div className="info-item payment-info">
                      <span className="info-label">Payment:</span>
                      <span className="info-value">${ride.cost.toFixed(2)}</span>
                    </div>
                    <div className="info-item">
                      <span className="info-label">Status:</span>
                      <span className="info-value status-completed">{ride.status}</span>
                    </div>
                  </div>
                </div>

                <button className="view-details-btn">View Details</button>
              </div>
            ))}
          </div>
        </section>

        {/* Transaction History Section */}
        <section className={`transaction-section ${activeTab === "transactions" ? "visible" : "hidden"}`}>
          <h2>Transaction History</h2>

          <div className="transaction-filters">
            <select className="filter-select">
              <option value="all">All Transactions</option>
              <option value="ride">Ride Payments</option>
              <option value="recharge">Wallet Recharges</option>
            </select>

            <div className="date-filter">
              <input type="date" className="date-input" placeholder="From" />
              <span>to</span>
              <input type="date" className="date-input" placeholder="To" />
              <button className="filter-btn">Apply</button>
            </div>
          </div>

          <div className="transaction-table-container">
            <table className="transaction-table">
              <thead>
                <tr>
                  <th>Transaction ID</th>
                  <th>Date & Time</th>
                  <th>Type</th>
                  <th>Amount</th>
                  <th>Payment Method</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {transactions.map((transaction, index) => (
                  <tr key={transaction.id} className="transaction-row" style={{ animationDelay: `${index * 0.1}s` }}>
                    <td className="transaction-id">{transaction.id}</td>
                    <td>{formatDate(transaction.date)}</td>
                    <td>{transaction.type}</td>
                    <td className={transaction.type === "Wallet Recharge" ? "amount-positive" : "amount-negative"}>
                      {transaction.type === "Wallet Recharge" ? "+" : "-"}${transaction.amount.toFixed(2)}
                    </td>
                    <td>{transaction.method}</td>
                    <td className={`status-${transaction.status.toLowerCase()}`}>{transaction.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="pagination">
            <button className="pagination-btn active">1</button>
            <button className="pagination-btn">2</button>
            <button className="pagination-btn">3</button>
            <button className="pagination-btn">Next</button>
          </div>
        </section>
      </div>
    </div>
  )
}

export default Activity


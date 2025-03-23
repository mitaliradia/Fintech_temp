"use client"

import { useState, useEffect } from "react"
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import "../index.css"
import { stationAPI } from "../services/api";

const Master_Dashboard = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const [stationData, setStationData] = useState({
    stationName: "Downtown Station",
    stationId: "ST-001",
    location: "123 Main Street, Downtown",
    stationMaster: "John Smith",
    totalEVs: 12,
    availableEVs: 5,
    bookedEVs: 6,
    maintenanceEVs: 1,
  });
  
  const [activeTab, setActiveTab] = useState("overview")
  const [showNotification, setShowNotification] = useState(false)
  const [selectedEV, setSelectedEV] = useState(null)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  // Station master data - with useState
  // Near the top of your component, add this state:
  useEffect(() => {
    async function fetchData() {
      try {
        // Get station data
        const stationResponse = await stationAPI.getStations();
        if (!stationResponse.data?.success || !stationResponse.data?.stations?.length) {
          return;
        }
        
        const station = stationResponse.data.stations[0];
        
        // Format and update basic station info
        const addressParts = [];
        if (station.address?.street) addressParts.push(station.address.street);
        if (station.address?.city) addressParts.push(station.address.city);
        if (station.address?.state) addressParts.push(station.address.state);
        const locationString = addressParts.length > 0 ? addressParts.join(', ') : 'No address provided';
        
        // Update station data
        setStationData(prev => ({
          ...prev,
          stationName: station.name || prev.stationName,
          stationId: station.id || prev.stationId,
          location: locationString,
          totalEVs: station.capacity || prev.totalEVs,
          availableEVs: station.available_spots || prev.availableEVs,
          bookedEVs: 0,  // Or fetch from a bookings API
          maintenanceEVs: 0  // Or fetch from a maintenance API
        }));
        
        // Try to fetch recent bookings if you have an endpoint
        try {
          // This is a placeholder - replace with your actual API call
          const bookingsResponse = await stationAPI.getRecentBookings(station.id);
          if (bookingsResponse.data?.success && bookingsResponse.data?.bookings) {
            setBookedEVs(bookingsResponse.data.bookings);
          }
        } catch (bookingErr) {
          console.error("Error fetching bookings:", bookingErr);
          // Keep the default bookedEVs data
        }
        
        // For battery status, you would need vehicle data with battery levels
        // This might be available from the same bookings API or a separate vehicles API

        let totalEVs = 0;
      let availableEVs = 0;
      let bookedEVs = 0;
      let maintenanceEVs = 0;
      
      if (vehicleResponse.data?.success && vehicleResponse.data?.vehicles) {
        const vehicles = vehicleResponse.data.vehicles;
        totalEVs = vehicles.length;
        
        // Count vehicles by status
        vehicles.forEach(vehicle => {
          if (vehicle.status === 'AVAILABLE') availableEVs++;
          else if (vehicle.status === 'RENTED') bookedEVs++;
          else if (vehicle.status === 'MAINTENANCE') maintenanceEVs++;
        });
      } else {
        // If vehicle data isn't available, use station capacity data
        totalEVs = station.capacity || 12;
        availableEVs = station.available_spots || totalEVs;
        bookedEVs = 0;
        maintenanceEVs = 0;
      }
      
      // Update the state with all new data
      setStationData({
        stationName: station.name || "Station",
        stationId: station.id || "ST-000",
        location: locationString,
        totalEVs,
        availableEVs,
        bookedEVs,
        maintenanceEVs
      });

        
      } catch (err) {
        console.error("Error fetching data", err);
      }
    }
    
    fetchData();
  }, []);

  // Available EVs data
  const availableEVs = [
    { id: "EV-001", name: "Urban Cruiser", batteryLevel: 92, status: "available", lastMaintenance: "2023-03-15" },
    { id: "EV-002", name: "City Explorer", batteryLevel: 78, status: "available", lastMaintenance: "2023-03-10" },
    { id: "EV-003", name: "Metro Glider", batteryLevel: 85, status: "available", lastMaintenance: "2023-03-12" },
    { id: "EV-004", name: "Trail Blazer", batteryLevel: 65, status: "available", lastMaintenance: "2023-03-05" },
    { id: "EV-005", name: "Nature Rider", batteryLevel: 88, status: "available", lastMaintenance: "2023-03-08" },
  ]

  // Booked EVs data with user details
  const bookedEVs = [
    {
      id: "EV-006",
      name: "Urban Commuter",
      userId: "USR-101",
      userName: "Alice Johnson",
      userPhone: "+1-555-123-4567",
      kycStatus: "Verified",
      startTime: "2023-03-22 09:30 AM",
      duration: "3 hours",
      cost: "$36.00",
      batteryLevel: 72,
    },
    {
      id: "EV-007",
      name: "City Hopper",
      userId: "USR-102",
      userName: "Bob Williams",
      userPhone: "+1-555-234-5678",
      kycStatus: "Verified",
      startTime: "2023-03-22 10:15 AM",
      duration: "2 hours",
      cost: "$26.00",
      batteryLevel: 81,
    },
    {
      id: "EV-008",
      name: "Campus Cruiser",
      userId: "USR-103",
      userName: "Carol Davis",
      userPhone: "+1-555-345-6789",
      kycStatus: "Pending",
      startTime: "2023-03-22 11:00 AM",
      duration: "4 hours",
      cost: "$36.00",
      batteryLevel: 65,
    },
    {
      id: "EV-009",
      name: "Student Speeder",
      userId: "USR-104",
      userName: "David Miller",
      userPhone: "+1-555-456-7890",
      kycStatus: "Verified",
      startTime: "2023-03-22 12:30 PM",
      duration: "1 hour",
      cost: "$9.00",
      batteryLevel: 90,
    },
    {
      id: "EV-010",
      name: "Coastal Glider",
      userId: "USR-105",
      userName: "Emma Wilson",
      userPhone: "+1-555-567-8901",
      kycStatus: "Verified",
      startTime: "2023-03-22 01:45 PM",
      duration: "5 hours",
      cost: "$80.00",
      batteryLevel: 75,
    },
    {
      id: "EV-011",
      name: "Beach Rover",
      userId: "USR-106",
      userName: "Frank Thomas",
      userPhone: "+1-555-678-9012",
      kycStatus: "Verified",
      startTime: "2023-03-22 02:30 PM",
      duration: "2 hours",
      cost: "$34.00",
      batteryLevel: 88,
    },
  ]

  // Maintenance EVs
  const maintenanceEVs = [
    {
      id: "EV-012",
      name: "Mountain Explorer",
      issue: "Battery replacement needed",
      since: "2023-03-20",
      estimatedCompletion: "2023-03-24",
    },
  ]

  // Recent notifications
  const notifications = [
    { id: 1, type: "booking", message: "New booking: EV-010 by Emma Wilson", time: "10 minutes ago" },
    { id: 2, type: "return", message: "EV-003 returned by Michael Brown", time: "25 minutes ago" },
    { id: 3, type: "maintenance", message: "EV-012 scheduled for maintenance", time: "1 hour ago" },
    { id: 4, type: "alert", message: "Low battery alert: EV-004 at 25%", time: "2 hours ago" },
    { id: 5, type: "feedback", message: "New feedback received from Alice Johnson", time: "3 hours ago" },
  ]

  // Recent user feedback
  const userFeedback = [
    {
      id: 1,
      userId: "USR-101",
      userName: "Alice Johnson",
      rating: 4.5,
      comment: "Great service, bike was in excellent condition!",
      date: "2023-03-21",
    },
    {
      id: 2,
      userId: "USR-107",
      userName: "George Brown",
      rating: 3.0,
      comment: "Battery was lower than indicated on the app.",
      date: "2023-03-20",
    },
    {
      id: 3,
      userId: "USR-108",
      userName: "Hannah Garcia",
      rating: 5.0,
      comment: "Perfect experience! Will definitely use again.",
      date: "2023-03-19",
    },
  ]

  useEffect(() => {
    // Animation for dashboard elements
    const dashboardElements = document.querySelectorAll(".animate-in")

    dashboardElements.forEach((element, index) => {
      setTimeout(() => {
        element.classList.add("visible")
      }, 100 * index)
    })

    // Show notification after 3 seconds
    const timer = setTimeout(() => {
      setShowNotification(true)

      // Hide notification after 5 seconds
      const hideTimer = setTimeout(() => {
        setShowNotification(false)
      }, 7000)

      return () => clearTimeout(hideTimer)
    }, 9000)

    return () => clearTimeout(timer)
  }, [])

  const handleContactUser = (ev) => {
    setSelectedEV(ev)
    setIsModalOpen(true)
  }

  const closeModal = () => {
    setIsModalOpen(false)
    setSelectedEV(null)
  }

  const getBatteryStatusClass = (level) => {
    if (level >= 70) return "battery-high"
    if (level >= 40) return "battery-medium"
    return "battery-low"
  }

  // Loading state with styled container
  // if (loading) {
  //   return (
  //     <div className="loading-container" style={{ 
  //       display: 'flex', 
  //       flexDirection: 'column', 
  //       alignItems: 'center', 
  //       justifyContent: 'center', 
  //       height: '100vh',
  //       padding: '20px'
  //     }}>
  //       <div className="loading-spinner" style={{
  //         border: '4px solid #f3f3f3',
  //         borderTop: '4px solid #3498db',
  //         borderRadius: '50%',
  //         width: '50px',
  //         height: '50px',
  //         animation: 'spin 2s linear infinite'
  //       }}></div>
  //       <p style={{ marginTop: '20px' }}>Loading station data...</p>
  //       <style>{`
  //         @keyframes spin {
  //           0% { transform: rotate(0deg); }
  //           100% { transform: rotate(360deg); }
  //         }
  //       `}</style>
  //     </div>
  //   );
  // }

  return (
    <div className="station-master-dashboard">
      {/* Error notification if we have an error but are using default data */}
      {error && (
        <div style={{ 
          backgroundColor: '#ffecb3', 
          color: '#664d03', 
          padding: '10px 20px', 
          borderRadius: '4px', 
          margin: '10px 0',
          border: '1px solid #ffc107'
        }}>
          <p><strong>Note:</strong> {error}</p>
        </div>
      )}

      {/* Header */}
      <header className="dashboard-header animate-in">
        <div className="header-left">
          <h1>Station Master Dashboard</h1>
          <div className="station-info">
            <h2>{stationData.stationName}</h2>
            <p>
              Station ID: {stationData.stationId} | Location: {stationData.location}
            </p>
          </div>
        </div>
        <div className="header-right">
          <div className="station-master-profile">
            <div className="profile-avatar">{stationData.stationMaster.charAt(0)}</div>
            <div className="profile-info">
              <p className="profile-name">{stationData.stationMaster}</p>
              <p className="profile-role">Station Master</p>
            </div>
          </div>
          <div className="notification-icon" onClick={() => setShowNotification(!showNotification)}>
            <span className="notification-badge">{notifications.length}</span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
            </svg>
          </div>
          {/* <button 
            className="logout-button" 
            onClick={handleLogout}
            style={{
              backgroundColor: '#f44336',
              color: 'white',
              border: 'none',
              padding: '8px 16px',
              borderRadius: '4px',
              cursor: 'pointer',
              marginLeft: '10px'
            }}
          >
            Logout
          </button> */}
        </div>
      </header>

      {/* Notification panel */}
      {showNotification && (
        <div className="notification-panel animate-in">
          <div className="notification-header">
            <h3>Recent Notifications</h3>
            <button onClick={() => setShowNotification(false)}>Close</button>
          </div>
          <div className="notification-list">
            {notifications.map((notification) => (
              <div key={notification.id} className={`notification-item ${notification.type}`}>
                <p>{notification.message}</p>
                <span className="notification-time">{notification.time}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Dashboard stats */}
      <div className="dashboard-stats animate-in">
        <div className="stat-card">
          <h3>Total EVs</h3>
          <p className="stat-value">{stationData.totalEVs}</p>
        </div>
        <div className="stat-card">
          <h3>Available</h3>
          <p className="stat-value available">{stationData.availableEVs}</p>
        </div>
        <div className="stat-card">
          <h3>Booked</h3>
          <p className="stat-value booked">{stationData.bookedEVs}</p>
        </div>
        <div className="stat-card">
          <h3>Maintenance</h3>
          <p className="stat-value maintenance">{stationData.maintenanceEVs}</p>
        </div>
      </div>

      {/* Dashboard tabs */}
      <div className="dashboard-tabs animate-in">
        <button
          className={`tab-button ${activeTab === "overview" ? "active" : ""}`}
          onClick={() => setActiveTab("overview")}
        >
          Overview
        </button>
        <button
          className={`tab-button ${activeTab === "available" ? "active" : ""}`}
          onClick={() => setActiveTab("available")}
        >
          Available EVs
        </button>
        <button
          className={`tab-button ${activeTab === "booked" ? "active" : ""}`}
          onClick={() => setActiveTab("booked")}
        >
          Booked EVs
        </button>
        <button
          className={`tab-button ${activeTab === "maintenance" ? "active" : ""}`}
          onClick={() => setActiveTab("maintenance")}
        >
          Maintenance
        </button>
        <button
          className={`tab-button ${activeTab === "feedback" ? "active" : ""}`}
          onClick={() => setActiveTab("feedback")}
        >
          User Feedback
        </button>
      </div>

      {/* Dashboard content */}
      <div className="dashboard-content animate-in">
        {/* Overview Tab */}
        {activeTab === "overview" && (
          <div className="overview-tab">
            <div className="overview-section">
              <h3>Station Status</h3>
              <div className="status-chart">
                <div className="chart-bar">
                  <div
                    className="bar-segment available"
                    style={{ width: `${(stationData.availableEVs / stationData.totalEVs) * 100}%` }}
                  >
                    <span className="segment-label">{stationData.availableEVs} Available</span>
                  </div>
                  <div
                    className="bar-segment booked"
                    style={{ width: `${(stationData.bookedEVs / stationData.totalEVs) * 100}%` }}
                  >
                    <span className="segment-label">{stationData.bookedEVs} Booked</span>
                  </div>
                  <div
                    className="bar-segment maintenance"
                    style={{ width: `${(stationData.maintenanceEVs / stationData.totalEVs) * 100}%` }}
                  >
                    <span className="segment-label">{stationData.maintenanceEVs} Maintenance</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="overview-grid">
              <div className="overview-section">
                <h3>Recent Bookings</h3>
                <div className="recent-bookings">
                  {bookedEVs.slice(0, 3).map((ev) => (
                    <div key={ev.id} className="booking-item">
                      <div className="booking-info">
                        <h4>
                          {ev.name} ({ev.id})
                        </h4>
                        <p>Booked by: {ev.userName}</p>
                        <p>Start: {ev.startTime}</p>
                        <p>Duration: {ev.duration}</p>
                      </div>
                      <div className="booking-status">
                        <span className="booking-cost">{ev.cost}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="overview-section">
                <h3>Battery Status</h3>
                <div className="battery-status">
                  {[...availableEVs, ...bookedEVs].slice(0, 5).map((ev) => (
                    <div key={ev.id} className="battery-item">
                      <div className="battery-info">
                        <h4>{ev.name}</h4>
                        <p>{ev.id}</p>
                      </div>
                      <div className="battery-level">
                        <div className={`battery-bar ${getBatteryStatusClass(ev.batteryLevel)}`}>
                          <div className="battery-fill" style={{ width: `${ev.batteryLevel}%` }}></div>
                        </div>
                        <span className="battery-percentage">{ev.batteryLevel}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Available EVs Tab */}
        {activeTab === "available" && (
          <div className="available-tab">
            <h3>Available EVs at {stationData.stationName}</h3>
            <div className="ev-table">
              <table>
                <thead>
                  <tr>
                    <th>EV ID</th>
                    <th>Name</th>
                    <th>Battery</th>
                    <th>Status</th>
                    <th>Last Maintenance</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {availableEVs.map((ev) => (
                    <tr key={ev.id}>
                      <td>{ev.id}</td>
                      <td>{ev.name}</td>
                      <td>
                        <div className="battery-indicator">
                          <div
                            className={`battery-level ${getBatteryStatusClass(ev.batteryLevel)}`}
                            style={{ width: `${ev.batteryLevel}%` }}
                          ></div>
                          <span>{ev.batteryLevel}%</span>
                        </div>
                      </td>
                      <td>
                        <span className="status-badge available">Available</span>
                      </td>
                      <td>{ev.lastMaintenance}</td>
                      <td>
                        <button className="action-button">Set to Maintenance</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Booked EVs Tab */}
        {activeTab === "booked" && (
          <div className="booked-tab">
            <h3>Currently Booked EVs</h3>
            <div className="ev-table">
              <table>
                <thead>
                  <tr>
                    <th>EV ID</th>
                    <th>EV Name</th>
                    <th>User</th>
                    <th>KYC Status</th>
                    <th>Start Time</th>
                    <th>Duration</th>
                    <th>Cost</th>
                    <th>Battery</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {bookedEVs.map((ev) => (
                    <tr key={ev.id}>
                      <td>{ev.id}</td>
                      <td>{ev.name}</td>
                      <td>
                        <div className="user-info">
                          <span className="user-name">{ev.userName}</span>
                          <span className="user-id">{ev.userId}</span>
                        </div>
                      </td>
                      <td>
                        <span className={`kyc-badge ${ev.kycStatus.toLowerCase()}`}>{ev.kycStatus}</span>
                      </td>
                      <td>{ev.startTime}</td>
                      <td>{ev.duration}</td>
                      <td>{ev.cost}</td>
                      <td>
                        <div className="battery-indicator">
                          <div
                            className={`battery-level ${getBatteryStatusClass(ev.batteryLevel)}`}
                            style={{ width: `${ev.batteryLevel}%` }}
                          ></div>
                          <span>{ev.batteryLevel}%</span>
                        </div>
                      </td>
                      <td>
                        <button className="action-button contact" onClick={() => handleContactUser(ev)}>
                          Contact User
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Maintenance Tab */}
        {activeTab === "maintenance" && (
          <div className="maintenance-tab">
            <h3>EVs Under Maintenance</h3>
            <div className="ev-table">
              <table>
                <thead>
                  <tr>
                    <th>EV ID</th>
                    <th>Name</th>
                    <th>Issue</th>
                    <th>Since</th>
                    <th>Estimated Completion</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {maintenanceEVs.map((ev) => (
                    <tr key={ev.id}>
                      <td>{ev.id}</td>
                      <td>{ev.name}</td>
                      <td>{ev.issue}</td>
                      <td>{ev.since}</td>
                      <td>{ev.estimatedCompletion}</td>
                      <td>
                        <button className="action-button">Mark as Available</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="maintenance-form">
              <h3>Schedule Maintenance</h3>
              <form>
                <div className="form-group">
                  <label>Select EV</label>
                  <select>
                    <option value="">-- Select an EV --</option>
                    {availableEVs.map((ev) => (
                      <option key={ev.id} value={ev.id}>
                        {ev.id} - {ev.name}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="form-group">
                  <label>Maintenance Issue</label>
                  <input type="text" placeholder="Describe the issue" />
                </div>
                <div className="form-group">
                  <label>Estimated Completion Date</label>
                  <input type="date" />
                </div>
                <button type="submit" className="submit-button">
                  Schedule Maintenance
                </button>
              </form>
            </div>
          </div>
        )}

        {/* User Feedback Tab */}
        {activeTab === "feedback" && (
          <div className="feedback-tab">
            <h3>Recent User Feedback</h3>
            <div className="feedback-list">
              {userFeedback.map((feedback) => (
                <div key={feedback.id} className="feedback-card">
                  <div className="feedback-header">
                    <div className="user-info">
                      <h4>{feedback.userName}</h4>
                      <span className="user-id">{feedback.userId}</span>
                    </div>
                    <div className="rating">
                      {[...Array(5)].map((_, i) => (
                        <span
                          key={i}
                          className={`star ${i < Math.floor(feedback.rating) ? "filled" : ""} ${i === Math.floor(feedback.rating) && feedback.rating % 1 !== 0 ? "half-filled" : ""}`}
                        >
                          ★
                        </span>
                      ))}
                      <span className="rating-value">{feedback.rating}</span>
                    </div>
                  </div>
                  <div className="feedback-body">
                    <p>{feedback.comment}</p>
                  </div>
                  <div className="feedback-footer">
                    <span className="feedback-date">{feedback.date}</span>
                    <button className="action-button">Respond</button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Contact User Modal */}
      {isModalOpen && selectedEV && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Contact User</h3>
              <button className="close-button" onClick={closeModal}>
                ×
              </button>
            </div>
            <div className="modal-body">
              <div className="user-contact-info">
                <h4>{selectedEV.userName}</h4>
                <p>User ID: {selectedEV.userId}</p>
                <p>Phone: {selectedEV.userPhone}</p>
                <p>
                  Currently using: {selectedEV.name} ({selectedEV.id})
                </p>
                <p>Rental started: {selectedEV.startTime}</p>
              </div>
              <div className="contact-options">
                <h4>Contact Options</h4>
                <div className="contact-buttons">
                  <button className="contact-button call">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                    </svg>
                    Call User
                  </button>
                  <button className="contact-button sms">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                    </svg>
                    Send SMS
                  </button>
                  <button className="contact-button emergency">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      >
                      <polygon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2"></polygon>
                      <line x1="12" y1="8" x2="12" y2="12"></line>
                      <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                    Emergency Alert
                  </button>
                </div>
              </div>
              <div className="message-form">
                <h4>Send Message</h4>
                <textarea placeholder="Type your message here..."></textarea>
                <button className="send-button">Send Message</button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Master_Dashboard
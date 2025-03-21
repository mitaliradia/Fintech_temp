import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../index.css";

const stations = [
  { id: 1, name: "Central Station", bikes: 5 },
  { id: 2, name: "North Station", bikes: 3 },
  { id: 3, name: "South Station", bikes: 7 },
];

export default function Home() {
  const [selectedStation, setSelectedStation] = useState("");
  const navigate = useNavigate();

  const handleBooking = () => {
    if (!selectedStation) {
      alert("Please select a station first");
      return;
    }
    navigate("/booking", { state: { stationId: selectedStation } });
  };

  return (
    <div className="home-container">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <h1>Electric Vehicle Rental Made Easy</h1>
          <p>
            Sustainable, convenient, and affordable transportation solutions
          </p>
          <button className="cta-button">Learn More</button>
        </div>
      </section>

      {/* Station Selection */}
      <section className="station-selector">
        <h2>Find Available EVs</h2>
        <div className="station-search">
          <select
            value={selectedStation}
            onChange={(e) => setSelectedStation(e.target.value)}
            className="station-dropdown"
          >
            <option value="">Select a Station</option>
            {stations.map((station) => (
              <option key={station.id} value={station.id}>
                {station.name} ({station.bikes} bikes available)
              </option>
            ))}
          </select>
          <button className="book-button" onClick={handleBooking}>
            Book a Ride
          </button>
        </div>
      </section>

      {/* Services Section */}
      <section className="services-section">
        <h2>Our Services</h2>
        <div className="services-grid">
          <div className="service-card">
            <i className="fas fa-bolt"></i>
            <h3>Electric Vehicles</h3>
            <p>100% electric fleet for eco-friendly rides</p>
          </div>
          <div className="service-card">
            <i className="fas fa-clock"></i>
            <h3>24/7 Availability</h3>
            <p>Rent anytime, anywhere</p>
          </div>
          <div className="service-card">
            <i className="fas fa-shield-alt"></i>
            <h3>Secure Payments</h3>
            <p>Safe and encrypted transactions</p>
          </div>
          <div className="service-card">
            <i className="fas fa-headset"></i>
            <h3>24/7 Support</h3>
            <p>Always here to help you</p>
          </div>
        </div>
      </section>
    </div>
  );
}

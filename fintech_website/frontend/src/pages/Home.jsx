import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../index.css";

const stations = [
  { id: 1, name: "Central Station", bikes: 5 },
  { id: 2, name: "North Station", bikes: 3 },
  { id: 3, name: "South Station", bikes: 7 },
];

const availableBikes = [
  { id: 1, name: "Bike A", rate: "₹50/hour", battery: "500W" },
  { id: 2, name: "Bike B", rate: "₹60/hour", battery: "600W" },
  { id: 3, name: "Bike C", rate: "₹70/hour", battery: "700W" },
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
          <h1 className="text-4xl font-bold mb-4">Electric Vehicle Rental Made Easy</h1>
          <p className="text-xl mb-6">Sustainable, convenient, and affordable transportation solutions</p>
          <button className="cta-button">Learn More</button>
        </div>
      </section>

      {/* Station Selection */}
      <section className="station-selector">
        <h2 className="text-2xl font-semibold mb-4">Find Available EVs</h2>
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
        {selectedStation && (
          <div className="available-bikes mt-6">
            <h3 className="text-xl font-semibold mb-4">Available Bikes</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {availableBikes.map((bike) => (
                <div key={bike.id} className="bike-card p-4 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow">
                  <h4 className="text-lg font-semibold">{bike.name}</h4>
                  <p>Rate: {bike.rate}</p>
                  <p>Battery: {bike.battery}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </section>

      {/* Why Choose Us */}
      <section className="why-choose-us py-12 bg-gray-100 text-center">
        <h2 className="text-3xl font-bold mb-6">Why Choose Us</h2>
        <ul className="list-none mb-6">
          <li className="mb-2">High-performance electric bikes</li>
          <li className="mb-2">Flexible rental plans</li>
          <li className="mb-2">Secure and easy payment options</li>
          <li className="mb-2">24/7 customer support</li>
        </ul>
        <button className="cta-button" onClick={() => navigate("/register")}>Start Now</button>
      </section>

      {/* Services Section */}
      <section className="services-section py-12">
        <h2 className="text-3xl font-bold text-center mb-6">Our Services</h2>
        <div className="services-grid grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="service-card p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <i className="fas fa-bolt text-4xl text-blue-500 mb-4"></i>
            <h3 className="text-xl font-semibold mb-2">Powerful Performance</h3>
            <p>Our bikes feature high-performance motors that provide smooth acceleration and effortless hill climbing.</p>
          </div>
          <div className="service-card p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <i className="fas fa-battery-full text-4xl text-blue-500 mb-4"></i>
            <h3 className="text-xl font-semibold mb-2">Extended Range</h3>
            <p>Long-lasting batteries that provide up to 60km of range on a single charge for worry-free adventures.</p>
          </div>
          <div className="service-card p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <i className="fas fa-shield-alt text-4xl text-blue-500 mb-4"></i>
            <h3 className="text-xl font-semibold mb-2">Enhanced Safety</h3>
            <p>Integrated safety features including automatic lights, reflective details, and responsive hydraulic brakes.</p>
          </div>
          <div className="service-card p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <i className="fas fa-map-marker-alt text-4xl text-blue-500 mb-4"></i>
            <h3 className="text-xl font-semibold mb-2">Real-time Tracking</h3>
            <p>GPS tracking and integration with our app allows you to always know the location of your bike.</p>
          </div>
          <div className="service-card p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <i className="fas fa-mobile-alt text-4xl text-blue-500 mb-4"></i>
            <h3 className="text-xl font-semibold mb-2">Smart App Control</h3>
            <p>Unlock, lock, and monitor your bike's status through our intuitive mobile application.</p>
          </div>
          <div className="service-card p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <i className="fas fa-calendar-alt text-4xl text-blue-500 mb-4"></i>
            <h3 className="text-xl font-semibold mb-2">Flexible Rentals</h3>
            <p>Choose from hourly, daily, or weekly rental plans to suit your needs with transparent pricing.</p>
          </div>
        </div>
      </section>

      {/* Process Section */}
      <section className="process-section py-12 bg-gray-100 text-center">
        <h2 className="text-3xl font-bold mb-6">Simple Process, Exceptional Experience</h2>
        <p className="text-lg mb-6">Renting an electric bike has never been easier. Follow these simple steps to start your eco-friendly journey today.</p>
        <div className="process-steps grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="process-step p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <h3 className="text-2xl font-bold mb-2">01</h3>
            <p>Sign Up</p>
            <p>Create an account in our app or website to access our fleet of premium electric bikes.</p>
          </div>
          <div className="process-step p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <h3 className="text-2xl font-bold mb-2">02</h3>
            <p>Choose a Bike</p>
            <p>Browse our fleet and select the bike that fits your needs and preferences.</p>
          </div>
          <div className="process-step p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <h3 className="text-2xl font-bold mb-2">03</h3>
            <p>Reserve & Unlock</p>
            <p>Book your bike and unlock it using our mobile app with just a few taps.</p>
          </div>
          <div className="process-step p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <h3 className="text-2xl font-bold mb-2">04</h3>
            <p>Ride & Return</p>
            <p>Enjoy your ride and return the bike to any of our designated stations when finished.</p>
          </div>
        </div>
      </section>
    </div>
  );
}

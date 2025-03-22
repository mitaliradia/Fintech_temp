"use client";

import { useState, useEffect } from "react";
import "../index.css";
import bike1 from "../images/bike1.jpg";
import bike2 from "../images/bike2.jpg";

const Home = () => {
  const [selectedStation, setSelectedStation] = useState("");
  const [showBikes, setShowBikes] = useState(false);
  const [userRole, setUserRole] = useState("stationMaster") // Default to station master view

  // Toggle between user and station master views
  const toggleRole = () => {
    setUserRole(userRole === "user" ? "stationMaster" : "user")
  }

  useEffect(() => {
    const processSteps = document.querySelectorAll(".process-step");

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry, index) => {
          if (entry.isIntersecting) {
            setTimeout(() => {
              entry.target.classList.add("visible");
            }, index * 200);
          }
        });
      },
      { threshold: 0.1 }
    );

    processSteps.forEach((step) => {
      observer.observe(step);
    });

    // Cleanup observer when component unmounts
    return () => {
      processSteps.forEach((step) => {
        observer.unobserve(step);
      });
    };
  }, []);

  const stations = [
    "Downtown Station",
    "Riverside Park",
    "Central Square",
    "University Campus",
    "Beach Boulevard",
  ];

  const availableBikes = {
    "Downtown Station": [
      {
        id: 1,
        name: "Urban Cruiser",
        rate: 12,
        battery: 500,
        image: bike1,
      },
      {
        id: 2,
        name: "City Explorer",
        rate: 15,
        battery: 650,
        image: bike2,
      },
      {
        id: 3,
        name: "Metro Glider",
        rate: 10,
        battery: 450,
        image: bike1,
      },
    ],
    "Riverside Park": [
      {
        id: 4,
        name: "Trail Blazer",
        rate: 18,
        battery: 700,
        image: bike2,
      },
      {
        id: 5,
        name: "Nature Rider",
        rate: 14,
        battery: 550,
        image: bike1,
      },
    ],
    "Central Square": [
      {
        id: 6,
        name: "Urban Commuter",
        rate: 11,
        battery: 480,
        image: bike2,
      },
      {
        id: 7,
        name: "City Hopper",
        rate: 13,
        battery: 520,
        image: bike1,
      },
    ],
    "University Campus": [
      {
        id: 8,
        name: "Campus Cruiser",
        rate: 9,
        battery: 420,
        image: bike2,
      },
      {
        id: 9,
        name: "Student Speeder",
        rate: 10,
        battery: 450,
        image: bike1,
      },
    ],
    "Beach Boulevard": [
      {
        id: 10,
        name: "Coastal Glider",
        rate: 16,
        battery: 600,
        image: bike2,
      },
      {
        id: 11,
        name: "Beach Rover",
        rate: 17,
        battery: 650,
        image: bike1,
      },
    ],
  };

  const handleStationSelect = (station) => {
    setSelectedStation(station);
    setShowBikes(true);
  };

  return (
    <div className="home-container">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <h1>Eco-Friendly Electric Bike Rentals</h1>
          <p>
            Explore the city with our premium electric bikes. Convenient,
            sustainable, and fun!
          </p>

          <div className="search-container">
            <h3>Find Available Bikes</h3>
            <div className="dropdown">
              <select
                value={selectedStation}
                onChange={(e) => handleStationSelect(e.target.value)}
                className="station-select"
              >
                <option value="">Select a Station</option>
                {stations.map((station, index) => (
                  <option key={index} value={station}>
                    {station}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </section>

      {/* Available Bikes Section */}
      {showBikes && (
        <section className="available-bikes-section">
          <h2>Available Bikes at {selectedStation}</h2>
          <div className="bikes-container">
            {availableBikes[selectedStation].map((bike) => (
              <div className="bike-card" key={bike.id}>
                <img 
                  src={bike.image}
                  alt={bike.name}
                  onError={(e) => {
                    console.error(`Failed to load image for ${bike.name}`);
                    e.target.src = "https://via.placeholder.com/200x200?text=Bike+Image";
                  }}
                />
                <h3>{bike.name}</h3>
                <div className="bike-details">
                  <p>
                    <strong>Rate:</strong> ${bike.rate}/hour
                  </p>
                  <p>
                    <strong>Battery:</strong> {bike.battery}W
                  </p>
                </div>
                <button className="reserve-btn">Reserve Now</button>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Features Section */}
      <section className="features-section">
        <h2>Our Premium Features</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="card-content">
              <h3>Powerful Performance</h3>
              <p>
                Our bikes feature high-performance motors that provide smooth
                acceleration and effortless hill climbing.
              </p>
            </div>
          </div>

          <div className="feature-card">
            <div className="card-content">
              <h3>Extended Range</h3>
              <p>
                Long-lasting batteries that provide up to 60km of range on a
                single charge for worry-free adventures.
              </p>
            </div>
          </div>

          <div className="feature-card">
            <div className="card-content">
              <h3>Enhanced Safety</h3>
              <p>
                Integrated safety features including automatic lights,
                reflective details, and responsive hydraulic brakes.
              </p>
            </div>
          </div>

          <div className="feature-card">
            <div className="card-content">
              <h3>Real-time Tracking</h3>
              <p>
                GPS tracking and integration with our app allows you to always
                know the location of your bike.
              </p>
            </div>
          </div>

          <div className="feature-card">
            <div className="card-content">
              <h3>Smart App Control</h3>
              <p>
                Unlock, lock, and monitor your bike's status through our
                intuitive mobile application.
              </p>
            </div>
          </div>

          <div className="feature-card">
            <div className="card-content">
              <h3>Flexible Rentals</h3>
              <p>
                Choose from hourly, daily, or weekly rental plans to suit your
                needs with transparent pricing.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Process Section */}
      <section className="process-section">
        <div className="process-header">
          <h2>Simple Process, Exceptional Experience</h2>
          <p>
            Renting an electric bike has never been easier. Follow these simple
            steps to start your eco-friendly journey today.
          </p>
        </div>

        <div className="process-steps">
          <div className="process-step" data-step="01">
            <div className="step-number">01</div>
            <h3>Sign Up</h3>
            <p>
              Create an account in our app or website to access our fleet of
              premium electric bikes.
            </p>
          </div>

          <div className="process-step" data-step="02">
            <div className="step-number">02</div>
            <h3>Choose a Bike</h3>
            <p>
              Browse our fleet and select the bike that fits your needs and
              preferences.
            </p>
          </div>

          <div className="process-step" data-step="03">
            <div className="step-number">03</div>
            <h3>Reserve & Unlock</h3>
            <p>
              Book your bike and unlock it using our mobile app with just a few
              taps.
            </p>
          </div>

          <div className="process-step" data-step="04">
            <div className="step-number">04</div>
            <h3>Ride & Return</h3>
            <p>
              Enjoy your ride and return the bike to any of our designated
              stations when finished.
            </p>
          </div>
        </div>
      </section>

      {/* Why Choose Us Section */}
      <section className="why-choose-section">
        <h2>Why Choose Us</h2>
        <div className="reasons-container">
          <div className="reason">
            <h3>Eco-Friendly Transportation</h3>
            <p>
              Reduce your carbon footprint while enjoying the convenience of
              personal transportation.
            </p>
          </div>

          <div className="reason">
            <h3>Premium Quality Bikes</h3>
            <p>
              Our fleet consists of top-tier electric bikes maintained to the
              highest standards.
            </p>
          </div>

          <div className="reason">
            <h3>Affordable Pricing</h3>
            <p>
              Competitive rates with flexible plans to suit your budget and
              schedule.
            </p>
          </div>

          <div className="reason">
            <h3>24/7 Customer Support</h3>
            <p>
              Our dedicated team is always ready to assist you with any
              questions or issues.
            </p>
          </div>
        </div>

        <button className="start-now-btn">Start Now</button>
      </section>
    </div>
  );
};

export default Home;
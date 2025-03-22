import { Routes, Route } from "react-router-dom";
import { useState } from 'react';
import Home from "./pages/Home";
import ContactUs from "./pages/ContactUs";
import AboutUs from "./pages/AboutUs";
import Login from "./pages/Login";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Pay from "./pages/pay";
import "./index.css";
import { AuthProvider } from "./context/AuthContext";
import Activity from "./pages/Activity";
import StationMasterDashboard from './pages/Master_Dashboard';

const App = () => {
  const [userRole, setUserRole] = useState("user"); // Default to user view

  const toggleRole = () => {
    setUserRole(userRole === "user" ? "stationMaster" : "user");
  };

  return (
    <AuthProvider>
      <div>
        <Navbar />
        <div className="role-toggle">
          <button onClick={toggleRole} className="toggle-btn">
            Switch to {userRole === "user" ? "Station Master" : "User"} View
          </button>
        </div>
        <main>
          {userRole === "user" ? (
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/contactus" element={<ContactUs />} />
              <Route path="/aboutus" element={<AboutUs />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/pay" element={<Pay />} />
              <Route path="/activity" element={<Activity />} />
            </Routes>
          ) : (
            <StationMasterDashboard />
          )}
        </main>
        <Footer />
      </div>
    </AuthProvider>
  );
};

export default App;

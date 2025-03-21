import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext"; // You'll need to create this

export default function Navbar() {
  const { isAuthenticated } = useAuth(); // Add authentication context

  return (
    <nav className="navbar">
      <h1 className="logo">EV Rentals</h1>
      <div>
        <Link to="/">Home</Link>
        <Link to="/aboutus">About Us</Link>
        <Link to="/contactus">Contact</Link>
        {isAuthenticated ? (
          <>
            <Link to="/activity">Activity</Link>
            <Link to="/pay">Pay</Link>
          </>
        ) : (
          <Link to="/login">Login</Link>
        )}
      </div>
    </nav>
  );
}

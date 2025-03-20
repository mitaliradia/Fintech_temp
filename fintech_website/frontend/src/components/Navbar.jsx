import { Link } from "react-router-dom";
import "../index.css"; // Import the CSS

export default function Navbar() {
  return (
    <nav className="navbar">
      <h1 className="logo">FinTechX</h1>
      <div>
        <Link to="/">Home</Link>
        <Link to="/aboutus">About Us</Link>
        <Link to="/contactus">Contact</Link>
        <Link to="/pay">Pay</Link>
        <Link to="/login">Login</Link>
      </div>
    </nav>
  );
}

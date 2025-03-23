import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "../index.css";

export default function Register() {
  const navigate = useNavigate();
  const { register, error } = useAuth();
  const [loading, setLoading] = useState(false);
  
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    password: "",
    confirm_password: "",
    date_of_birth: "",
    marketing_consent: false
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    // Validate password match
    if (formData.password !== formData.confirm_password) {
      alert("Passwords do not match!");
      setLoading(false);
      return;
    }
    
    // Remove confirm_password before sending to API
    const { confirm_password, ...registerData } = formData;
    
    const result = await register(registerData);
    
    if (result.success) {
      navigate("/");
    }
    
    setLoading(false);
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Create an Account</h2>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label>First Name</label>
            <input
              type="text"
              name="first_name"
              placeholder="Enter your first name"
              value={formData.first_name}
              onChange={handleChange}
              required
            />
          </div>
          
          <div className="input-group">
            <label>Last Name</label>
            <input
              type="text"
              name="last_name"
              placeholder="Enter your last name"
              value={formData.last_name}
              onChange={handleChange}
              required
            />
          </div>
          
          <div className="input-group">
            <label>Email</label>
            <input
              type="email"
              name="email"
              placeholder="Enter your email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>
          
          <div className="input-group">
            <label>Phone</label>
            <input
              type="tel"
              name="phone"
              placeholder="Enter your phone number"
              value={formData.phone}
              onChange={handleChange}
              required
            />
          </div>
          
          <div className="input-group">
            <label>Date of Birth (Optional)</label>
            <input
              type="date"
              name="date_of_birth"
              value={formData.date_of_birth}
              onChange={handleChange}
            />
          </div>
          
          <div className="input-group">
            <label>Password</label>
            <input
              type="password"
              name="password"
              placeholder="Create a password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>
          
          <div className="input-group">
            <label>Confirm Password</label>
            <input
              type="password"
              name="confirm_password"
              placeholder="Confirm your password"
              value={formData.confirm_password}
              onChange={handleChange}
              required
            />
          </div>
          
          <div className="input-group checkbox-group">
            <input
              type="checkbox"
              name="marketing_consent"
              id="marketing_consent"
              checked={formData.marketing_consent}
              onChange={handleChange}
            />
            <label htmlFor="marketing_consent">
              I agree to receive marketing communications
            </label>
          </div>
          
          <button 
            className="login-btn" 
            type="submit"
            disabled={loading}
          >
            {loading ? "Registering..." : "Register"}
          </button>
        </form>
        
        <p className="register-link">
          Already have an account? 
          <span className="link-text" onClick={() => navigate("/login")}>
            {" "}
            Login
          </span>
        </p>
      </div>
    </div>
  );
}
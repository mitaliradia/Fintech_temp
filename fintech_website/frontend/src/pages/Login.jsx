import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "../index.css";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isAdmin, setIsAdmin] = useState(false);
  const [loading, setLoading] = useState(false);
  
  const navigate = useNavigate();
  const { login, adminLogin, error, setError } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    
    let result;
    if (isAdmin) {
      result = await adminLogin(email, password);
      if (result.success) {
        navigate("/admin/dashboard");  // This should match the route in App.jsx
      }
    } else {
      result = await login(email, password);
      if (result.success) {
        navigate("/activity");  // Updated to go to dashboard instead of home
      }
    }
    
    setLoading(false);
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>{isAdmin ? "Admin Login" : "Login"}</h2>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label>Email</label>
            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          
          <div className="input-group">
            <label>Password</label>
            <input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          
          <div className="input-group checkbox-group">
            <input
              type="checkbox"
              id="admin-login"
              checked={isAdmin}
              onChange={(e) => setIsAdmin(e.target.checked)}
            />
            <label htmlFor="admin-login">Login as Admin</label>
          </div>
          
          <button 
            className="login-btn" 
            type="submit"
            disabled={loading}
          >
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>
        
        {!isAdmin && (
          <p className="register-link">
            Don't have an account?
            <span className="link-text" onClick={() => navigate("/register")}>
              {" "}
              Register
            </span>
          </p>
        )}
      </div>
    </div>
  );
}
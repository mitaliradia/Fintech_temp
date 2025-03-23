import { createContext, useContext, useState, useEffect } from "react";
import { authAPI } from "../services/api";

// Create the context
const AuthContext = createContext(null);

// Create the provider component
export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [userRole, setUserRole] = useState("user"); // 'user' or 'admin'

  useEffect(() => {
    // Check if user is logged in when app loads
    checkAuthStatus();
  }, []);

  const checkAuthStatus = () => {
    // Check localStorage for auth tokens
    const token = localStorage.getItem("token");
    const userInfo = localStorage.getItem("user");
    const role = localStorage.getItem("userRole");
    
    if (token && userInfo) {
      setIsAuthenticated(true);
      setUser(JSON.parse(userInfo));
      setUserRole(role || "user");
    }
    
    setLoading(false);
  };

  const login = async (email, password) => {
    try {
      setError("");
      const response = await authAPI.login({ email, password });
      
      if (response.data.success) {
        localStorage.setItem("token", response.data.access_token);
        localStorage.setItem("refreshToken", response.data.refresh_token);
        localStorage.setItem("user", JSON.stringify(response.data.user || {}));
        localStorage.setItem("userRole", "user");
        
        setIsAuthenticated(true);
        setUser(response.data.user || {});
        setUserRole("user");
        
        return { success: true };
      } else {
        setError(response.data.message || "Login failed");
        return { success: false, error: response.data.message };
      }
    } catch (error) {
      const errorMessage = error.response?.data?.message || "Login failed";
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const adminLogin = async (email, password) => {
    try {
      setError("");
      const response = await authAPI.adminLogin({ email, password });
      
      if (response.data.message === "Login successful") {
        localStorage.setItem("token", response.data.access_token);
        localStorage.setItem("refreshToken", response.data.refresh_token);
        localStorage.setItem("user", JSON.stringify(response.data.admin || {}));
        localStorage.setItem("userRole", "admin");
        
        setIsAuthenticated(true);
        setUser(response.data.admin || {});
        setUserRole("admin");
        
        return { success: true };
      } else {
        setError(response.data.error || "Login failed");
        return { success: false, error: response.data.error };
      }
    } catch (error) {
      const errorMessage = error.response?.data?.error || "Login failed";
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const register = async (userData) => {
    try {
      setError("");
      const response = await authAPI.register(userData);
      
      if (response.data.success) {
        localStorage.setItem("token", response.data.token);
        localStorage.setItem("user", JSON.stringify(response.data.user || {}));
        localStorage.setItem("userRole", "user");
        
        setIsAuthenticated(true);
        setUser(response.data.user || {});
        setUserRole("user");
        
        return { success: true };
      } else {
        setError(response.data.message || "Registration failed");
        return { success: false, error: response.data.message };
      }
    } catch (error) {
      const errorMessage = error.response?.data?.message || "Registration failed";
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

const logout = async () => {
  try {
    // Call the logout API
    await authAPI.logout();
  } catch (error) {
    console.error("Logout error:", error);
  } finally {
    // Clear all auth data from localStorage
    localStorage.removeItem("token");
    localStorage.removeItem("refreshToken");
    localStorage.removeItem("user");
    localStorage.removeItem("userRole");
    
    // Reset the auth state
    setIsAuthenticated(false);
    setUser(null);
    setUserRole("user");
  }
};

  const value = {
    isAuthenticated,
    user,
    loading,
    error,
    userRole,
    login,
    adminLogin,
    register,
    logout,
    setUserRole,
    setError
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export default AuthContext;
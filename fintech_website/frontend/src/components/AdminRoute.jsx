// src/components/AdminRoute.jsx
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const AdminRoute = ({ children }) => {
  const { isAuthenticated, userRole } = useAuth();
  const adminRole = localStorage.getItem("adminRole");
  
  if (!isAuthenticated || userRole !== "admin") {
    return <Navigate to="/login" />;
  }
  
  return children;
};

export default AdminRoute;
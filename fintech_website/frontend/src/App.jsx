import { Routes, Route } from "react-router-dom";
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
import StationMasterDashboard from "./pages/Master_Dashboard";
import UserRoute from "./components/UserRoute";
import AdminRoute from "./components/AdminRoute";
// Import StationManagement components
import StationManagement from "./pages/stationmanagement";
// import AddStation from "./pages/StationManagement/AddStation";
// import EditStation from "./pages/StationManagement/EditStation";
// import ViewStations from "./pages/StationManagement/ViewStations";
import StationDetail from "./pages/StationDetail";

const App = () => {
  return (
    <AuthProvider>
      <div>
        <Navbar />
        <main style={{ marginTop: "80px" }}>
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={<Home />} />
            <Route path="/contactus" element={<ContactUs />} />
            <Route path="/aboutus" element={<AboutUs />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/* Protected User Routes */}
            <Route path="/dashboard" element={
              <UserRoute>
                <Dashboard />
              </UserRoute>
            } />
            <Route path="/pay" element={
              <UserRoute>
                <Pay />
              </UserRoute>
            } />
            <Route path="/activity" element={
              <UserRoute>
                <Activity />
              </UserRoute>
            } />

            {/* Protected Admin Routes */}
            <Route path="/admin/dashboard" element={
              <AdminRoute>
                <StationMasterDashboard />
              </AdminRoute>
            } />

            {/* Station Management Routes */}
            <Route path="/admin/stations" element={
              <AdminRoute>
                <StationManagement />
              </AdminRoute>
            } />
            <Route path="/station/:stationId" element={
              <AdminRoute>
                <StationDetail />
              </AdminRoute>
            } />
            {/* <Route path="/admin/stations/add" element={
              <AdminRoute>
                <AddStation />
              </AdminRoute>
            } />
            <Route path="/admin/stations/edit/:id" element={
              <AdminRoute>
                <EditStation />
              </AdminRoute>
            } />
            <Route path="/admin/stations/view" element={
              <AdminRoute>
                <ViewStations />
              </AdminRoute>
            } /> */}
          </Routes>
        </main>
        <Footer />
      </div>
    </AuthProvider>
  );
};

export default App;
// src/pages/StationDetail.jsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
// import { stationAPI } from '../services/stationService';
import { useAuth } from '../context/AuthContext';

const StationDetail = () => {
  const { stationId } = useParams();
  const navigate = useNavigate();
  const { userRole, user } = useAuth();
  
  const [station, setStation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Check if user is a Super Admin
  const isSuperAdmin = user?.role === 'SUPER_ADMIN';
  
  // Fetch station details
  useEffect(() => {
    const fetchStation = async () => {
      setLoading(true);
      try {
        const response = await stationAPI.getStation(stationId);
        if (response.data.success) {
          setStation(response.data.station);
        } else {
          setError('Failed to load station details');
        }
      } catch (err) {
        setError('Error loading station: ' + (err.response?.data?.error || err.message));
      } finally {
        setLoading(false);
      }
    };
    
    fetchStation();
  }, [stationId]);
  
  if (loading) return <div className="loading">Loading station details...</div>;
  if (error) return <div className="error-alert">{error}</div>;
  if (!station) return <div className="not-found">Station not found</div>;
  
  return (
    <div className="station-detail">
      <div className="page-header">
        <button onClick={() => navigate(-1)} className="back-btn">
          &larr; Back to Stations
        </button>
        
        <h1>{station.name}</h1>
        
        <span className={`status ${station.is_active ? 'active' : 'inactive'}`}>
          {station.is_active ? 'Active' : 'Inactive'}
        </span>
      </div>
      
      <div className="station-info-grid">
        <div className="info-card">
          <h3>Location</h3>
          <p>
            {station.address.street && `${station.address.street}, `}
            {station.address.city}, {station.address.state} {station.address.zip_code}
            {station.address.country && `, ${station.address.country}`}
          </p>
          
          <p className="coordinates">
            Lat: {station.location.latitude}, Long: {station.location.longitude}
          </p>
          
          {/* You could add a map here with the station location */}
        </div>
        
        <div className="info-card">
          <h3>Contact Information</h3>
          {station.contact.phone && <p>Phone: {station.contact.phone}</p>}
          {station.contact.email && <p>Email: {station.contact.email}</p>}
        </div>
        
        <div className="info-card">
          <h3>Capacity</h3>
          <div className="capacity-stats">
            <div className="stat">
              <span className="stat-label">Parking Spots</span>
              <span className="stat-value">
                {station.available_spots} / {station.capacity}
              </span>
            </div>
            
            <div className="stat">
              <span className="stat-label">Charging Stations</span>
              <span className="stat-value">{station.charging_stations}</span>
            </div>
          </div>
          
          <div className="capacity-meter">
            <div 
              className="meter-fill" 
              style={{ width: `${(station.available_spots / station.capacity) * 100}%` }}
            ></div>
          </div>
          
          <button
            className="update-spots-btn"
            onClick={() => navigate(`/stations/${stationId}/update-availability`)}
          >
            Update Available Spots
          </button>
        </div>
        
        {station.operating_hours && (
          <div className="info-card">
            <h3>Operating Hours</h3>
            <p>{station.operating_hours}</p>
          </div>
        )}
        
        {station.station_master && (
          <div className="info-card">
            <h3>Station Master</h3>
            <p>{station.station_master.name}</p>
            <p>{station.station_master.email}</p>
          </div>
        )}
      </div>
      
      <div className="station-actions">
        <button onClick={() => navigate(`/stations/${stationId}/edit`)}>
          Edit Station
        </button>
        
        {isSuperAdmin && (
          <button 
            className="delete-btn"
            onClick={() => {
              if (window.confirm('Are you sure you want to delete this station?')) {
                stationAPI.deleteStation(stationId).then(() => {
                  navigate('/stations');
                });
              }
            }}
          >
            Delete Station
          </button>
        )}
      </div>
    </div>
  );
};

export default StationDetail;
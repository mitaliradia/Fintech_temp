// src/pages/StationManagement.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
// import { stationAPI } from '../services/stationService';
import { useAuth } from '../context/AuthContext';

const StationManagement = () => {
  const { userRole, user } = useAuth();
  const navigate = useNavigate();
  const [stations, setStations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');
  const [showOnlyActive, setShowOnlyActive] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [selectedStation, setSelectedStation] = useState(null);
  
  // Check if user is a Super Admin
  const isSuperAdmin = user?.role === 'SUPER_ADMIN';
  
  // Fetch stations
  const fetchStations = async () => {
    setLoading(true);
    try {
      const filters = {};
      if (searchTerm) filters.name = searchTerm;
      if (showOnlyActive !== null) filters.is_active = showOnlyActive;
      
      const response = await stationAPI.getStations(page, 10, filters);
      
      if (response.data.success) {
        setStations(response.data.stations);
        setTotalPages(response.data.pagination.pages);
      } else {
        setError('Failed to load stations');
      }
    } catch (err) {
      setError('Error loading stations: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };
  
  // Load stations on component mount and when filters change
  useEffect(() => {
    fetchStations();
  }, [page, searchTerm, showOnlyActive]);
  
  // Handle station creation
  const handleCreateStation = async (stationData) => {
    try {
      const response = await stationAPI.createStation(stationData);
      if (response.data.success) {
        setShowCreateForm(false);
        fetchStations();
      } else {
        setError('Failed to create station');
      }
    } catch (err) {
      setError('Error creating station: ' + (err.response?.data?.error || err.message));
    }
  };
  
  // Handle station update
  const handleUpdateStation = async (stationId, stationData) => {
    try {
      const response = await stationAPI.updateStation(stationId, stationData);
      if (response.data.success) {
        setSelectedStation(null);
        fetchStations();
      } else {
        setError('Failed to update station');
      }
    } catch (err) {
      setError('Error updating station: ' + (err.response?.data?.error || err.message));
    }
  };
  
  // Handle station deletion
  const handleDeleteStation = async (stationId) => {
    if (!window.confirm('Are you sure you want to delete this station?')) return;
    
    try {
      const response = await stationAPI.deleteStation(stationId);
      if (response.data.success) {
        fetchStations();
      } else {
        setError('Failed to delete station');
      }
    } catch (err) {
      setError('Error deleting station: ' + (err.response?.data?.error || err.message));
    }
  };
  
  // Handle availability update
  const handleUpdateAvailability = async (stationId, availableSpots) => {
    try {
      const response = await stationAPI.updateAvailability(stationId, availableSpots);
      if (response.data.success) {
        fetchStations();
      } else {
        setError('Failed to update availability');
      }
    } catch (err) {
      setError('Error updating availability: ' + (err.response?.data?.error || err.message));
    }
  };
  
  // View station details
  const handleViewStation = (stationId) => {
    navigate(`/station/${stationId}`);
  };
  
  // Edit station
  const handleEditStation = (station) => {
    setSelectedStation(station);
  };
  
  return (
    <div className="station-management">
      <h1>{isSuperAdmin ? 'Station Management' : 'My Stations'}</h1>
      
      {error && <div className="error-alert">{error}</div>}
      
      {/* Search and filters */}
      <div className="station-filters">
        <input
          type="text"
          placeholder="Search stations..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        
        <label>
          <input
            type="checkbox"
            checked={showOnlyActive}
            onChange={(e) => setShowOnlyActive(e.target.checked)}
          />
          Show only active stations
        </label>
        
        {isSuperAdmin && (
          <button 
            className="create-btn"
            onClick={() => setShowCreateForm(true)}
          >
            Create New Station
          </button>
        )}
      </div>
      
      {/* Stations table */}
      {loading ? (
        <div className="loading">Loading stations...</div>
      ) : stations.length === 0 ? (
        <div className="no-data">No stations found</div>
      ) : (
        <table className="stations-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Location</th>
              <th>Capacity</th>
              <th>Available Spots</th>
              {isSuperAdmin && <th>Station Master</th>}
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {stations.map(station => (
              <tr key={station.id}>
                <td>{station.name}</td>
                <td>
                  {station.address.city}, {station.address.state}
                </td>
                <td>{station.capacity}</td>
                <td>
                  <span className={station.available_spots === 0 ? 'full' : ''}>
                    {station.available_spots} / {station.capacity}
                  </span>
                </td>
                {isSuperAdmin && (
                  <td>
                    {station.station_master ? (
                      <span>{station.station_master.name}</span>
                    ) : (
                      <span className="unassigned">Unassigned</span>
                    )}
                  </td>
                )}
                <td>
                  <span className={`status ${station.is_active ? 'active' : 'inactive'}`}>
                    {station.is_active ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td className="actions">
                  <button onClick={() => handleViewStation(station.id)}>View</button>
                  <button onClick={() => handleEditStation(station)}>Edit</button>
                  
                  {/* Only Super Admins can delete stations */}
                  {isSuperAdmin && (
                    <button 
                      className="delete"
                      onClick={() => handleDeleteStation(station.id)}
                    >
                      Delete
                    </button>
                  )}
                  
                  {/* Both Super Admins and Station Masters can update availability */}
                  <button onClick={() => setSelectedStation({
                    ...station,
                    updateAvailability: true
                  })}>
                    Update Spots
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      
      {/* Pagination */}
      <div className="pagination">
        <button 
          disabled={page === 1} 
          onClick={() => setPage(p => Math.max(1, p - 1))}
        >
          Previous
        </button>
        <span>Page {page} of {totalPages}</span>
        <button 
          disabled={page === totalPages} 
          onClick={() => setPage(p => Math.min(totalPages, p + 1))}
        >
          Next
        </button>
      </div>
      
      {/* Create Station Form Modal */}
      {showCreateForm && (
        <StationForm 
          onSubmit={handleCreateStation}
          onCancel={() => setShowCreateForm(false)}
          isSuperAdmin={isSuperAdmin}
        />
      )}
      
      {/* Edit Station Modal */}
      {selectedStation && !selectedStation.updateAvailability && (
        <StationForm 
          station={selectedStation}
          onSubmit={(data) => handleUpdateStation(selectedStation.id, data)}
          onCancel={() => setSelectedStation(null)}
          isSuperAdmin={isSuperAdmin}
        />
      )}
      
      {/* Update Availability Modal */}
      {selectedStation && selectedStation.updateAvailability && (
        <UpdateAvailabilityForm 
          station={selectedStation}
          onSubmit={(spots) => handleUpdateAvailability(selectedStation.id, spots)}
          onCancel={() => setSelectedStation(null)}
        />
      )}
    </div>
  );
};

// Station Form Component
const StationForm = ({ station, onSubmit, onCancel, isSuperAdmin }) => {
  const isEditing = !!station;
  const [formData, setFormData] = useState(
    station ? {
      name: station.name,
      street: station.address.street || '',
      city: station.address.city || '',
      state: station.address.state || '',
      zip_code: station.address.zip_code || '',
      country: station.address.country || '',
      latitude: station.location.latitude,
      longitude: station.location.longitude,
      contact_phone: station.contact.phone || '',
      contact_email: station.contact.email || '',
      operating_hours: station.operating_hours || '',
      capacity: station.capacity,
      charging_stations: station.charging_stations,
      is_active: station.is_active,
      station_master_id: station.station_master_id || ''
    } : {
      name: '',
      street: '',
      city: '',
      state: '',
      zip_code: '',
      country: '',
      latitude: '',
      longitude: '',
      contact_phone: '',
      contact_email: '',
      operating_hours: '',
      capacity: 10,
      charging_stations: 0,
      is_active: true,
      station_master_id: ''
    }
  );
  
  const [stationMasters, setStationMasters] = useState([]);
  const [loadingMasters, setLoadingMasters] = useState(false);
  
  // Fetch station masters for the dropdown (only for Super Admin)
  useEffect(() => {
    if (isSuperAdmin) {
      const fetchStationMasters = async () => {
        setLoadingMasters(true);
        try {
          // This would need an API endpoint to fetch admin users with STATION_MASTER role
          // For now, we'll just simulate it
          setStationMasters([
            { id: '1', name: 'John Doe' },
            { id: '2', name: 'Jane Smith' }
          ]);
        } catch (error) {
          console.error('Error fetching station masters:', error);
        } finally {
          setLoadingMasters(false);
        }
      };
      
      fetchStationMasters();
    }
  }, [isSuperAdmin]);
  
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };
  
  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h2>{isEditing ? 'Edit Station' : 'Create New Station'}</h2>
          <button className="close-btn" onClick={onCancel}>×</button>
        </div>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">Station Name*</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
            />
          </div>
          
          <div className="form-section">
            <h3>Address</h3>
            
            <div className="form-group">
              <label htmlFor="street">Street</label>
              <input
                type="text"
                id="street"
                name="street"
                value={formData.street}
                onChange={handleChange}
              />
            </div>
            
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="city">City</label>
                <input
                  type="text"
                  id="city"
                  name="city"
                  value={formData.city}
                  onChange={handleChange}
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="state">State</label>
                <input
                  type="text"
                  id="state"
                  name="state"
                  value={formData.state}
                  onChange={handleChange}
                />
              </div>
            </div>
            
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="zip_code">Zip Code</label>
                <input
                  type="text"
                  id="zip_code"
                  name="zip_code"
                  value={formData.zip_code}
                  onChange={handleChange}
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="country">Country</label>
                <input
                  type="text"
                  id="country"
                  name="country"
                  value={formData.country}
                  onChange={handleChange}
                />
              </div>
            </div>
          </div>
          
          <div className="form-section">
            <h3>Location</h3>
            
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="latitude">Latitude*</label>
                <input
                  type="number"
                  id="latitude"
                  name="latitude"
                  value={formData.latitude}
                  onChange={handleChange}
                  step="0.000001"
                  required
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="longitude">Longitude*</label>
                <input
                  type="number"
                  id="longitude"
                  name="longitude"
                  value={formData.longitude}
                  onChange={handleChange}
                  step="0.000001"
                  required
                />
              </div>
            </div>
          </div>
          
          <div className="form-section">
            <h3>Contact Information</h3>
            
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="contact_phone">Phone</label>
                <input
                  type="tel"
                  id="contact_phone"
                  name="contact_phone"
                  value={formData.contact_phone}
                  onChange={handleChange}
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="contact_email">Email</label>
                <input
                  type="email"
                  id="contact_email"
                  name="contact_email"
                  value={formData.contact_email}
                  onChange={handleChange}
                />
              </div>
            </div>
          </div>
          
          <div className="form-section">
            <h3>Station Details</h3>
            
            <div className="form-group">
              <label htmlFor="operating_hours">Operating Hours</label>
              <input
                type="text"
                id="operating_hours"
                name="operating_hours"
                value={formData.operating_hours}
                onChange={handleChange}
                placeholder="e.g., 9:00 AM - 6:00 PM"
              />
            </div>
            
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="capacity">Parking Capacity*</label>
                <input
                  type="number"
                  id="capacity"
                  name="capacity"
                  value={formData.capacity}
                  onChange={handleChange}
                  min="1"
                  required
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="charging_stations">Charging Stations</label>
                <input
                  type="number"
                  id="charging_stations"
                  name="charging_stations"
                  value={formData.charging_stations}
                  onChange={handleChange}
                  min="0"
                />
              </div>
            </div>
            
            <div className="form-group checkbox">
              <input
                type="checkbox"
                id="is_active"
                name="is_active"
                checked={formData.is_active}
                onChange={handleChange}
              />
              <label htmlFor="is_active">Station is active</label>
            </div>
            
            {isSuperAdmin && (
              <div className="form-group">
                <label htmlFor="station_master_id">Station Master</label>
                <select
                  id="station_master_id"
                  name="station_master_id"
                  value={formData.station_master_id}
                  onChange={handleChange}
                >
                  <option value="">-- Select Station Master --</option>
                  {loadingMasters ? (
                    <option disabled>Loading...</option>
                  ) : (
                    stationMasters.map(master => (
                      <option key={master.id} value={master.id}>
                        {master.name}
                      </option>
                    ))
                  )}
                </select>
              </div>
            )}
          </div>
          
          <div className="form-actions">
            <button type="button" className="cancel-btn" onClick={onCancel}>
              Cancel
            </button>
            <button type="submit" className="submit-btn">
              {isEditing ? 'Update Station' : 'Create Station'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// Update Availability Form Component
const UpdateAvailabilityForm = ({ station, onSubmit, onCancel }) => {
  const [availableSpots, setAvailableSpots] = useState(station.available_spots);
  
  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(Number(availableSpots));
  };
  
  return (
    <div className="modal-overlay">
      <div className="modal-content small">
        <div className="modal-header">
          <h2>Update Available Spots</h2>
          <button className="close-btn" onClick={onCancel}>×</button>
        </div>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="available_spots">
              Available Spots (max: {station.capacity})
            </label>
            <input
              type="number"
              id="available_spots"
              value={availableSpots}
              onChange={(e) => setAvailableSpots(e.target.value)}
              min="0"
              max={station.capacity}
              required
            />
          </div>
          
          <div className="form-actions">
            <button type="button" className="cancel-btn" onClick={onCancel}>
              Cancel
            </button>
            <button type="submit" className="submit-btn">
              Update
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default StationManagement;
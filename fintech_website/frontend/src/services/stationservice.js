import api from './api';

export const stationAPI = {
  // Get list of stations with pagination and filtering
  getStations: (page = 1, perPage = 10, filters = {}) => {
    const params = {
      page,
      per_page: perPage,
      ...filters
    };
    return api.get('/api/station/list', { params });
  },
  
  // Get a single station by ID
  getStation: (stationId) => api.get(`/api/station/${stationId}`),
  
  // Create a new station
  createStation: (stationData) => api.post('/api/station/create', stationData),
  
  // Update an existing station
  updateStation: (stationId, stationData) => api.put(`/api/station/${stationId}`, stationData),
  
  // Delete a station (soft delete)
  deleteStation: (stationId) => api.delete(`/api/station/${stationId}`),
  
  // Update station availability
  updateAvailability: (stationId, availableSpots) => 
    api.patch(`/api/station/${stationId}/update-availability`, { available_spots: availableSpots })
};
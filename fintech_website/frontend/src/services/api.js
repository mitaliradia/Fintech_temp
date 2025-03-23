// src/services/api.js
import axios from 'axios';

// Base URL for your API - empty string for proxy to work
// const API_URL = 'http://127.0.0.1:5000';
// for deployment
const API_URL = 'https://fintech-backend-dj0j.onrender.com';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor for adding auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Auth API
// Auth API
export const authAPI = {
    login: (credentials) => api.post('/api/auth/login', credentials),
    register: (userData) => api.post('/api/auth/register', userData),
    logout: () => api.post('/api/auth/logout'),
    refreshToken: (refreshToken) =>
      api.post('/api/auth/refresh', {}, {
        headers: { 'Authorization': `Bearer ${refreshToken}` }
      }),
    // Add this line:
    adminLogin: (credentials) => api.post('/api/auth/admin/login', credentials)
  };

// Vehicle API
export const vehicleAPI = {
  getVehicles: (params) => api.get('/api/vehicle', { params }),
  getVehicleById: (id) => api.get(`/api/vehicle/${id}`)
};

// Station API
export const stationAPI = {
    getStations: (params) => api.get('/api/station/list', { params }),
    getStation: (stationId) => api.get(`/api/station/${stationId}`),
    createStation: (stationData) => api.post('/api/station/create', stationData),
    updateStation: (stationId, stationData) => api.put(`/api/station/${stationId}`, stationData),
    deleteStation: (stationId) => api.delete(`/api/station/${stationId}`),
    updateAvailability: (stationId, availableSpots) => 
      api.patch(`/api/station/${stationId}/update-availability`, { available_spots: availableSpots })
  };

// Rental API
export const rentalAPI = {
  createRental: (data) => api.post('/api/rentals', data),
  getActiveRentals: () => api.get('/api/rentals/active'),
  getPastRentals: () => api.get('/api/rentals/past')
};

// Payment API
export const paymentAPI = {
  createOrder: (data) => api.post('/pay/create_order', data)
};

export default api;
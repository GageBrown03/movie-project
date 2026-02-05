// src/services/api.js
// This file centralizes all API calls to your Flask backend

// Use environment variable in production, localhost in development
const API_BASE =
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';


// Helper function to get auth token
function getAuthHeaders() {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` })
  };
}

// Authentication API
export const authAPI = {
  async register(username, email, password) {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, email, password })
    });
    
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error || 'Registration failed');
    }
    
    return res.json();
  },
  
  async login(username, password) {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error || 'Login failed');
    }
    
    return res.json();
  },
  
  async getCurrentUser() {
    const res = await fetch(`${API_BASE}/auth/me`, {
      headers: getAuthHeaders()
    });
    
    if (!res.ok) {
      throw new Error('Failed to get user info');
    }
    
    return res.json();
  },
  
  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }
};

// Movie API (now with authentication)
export const movieAPI = {
  async getAll() {
    const res = await fetch(`${API_BASE}/movies`, {
      headers: getAuthHeaders()
    });
    
    if (!res.ok) throw new Error('Failed to fetch movies');
    return res.json();
  },
  
  async getOne(id) {
    const res = await fetch(`${API_BASE}/movies/${id}`, {
      headers: getAuthHeaders()
    });
    
    if (!res.ok) throw new Error('Movie not found');
    return res.json();
  },
  
  async create(movieData) {
    const res = await fetch(`${API_BASE}/movies`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(movieData)
    });
    
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error || 'Failed to create movie');
    }
    
    return res.json();
  },
  
  async update(id, movieData) {
    const res = await fetch(`${API_BASE}/movies/${id}`, {
      method: 'PATCH',
      headers: getAuthHeaders(),
      body: JSON.stringify(movieData)
    });
    
    if (!res.ok) throw new Error('Failed to update movie');
    return res.json();
  },
  
  async delete(id) {
    const res = await fetch(`${API_BASE}/movies/${id}`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    });
    
    if (!res.ok) throw new Error('Failed to delete movie');
    return res.json();
  }
};
// src/services/api-production.js
// This file centralizes all API calls to your Flask backend

// Use environment variable in production, localhost in development
const API_BASE = process.env.VUE_APP_API_BASE_URL || 'http://localhost:5000';

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

// TMDB API (search movies + TV shows)
export const tmdbAPI = {
  async search(query) {
    const res = await fetch(`${API_BASE}/tmdb/search?query=${encodeURIComponent(query)}`, {
      headers: getAuthHeaders()
    });
    
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error || 'TMDB search failed');
    }
    
    return res.json();
  },
  
  async getMovieDetails(tmdbId) {
    const res = await fetch(`${API_BASE}/tmdb/movie/${tmdbId}`, {
      headers: getAuthHeaders()
    });
    
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error || 'Failed to get movie details');
    }
    
    return res.json();
  },
  
  async getTVDetails(tmdbId) {
    const res = await fetch(`${API_BASE}/tmdb/tv/${tmdbId}`, {
      headers: getAuthHeaders()
    });
    
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error || 'Failed to get TV details');
    }
    
    return res.json();
  }
};

// Media API (movies + TV shows - replaces movieAPI)
export const mediaAPI = {
  async getAll(filters = {}) {
    const params = new URLSearchParams();
    if (filters.type) params.append('type', filters.type);
    if (filters.status) params.append('status', filters.status);
    
    const queryString = params.toString();
    const url = `${API_BASE}/media${queryString ? '?' + queryString : ''}`;
    
    const res = await fetch(url, {
      headers: getAuthHeaders()
    });
    
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error || 'Failed to fetch media');
    }
    
    return res.json();
  },
  
  async getOne(id) {
    const res = await fetch(`${API_BASE}/media/${id}`, {
      headers: getAuthHeaders()
    });
    
    if (!res.ok) throw new Error('Media not found');
    return res.json();
  },
  
  async create(mediaData) {
    const res = await fetch(`${API_BASE}/media`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(mediaData)
    });
    
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error || 'Failed to create media');
    }
    
    return res.json();
  },
  
  async update(id, mediaData) {
    const res = await fetch(`${API_BASE}/media/${id}`, {
      method: 'PATCH',
      headers: getAuthHeaders(),
      body: JSON.stringify(mediaData)
    });
    
    if (!res.ok) throw new Error('Failed to update media');
    return res.json();
  },
  
  async delete(id) {
    const res = await fetch(`${API_BASE}/media/${id}`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    });
    
    if (!res.ok) throw new Error('Failed to delete media');
    return res.json();
  }
};

// Privacy API (NEW - Week 2)
export const privacyAPI = {
  async getSettings() {
    const res = await fetch(`${API_BASE}/api/privacy`, {
      headers: getAuthHeaders()
    });
    
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error || 'Failed to get privacy settings');
    }
    
    return res.json();
  },
  
  async updateSettings(settings) {
    const res = await fetch(`${API_BASE}/api/privacy`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(settings)
    });
    
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error || 'Failed to update privacy settings');
    }
    
    return res.json();
  },
  
  async checkPermissions(userId) {
    const res = await fetch(`${API_BASE}/api/privacy/check/${userId}`, {
      headers: getAuthHeaders()
    });
    
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error || 'Failed to check permissions');
    }
    
    return res.json();
  }
};

// Friends API (NEW - Week 2)
export const friendsAPI = {
  async getAll() {
    const res = await fetch(`${API_BASE}/api/friends`, {
      headers: getAuthHeaders()
    });
    
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error || 'Failed to get friends');
    }
    
    return res.json();
  },
  
  async getPending() {
    const res = await fetch(`${API_BASE}/api/friends/pending`, {
      headers: getAuthHeaders()
    });
    
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error || 'Failed to get pending requests');
    }
    
    return res.json();
  },
  
  async search(query) {
    const res = await fetch(`${API_BASE}/api/friends/search?q=${encodeURIComponent(query)}`, {
      headers: getAuthHeaders()
    });
    
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error || 'Failed to search users');
    }
    
    return res.json();
  },
  
  async sendRequest(username) {
    const res = await fetch(`${API_BASE}/api/friends/request`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ username })
    });
    
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error || 'Failed to send friend request');
    }
    
    return res.json();
  },
  
  async acceptRequest(friendshipId) {
    const res = await fetch(`${API_BASE}/api/friends/accept/${friendshipId}`, {
      method: 'POST',
      headers: getAuthHeaders()
    });
    
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error || 'Failed to accept request');
    }
    
    return res.json();
  },
  
  async declineRequest(friendshipId) {
    const res = await fetch(`${API_BASE}/api/friends/decline/${friendshipId}`, {
      method: 'POST',
      headers: getAuthHeaders()
    });
    
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error || 'Failed to decline request');
    }
    
    return res.json();
  },
  
  async remove(friendshipId) {
    const res = await fetch(`${API_BASE}/api/friends/${friendshipId}`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    });
    
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error || 'Failed to remove friend');
    }
    
    return res.json();
  }
};

// Compare API (NEW - Week 2)
export const compareAPI = {
  async getRatings(username) {
    const res = await fetch(`${API_BASE}/api/compare/${username}`, {
      headers: getAuthHeaders()
    });
    
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error || 'Failed to get comparison');
    }
    
    return res.json();
  },
  
  async getStats(username) {
    const res = await fetch(`${API_BASE}/api/compare/${username}/stats`, {
      headers: getAuthHeaders()
    });
    
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error || 'Failed to get stats');
    }
    
    return res.json();
  }
};

// Legacy alias for backward compatibility (can remove later)
export const movieAPI = mediaAPI;
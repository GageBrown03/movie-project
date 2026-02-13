// src/services/analytics.js - Analytics API service

const API_BASE_URL = process.env.VUE_APP_API_BASE_URL || 'http://localhost:5000';

/**
 * Get JWT token from localStorage
 */
function getAuthHeaders() {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    'Authorization': token ? `Bearer ${token}` : ''
  };
}

/**
 * Handle API response
 */
async function handleResponse(response) {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
  }
  return response.json();
}

/**
 * Analytics API methods
 */
export const analyticsAPI = {
  /**
   * Get top actors and directors with photos
   */
  async getTopPeople() {
    const response = await fetch(`${API_BASE_URL}/api/analytics/top-people`, {
      method: 'GET',
      headers: getAuthHeaders()
    });
    return handleResponse(response);
  },

  /**
   * Get decade preferences
   */
  async getDecadePreferences() {
    const response = await fetch(`${API_BASE_URL}/api/analytics/decades`, {
      method: 'GET',
      headers: getAuthHeaders()
    });
    return handleResponse(response);
  },

  /**
   * Get all-time records
   */
  async getRecords() {
    const response = await fetch(`${API_BASE_URL}/api/analytics/records`, {
      method: 'GET',
      headers: getAuthHeaders()
    });
    return handleResponse(response);
  },

  /**
   * Get collection card stats
   */
  async getCollectionCard() {
    const response = await fetch(`${API_BASE_URL}/api/analytics/collection-card`, {
      method: 'GET',
      headers: getAuthHeaders()
    });
    return handleResponse(response);
  }
};
// src/services/showcase-api.js

const API_BASE = process.env.VUE_APP_API_BASE_URL || 'http://localhost:5000';

function getAuthHeaders() {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
  };
}

async function handleResponse(res) {
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || `HTTP ${res.status}`);
  }
  return res.json();
}

export const showcaseAPI = {
  /** Fetch any user's showcase (respects privacy). */
  async getByUsername(username) {
    const res = await fetch(`${API_BASE}/api/showcase/${username}`, {
      headers: getAuthHeaders(),
    });
    return handleResponse(res);
  },

  /** Fetch own showcase with full edit metadata. */
  async getMine() {
    const res = await fetch(`${API_BASE}/api/showcase/mine`, {
      headers: getAuthHeaders(),
    });
    return handleResponse(res);
  },

  /**
   * Save entire showcase in one call.
   * Only keys present in `payload` are updated.
   *
   * @param {Object} payload
   * @param {Array}  [payload.topMovies]   - [{ mediaId, rank }]
   * @param {Array}  [payload.topTv]       - [{ mediaId, rank }]
   * @param {Array}  [payload.favSeries]   - [{ mediaId, rank, tmdbCollectionId, tmdbCollectionName }]
   * @param {Object|null} [payload.hiddenGem] - { mediaId, rank, note } or null to clear
   */
  async save(payload) {
    const res = await fetch(`${API_BASE}/api/showcase`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(payload),
    });
    return handleResponse(res);
  },
};
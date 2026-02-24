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

/**
 * Normalize a single showcase entry to a consistent shape.
 * Accepts snake_case / camelCase and preserves embedded media for rendering.
 */
function mapEntry(e = {}) {
  const media =
    e.media ||
    e.media_obj || // just in case
    null;

  return {
    mediaId:
      e.mediaId ??
      e.media_id ??
      media?.mediaId ??
      media?.media_id ??
      null,
    rank: e.rank ?? e.order ?? null,
    tmdbCollectionId: e.tmdbCollectionId ?? e.tmdb_collection_id ?? null,
    tmdbCollectionName: e.tmdbCollectionName ?? e.tmdb_collection_name ?? null,
    media: media || null,
  };
}

/**
 * Normalize hidden gem to either { mediaId, note, media } or null.
 */
function mapHiddenGem(hg) {
  if (!hg || typeof hg !== 'object') return null;

  const media =
    hg.media ||
    hg.media_obj ||
    null;

  const mediaId =
    hg.mediaId ??
    hg.media_id ??
    media?.mediaId ??
    media?.media_id ??
    null;

  if (!mediaId) return null; // <- critical so "empty object" isn't treated as real content

  return {
    mediaId,
    note: hg.note || null,
    media: media || null,
  };
}

/**
 * Normalize the backend showcase payload into a clean, camelCased object
 * that the UI can rely on (arrays always present, hiddenGem is null unless real).
 *
 * Accepts either { showcase: {...} } OR a showcase object directly.
 */
function normalizeShowcase(payload) {
  const src = payload?.showcase || payload || {};

  const topMovies = Array.isArray(src.topMovies) ? src.topMovies
                   : Array.isArray(src.top_movies) ? src.top_movies
                   : [];
  const topTv = Array.isArray(src.topTv) ? src.topTv
                 : Array.isArray(src.top_tv) ? src.top_tv
                 : [];
  const favSeries = Array.isArray(src.favSeries) ? src.favSeries
                   : Array.isArray(src.fav_series) ? src.fav_series
                   : [];
  const hiddenGemRaw = src.hiddenGem ?? src.hidden_gem ?? null;

  return {
    topMovies: topMovies.map(mapEntry),
    topTv: topTv.map(mapEntry),
    favSeries: favSeries.map(mapEntry),
    hiddenGem: mapHiddenGem(hiddenGemRaw),
  };
}

export const showcaseAPI = {
  /** Fetch any user's showcase (respects privacy). */
  async getByUsername(username) {
    const res = await fetch(`${API_BASE}/api/showcase/${username}`, {
      headers: getAuthHeaders(),
    });
    const json = await handleResponse(res);
    const showcase = normalizeShowcase(json);
    // return a uniform envelope so callers can always do result.showcase
    return { showcase };
  },

  /** Fetch own showcase with full edit metadata. */
  async getMine() {
    const res = await fetch(`${API_BASE}/api/showcase/mine`, {
      headers: getAuthHeaders(),
    });
    const json = await handleResponse(res);
    const showcase = normalizeShowcase(json);
    return { showcase };
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
    const json = await handleResponse(res);
    const showcase = normalizeShowcase(json);
    return { showcase };
  },
};
// TMDB API Service
// If you already have this file, you can skip this!

const TMDB_API_KEY = process.env.VUE_APP_TMDB_API_KEY || 'your_api_key_here';
const TMDB_BASE_URL = 'https://api.themoviedb.org/3';

export const tmdbAPI = {
  /**
   * Search for movies and TV shows
   */
  async searchMulti(query) {
    const response = await fetch(
      `${TMDB_BASE_URL}/search/multi?api_key=${TMDB_API_KEY}&query=${encodeURIComponent(query)}&page=1`
    );
    
    if (!response.ok) {
      throw new Error('TMDB search failed');
    }
    
    const data = await response.json();
    return data.results || [];
  },

  /**
   * Get movie details
   */
  async getMovieDetails(movieId) {
    const response = await fetch(
      `${TMDB_BASE_URL}/movie/${movieId}?api_key=${TMDB_API_KEY}&append_to_response=credits,videos`
    );
    
    if (!response.ok) {
      throw new Error('Failed to fetch movie details');
    }
    
    return await response.json();
  },

  /**
   * Get TV show details
   */
  async getTVDetails(tvId) {
    const response = await fetch(
      `${TMDB_BASE_URL}/tv/${tvId}?api_key=${TMDB_API_KEY}&append_to_response=credits,videos`
    );
    
    if (!response.ok) {
      throw new Error('Failed to fetch TV details');
    }
    
    return await response.json();
  },

  /**
   * Get trending content
   */
  async getTrending(mediaType = 'all', timeWindow = 'week') {
    const response = await fetch(
      `${TMDB_BASE_URL}/trending/${mediaType}/${timeWindow}?api_key=${TMDB_API_KEY}`
    );
    
    if (!response.ok) {
      throw new Error('Failed to fetch trending');
    }
    
    const data = await response.json();
    return data.results || [];
  }
};
// recommendations.js - Service for fetching recommendations from TMDB

const TMDB_API_KEY = process.env.VITE_TMDB_API_KEY;
const TMDB_BASE_URL = 'https://api.themoviedb.org/3';

export const recommendationsAPI = {
  /**
   * Get similar movies/TV shows for a specific media item
   */
  async getSimilar(tmdbId, mediaType) {
    const endpoint = mediaType === 'movie' 
      ? `${TMDB_BASE_URL}/movie/${tmdbId}/similar`
      : `${TMDB_BASE_URL}/tv/${tmdbId}/similar`;
    
    const response = await fetch(`${endpoint}?api_key=${TMDB_API_KEY}&page=1`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch similar content');
    }
    
    const data = await response.json();
    
    // Transform TMDB results to our format
    return data.results.slice(0, 12).map(item => ({
      tmdbId: item.id,
      title: item.title || item.name,
      mediaType: mediaType,
      posterUrl: item.poster_path 
        ? `https://image.tmdb.org/t/p/w500${item.poster_path}`
        : null,
      backdropUrl: item.backdrop_path
        ? `https://image.tmdb.org/t/p/original${item.backdrop_path}`
        : null,
      releaseYear: item.release_date 
        ? new Date(item.release_date).getFullYear()
        : (item.first_air_date ? new Date(item.first_air_date).getFullYear() : null),
      tmdbRating: item.vote_average,
      plot: item.overview,
    }));
  },

  /**
   * Get recommendations based on a genre
   */
  async getByGenre(genreId, mediaType, page = 1) {
    const endpoint = mediaType === 'movie'
      ? `${TMDB_BASE_URL}/discover/movie`
      : `${TMDB_BASE_URL}/discover/tv`;
    
    const response = await fetch(
      `${endpoint}?api_key=${TMDB_API_KEY}&with_genres=${genreId}&sort_by=vote_average.desc&vote_count.gte=100&page=${page}`
    );
    
    if (!response.ok) {
      throw new Error('Failed to fetch genre recommendations');
    }
    
    const data = await response.json();
    
    return data.results.slice(0, 20).map(item => ({
      tmdbId: item.id,
      title: item.title || item.name,
      mediaType: mediaType,
      posterUrl: item.poster_path 
        ? `https://image.tmdb.org/t/p/w500${item.poster_path}`
        : null,
      backdropUrl: item.backdrop_path
        ? `https://image.tmdb.org/t/p/original${item.backdrop_path}`
        : null,
      releaseYear: item.release_date 
        ? new Date(item.release_date).getFullYear()
        : (item.first_air_date ? new Date(item.first_air_date).getFullYear() : null),
      tmdbRating: item.vote_average,
      plot: item.overview,
    }));
  },

  /**
   * Get media by a specific actor
   */
  async getByActor(actorId, page = 1) {
    // Get actor's movie credits
    const movieResponse = await fetch(
      `${TMDB_BASE_URL}/person/${actorId}/movie_credits?api_key=${TMDB_API_KEY}`
    );
    
    const tvResponse = await fetch(
      `${TMDB_BASE_URL}/person/${actorId}/tv_credits?api_key=${TMDB_API_KEY}`
    );
    
    if (!movieResponse.ok || !tvResponse.ok) {
      throw new Error('Failed to fetch actor credits');
    }
    
    const movieData = await movieResponse.json();
    const tvData = await tvResponse.json();
    
    // Combine and sort by popularity
    const movies = movieData.cast.map(item => ({
      tmdbId: item.id,
      title: item.title,
      mediaType: 'movie',
      posterUrl: item.poster_path 
        ? `https://image.tmdb.org/t/p/w500${item.poster_path}`
        : null,
      releaseYear: item.release_date 
        ? new Date(item.release_date).getFullYear()
        : null,
      tmdbRating: item.vote_average,
      popularity: item.popularity,
    }));
    
    const tvShows = tvData.cast.map(item => ({
      tmdbId: item.id,
      title: item.name,
      mediaType: 'tv',
      posterUrl: item.poster_path 
        ? `https://image.tmdb.org/t/p/w500${item.poster_path}`
        : null,
      releaseYear: item.first_air_date 
        ? new Date(item.first_air_date).getFullYear()
        : null,
      tmdbRating: item.vote_average,
      popularity: item.popularity,
    }));
    
    // Combine and sort by popularity
    return [...movies, ...tvShows]
      .sort((a, b) => b.popularity - a.popularity)
      .slice(0, 20);
  },

  /**
   * Get trending content
   */
  async getTrending(mediaType = 'all', timeWindow = 'week') {
    const response = await fetch(
      `${TMDB_BASE_URL}/trending/${mediaType}/${timeWindow}?api_key=${TMDB_API_KEY}`
    );
    
    if (!response.ok) {
      throw new Error('Failed to fetch trending content');
    }
    
    const data = await response.json();
    
    return data.results.slice(0, 20).map(item => ({
      tmdbId: item.id,
      title: item.title || item.name,
      mediaType: item.media_type || mediaType,
      posterUrl: item.poster_path 
        ? `https://image.tmdb.org/t/p/w500${item.poster_path}`
        : null,
      backdropUrl: item.backdrop_path
        ? `https://image.tmdb.org/t/p/original${item.backdrop_path}`
        : null,
      releaseYear: item.release_date 
        ? new Date(item.release_date).getFullYear()
        : (item.first_air_date ? new Date(item.first_air_date).getFullYear() : null),
      tmdbRating: item.vote_average,
      plot: item.overview,
    }));
  },

  /**
   * Genre ID mapping (TMDB genre IDs)
   */
  genreMap: {
    // Movies
    'Action': 28,
    'Adventure': 12,
    'Animation': 16,
    'Comedy': 35,
    'Crime': 80,
    'Documentary': 99,
    'Drama': 18,
    'Family': 10751,
    'Fantasy': 14,
    'History': 36,
    'Horror': 27,
    'Music': 10402,
    'Mystery': 9648,
    'Romance': 10749,
    'Science Fiction': 878,
    'Thriller': 53,
    'War': 10752,
    'Western': 37,
    // TV
    'Action & Adventure': 10759,
    'Sci-Fi & Fantasy': 10765,
    'War & Politics': 10768,
  }
};
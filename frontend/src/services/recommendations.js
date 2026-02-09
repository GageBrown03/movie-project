// recommendations.js - Service for fetching recommendations from TMDB

// FIXED: Use process.env, and VUE_APP prefix for environment variables in Vue
const TMDB_API_KEY = process.env.VUE_APP_TMDB_API_KEY;
const TMDB_BASE_URL = 'https://api.themoviedb.org/3';

// Debug: Check if API key is loaded
if (!TMDB_API_KEY) {
  console.error('TMDB_API_KEY is not defined! Check your .env file.');
}

export const recommendationsAPI = {
  /**
   * Get similar movies/TV shows for a specific media item
   */
  async getSimilar(tmdbId, mediaType) {
    const endpoint = mediaType === 'movie' 
      ? `${TMDB_BASE_URL}/movie/${tmdbId}/similar`
      : `${TMDB_BASE_URL}/tv/${tmdbId}/similar`;
    
    const url = `${endpoint}?api_key=${TMDB_API_KEY}&page=1`;
    console.log('Fetching similar content:', url.replace(TMDB_API_KEY, 'API_KEY'));
    
    const response = await fetch(url);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('TMDB API Error:', response.status, errorText);
      throw new Error(`Failed to fetch similar content: ${response.status}`);
    }
    
    const data = await response.json();
    console.log('Similar content results:', data.results?.length || 0);
    
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
    
    const url = `${endpoint}?api_key=${TMDB_API_KEY}&with_genres=${genreId}&sort_by=vote_average.desc&vote_count.gte=100&page=${page}`;
    console.log('Fetching genre recommendations:', url.replace(TMDB_API_KEY, 'API_KEY'));
    
    const response = await fetch(url);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('TMDB API Error:', response.status, errorText);
      throw new Error(`Failed to fetch genre recommendations: ${response.status}`);
    }
    
    const data = await response.json();
    console.log('Genre recommendations results:', data.results?.length || 0);
    
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
    console.log('Fetching actor credits for:', actorId);
    
    // Get actor's movie credits
    const movieResponse = await fetch(
      `${TMDB_BASE_URL}/person/${actorId}/movie_credits?api_key=${TMDB_API_KEY}`
    );
    
    const tvResponse = await fetch(
      `${TMDB_BASE_URL}/person/${actorId}/tv_credits?api_key=${TMDB_API_KEY}`
    );
    
    if (!movieResponse.ok || !tvResponse.ok) {
      console.error('Actor credits error:', movieResponse.status, tvResponse.status);
      throw new Error('Failed to fetch actor credits');
    }
    
    const movieData = await movieResponse.json();
    const tvData = await tvResponse.json();
    
    console.log('Actor credits:', {
      movies: movieData.cast?.length || 0,
      tv: tvData.cast?.length || 0
    });
    
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
    const url = `${TMDB_BASE_URL}/trending/${mediaType}/${timeWindow}?api_key=${TMDB_API_KEY}`;
    console.log('Fetching trending:', url.replace(TMDB_API_KEY, 'API_KEY'));
    
    const response = await fetch(url);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('TMDB API Error:', response.status, errorText);
      throw new Error(`Failed to fetch trending content: ${response.status}`);
    }
    
    const data = await response.json();
    console.log('Trending results:', data.results?.length || 0);
    
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
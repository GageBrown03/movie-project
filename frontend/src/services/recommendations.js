// recommendations.js - IMPROVED with franchise/collection support

const TMDB_API_KEY = process.env.VUE_APP_TMDB_API_KEY;
const TMDB_BASE_URL = 'https://api.themoviedb.org/3';

if (!TMDB_API_KEY) {
  console.error('TMDB_API_KEY is not defined! Check your .env file.');
}

export const recommendationsAPI = {
  /**
   * NEW: Get comprehensive related content (collections, sequels, spinoffs, similar)
   * This is the main method to use for "Similar Content"
   */
  async getRelatedContent(tmdbId, mediaType) {
    console.log('🔍 Fetching comprehensive related content for:', tmdbId, mediaType);
    
    const results = {
      collection: [],      // Movies in same franchise (e.g., Avengers series)
      similar: [],         // TMDB similar algorithm
      recommendations: [], // TMDB recommendations algorithm
      spinoffs: []        // Related TV shows for movies, or vice versa
    };

    try {
      // 1. Get full media details (includes belongs_to_collection for movies)
      const details = await this.getMediaDetails(tmdbId, mediaType);
      
      // 2. If movie belongs to a collection, get all movies in that collection
      if (mediaType === 'movie' && details.belongs_to_collection) {
        results.collection = await this.getCollection(details.belongs_to_collection.id);
        console.log('✅ Found collection:', details.belongs_to_collection.name, results.collection.length);
      }

      // 3. Get TMDB similar content
      const similar = await this.getSimilar(tmdbId, mediaType);
      results.similar = similar;
      console.log('✅ Found similar:', results.similar.length);

      // 4. Get TMDB recommendations (different algorithm than similar)
      const recommendations = await this.getRecommendations(tmdbId, mediaType);
      results.recommendations = recommendations;
      console.log('✅ Found recommendations:', results.recommendations.length);

      // 5. Check for spinoffs (if movie, find related TV; if TV, find related movies)
      if (details.keywords?.length > 0) {
        results.spinoffs = await this.getSpinoffs(details.keywords, mediaType);
        console.log('✅ Found spinoffs:', results.spinoffs.length);
      }

      // Combine and deduplicate all results
      const combined = this.combineAndDeduplicate(results, tmdbId);
      console.log('🎬 Total related content found:', combined.length);
      
      return combined;

    } catch (err) {
      console.error('Error fetching related content:', err);
      // Fallback to just similar if comprehensive search fails
      return await this.getSimilar(tmdbId, mediaType);
    }
  },

  /**
   * NEW: Get full media details including collections and keywords
   */
  async getMediaDetails(tmdbId, mediaType) {
    const endpoint = mediaType === 'movie' 
      ? `${TMDB_BASE_URL}/movie/${tmdbId}`
      : `${TMDB_BASE_URL}/tv/${tmdbId}`;
    
    const url = `${endpoint}?api_key=${TMDB_API_KEY}&append_to_response=keywords`;
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch media details: ${response.status}`);
    }
    
    const data = await response.json();
    
    // Extract keywords for spinoff detection
    const keywords = mediaType === 'movie' 
      ? data.keywords?.keywords || []
      : data.keywords?.results || [];
    
    return {
      ...data,
      keywords: keywords.map(k => k.name)
    };
  },

  /**
   * NEW: Get all movies in a collection (franchise)
   */
  async getCollection(collectionId) {
    const url = `${TMDB_BASE_URL}/collection/${collectionId}?api_key=${TMDB_API_KEY}`;
    console.log('Fetching collection:', collectionId);
    
    const response = await fetch(url);
    
    if (!response.ok) {
      console.error('Collection fetch error:', response.status);
      return [];
    }
    
    const data = await response.json();
    
    return (data.parts || [])
      .filter(item => item.poster_path)
      .map(item => ({
        tmdbId: item.id,
        title: item.title,
        mediaType: 'movie',
        posterUrl: `https://image.tmdb.org/t/p/w500${item.poster_path}`,
        backdropUrl: item.backdrop_path
          ? `https://image.tmdb.org/t/p/original${item.backdrop_path}`
          : null,
        releaseYear: item.release_date 
          ? new Date(item.release_date).getFullYear()
          : null,
        tmdbRating: item.vote_average,
        plot: item.overview,
        relationType: 'collection' // Tag for UI
      }));
  },

  /**
   * NEW: Get TMDB recommendations (different algorithm than similar)
   */
  async getRecommendations(tmdbId, mediaType) {
    const endpoint = mediaType === 'movie' 
      ? `${TMDB_BASE_URL}/movie/${tmdbId}/recommendations`
      : `${TMDB_BASE_URL}/tv/${tmdbId}/recommendations`;
    
    const url = `${endpoint}?api_key=${TMDB_API_KEY}&page=1`;
    
    const response = await fetch(url);
    
    if (!response.ok) {
      return [];
    }
    
    const data = await response.json();
    
    return (data.results || [])
      .filter(item => item.poster_path)
      .slice(0, 12)
      .map(item => ({
        tmdbId: item.id,
        title: item.title || item.name,
        mediaType: mediaType,
        posterUrl: `https://image.tmdb.org/t/p/w500${item.poster_path}`,
        backdropUrl: item.backdrop_path
          ? `https://image.tmdb.org/t/p/original${item.backdrop_path}`
          : null,
        releaseYear: item.release_date 
          ? new Date(item.release_date).getFullYear()
          : (item.first_air_date ? new Date(item.first_air_date).getFullYear() : null),
        tmdbRating: item.vote_average,
        plot: item.overview,
        relationType: 'recommended'
      }));
  },

  /**
   * NEW: Find spinoffs (TV shows for movies, or movies for TV shows)
   * Uses keywords to find related content in opposite media type
   */
  async getSpinoffs(keywords, originalMediaType) {
    if (keywords.length === 0) return [];
    
    // Use first 2-3 most relevant keywords
    const topKeywords = keywords.slice(0, 3);
    const oppositeType = originalMediaType === 'movie' ? 'tv' : 'movie';
    
    const endpoint = oppositeType === 'movie'
      ? `${TMDB_BASE_URL}/discover/movie`
      : `${TMDB_BASE_URL}/discover/tv`;
    
    // Search using keywords (this finds related content in opposite media type)
    const url = `${endpoint}?api_key=${TMDB_API_KEY}&sort_by=popularity.desc&vote_count.gte=100&with_keywords=${topKeywords.join(',')}`;
    
    const response = await fetch(url);
    
    if (!response.ok) {
      return [];
    }
    
    const data = await response.json();
    
    return (data.results || [])
      .filter(item => item.poster_path)
      .slice(0, 6)
      .map(item => ({
        tmdbId: item.id,
        title: item.title || item.name,
        mediaType: oppositeType,
        posterUrl: `https://image.tmdb.org/t/p/w500${item.poster_path}`,
        backdropUrl: item.backdrop_path
          ? `https://image.tmdb.org/t/p/original${item.backdrop_path}`
          : null,
        releaseYear: item.release_date 
          ? new Date(item.release_date).getFullYear()
          : (item.first_air_date ? new Date(item.first_air_date).getFullYear() : null),
        tmdbRating: item.vote_average,
        plot: item.overview,
        relationType: 'spinoff'
      }));
  },

  /**
   * NEW: Combine and deduplicate results from all sources
   * Priority: Collection > Recommendations > Similar > Spinoffs
   */
  combineAndDeduplicate(results, excludeTmdbId) {
    const seen = new Set([excludeTmdbId]); // Exclude the current media
    const combined = [];

    // Priority order: collection first (most relevant)
    const sources = [
      { items: results.collection, label: 'In Series' },
      { items: results.recommendations, label: 'Recommended' },
      { items: results.similar, label: 'Similar' },
      { items: results.spinoffs, label: 'Related' }
    ];

    sources.forEach(source => {
      source.items.forEach(item => {
        const key = `${item.mediaType}-${item.tmdbId}`;
        if (!seen.has(key)) {
          seen.add(key);
          combined.push({
            ...item,
            relationLabel: source.label // Add label for UI grouping
          });
        }
      });
    });

    return combined.slice(0, 20); // Max 20 items
  },

  /**
   * EXISTING: Get similar movies/TV shows (now used as part of comprehensive search)
   */
  async getSimilar(tmdbId, mediaType) {
    const endpoint = mediaType === 'movie' 
      ? `${TMDB_BASE_URL}/movie/${tmdbId}/similar`
      : `${TMDB_BASE_URL}/tv/${tmdbId}/similar`;
    
    const url = `${endpoint}?api_key=${TMDB_API_KEY}&page=1`;
    
    const response = await fetch(url);
    
    if (!response.ok) {
      return [];
    }
    
    const data = await response.json();
    
    return (data.results || [])
      .filter(item => item.poster_path)
      .slice(0, 12)
      .map(item => ({
        tmdbId: item.id,
        title: item.title || item.name,
        mediaType: mediaType,
        posterUrl: `https://image.tmdb.org/t/p/w500${item.poster_path}`,
        backdropUrl: item.backdrop_path
          ? `https://image.tmdb.org/t/p/original${item.backdrop_path}`
          : null,
        releaseYear: item.release_date 
          ? new Date(item.release_date).getFullYear()
          : (item.first_air_date ? new Date(item.first_air_date).getFullYear() : null),
        tmdbRating: item.vote_average,
        plot: item.overview,
        relationType: 'similar'
      }));
  },

  // EXISTING METHODS - Keep unchanged
  async getByGenre(genreId, mediaType, page = 1) {
    const endpoint = mediaType === 'movie'
      ? `${TMDB_BASE_URL}/discover/movie`
      : `${TMDB_BASE_URL}/discover/tv`;
    
    const url = `${endpoint}?api_key=${TMDB_API_KEY}&with_genres=${genreId}&sort_by=popularity.desc&vote_count.gte=500&vote_average.gte=6.5&page=${page}`;
    
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch genre recommendations: ${response.status}`);
    }
    
    const data = await response.json();
    
    return (data.results || [])
      .filter(item => item.poster_path && item.vote_average >= 6.5)
      .slice(0, 20)
      .map(item => ({
        tmdbId: item.id,
        title: item.title || item.name,
        mediaType: mediaType,
        posterUrl: `https://image.tmdb.org/t/p/w500${item.poster_path}`,
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

  async getByActor(actorId) {
    const [movieResponse, tvResponse] = await Promise.all([
      fetch(`${TMDB_BASE_URL}/person/${actorId}/movie_credits?api_key=${TMDB_API_KEY}`),
      fetch(`${TMDB_BASE_URL}/person/${actorId}/tv_credits?api_key=${TMDB_API_KEY}`),
    ]);

    if (!movieResponse.ok || !tvResponse.ok) {
      throw new Error('Failed to fetch actor credits');
    }

    const [movieData, tvData] = await Promise.all([
      movieResponse.json(),
      tvResponse.json(),
    ]);

    // ── Movies ──────────────────────────────────────────────────────────────
    // Filter for quality content and significant roles
    const movies = (movieData.cast || [])
      .filter(item =>
        item.poster_path &&
        (item.vote_count || 0) >= 100 &&    // More votes = better filtering
        (item.vote_average || 0) >= 6.5 &&  // Higher rating threshold
        !item.adult
      )
      .map(item => ({
        tmdbId: item.id,
        title: item.title,
        mediaType: 'movie',
        posterUrl: `https://image.tmdb.org/t/p/w500${item.poster_path}`,
        releaseYear: item.release_date ? new Date(item.release_date).getFullYear() : null,
        tmdbRating: item.vote_average || 0,
        voteCount: item.vote_count || 0,
        popularity: item.popularity || 0,
      }));

    // ── TV shows ─────────────────────────────────────────────────────────────
    // More stringent filtering for TV shows
    const tvShows = (tvData.cast || [])
      .filter(item =>
        item.poster_path &&
        (item.vote_count || 0) >= 100 &&
        (item.vote_average || 0) >= 6.5 &&  // Higher rating threshold
        (item.episode_count || 0) >= 5      // Must be more than guest appearance
      )
      .map(item => ({
        tmdbId: item.id,
        title: item.name,
        mediaType: 'tv',
        posterUrl: `https://image.tmdb.org/t/p/w500${item.poster_path}`,
        releaseYear: item.first_air_date ? new Date(item.first_air_date).getFullYear() : null,
        tmdbRating: item.vote_average || 0,
        voteCount: item.vote_count || 0,
        popularity: item.popularity || 0,
        episodeCount: item.episode_count || 0,
      }));

    // ── Enhanced Quality Scoring ─────────────────────────────────────────────
    const all = [...movies, ...tvShows];
    if (all.length === 0) return [];

    // Normalize popularity and vote count for better scoring
    const maxPop = Math.max(...all.map(i => i.popularity), 1);
    const maxVotes = Math.max(...all.map(i => i.voteCount), 1);

    const scored = all.map(item => {
      // Rating weight: 40%
      const ratingScore = (item.tmdbRating / 10) * 0.4;
      
      // Vote count (reliability): 30%
      const voteScore = (Math.log1p(item.voteCount) / Math.log1p(maxVotes)) * 0.3;
      
      // Popularity (cultural impact): 30%
      const popScore = (Math.log1p(item.popularity) / Math.log1p(maxPop)) * 0.3;
      
      return {
        ...item,
        _score: ratingScore + voteScore + popScore
      };
    });

    return scored
      .sort((a, b) => b._score - a._score)
      .slice(0, 30)   // Return more results for better filtering
      .map(({ _score, ...item }) => item);
  },

  async getTrending(mediaType = 'all', timeWindow = 'week') {
    const url = `${TMDB_BASE_URL}/trending/${mediaType}/${timeWindow}?api_key=${TMDB_API_KEY}`;
    
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch trending content: ${response.status}`);
    }
    
    const data = await response.json();
    
    return (data.results || [])
      .filter(item => item.poster_path)
      .slice(0, 20)
      .map(item => ({
        tmdbId: item.id,
        title: item.title || item.name,
        mediaType: item.media_type || mediaType,
        posterUrl: `https://image.tmdb.org/t/p/w500${item.poster_path}`,
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

  genreMap: {
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
    'Action & Adventure': 10759,
    'Sci-Fi & Fantasy': 10765,
    'War & Politics': 10768,
  }
};
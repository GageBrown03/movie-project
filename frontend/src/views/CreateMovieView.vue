<template>
  <div class="create-movie">
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4">Add a Movie</h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Search for a movie to automatically fetch details
        </p>
      </v-col>
    </v-row>

    <!-- Step 1: Search TMDB -->
    <v-card v-if="!selectedMovie" class="mb-6" elevation="2">
      <v-card-title>Search for Movie</v-card-title>
      <v-card-text>
        <v-text-field
          v-model="searchQuery"
          label="Movie title..."
          prepend-inner-icon="mdi-magnify"
          variant="outlined"
          @keyup.enter="searchTMDB"
          :loading="searching"
          clearable
        />
        <v-btn
          color="primary"
          @click="searchTMDB"
          :loading="searching"
          :disabled="!searchQuery"
          class="mt-2"
        >
          Search
        </v-btn>
        <v-btn
          variant="text"
          @click="skipSearch"
          class="mt-2 ml-2"
        >
          Enter Manually
        </v-btn>
      </v-card-text>
    </v-card>

    <!-- Search Results -->
    <v-card v-if="searchResults.length > 0 && !selectedMovie" class="mb-6">
      <v-card-title>Search Results</v-card-title>
      <v-list lines="two">
        <v-list-item
          v-for="result in searchResults"
          :key="result.tmdbId"
          @click="selectMovie(result)"
          link
        >
          <template v-slot:prepend>
            <v-avatar size="80" rounded class="mr-4">
              <v-img v-if="result.posterUrl" :src="result.posterUrl" cover />
              <v-icon v-else size="40">mdi-movie-outline</v-icon>
            </v-avatar>
          </template>

          <v-list-item-title>
            {{ result.title }} 
            <span v-if="result.releaseYear" class="text-medium-emphasis">
              ({{ result.releaseYear }})
            </span>
          </v-list-item-title>

          <v-list-item-subtitle>
            {{ truncate(result.plot, 120) }}
          </v-list-item-subtitle>

          <template v-slot:append>
            <v-chip v-if="result.tmdbRating" size="small">
              <v-icon start size="small">mdi-star</v-icon>
              {{ result.tmdbRating.toFixed(1) }}
            </v-chip>
          </template>
        </v-list-item>
      </v-list>
    </v-card>

    <!-- Step 2: Rate the Movie -->
    <v-card v-if="selectedMovie" class="mb-6" elevation="3">
      <v-row no-gutters>
        <!-- Movie Poster -->
        <v-col cols="12" md="4">
          <div class="poster-preview">
            <v-img
              v-if="selectedMovie.posterUrl"
              :src="selectedMovie.posterUrl"
              aspect-ratio="2/3"
              cover
            />
            <div v-else class="poster-placeholder">
              <v-icon size="64">mdi-movie-outline</v-icon>
            </div>
          </div>
        </v-col>

        <!-- Movie Details & Rating -->
        <v-col cols="12" md="8">
          <v-card-text>
            <h2 class="text-h5 mb-2">{{ selectedMovie.title }}</h2>
            
            <div class="mb-4">
              <v-chip v-if="selectedMovie.releaseYear" size="small" class="mr-2">
                {{ selectedMovie.releaseYear }}
              </v-chip>
              <v-chip v-if="selectedMovie.runtime" size="small" class="mr-2">
                {{ selectedMovie.runtime }} min
              </v-chip>
              <v-chip v-if="selectedMovie.tmdbRating" size="small">
                <v-icon start size="small">mdi-star</v-icon>
                {{ selectedMovie.tmdbRating.toFixed(1) }} TMDB
              </v-chip>
            </div>

            <p v-if="selectedMovie.director" class="text-subtitle-1 mb-2">
              <strong>Director:</strong> {{ selectedMovie.director }}
            </p>

            <p v-if="selectedMovie.genres" class="text-subtitle-2 mb-3">
              {{ selectedMovie.genres }}
            </p>

            <p v-if="selectedMovie.plot" class="text-body-2 mb-4">
              {{ selectedMovie.plot }}
            </p>

            <!-- Your Rating -->
            <v-divider class="my-4" />
            <h3 class="text-h6 mb-3">Your Rating</h3>
            
            <v-rating
              v-model="userRating"
              color="primary"
              size="large"
              hover
            />
            
            <p class="text-caption mt-2">
              {{ userRating ? `${userRating} out of 5 stars` : 'Tap to rate' }}
            </p>

            <!-- Optional: Personal Notes -->
            <v-textarea
              v-model="userNotes"
              label="Personal notes (optional)"
              variant="outlined"
              rows="3"
              class="mt-4"
              placeholder="What did you think?"
            />

            <!-- Actions -->
            <v-card-actions class="px-0">
              <v-btn
                variant="text"
                @click="clearSelection"
              >
                Back to Search
              </v-btn>
              <v-spacer />
              <v-btn
                color="primary"
                size="large"
                @click="saveMovie"
                :loading="saving"
                :disabled="!userRating"
              >
                Add to Collection
              </v-btn>
            </v-card-actions>
          </v-card-text>
        </v-col>
      </v-row>
    </v-card>

    <!-- Manual Entry Form (fallback) -->
    <v-card v-if="manualEntry && !selectedMovie" class="mb-6">
      <v-card-title>Manual Entry</v-card-title>
      <v-card-text>
        <v-text-field
          v-model="manualTitle"
          label="Movie Title"
          variant="outlined"
          required
        />
        <v-text-field
          v-model="manualDirector"
          label="Director (optional)"
          variant="outlined"
        />
        <v-rating
          v-model="userRating"
          label="Your Rating"
          color="primary"
          size="large"
          hover
        />
        <v-textarea
          v-model="userNotes"
          label="Notes (optional)"
          variant="outlined"
          rows="3"
          class="mt-4"
        />
        <v-btn
          color="primary"
          @click="saveManualMovie"
          :loading="saving"
          :disabled="!manualTitle || !userRating"
        >
          Add Movie
        </v-btn>
        <v-btn
          variant="text"
          @click="manualEntry = false"
          class="ml-2"
        >
          Back to Search
        </v-btn>
      </v-card-text>
    </v-card>

    <!-- Error Display -->
    <v-alert v-if="error" type="error" class="mb-4" closable @click:close="error = null">
      {{ error }}
    </v-alert>
  </div>
</template>

<script>
import { tmdbAPI, movieAPI } from '@/services/api-production';

export default {
  name: 'CreateMovieView',
  
  data() {
    return {
      // Search state
      searchQuery: '',
      searching: false,
      searchResults: [],
      
      // Selected movie from TMDB
      selectedMovie: null,
      
      // User input
      userRating: null,
      userNotes: '',
      
      // Manual entry
      manualEntry: false,
      manualTitle: '',
      manualDirector: '',
      
      // UI state
      saving: false,
      error: null,
    };
  },
  
  methods: {
    async searchTMDB() {
      if (!this.searchQuery.trim()) return;
      
      this.searching = true;
      this.error = null;
      this.searchResults = [];
      
      try {
        this.searchResults = await tmdbAPI.search(this.searchQuery);
        
        if (this.searchResults.length === 0) {
          this.error = 'No results found. Try a different search or enter manually.';
        }
      } catch (err) {
        console.error('Search error:', err);
        this.error = 'Search failed. You can enter the movie manually instead.';
      } finally {
        this.searching = false;
      }
    },
    
    async selectMovie(result) {
      // Fetch full details for selected movie
      try {
        const details = await tmdbAPI.getMovieDetails(result.tmdbId);
        this.selectedMovie = details;
      } catch (err) {
        console.error('Error fetching details:', err);
        // Fall back to search result if details fail
        this.selectedMovie = result;
      }
    },
    
    async saveMovie() {
      if (!this.userRating) {
        this.error = 'Please add your rating';
        return;
      }
      
      this.saving = true;
      this.error = null;
      
      try {
        const movieData = {
          title: this.selectedMovie.title,
          rating: this.userRating,
          director: this.selectedMovie.director,
          release_year: this.selectedMovie.releaseYear,
          runtime: this.selectedMovie.runtime,
          plot: this.selectedMovie.plot,
          genres: this.selectedMovie.genres,
          tmdb_id: this.selectedMovie.tmdbId,
          poster_url: this.selectedMovie.posterUrl,
          backdrop_url: this.selectedMovie.backdropUrl,
          tmdb_rating: this.selectedMovie.tmdbRating,
          imdb_rating: this.selectedMovie.imdbRating,
          notes: this.userNotes || null,
        };
        
        const created = await movieAPI.create(movieData);
        
        // Redirect to movie detail or list
        this.$router.push(`/movies/${created.movieId}`);
        
      } catch (err) {
        console.error('Save error:', err);
        this.error = 'Failed to save movie. Please try again.';
      } finally {
        this.saving = false;
      }
    },
    
    async saveManualMovie() {
      if (!this.manualTitle || !this.userRating) {
        this.error = 'Title and rating are required';
        return;
      }
      
      this.saving = true;
      this.error = null;
      
      try {
        const movieData = {
          title: this.manualTitle,
          director: this.manualDirector || null,
          rating: this.userRating,
          notes: this.userNotes || null,
        };
        
        const created = await movieAPI.create(movieData);
        this.$router.push(`/movies/${created.movieId}`);
        
      } catch (err) {
        console.error('Save error:', err);
        this.error = 'Failed to save movie. Please try again.';
      } finally {
        this.saving = false;
      }
    },
    
    clearSelection() {
      this.selectedMovie = null;
      this.userRating = null;
      this.userNotes = '';
    },
    
    skipSearch() {
      this.manualEntry = true;
      this.searchResults = [];
    },
    
    truncate(text, length) {
      if (!text) return '';
      return text.length > length ? text.substring(0, length) + '...' : text;
    }
  }
};
</script>

<style scoped>
.create-movie {
  max-width: 900px;
  margin: 0 auto;
}

.poster-preview {
  height: 100%;
  min-height: 400px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.poster-placeholder {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

@media (max-width: 960px) {
  .poster-preview {
    min-height: 300px;
  }
}
</style>
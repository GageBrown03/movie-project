<template>
  <div class="create-media">
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4">Add Movie or TV Show</h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Search to automatically fetch details
        </p>
      </v-col>
    </v-row>

    <!-- Step 1: Search TMDB -->
    <v-card v-if="!selectedMedia" class="mb-6" elevation="2">
      <v-card-title>Search for Movie or TV Show</v-card-title>
      <v-card-text>
        <v-text-field
          v-model="searchQuery"
          label="Title..."
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
    <v-card v-if="searchResults.length > 0 && !selectedMedia" class="mb-6">
      <v-card-title>Search Results</v-card-title>
      <v-list lines="two">
        <v-list-item
          v-for="result in searchResults"
          :key="`${result.mediaType}-${result.tmdbId}`"
          @click="selectMedia(result)"
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
            <v-chip size="x-small" :color="result.mediaType === 'movie' ? 'primary' : 'secondary'" class="ml-2">
              {{ result.mediaType === 'movie' ? 'MOVIE' : 'TV' }}
            </v-chip>
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

    <!-- Step 2: Choose Action (Watchlist vs Watched) -->
    <v-card v-if="selectedMedia" class="mb-6" elevation="3">
      <v-row no-gutters>
        <!-- Poster -->
        <v-col cols="12" md="4">
          <div class="poster-preview">
            <v-img
              v-if="selectedMedia.posterUrl"
              :src="selectedMedia.posterUrl"
              aspect-ratio="2/3"
              cover
            />
            <div v-else class="poster-placeholder">
              <v-icon size="64">mdi-movie-outline</v-icon>
            </div>
          </div>
        </v-col>

        <!-- Details & Action Choice -->
        <v-col cols="12" md="8">
          <v-card-text>
            <v-chip :color="selectedMedia.mediaType === 'movie' ? 'primary' : 'secondary'" size="small" class="mb-2">
              {{ selectedMedia.mediaType === 'movie' ? 'MOVIE' : 'TV SHOW' }}
            </v-chip>
            <h2 class="text-h5 mb-2">{{ selectedMedia.title }}</h2>
            
            <div class="mb-4">
              <v-chip v-if="selectedMedia.releaseYear" size="small" class="mr-2">
                {{ selectedMedia.releaseYear }}
              </v-chip>
              <v-chip v-if="selectedMedia.runtime" size="small" class="mr-2">
                {{ selectedMedia.runtime }} min
              </v-chip>
              <v-chip v-if="selectedMedia.numberOfSeasons" size="small" class="mr-2">
                {{ selectedMedia.numberOfSeasons }} {{ selectedMedia.numberOfSeasons === 1 ? 'Season' : 'Seasons' }}
              </v-chip>
              <v-chip v-if="selectedMedia.tmdbRating" size="small">
                <v-icon start size="small">mdi-star</v-icon>
                {{ selectedMedia.tmdbRating.toFixed(1) }} TMDB
              </v-chip>
            </div>

            <p v-if="selectedMedia.director" class="text-subtitle-1 mb-2">
              <strong>{{ selectedMedia.mediaType === 'tv' ? 'Created by' : 'Director' }}:</strong> {{ selectedMedia.director }}
            </p>

            <p v-if="selectedMedia.genres" class="text-subtitle-2 mb-3">
              {{ selectedMedia.genres }}
            </p>

            <p v-if="selectedMedia.plot" class="text-body-2 mb-4">
              {{ selectedMedia.plot }}
            </p>

            <!-- Action Choice: Watchlist or Watched -->
            <v-divider class="my-4" />
            <h3 class="text-h6 mb-3">What would you like to do?</h3>
            
            <!-- Two-Button Flow -->
            <v-row>
              <!-- Option 1: Add to Watchlist -->
              <v-col cols="12" sm="6">
                <v-card variant="outlined" class="pa-4 text-center" hover @click="addToWatchlist">
                  <v-icon size="48" color="secondary" class="mb-2">mdi-bookmark-plus-outline</v-icon>
                  <h4 class="text-h6 mb-1">Add to Watchlist</h4>
                  <p class="text-caption">Plan to watch later</p>
                </v-card>
              </v-col>

              <!-- Option 2: I've Watched This -->
              <v-col cols="12" sm="6">
                <v-card variant="outlined" class="pa-4 text-center" hover @click="showRatingDialog = true">
                  <v-icon size="48" color="primary" class="mb-2">mdi-check-circle-outline</v-icon>
                  <h4 class="text-h6 mb-1">I've Watched This</h4>
                  <p class="text-caption">Rate it now</p>
                </v-card>
              </v-col>
            </v-row>

            <v-btn
              variant="text"
              @click="clearSelection"
              class="mt-4"
            >
              Back to Search
            </v-btn>
          </v-card-text>
        </v-col>
      </v-row>
    </v-card>

    <!-- Rating Dialog (for "I've Watched This") -->
    <v-dialog v-model="showRatingDialog" max-width="500">
      <v-card>
        <v-card-title>Rate {{ selectedMedia?.title }}</v-card-title>
        <v-card-text>
          <v-rating
            v-model="userRating"
            color="primary"
            size="large"
            hover
          />
          <p class="text-caption mt-2">
            {{ userRating ? `${userRating} out of 5 stars` : 'Tap to rate' }}
          </p>

          <v-textarea
            v-model="userNotes"
            label="Personal notes (optional)"
            variant="outlined"
            rows="3"
            class="mt-4"
            placeholder="What did you think?"
          />

          <!-- TV-specific: Seasons watched -->
          <v-text-field
            v-if="selectedMedia?.mediaType === 'tv' && selectedMedia?.numberOfSeasons"
            v-model.number="seasonsWatched"
            label="Seasons watched (optional)"
            type="number"
            variant="outlined"
            :hint="`Total: ${selectedMedia.numberOfSeasons} seasons`"
            persistent-hint
            :max="selectedMedia.numberOfSeasons"
            min="1"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="showRatingDialog = false">Cancel</v-btn>
          <v-btn
            color="primary"
            @click="saveAsWatched"
            :loading="saving"
            :disabled="!userRating"
          >
            Add to Collection
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Manual Entry Form -->
    <v-card v-if="manualEntry && !selectedMedia" class="mb-6">
      <v-card-title>Manual Entry</v-card-title>
      <v-card-text>
        <v-select
          v-model="manualType"
          :items="[{title: 'Movie', value: 'movie'}, {title: 'TV Show', value: 'tv'}]"
          label="Type"
          variant="outlined"
          required
        />
        <v-text-field
          v-model="manualTitle"
          label="Title"
          variant="outlined"
          required
        />
        <v-text-field
          v-model="manualDirector"
          :label="manualType === 'tv' ? 'Creator(s)' : 'Director'"
          variant="outlined"
        />
        
        <v-divider class="my-4" />
        <h4 class="text-subtitle-1 mb-2">Status</h4>
        <v-radio-group v-model="manualStatus">
          <v-radio label="Add to Watchlist" value="want_to_watch" />
          <v-radio label="I've Watched This" value="watched" />
        </v-radio-group>

        <v-rating
          v-if="manualStatus === 'watched'"
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
          @click="saveManualMedia"
          :loading="saving"
          :disabled="!manualTitle || (manualStatus === 'watched' && !userRating)"
        >
          Add {{ manualType === 'movie' ? 'Movie' : 'TV Show' }}
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
import { tmdbAPI, mediaAPI } from '@/services/api-production';

export default {
  name: 'CreateMediaView',
  
  data() {
    return {
      // Search state
      searchQuery: '',
      searching: false,
      searchResults: [],
      
      // Selected media from TMDB
      selectedMedia: null,
      
      // Rating dialog
      showRatingDialog: false,
      userRating: null,
      userNotes: '',
      seasonsWatched: null,
      
      // Manual entry
      manualEntry: false,
      manualTitle: '',
      manualDirector: '',
      manualType: 'movie',
      manualStatus: 'watched',
      
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
        this.error = 'Search failed. You can enter the media manually instead.';
      } finally {
        this.searching = false;
      }
    },
    
    async selectMedia(result) {
      // Fetch full details based on type
      try {
        if (result.mediaType === 'movie') {
          this.selectedMedia = await tmdbAPI.getMovieDetails(result.tmdbId);
        } else {
          this.selectedMedia = await tmdbAPI.getTVDetails(result.tmdbId);
        }
      } catch (err) {
        console.error('Error fetching details:', err);
        this.selectedMedia = result; // Fall back to search result
      }
    },
    
    async addToWatchlist() {
      this.saving = true;
      this.error = null;
      
      try {
        const mediaData = {
          title: this.selectedMedia.title,
          media_type: this.selectedMedia.mediaType,
          status: 'want_to_watch',
          // No rating for watchlist items
          ...this.buildMediaData()
        };
        
        const created = await mediaAPI.create(mediaData);
        this.$router.push('/movies'); // Redirect to media list
        
      } catch (err) {
        console.error('Save error:', err);
        this.error = 'Failed to add to watchlist. Please try again.';
      } finally {
        this.saving = false;
      }
    },
    
    async saveAsWatched() {
      if (!this.userRating) {
        this.error = 'Please add your rating';
        return;
      }
      
      this.saving = true;
      this.error = null;
      
      try {
        const mediaData = {
          title: this.selectedMedia.title,
          media_type: this.selectedMedia.mediaType,
          status: 'watched',
          rating: this.userRating,
          notes: this.userNotes || null,
          ...this.buildMediaData()
        };
        
        // Add TV-specific fields
        if (this.selectedMedia.mediaType === 'tv' && this.seasonsWatched) {
          mediaData.seasons_watched = this.seasonsWatched;
        }
        
        const created = await mediaAPI.create(mediaData);
        this.$router.push(`/movies/${created.mediaId}`);
        
      } catch (err) {
        console.error('Save error:', err);
        this.error = 'Failed to save. Please try again.';
      } finally {
        this.saving = false;
      }
    },
    
    buildMediaData() {
      // Common fields for both movies and TV
      const data = {
        tmdb_id: this.selectedMedia.tmdbId,
        release_year: this.selectedMedia.releaseYear,
        plot: this.selectedMedia.plot,
        genres: this.selectedMedia.genres,
        poster_url: this.selectedMedia.posterUrl,
        backdrop_url: this.selectedMedia.backdropUrl,
        tmdb_rating: this.selectedMedia.tmdbRating,
        imdb_rating: this.selectedMedia.imdbRating,
        cast: this.selectedMedia.cast || [],
      };
      
      // Movie-specific
      if (this.selectedMedia.mediaType === 'movie') {
        data.director = this.selectedMedia.director;
        data.runtime = this.selectedMedia.runtime;
      }
      
      // TV-specific
      if (this.selectedMedia.mediaType === 'tv') {
        data.director = this.selectedMedia.director; // Creators
        data.number_of_seasons = this.selectedMedia.numberOfSeasons;
        data.number_of_episodes = this.selectedMedia.numberOfEpisodes;
        data.show_status = this.selectedMedia.showStatus;
      }
      
      return data;
    },
    
    async saveManualMedia() {
      if (!this.manualTitle || (this.manualStatus === 'watched' && !this.userRating)) {
        this.error = 'Title and rating (if watched) are required';
        return;
      }
      
      this.saving = true;
      this.error = null;
      
      try {
        const mediaData = {
          title: this.manualTitle,
          media_type: this.manualType,
          director: this.manualDirector || null,
          status: this.manualStatus,
          rating: this.manualStatus === 'watched' ? this.userRating : null,
          notes: this.userNotes || null,
        };
        
        const created = await mediaAPI.create(mediaData);
        this.$router.push(`/movies/${created.mediaId}`);
        
      } catch (err) {
        console.error('Save error:', err);
        this.error = 'Failed to save. Please try again.';
      } finally {
        this.saving = false;
      }
    },
    
    clearSelection() {
      this.selectedMedia = null;
      this.userRating = null;
      this.userNotes = '';
      this.showRatingDialog = false;
      this.seasonsWatched = null;
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
.create-media {
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
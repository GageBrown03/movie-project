<template>
  <div class="edit-media">
    <v-row class="mb-4 align-center">
      <v-col>
        <h1 class="text-h4">Edit {{ media?.mediaType === 'tv' ? 'TV Show' : 'Movie' }}</h1>
      </v-col>
      <v-col cols="auto">
        <v-btn
          variant="text"
          @click="$router.push(`/movies/${mediaId}`)"
          prepend-icon="mdi-arrow-left"
        >
          Back
        </v-btn>
      </v-col>
    </v-row>

    <!-- Loading State -->
    <v-row v-if="loading" justify="center" class="my-12">
      <v-progress-circular indeterminate size="64" color="primary" />
    </v-row>

    <!-- Error State -->
    <v-alert v-else-if="loadError" type="error" variant="tonal" class="mb-4">
      {{ loadError }}
      <v-btn @click="$router.push('/movies')" class="mt-2">Back to Collection</v-btn>
    </v-alert>

    <!-- Edit Form -->
    <v-card v-else-if="media" elevation="2">
      <v-card-text>
        <v-alert v-if="saveError" type="error" class="mb-4" closable @click:close="saveError = null">
          {{ saveError }}
        </v-alert>

        <v-row>
          <!-- Poster Preview -->
          <v-col cols="12" md="4">
            <v-card elevation="4">
              <v-chip 
                :color="media.mediaType === 'movie' ? 'primary' : 'secondary'" 
                size="small" 
                class="ma-2"
              >
                {{ media.mediaType === 'movie' ? 'MOVIE' : 'TV SHOW' }}
              </v-chip>
              <v-img
                v-if="media.posterUrl"
                :src="media.posterUrl"
                aspect-ratio="2/3"
                cover
              />
              <div v-else class="poster-placeholder">
                <v-icon size="120" color="grey">mdi-movie-outline</v-icon>
              </div>
            </v-card>
            <p class="text-caption text-center mt-2 text-medium-emphasis">
              To change poster, re-add from TMDB
            </p>
          </v-col>

          <!-- Edit Fields -->
          <v-col cols="12" md="8">
            <v-form ref="form" @submit.prevent="saveMedia">
              <!-- Title -->
              <v-text-field
                v-model="media.title"
                label="Title"
                variant="outlined"
                required
                :rules="[v => !!v || 'Title is required']"
              />

              <!-- Status -->
              <v-select
                v-model="media.status"
                :items="statusOptions"
                label="Status"
                variant="outlined"
                @update:model-value="handleStatusChange"
              />

              <!-- Your Rating (only if watched) -->
              <div v-if="media.status === 'watched'" class="mb-4">
                <label class="text-subtitle-1 mb-2 d-block">Your Rating</label>
                <v-rating
                  v-model="media.rating"
                  color="primary"
                  size="large"
                  hover
                />
                <p class="text-caption mt-1">
                  {{ media.rating }}/5 stars
                </p>
              </div>

              <!-- Director / Creator -->
              <v-text-field
                v-model="media.director"
                :label="media.mediaType === 'tv' ? 'Creator(s)' : 'Director'"
                variant="outlined"
              />

              <!-- Release Year -->
              <v-text-field
                v-model.number="media.releaseYear"
                :label="media.mediaType === 'tv' ? 'First Aired' : 'Release Year'"
                type="number"
                variant="outlined"
              />

              <!-- Movie-specific: Runtime -->
              <v-text-field
                v-if="media.mediaType === 'movie'"
                v-model.number="media.runtime"
                label="Runtime (minutes)"
                type="number"
                variant="outlined"
              />

              <!-- TV-specific fields -->
              <template v-if="media.mediaType === 'tv'">
                <v-text-field
                  v-model.number="media.numberOfSeasons"
                  label="Number of Seasons"
                  type="number"
                  variant="outlined"
                  readonly
                  hint="From TMDB (read-only)"
                  persistent-hint
                />

                <v-text-field
                  v-model.number="media.numberOfEpisodes"
                  label="Total Episodes"
                  type="number"
                  variant="outlined"
                  readonly
                  hint="From TMDB (read-only)"
                  persistent-hint
                />

                <v-text-field
                  v-if="media.status === 'watched'"
                  v-model.number="media.seasonsWatched"
                  label="Seasons You've Watched (optional)"
                  type="number"
                  variant="outlined"
                  :hint="`Total: ${media.numberOfSeasons} seasons`"
                  persistent-hint
                  :max="media.numberOfSeasons"
                  min="0"
                />
              </template>

              <!-- Genres -->
              <v-text-field
                v-model="genresText"
                label="Genres (comma-separated)"
                variant="outlined"
                hint="e.g., Action, Sci-Fi, Drama"
                persistent-hint
              />

              <!-- Plot -->
              <v-textarea
                v-model="media.plot"
                :label="media.mediaType === 'tv' ? 'Overview' : 'Plot'"
                variant="outlined"
                rows="4"
                class="mt-4"
              />

              <!-- Personal Notes -->
              <v-textarea
                v-model="media.notes"
                label="Your Personal Notes"
                variant="outlined"
                rows="4"
                placeholder="What did you think? Any memorable moments?"
              />

              <!-- Watched Date (only if watched) -->
              <v-text-field
                v-if="media.status === 'watched'"
                v-model="media.watchedDate"
                label="Date Watched"
                type="date"
                variant="outlined"
              />

              <!-- Action Buttons -->
              <div class="d-flex justify-end mt-6">
                <v-btn
                  variant="text"
                  @click="$router.push(`/movies/${mediaId}`)"
                  class="mr-2"
                >
                  Cancel
                </v-btn>
                <v-btn
                  type="submit"
                  color="primary"
                  size="large"
                  :loading="saving"
                  :disabled="!media.title || (media.status === 'watched' && !media.rating)"
                >
                  Save Changes
                </v-btn>
              </div>
            </v-form>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { mediaAPI } from '@/services/api-production';

export default {
  name: 'EditMediaView',
  
  data() {
    return {
      media: null,
      loading: false,
      saving: false,
      loadError: null,
      saveError: null,
      
      statusOptions: [
        { title: 'Watched', value: 'watched' },
        { title: 'Want to Watch', value: 'want_to_watch' },
        { title: 'Currently Watching', value: 'watching' },
      ],
    };
  },
  
  computed: {
    mediaId() {
      return this.$route.params.movieId; // Keep using movieId for route compatibility
    },
    
    genresText: {
      get() {
        if (!this.media || !this.media.genres) return '';
        return Array.isArray(this.media.genres)
          ? this.media.genres.join(', ')
          : this.media.genres;
      },
      set(value) {
        if (this.media) {
          this.media.genres = value;
        }
      }
    }
  },
  
  created() {
    this.loadMedia();
  },
  
  methods: {
    async loadMedia() {
      this.loading = true;
      this.loadError = null;
      
      try {
        this.media = await mediaAPI.getOne(this.mediaId);
      } catch (err) {
        console.error('Error loading media:', err);
        this.loadError = 'Failed to load. It may have been deleted.';
      } finally {
        this.loading = false;
      }
    },
    
    handleStatusChange(newStatus) {
      // If changing to watchlist, clear rating
      if (newStatus === 'want_to_watch') {
        this.media.rating = null;
      }
    },
    
    async saveMedia() {
      // Validation
      if (!this.media.title) {
        this.saveError = 'Title is required';
        return;
      }
      
      if (this.media.status === 'watched' && !this.media.rating) {
        this.saveError = 'Rating is required for watched items';
        return;
      }
      
      this.saving = true;
      this.saveError = null;
      
      try {
        // Prepare data for API
        const updateData = {
          title: this.media.title,
          status: this.media.status,
          rating: this.media.status === 'watched' ? this.media.rating : null,
          director: this.media.director || null,
          releaseYear: this.media.releaseYear || null,
          plot: this.media.plot || null,
          genres: this.media.genres || null,
          notes: this.media.notes || null,
          watchedDate: this.media.watchedDate || null,
        };
        
        // Add movie-specific fields
        if (this.media.mediaType === 'movie') {
          updateData.runtime = this.media.runtime || null;
        }
        
        // Add TV-specific fields
        if (this.media.mediaType === 'tv') {
          updateData.seasonsWatched = this.media.seasonsWatched || null;
        }
        
        await mediaAPI.update(this.mediaId, updateData);
        
        // Redirect back to detail page
        this.$router.push(`/movies/${this.mediaId}`);
        
      } catch (err) {
        console.error('Save error:', err);
        this.saveError = 'Failed to save changes. Please try again.';
      } finally {
        this.saving = false;
      }
    }
  }
};
</script>

<style scoped>
.edit-media {
  max-width: 1200px;
  margin: 0 auto;
}

.poster-placeholder {
  aspect-ratio: 2/3;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.05);
}
</style>
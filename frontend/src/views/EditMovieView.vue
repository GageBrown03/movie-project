<template>
  <div class="edit-movie">
    <v-row class="mb-4 align-center">
      <v-col>
        <h1 class="text-h4">Edit Movie</h1>
      </v-col>
      <v-col cols="auto">
        <v-btn
          variant="text"
          @click="$router.push(`/movies/${movieId}`)"
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
      <v-btn @click="$router.push('/movies')" class="mt-2">Back to Movies</v-btn>
    </v-alert>

    <!-- Edit Form -->
    <v-card v-else-if="movie" elevation="2">
      <v-card-text>
        <v-alert v-if="saveError" type="error" class="mb-4" closable @click:close="saveError = null">
          {{ saveError }}
        </v-alert>

        <v-row>
          <!-- Poster Preview -->
          <v-col cols="12" md="4">
            <v-card elevation="4">
              <v-img
                v-if="movie.posterUrl"
                :src="movie.posterUrl"
                aspect-ratio="2/3"
                cover
              />
              <div v-else class="poster-placeholder">
                <v-icon size="120" color="grey">mdi-movie-outline</v-icon>
              </div>
            </v-card>
            <p class="text-caption text-center mt-2 text-medium-emphasis">
              To change poster, re-add the movie from TMDB
            </p>
          </v-col>

          <!-- Edit Fields -->
          <v-col cols="12" md="8">
            <v-form ref="form" @submit.prevent="saveMovie">
              <!-- Title -->
              <v-text-field
                v-model="movie.title"
                label="Title"
                variant="outlined"
                required
                :rules="[v => !!v || 'Title is required']"
              />

              <!-- Director -->
              <v-text-field
                v-model="movie.director"
                label="Director"
                variant="outlined"
              />

              <!-- Your Rating -->
              <div class="mb-4">
                <label class="text-subtitle-1 mb-2 d-block">Your Rating</label>
                <v-rating
                  v-model="movie.rating"
                  color="primary"
                  size="large"
                  hover
                />
                <p class="text-caption mt-1">
                  {{ movie.rating }}/5 stars
                </p>
              </div>

              <!-- Release Year -->
              <v-text-field
                v-model.number="movie.releaseYear"
                label="Release Year"
                type="number"
                variant="outlined"
              />

              <!-- Runtime -->
              <v-text-field
                v-model.number="movie.runtime"
                label="Runtime (minutes)"
                type="number"
                variant="outlined"
              />

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
                v-model="movie.plot"
                label="Plot"
                variant="outlined"
                rows="4"
                class="mt-4"
              />

              <!-- Personal Notes -->
              <v-textarea
                v-model="movie.notes"
                label="Your Personal Notes"
                variant="outlined"
                rows="4"
                placeholder="What did you think? Any memorable moments?"
              />

              <!-- Watched Date -->
              <v-text-field
                v-model="movie.watchedDate"
                label="Date Watched"
                type="date"
                variant="outlined"
              />

              <!-- Action Buttons -->
              <div class="d-flex justify-end mt-6">
                <v-btn
                  variant="text"
                  @click="$router.push(`/movies/${movieId}`)"
                  class="mr-2"
                >
                  Cancel
                </v-btn>
                <v-btn
                  type="submit"
                  color="primary"
                  size="large"
                  :loading="saving"
                  :disabled="!movie.title || !movie.rating"
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
import { movieAPI } from '@/services/api-production';

export default {
  name: 'EditMovieView',
  
  data() {
    return {
      movie: null,
      loading: false,
      saving: false,
      loadError: null,
      saveError: null
    };
  },
  
  computed: {
    movieId() {
      return this.$route.params.movieId;
    },
    
    genresText: {
      get() {
        if (!this.movie || !this.movie.genres) return '';
        return Array.isArray(this.movie.genres)
          ? this.movie.genres.join(', ')
          : this.movie.genres;
      },
      set(value) {
        if (this.movie) {
          this.movie.genres = value;
        }
      }
    }
  },
  
  created() {
    this.loadMovie();
  },
  
  methods: {
    async loadMovie() {
      this.loading = true;
      this.loadError = null;
      
      try {
        this.movie = await movieAPI.getOne(this.movieId);
      } catch (err) {
        console.error('Error loading movie:', err);
        this.loadError = 'Failed to load movie. It may have been deleted.';
      } finally {
        this.loading = false;
      }
    },
    
    async saveMovie() {
      if (!this.movie.title || !this.movie.rating) {
        this.saveError = 'Title and rating are required';
        return;
      }
      
      this.saving = true;
      this.saveError = null;
      
      try {
        // Prepare data for API
        const updateData = {
          title: this.movie.title,
          director: this.movie.director || null,
          rating: this.movie.rating,
          releaseYear: this.movie.releaseYear || null,
          runtime: this.movie.runtime || null,
          plot: this.movie.plot || null,
          genres: this.movie.genres || null,
          notes: this.movie.notes || null,
          watchedDate: this.movie.watchedDate || null
        };
        
        await movieAPI.update(this.movieId, updateData);
        
        // Redirect back to movie detail page
        this.$router.push(`/movies/${this.movieId}`);
        
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
.edit-movie {
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
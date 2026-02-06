<template>
  <div class="single-movie">
    <!-- Loading State -->
    <v-row v-if="loading" justify="center" class="my-12">
      <v-progress-circular indeterminate size="64" color="primary" />
    </v-row>

    <!-- Error State -->
    <v-alert v-else-if="error" type="error" variant="tonal" class="mb-4">
      {{ error }}
      <template v-slot:append>
        <v-btn to="/movies" variant="text">Back to Movies</v-btn>
      </template>
    </v-alert>

    <!-- Movie Content -->
    <div v-else-if="movie">
      <!-- Hero Backdrop -->
      <div class="hero-section">
        <v-img
          v-if="movie.backdropUrl"
          :src="movie.backdropUrl"
          height="400"
          cover
          gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.8)"
          class="hero-backdrop"
        >
          <div class="hero-content">
            <v-container>
              <v-btn
                icon="mdi-arrow-left"
                variant="text"
                color="white"
                size="small"
                @click="$router.push('/movies')"
                class="back-button"
              />
              <h1 class="text-h3 text-white mb-2">{{ movie.title }}</h1>
              <div class="hero-meta">
                <v-chip v-if="movie.releaseYear" size="small" color="white" variant="flat" class="mr-2">
                  {{ movie.releaseYear }}
                </v-chip>
                <v-chip v-if="movie.runtime" size="small" color="white" variant="flat" class="mr-2">
                  {{ movie.runtime }} min
                </v-chip>
                <v-chip v-if="movie.director" size="small" color="white" variant="flat">
                  {{ movie.director }}
                </v-chip>
              </div>
            </v-container>
          </div>
        </v-img>
        <div v-else class="hero-fallback">
          <v-container>
            <v-btn
              icon="mdi-arrow-left"
              variant="text"
              size="small"
              @click="$router.push('/movies')"
              class="back-button mb-4"
            />
            <h1 class="text-h3 mb-2">{{ movie.title }}</h1>
            <div class="hero-meta">
              <v-chip v-if="movie.releaseYear" size="small" class="mr-2">
                {{ movie.releaseYear }}
              </v-chip>
              <v-chip v-if="movie.runtime" size="small" class="mr-2">
                {{ movie.runtime }} min
              </v-chip>
              <v-chip v-if="movie.director" size="small">
                {{ movie.director }}
              </v-chip>
            </div>
          </v-container>
        </div>
      </div>

      <!-- Main Content -->
      <v-container class="mt-6">
        <v-row>
          <!-- Left Column: Poster + Actions -->
          <v-col cols="12" md="4">
            <v-card elevation="4" class="sticky-poster">
              <v-img
                v-if="movie.posterUrl"
                :src="movie.posterUrl"
                aspect-ratio="2/3"
                cover
              />
              <div v-else class="poster-placeholder">
                <v-icon size="120" color="grey">mdi-movie-outline</v-icon>
              </div>

              <v-card-actions class="flex-column align-stretch pa-4">
                <v-btn
                  color="primary"
                  size="large"
                  block
                  @click="$router.push(`/movies/${movie.movieId}/edit`)"
                  prepend-icon="mdi-pencil"
                  class="mb-2"
                >
                  Edit Movie
                </v-btn>
                <v-btn
                  color="error"
                  variant="outlined"
                  size="large"
                  block
                  @click="confirmDelete"
                  prepend-icon="mdi-delete"
                >
                  Delete Movie
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>

          <!-- Right Column: Details -->
          <v-col cols="12" md="8">
            <!-- Your Rating -->
            <v-card class="mb-4" elevation="2">
              <v-card-title class="text-h5">Your Rating</v-card-title>
              <v-card-text>
                <v-rating
                  :model-value="movie.rating"
                  color="primary"
                  size="large"
                  readonly
                />
                <p class="text-h6 mt-2">{{ movie.rating }} out of 5 stars</p>
                <p v-if="movie.watchedDate" class="text-caption text-medium-emphasis mt-1">
                  Watched on {{ formatDate(movie.watchedDate) }}
                </p>
              </v-card-text>
            </v-card>

            <!-- External Ratings -->
            <v-card v-if="movie.tmdbRating || movie.imdbRating" class="mb-4" elevation="2">
              <v-card-title class="text-h6">External Ratings</v-card-title>
              <v-card-text>
                <v-row>
                  <v-col v-if="movie.tmdbRating" cols="6">
                    <div class="text-center">
                      <div class="text-h4 text-primary">{{ movie.tmdbRating.toFixed(1) }}</div>
                      <div class="text-caption">TMDB Rating</div>
                    </div>
                  </v-col>
                  <v-col v-if="movie.imdbRating" cols="6">
                    <div class="text-center">
                      <div class="text-h4 text-warning">{{ movie.imdbRating.toFixed(1) }}</div>
                      <div class="text-caption">IMDb Rating</div>
                    </div>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>

            <!-- Plot -->
            <v-card v-if="movie.plot" class="mb-4" elevation="2">
              <v-card-title class="text-h6">Plot</v-card-title>
              <v-card-text>
                <p class="text-body-1">{{ movie.plot }}</p>
              </v-card-text>
            </v-card>

            <!-- Details Grid -->
            <v-card class="mb-4" elevation="2">
              <v-card-title class="text-h6">Details</v-card-title>
              <v-card-text>
                <v-row dense>
                  <v-col v-if="movie.director" cols="12" sm="6">
                    <div class="detail-item">
                      <div class="text-caption text-medium-emphasis">Director</div>
                      <div class="text-body-1">{{ movie.director }}</div>
                    </div>
                  </v-col>
                  <v-col v-if="movie.releaseYear" cols="12" sm="6">
                    <div class="detail-item">
                      <div class="text-caption text-medium-emphasis">Release Year</div>
                      <div class="text-body-1">{{ movie.releaseYear }}</div>
                    </div>
                  </v-col>
                  <v-col v-if="movie.runtime" cols="12" sm="6">
                    <div class="detail-item">
                      <div class="text-caption text-medium-emphasis">Runtime</div>
                      <div class="text-body-1">{{ movie.runtime }} minutes</div>
                    </div>
                  </v-col>
                  <v-col v-if="movie.genres && movie.genres.length > 0" cols="12">
                    <div class="detail-item">
                      <div class="text-caption text-medium-emphasis mb-2">Genres</div>
                      <v-chip
                        v-for="genre in movie.genres"
                        :key="genre"
                        size="small"
                        class="mr-1 mb-1"
                      >
                        {{ genre }}
                      </v-chip>
                    </div>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>

            <!-- Personal Notes -->
            <v-card v-if="movie.notes" class="mb-4" elevation="2">
              <v-card-title class="text-h6">Your Notes</v-card-title>
              <v-card-text>
                <p class="text-body-1" style="white-space: pre-wrap;">{{ movie.notes }}</p>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </div>

    <!-- Delete Confirmation -->
    <delete-confirm-dialog
      :show="showDeleteDialog"
      :movie-title="movie?.title || ''"
      :deleting="isDeleting"
      @cancel="cancelDelete"
      @confirm="handleDelete"
    />
  </div>
</template>

<script>
import { movieAPI } from '@/services/api-production';
import DeleteConfirmDialog from '@/components/DeleteConfirmDialog.vue';

export default {
  name: 'SingleMovieView',
  
  components: {
    DeleteConfirmDialog
  },

  data() {
    return {
      movie: null,
      loading: false,
      error: null,
      showDeleteDialog: false,
      isDeleting: false
    };
  },

  computed: {
    movieId() {
      return this.$route.params.movieId;
    }
  },

  created() {
    this.getMovie();
  },

  methods: {
    async getMovie() {
      this.loading = true;
      this.error = null;
      
      try {
        this.movie = await movieAPI.getOne(this.movieId);
      } catch (err) {
        console.error('Error loading movie:', err);
        this.error = 'Failed to load movie. It may have been deleted.';
      } finally {
        this.loading = false;
      }
    },

    confirmDelete() {
      this.showDeleteDialog = true;
    },
    
    cancelDelete() {
      this.showDeleteDialog = false;
    },

    async handleDelete() {
      this.isDeleting = true;
      
      try {
        await movieAPI.delete(this.movieId);
        this.$router.push('/movies');
      } catch (err) {
        console.error('Error deleting movie:', err);
        this.error = 'Failed to delete movie. Please try again.';
        this.showDeleteDialog = false;
      } finally {
        this.isDeleting = false;
      }
    },
    
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      });
    }
  }
};
</script>

<style scoped>
.single-movie {
  min-height: 100vh;
}

.hero-section {
  margin: -24px -24px 0 -24px; /* Negative margin to extend to edges */
}

.hero-backdrop {
  position: relative;
}

.hero-content {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 40px 0 40px 0;
}

.hero-fallback {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 60px 0 40px 0;
  color: white;
}

.back-button {
  margin-bottom: 16px;
}

.hero-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}

.sticky-poster {
  position: sticky;
  top: 24px;
}

.poster-placeholder {
  aspect-ratio: 2/3;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.detail-item {
  margin-bottom: 16px;
}

@media (max-width: 960px) {
  .sticky-poster {
    position: static;
  }
  
  .hero-section {
    margin: -16px -16px 0 -16px;
  }
}
</style>
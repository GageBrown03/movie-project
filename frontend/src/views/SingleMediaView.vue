<template>
  <div class="single-media">
    <!-- Loading State -->
    <v-row v-if="loading" justify="center" class="my-12">
      <v-progress-circular indeterminate size="64" color="primary" />
    </v-row>

    <!-- Error State -->
    <v-alert v-else-if="error" type="error" variant="tonal" class="mb-4">
      {{ error }}
      <template v-slot:append>
        <v-btn to="/movies" variant="text">Back to Collection</v-btn>
      </template>
    </v-alert>

    <!-- Media Content -->
    <div v-else-if="media">
      <!-- Hero Backdrop -->
      <div class="hero-section">
        <v-img
          v-if="media.backdropUrl"
          :src="media.backdropUrl"
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
              <v-chip 
                :color="media.mediaType === 'movie' ? 'primary' : 'secondary'" 
                size="small" 
                class="mb-2"
              >
                {{ media.mediaType === 'movie' ? 'MOVIE' : 'TV SHOW' }}
              </v-chip>
              <h1 class="text-h3 text-white mb-2">{{ media.title }}</h1>
              <div class="hero-meta">
                <v-chip v-if="media.releaseYear" size="small" color="white" variant="flat" class="mr-2">
                  {{ media.releaseYear }}
                </v-chip>
                <v-chip v-if="media.runtime" size="small" color="white" variant="flat" class="mr-2">
                  {{ media.runtime }} min
                </v-chip>
                <v-chip v-if="media.numberOfSeasons" size="small" color="white" variant="flat" class="mr-2">
                  {{ media.numberOfSeasons }} {{ media.numberOfSeasons === 1 ? 'Season' : 'Seasons' }}
                </v-chip>
                <v-chip v-if="media.director" size="small" color="white" variant="flat">
                  {{ media.mediaType === 'tv' ? media.director : `Dir: ${media.director}` }}
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
            <v-chip 
              :color="media.mediaType === 'movie' ? 'primary' : 'secondary'" 
              size="small" 
              class="mb-2"
            >
              {{ media.mediaType === 'movie' ? 'MOVIE' : 'TV SHOW' }}
            </v-chip>
            <h1 class="text-h3 mb-2">{{ media.title }}</h1>
            <div class="hero-meta">
              <v-chip v-if="media.releaseYear" size="small" class="mr-2">
                {{ media.releaseYear }}
              </v-chip>
              <v-chip v-if="media.runtime" size="small" class="mr-2">
                {{ media.runtime }} min
              </v-chip>
              <v-chip v-if="media.numberOfSeasons" size="small" class="mr-2">
                {{ media.numberOfSeasons }} {{ media.numberOfSeasons === 1 ? 'Season' : 'Seasons' }}
              </v-chip>
              <v-chip v-if="media.director" size="small">
                {{ media.director }}
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
                v-if="media.posterUrl"
                :src="media.posterUrl"
                aspect-ratio="2/3"
                cover
              />
              <div v-else class="poster-placeholder">
                <v-icon size="120" color="grey">mdi-movie-outline</v-icon>
              </div>

              <v-card-actions class="flex-column align-stretch pa-4">
                <!-- Watchlist item: Mark as Watched button -->
                <v-btn
                  v-if="media.status === 'want_to_watch'"
                  color="success"
                  size="large"
                  block
                  @click="showMarkWatchedDialog = true"
                  prepend-icon="mdi-check-circle"
                  class="mb-2"
                >
                  Mark as Watched
                </v-btn>
                
                <!-- Watched item: Edit button -->
                <v-btn
                  v-else
                  color="primary"
                  size="large"
                  block
                  @click="$router.push(`/movies/${media.mediaId}/edit`)"
                  prepend-icon="mdi-pencil"
                  class="mb-2"
                >
                  Edit
                </v-btn>
                
                <v-btn
                  color="error"
                  variant="outlined"
                  size="large"
                  block
                  @click="confirmDelete"
                  prepend-icon="mdi-delete"
                >
                  Delete
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>

          <!-- Right Column: Details -->
          <v-col cols="12" md="8">
            <!-- Watchlist Banner -->
            <v-alert v-if="media.status === 'want_to_watch'" type="info" variant="tonal" class="mb-4">
              <v-icon start>mdi-bookmark</v-icon>
              This is on your watchlist. Click "Mark as Watched" to rate it!
            </v-alert>

            <!-- Your Rating (if watched) -->
            <v-card v-if="media.rating" class="mb-4" elevation="2">
              <v-card-title class="text-h5">Your Rating</v-card-title>
              <v-card-text>
                <v-rating
                  :model-value="media.rating"
                  color="primary"
                  size="large"
                  readonly
                />
                <p class="text-h6 mt-2">{{ media.rating }} out of 5 stars</p>
                <p v-if="media.watchedDate" class="text-caption text-medium-emphasis mt-1">
                  Watched on {{ formatDate(media.watchedDate) }}
                </p>
                
                <!-- TV-specific: Seasons watched -->
                <p v-if="media.mediaType === 'tv' && media.seasonsWatched" class="text-body-2 mt-2">
                  Watched {{ media.seasonsWatched }} of {{ media.numberOfSeasons }} seasons
                </p>
              </v-card-text>
            </v-card>

            <!-- External Ratings -->
            <v-card v-if="media.tmdbRating || media.imdbRating" class="mb-4" elevation="2">
              <v-card-title class="text-h6">External Ratings</v-card-title>
              <v-card-text>
                <v-row>
                  <v-col v-if="media.tmdbRating" cols="6">
                    <div class="text-center">
                      <div class="text-h4 text-primary">{{ media.tmdbRating.toFixed(1) }}</div>
                      <div class="text-caption">TMDB Rating</div>
                    </div>
                  </v-col>
                  <v-col v-if="media.imdbRating" cols="6">
                    <div class="text-center">
                      <div class="text-h4 text-warning">{{ media.imdbRating.toFixed(1) }}</div>
                      <div class="text-caption">IMDb Rating</div>
                    </div>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>

            <!-- Cast -->
            <v-card v-if="media.cast && media.cast.length > 0" class="mb-4" elevation="2">
              <v-card-title class="text-h6">Cast</v-card-title>
              <v-card-text>
                <v-row>
                  <v-col 
                    v-for="actor in media.cast.slice(0, 5)" 
                    :key="actor.actorId"
                    cols="6"
                    sm="4"
                    md="2"
                  >
                    <div class="text-center">
                      <v-avatar size="80" class="mb-2">
                        <v-img v-if="actor.profileUrl" :src="actor.profileUrl" cover />
                        <v-icon v-else size="40">mdi-account</v-icon>
                      </v-avatar>
                      <p class="text-caption font-weight-bold">{{ actor.name }}</p>
                      <p v-if="actor.character" class="text-caption text-medium-emphasis">
                        {{ actor.character }}
                      </p>
                    </div>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>

            <!-- Plot -->
            <v-card v-if="media.plot" class="mb-4" elevation="2">
              <v-card-title class="text-h6">{{ media.mediaType === 'tv' ? 'Overview' : 'Plot' }}</v-card-title>
              <v-card-text>
                <p class="text-body-1">{{ media.plot }}</p>
              </v-card-text>
            </v-card>

            <!-- Details Grid -->
            <v-card class="mb-4" elevation="2">
              <v-card-title class="text-h6">Details</v-card-title>
              <v-card-text>
                <v-row dense>
                  <v-col v-if="media.director" cols="12" sm="6">
                    <div class="detail-item">
                      <div class="text-caption text-medium-emphasis">
                        {{ media.mediaType === 'tv' ? 'Created By' : 'Director' }}
                      </div>
                      <div class="text-body-1">{{ media.director }}</div>
                    </div>
                  </v-col>
                  <v-col v-if="media.releaseYear" cols="12" sm="6">
                    <div class="detail-item">
                      <div class="text-caption text-medium-emphasis">
                        {{ media.mediaType === 'tv' ? 'First Aired' : 'Release Year' }}
                      </div>
                      <div class="text-body-1">{{ media.releaseYear }}</div>
                    </div>
                  </v-col>
                  <v-col v-if="media.runtime" cols="12" sm="6">
                    <div class="detail-item">
                      <div class="text-caption text-medium-emphasis">Runtime</div>
                      <div class="text-body-1">{{ media.runtime }} minutes</div>
                    </div>
                  </v-col>
                  <v-col v-if="media.numberOfSeasons" cols="12" sm="6">
                    <div class="detail-item">
                      <div class="text-caption text-medium-emphasis">Seasons</div>
                      <div class="text-body-1">{{ media.numberOfSeasons }}</div>
                    </div>
                  </v-col>
                  <v-col v-if="media.numberOfEpisodes" cols="12" sm="6">
                    <div class="detail-item">
                      <div class="text-caption text-medium-emphasis">Total Episodes</div>
                      <div class="text-body-1">{{ media.numberOfEpisodes }}</div>
                    </div>
                  </v-col>
                  <v-col v-if="media.showStatus" cols="12" sm="6">
                    <div class="detail-item">
                      <div class="text-caption text-medium-emphasis">Status</div>
                      <div class="text-body-1">{{ media.showStatus }}</div>
                    </div>
                  </v-col>
                  <v-col v-if="media.genres && media.genres.length > 0" cols="12">
                    <div class="detail-item">
                      <div class="text-caption text-medium-emphasis mb-2">Genres</div>
                      <v-chip
                        v-for="genre in media.genres"
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
            <v-card v-if="media.notes" class="mb-4" elevation="2">
              <v-card-title class="text-h6">Your Notes</v-card-title>
              <v-card-text>
                <p class="text-body-1" style="white-space: pre-wrap;">{{ media.notes }}</p>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </div>

    <!-- Mark as Watched Dialog -->
    <v-dialog v-model="showMarkWatchedDialog" max-width="500">
      <v-card>
        <v-card-title>Rate {{ media?.title }}</v-card-title>
        <v-card-text>
          <v-rating
            v-model="newRating"
            color="primary"
            size="large"
            hover
          />
          <p class="text-caption mt-2">
            {{ newRating ? `${newRating} out of 5 stars` : 'Tap to rate' }}
          </p>

          <v-textarea
            v-model="newNotes"
            label="Add notes (optional)"
            variant="outlined"
            rows="3"
            class="mt-4"
          />

          <!-- TV-specific -->
          <v-text-field
            v-if="media?.mediaType === 'tv' && media?.numberOfSeasons"
            v-model.number="newSeasonsWatched"
            label="Seasons watched (optional)"
            type="number"
            variant="outlined"
            :hint="`Total: ${media.numberOfSeasons} seasons`"
            persistent-hint
            :max="media.numberOfSeasons"
            min="1"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="showMarkWatchedDialog = false">Cancel</v-btn>
          <v-btn
            color="primary"
            @click="markAsWatched"
            :loading="isUpdating"
            :disabled="!newRating"
          >
            Mark as Watched
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation -->
    <delete-confirm-dialog
      :show="showDeleteDialog"
      :movie-title="media?.title || ''"
      :deleting="isDeleting"
      @cancel="cancelDelete"
      @confirm="handleDelete"
    />
  </div>
</template>

<script>
import { mediaAPI } from '@/services/api-production';
import DeleteConfirmDialog from '@/components/DeleteConfirmDialog.vue';

export default {
  name: 'SingleMediaView',
  
  components: {
    DeleteConfirmDialog
  },

  data() {
    return {
      media: null,
      loading: false,
      error: null,
      showDeleteDialog: false,
      isDeleting: false,
      
      // Mark as watched
      showMarkWatchedDialog: false,
      newRating: null,
      newNotes: '',
      newSeasonsWatched: null,
      isUpdating: false,
    };
  },

  computed: {
    mediaId() {
      return this.$route.params.movieId; // Keep using movieId for route compatibility
    }
  },

  created() {
    this.getMedia();
  },

  methods: {
    async getMedia() {
      this.loading = true;
      this.error = null;
      
      try {
        this.media = await mediaAPI.getOne(this.mediaId);
      } catch (err) {
        console.error('Error loading media:', err);
        this.error = 'Failed to load. It may have been deleted.';
      } finally {
        this.loading = false;
      }
    },
    
    async markAsWatched() {
      if (!this.newRating) return;
      
      this.isUpdating = true;
      
      try {
        const updateData = {
          status: 'watched',
          rating: this.newRating,
          notes: this.newNotes || this.media.notes,
        };
        
        if (this.media.mediaType === 'tv' && this.newSeasonsWatched) {
          updateData.seasonsWatched = this.newSeasonsWatched;
        }
        
        this.media = await mediaAPI.update(this.mediaId, updateData);
        this.showMarkWatchedDialog = false;
        this.newRating = null;
        this.newNotes = '';
        this.newSeasonsWatched = null;
        
      } catch (err) {
        console.error('Update error:', err);
        this.error = 'Failed to update. Please try again.';
      } finally {
        this.isUpdating = false;
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
        await mediaAPI.delete(this.mediaId);
        this.$router.push('/movies');
      } catch (err) {
        console.error('Error deleting:', err);
        this.error = 'Failed to delete. Please try again.';
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
.single-media {
  min-height: 100vh;
}

.hero-section {
  margin: -24px -24px 0 -24px;
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
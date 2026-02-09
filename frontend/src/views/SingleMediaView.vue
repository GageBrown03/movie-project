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
        <v-btn to="/media" variant="text">Back to Collection</v-btn>
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
                @click="$router.push('/media')"
                class="back-button"
              />
              
              <!-- Type Badge - Consistent with AllMediaView -->
              <v-chip 
                :color="media.mediaType === 'movie' ? '#1976D2' : '#7B1FA2'" 
                size="small" 
                class="mb-2 text-white font-weight-black"
                variant="flat"
                label
              >
                {{ media.mediaType === 'movie' ? 'MOVIE' : 'TV' }}
              </v-chip>
              
              <h1 class="text-h3 text-white mb-2">{{ media.title }}</h1>
              
              <div class="hero-meta">
                <v-chip v-if="media.releaseYear" size="small" color="white" variant="flat" class="mr-2">
                  {{ media.releaseYear }}
                </v-chip>
                
                <!-- Movie-specific: Runtime -->
                <v-chip v-if="media.mediaType === 'movie' && media.runtime" size="small" color="white" variant="flat" class="mr-2">
                  {{ media.runtime }} min
                </v-chip>
                
                <!-- TV-specific: Seasons -->
                <v-chip v-if="media.mediaType === 'tv' && media.numberOfSeasons" size="small" color="white" variant="flat" class="mr-2">
                  {{ media.numberOfSeasons }} {{ media.numberOfSeasons === 1 ? 'Season' : 'Seasons' }}
                </v-chip>
                
                <!-- Director/Creator -->
                <v-chip v-if="media.director" size="small" color="white" variant="flat">
                  {{ media.mediaType === 'tv' ? media.director : `Dir: ${media.director}` }}
                </v-chip>
              </div>
              <similar-content 
                v-if="media && media.tmdbId"
                :tmdb-id="media.tmdbId"
                :media-type="media.mediaType"
              />
            </v-container>
          </div>
        </v-img>
        <div v-else class="hero-fallback">
          <v-container>
            <v-btn
              icon="mdi-arrow-left"
              variant="text"
              size="small"
              @click="$router.push('/media')"
              class="back-button mb-4"
            />
            
            <!-- Type Badge - Consistent with AllMediaView -->
            <v-chip 
              :color="media.mediaType === 'movie' ? '#1976D2' : '#7B1FA2'" 
              size="small" 
              class="mb-2 text-white font-weight-black"
              variant="flat"
              label
            >
              {{ media.mediaType === 'movie' ? 'MOVIE' : 'TV' }}
            </v-chip>
            
            <h1 class="text-h3 mb-2">{{ media.title }}</h1>
            
            <div class="hero-meta">
              <v-chip v-if="media.releaseYear" size="small" class="mr-2">
                {{ media.releaseYear }}
              </v-chip>
              
              <!-- Movie-specific: Runtime -->
              <v-chip v-if="media.mediaType === 'movie' && media.runtime" size="small" class="mr-2">
                {{ media.runtime }} min
              </v-chip>
              
              <!-- TV-specific: Seasons -->
              <v-chip v-if="media.mediaType === 'tv' && media.numberOfSeasons" size="small" class="mr-2">
                {{ media.numberOfSeasons }} {{ media.numberOfSeasons === 1 ? 'Season' : 'Seasons' }}
              </v-chip>
              
              <!-- Director/Creator -->
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
                <!-- VIEW MODE: Quick actions -->
                <template v-if="!editMode">
                  <!-- Watchlist item: Mark as Watched button -->
                  <v-btn
                    v-if="media.status === 'want_to_watch'"
                    color="success"
                    size="large"
                    block
                    @click="quickMarkAsWatched"
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
                    @click="enterEditMode"
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
                </template>

                <!-- EDIT MODE: Save/Cancel -->
                <template v-else>
                  <v-btn
                    color="success"
                    size="large"
                    block
                    @click="saveChanges"
                    prepend-icon="mdi-check"
                    :loading="saving"
                    class="mb-2"
                  >
                    Save Changes
                  </v-btn>
                  <v-btn
                    variant="outlined"
                    size="large"
                    block
                    @click="cancelEdit"
                    prepend-icon="mdi-close"
                    :disabled="saving"
                  >
                    Cancel
                  </v-btn>
                </template>
              </v-card-actions>
            </v-card>
          </v-col>

          <!-- Right Column: Details -->
          <v-col cols="12" md="8">
            <!-- Edit Mode Banner -->
            <v-alert v-if="editMode" type="info" variant="tonal" class="mb-4" prominent>
              <v-icon start>mdi-pencil</v-icon>
              <strong>Edit Mode:</strong> Make changes to your personal data below. TMDB info is read-only.
            </v-alert>

            <!-- Watchlist Banner (view mode only) -->
            <v-alert v-if="!editMode && media.status === 'want_to_watch'" type="info" variant="tonal" class="mb-4">
              <v-icon start>mdi-bookmark</v-icon>
              This is on your watchlist. Click "Mark as Watched" to rate it!
            </v-alert>

            <!-- EDITABLE: Status (in edit mode) -->
            <v-card v-if="editMode" class="mb-4" elevation="2">
              <v-card-title class="text-h6">
                <v-icon start color="primary">mdi-pencil</v-icon>
                Status
              </v-card-title>
              <v-card-text>
                <v-select
                  v-model="editData.status"
                  :items="statusOptions"
                  label="Status"
                  variant="outlined"
                  density="comfortable"
                />
              </v-card-text>
            </v-card>

            <!-- EDITABLE: Your Rating -->
            <v-card v-if="editMode || media.rating" class="mb-4" elevation="2">
              <v-card-title class="text-h6">
                <v-icon v-if="editMode" start color="primary">mdi-pencil</v-icon>
                Your Rating
              </v-card-title>
              <v-card-text>
                <!-- EDIT MODE -->
                <template v-if="editMode">
                  <v-rating
                    v-model="editData.rating"
                    color="primary"
                    size="large"
                    hover
                  />
                  <p class="text-caption mt-2">
                    {{ editData.rating ? `${editData.rating} out of 5 stars` : 'Not rated yet' }}
                  </p>
                </template>

                <!-- VIEW MODE -->
                <template v-else>
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
                </template>
              </v-card-text>
            </v-card>

            <!-- EDITABLE: Date Watched (edit mode only) -->
            <v-card v-if="editMode && editData.status === 'watched'" class="mb-4" elevation="2">
              <v-card-title class="text-h6">
                <v-icon start color="primary">mdi-pencil</v-icon>
                Date Watched
              </v-card-title>
              <v-card-text>
                <v-text-field
                  v-model="editData.watchedDate"
                  type="date"
                  variant="outlined"
                  density="comfortable"
                  label="When did you watch this?"
                />
              </v-card-text>
            </v-card>

            <!-- EDITABLE: Seasons Watched (TV only, edit mode) -->
            <v-card v-if="editMode && media.mediaType === 'tv' && editData.status === 'watched'" class="mb-4" elevation="2">
              <v-card-title class="text-h6">
                <v-icon start color="primary">mdi-pencil</v-icon>
                Seasons Watched
              </v-card-title>
              <v-card-text>
                <v-text-field
                  v-model.number="editData.seasonsWatched"
                  type="number"
                  variant="outlined"
                  density="comfortable"
                  label="How many seasons have you watched?"
                  :hint="`Total: ${media.numberOfSeasons} seasons`"
                  persistent-hint
                  :max="media.numberOfSeasons"
                  min="0"
                />
              </v-card-text>
            </v-card>

            <!-- READ-ONLY: External Ratings -->
            <v-card v-if="media.tmdbRating || media.imdbRating" class="mb-4" elevation="2">
              <v-card-title class="text-h6">
                <v-icon start>mdi-lock</v-icon>
                External Ratings
                <v-chip v-if="editMode" size="x-small" color="grey" class="ml-2">Read-only</v-chip>
              </v-card-title>
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

            <!-- READ-ONLY: Cast -->
            <v-card v-if="media.cast && media.cast.length > 0" class="mb-4" elevation="2">
              <v-card-title class="text-h6">
                <v-icon start>mdi-lock</v-icon>
                Cast
                <v-chip v-if="editMode" size="x-small" color="grey" class="ml-2">Read-only</v-chip>
              </v-card-title>
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

            <!-- READ-ONLY: Plot -->
            <v-card v-if="media.plot" class="mb-4" elevation="2">
              <v-card-title class="text-h6">
                <v-icon start>mdi-lock</v-icon>
                {{ media.mediaType === 'tv' ? 'Overview' : 'Plot' }}
                <v-chip v-if="editMode" size="x-small" color="grey" class="ml-2">Read-only</v-chip>
              </v-card-title>
              <v-card-text>
                <p class="text-body-1">{{ media.plot }}</p>
              </v-card-text>
            </v-card>

            <!-- READ-ONLY: Details Grid -->
            <v-card class="mb-4" elevation="2">
              <v-card-title class="text-h6">
                <v-icon start>mdi-lock</v-icon>
                Details
                <v-chip v-if="editMode" size="x-small" color="grey" class="ml-2">Read-only</v-chip>
              </v-card-title>
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

            <!-- EDITABLE: Personal Notes -->
            <v-card class="mb-4" elevation="2">
              <v-card-title class="text-h6">
                <v-icon v-if="editMode" start color="primary">mdi-pencil</v-icon>
                <v-icon v-else start>mdi-note-text</v-icon>
                Your Personal Notes
              </v-card-title>
              <v-card-text>
                <!-- EDIT MODE -->
                <v-textarea
                  v-if="editMode"
                  v-model="editData.notes"
                  variant="outlined"
                  rows="5"
                  placeholder="What did you think? Any memorable moments?"
                  hint="These notes are private and only visible to you"
                  persistent-hint
                />

                <!-- VIEW MODE -->
                <p v-else-if="media.notes" class="text-body-1" style="white-space: pre-wrap;">{{ media.notes }}</p>
                <p v-else class="text-body-2 text-medium-emphasis">No notes yet. Click "Edit" to add your thoughts!</p>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </div>

    <!-- Quick Mark as Watched Dialog (for watchlist items) -->
    <v-dialog v-model="showMarkWatchedDialog" max-width="500">
      <v-card>
        <v-card-title>Rate {{ media?.title }}</v-card-title>
        <v-card-text>
          <v-rating
            v-model="quickRating"
            color="primary"
            size="large"
            hover
          />
          <p class="text-caption mt-2">
            {{ quickRating ? `${quickRating} out of 5 stars` : 'Tap to rate' }}
          </p>

          <v-textarea
            v-model="quickNotes"
            label="Add notes (optional)"
            variant="outlined"
            rows="3"
            class="mt-4"
          />

          <!-- TV-specific -->
          <v-text-field
            v-if="media?.mediaType === 'tv' && media?.numberOfSeasons"
            v-model.number="quickSeasonsWatched"
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
            :loading="saving"
            :disabled="!quickRating"
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
import SimilarContent from '@/components/SimilarContent.vue';

export default {
  name: 'SingleMediaView',
  
  components: {
    DeleteConfirmDialog,
    SimilarContent
  },

  data() {
    return {
      media: null,
      loading: false,
      error: null,
      showDeleteDialog: false,
      isDeleting: false,
      
      // Edit mode
      editMode: false,
      editData: {
        status: null,
        rating: null,
        notes: '',
        watchedDate: null,
        seasonsWatched: null,
      },
      saving: false,
      
      // Quick mark as watched (for watchlist items)
      showMarkWatchedDialog: false,
      quickRating: null,
      quickNotes: '',
      quickSeasonsWatched: null,
      
      statusOptions: [
        { title: 'Watched', value: 'watched' },
        { title: 'Want to Watch', value: 'want_to_watch' },
        { title: 'Currently Watching', value: 'watching' },
      ],
    };
  },

  computed: {
    mediaId() {
      // FIXED: Changed from movieId to mediaId to match route param
      return this.$route.params.mediaId;
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
    
    enterEditMode() {
      // Copy current values to editData
      this.editData = {
        status: this.media.status,
        rating: this.media.rating,
        notes: this.media.notes || '',
        watchedDate: this.media.watchedDate || null,
        seasonsWatched: this.media.seasonsWatched || null,
      };
      this.editMode = true;
    },
    
    cancelEdit() {
      this.editMode = false;
      this.editData = {
        status: null,
        rating: null,
        notes: '',
        watchedDate: null,
        seasonsWatched: null,
      };
    },
    
    async saveChanges() {
      // Validation
      if (this.editData.status === 'watched' && !this.editData.rating) {
        this.error = 'Rating is required for watched items';
        return;
      }
      
      this.saving = true;
      this.error = null;
      
      try {
        const updateData = {
          status: this.editData.status,
          rating: this.editData.status === 'watched' ? this.editData.rating : null,
          notes: this.editData.notes || null,
          watchedDate: this.editData.watchedDate || null,
        };
        
        // TV-specific
        if (this.media.mediaType === 'tv' && this.editData.seasonsWatched) {
          updateData.seasonsWatched = this.editData.seasonsWatched;
        }
        
        this.media = await mediaAPI.update(this.mediaId, updateData);
        this.editMode = false;
        
      } catch (err) {
        console.error('Update error:', err);
        this.error = 'Failed to save changes. Please try again.';
      } finally {
        this.saving = false;
      }
    },
    
    quickMarkAsWatched() {
      this.showMarkWatchedDialog = true;
    },
    
    async markAsWatched() {
      if (!this.quickRating) return;
      
      this.saving = true;
      
      try {
        const updateData = {
          status: 'watched',
          rating: this.quickRating,
          notes: this.quickNotes || this.media.notes,
        };
        
        if (this.media.mediaType === 'tv' && this.quickSeasonsWatched) {
          updateData.seasonsWatched = this.quickSeasonsWatched;
        }
        
        this.media = await mediaAPI.update(this.mediaId, updateData);
        this.showMarkWatchedDialog = false;
        this.quickRating = null;
        this.quickNotes = '';
        this.quickSeasonsWatched = null;
        
      } catch (err) {
        console.error('Update error:', err);
        this.error = 'Failed to update. Please try again.';
      } finally {
        this.saving = false;
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
        this.$router.push('/media');
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
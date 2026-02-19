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
      <!-- DESKTOP/TABLET: Hero Backdrop -->
      <div class="hero-section d-none d-md-block">
        <v-img
          v-if="media.backdropUrl"
          :src="media.backdropUrl"
          height="350"
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
                
                <v-chip v-if="media.mediaType === 'movie' && media.runtime" size="small" color="white" variant="flat" class="mr-2">
                  {{ media.runtime }} min
                </v-chip>
                
                <v-chip v-if="media.mediaType === 'tv' && media.numberOfSeasons" size="small" color="white" variant="flat" class="mr-2">
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
              @click="$router.push('/media')"
              class="back-button mb-4"
            />
            
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
              
              <v-chip v-if="media.mediaType === 'movie' && media.runtime" size="small" class="mr-2">
                {{ media.runtime }} min
              </v-chip>
              
              <v-chip v-if="media.mediaType === 'tv' && media.numberOfSeasons" size="small" class="mr-2">
                {{ media.numberOfSeasons }} {{ media.numberOfSeasons === 1 ? 'Season' : 'Seasons' }}
              </v-chip>
              
              <v-chip v-if="media.director" size="small">
                {{ media.director }}
              </v-chip>
            </div>
          </v-container>
        </div>
      </div>

      <!-- MOBILE: Compact Hero -->
      <div class="mobile-hero d-md-none">
        <v-container class="py-4">
          <v-btn
            icon="mdi-arrow-left"
            variant="text"
            size="small"
            @click="$router.push('/media')"
            class="mb-3"
          />
          
          <div class="d-flex gap-3">
            <!-- Compact Poster -->
            <div class="mobile-poster-wrapper">
              <v-img
                v-if="media.posterUrl"
                :src="media.posterUrl"
                aspect-ratio="2/3"
                width="120"
                cover
                class="rounded"
              />
              <div v-else class="mobile-poster-placeholder">
                <v-icon size="40" color="grey">mdi-movie-outline</v-icon>
              </div>
            </div>
            
            <!-- Title & Meta -->
            <div class="flex-grow-1">
              <v-chip 
                :color="media.mediaType === 'movie' ? '#1976D2' : '#7B1FA2'" 
                size="x-small" 
                class="mb-2 text-white font-weight-black"
                variant="flat"
                label
              >
                {{ media.mediaType === 'movie' ? 'MOVIE' : 'TV' }}
              </v-chip>
              
              <h1 class="text-h5 mb-2">{{ media.title }}</h1>
              
              <div class="text-caption text-medium-emphasis mb-3">
                <div v-if="media.releaseYear">{{ media.releaseYear }}</div>
                <div v-if="media.mediaType === 'movie' && media.runtime">{{ media.runtime }} min</div>
                <div v-if="media.mediaType === 'tv' && media.numberOfSeasons">
                  {{ media.numberOfSeasons }} {{ media.numberOfSeasons === 1 ? 'Season' : 'Seasons' }}
                </div>
                <div v-if="media.director" class="text-truncate">{{ media.director }}</div>
              </div>
              
              <!-- Mobile Quick Actions -->
              <div class="mobile-actions">
                <v-btn
                  v-if="media.status === 'want_to_watch'"
                  color="success"
                  size="small"
                  block
                  @click="quickMarkAsWatched"
                  prepend-icon="mdi-check"
                  class="mb-1"
                >
                  Mark Watched
                </v-btn>
                
                <div class="d-flex gap-1">
                  <v-btn
                    size="small"
                    variant="tonal"
                    @click="editMode = true"
                    prepend-icon="mdi-pencil"
                    class="flex-grow-1"
                  >
                    Edit
                  </v-btn>
                  <v-btn
                    size="small"
                    variant="tonal"
                    color="error"
                    @click="deleteDialog = true"
                    icon="mdi-delete"
                  />
                </div>
              </div>
            </div>
          </div>
        </v-container>
      </div>

      <!-- Main Content -->
      <v-container class="mt-6">
        <v-row>
          <!-- DESKTOP/TABLET: Left Column with Poster + Actions -->
          <v-col cols="12" md="4" class="d-none d-md-block">
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
                <template v-if="!editMode">
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
                  
                  <v-btn
                    variant="tonal"
                    size="large"
                    block
                    @click="editMode = true"
                    prepend-icon="mdi-pencil"
                    class="mb-2"
                  >
                    Edit Details
                  </v-btn>
                  
                  <v-btn
                    variant="tonal"
                    color="error"
                    size="large"
                    block
                    @click="deleteDialog = true"
                    prepend-icon="mdi-delete"
                  >
                    Delete
                  </v-btn>
                </template>
                
                <template v-else>
                  <v-btn
                    color="primary"
                    size="large"
                    block
                    @click="saveChanges"
                    :loading="saving"
                    prepend-icon="mdi-content-save"
                    class="mb-2"
                  >
                    Save Changes
                  </v-btn>
                  
                  <v-btn
                    variant="outlined"
                    size="large"
                    block
                    @click="cancelEdit"
                  >
                    Cancel
                  </v-btn>
                </template>
              </v-card-actions>
            </v-card>
          </v-col>

          <!-- Right Column: Details -->
          <v-col cols="12" md="8">
            <!-- VIEW MODE -->
            <div v-if="!editMode">
              <!-- Status & Rating -->
              <v-card elevation="2" class="mb-4">
                <v-card-text>
                  <v-row>
                    <v-col cols="12" sm="6">
                      <div class="detail-item">
                        <div class="text-caption text-medium-emphasis mb-1">Status</div>
                        <v-chip 
                          :color="statusColor" 
                          variant="flat"
                          size="small"
                        >
                          {{ statusLabel }}
                        </v-chip>
                      </div>
                    </v-col>
                    
                    <v-col cols="12" sm="6">
                      <div class="detail-item" v-if="media.rating">
                        <div class="text-caption text-medium-emphasis mb-1">Your Rating</div>
                        <v-rating
                          :model-value="media.rating"
                          readonly
                          density="compact"
                          color="amber"
                        />
                      </div>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>

              <!-- Plot -->
              <v-card elevation="2" class="mb-4" v-if="media.plot">
                <v-card-title class="text-h6">Plot</v-card-title>
                <v-card-text>
                  <p class="text-body-1">{{ media.plot }}</p>
                </v-card-text>
              </v-card>

              <!-- Details Grid -->
              <v-card elevation="2" class="mb-4">
                <v-card-title class="text-h6">Details</v-card-title>
                <v-card-text>
                  <v-row>
                    <v-col cols="12" sm="6" v-if="media.releaseYear">
                      <div class="detail-item">
                        <div class="text-caption text-medium-emphasis">Release Year</div>
                        <div class="text-body-1 font-weight-medium">{{ media.releaseYear }}</div>
                      </div>
                    </v-col>
                    
                    <v-col cols="12" sm="6" v-if="media.genres && media.genres.length">
                      <div class="detail-item">
                        <div class="text-caption text-medium-emphasis mb-1">Genres</div>
                        <div class="d-flex flex-wrap gap-1">
                          <v-chip 
                            v-for="genre in media.genres" 
                            :key="genre" 
                            size="small"
                            variant="tonal"
                          >
                            {{ genre }}
                          </v-chip>
                        </div>
                      </div>
                    </v-col>
                    
                    <v-col cols="12" sm="6" v-if="media.mediaType === 'movie' && media.runtime">
                      <div class="detail-item">
                        <div class="text-caption text-medium-emphasis">Runtime</div>
                        <div class="text-body-1 font-weight-medium">{{ media.runtime }} minutes</div>
                      </div>
                    </v-col>
                    
                    <v-col cols="12" sm="6" v-if="media.mediaType === 'tv' && media.numberOfSeasons">
                      <div class="detail-item">
                        <div class="text-caption text-medium-emphasis">Seasons</div>
                        <div class="text-body-1 font-weight-medium">{{ media.numberOfSeasons }}</div>
                      </div>
                    </v-col>
                    
                    <v-col cols="12" sm="6" v-if="media.mediaType === 'tv' && media.numberOfEpisodes">
                      <div class="detail-item">
                        <div class="text-caption text-medium-emphasis">Episodes</div>
                        <div class="text-body-1 font-weight-medium">{{ media.numberOfEpisodes }}</div>
                      </div>
                    </v-col>
                    
                    <v-col cols="12" sm="6" v-if="media.director">
                      <div class="detail-item">
                        <div class="text-caption text-medium-emphasis">
                          {{ media.mediaType === 'tv' ? 'Creator' : 'Director' }}
                        </div>
                        <div class="text-body-1 font-weight-medium">{{ media.director }}</div>
                      </div>
                    </v-col>
                    
                    <v-col cols="12" sm="6" v-if="media.tmdbRating">
                      <div class="detail-item">
                        <div class="text-caption text-medium-emphasis">TMDB Rating</div>
                        <div class="text-body-1 font-weight-medium">
                          <v-icon size="small" color="amber" class="mr-1">mdi-star</v-icon>
                          {{ media.tmdbRating.toFixed(1) }}/10
                        </div>
                      </div>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>

              <!-- Cast -->
              <v-card elevation="2" class="mb-4" v-if="media.cast && media.cast.length">
                <v-card-title class="text-h6">Cast</v-card-title>
                <v-card-text>
                  <div class="cast-grid">
                    <div 
                      v-for="actor in media.cast.slice(0, 6)" 
                      :key="actor.actorId"
                      class="cast-member"
                    >
                      <v-avatar size="60" class="mb-2">
                        <v-img 
                          v-if="actor.profileUrl" 
                          :src="actor.profileUrl"
                        />
                        <v-icon v-else size="32">mdi-account</v-icon>
                      </v-avatar>
                      <div class="text-caption font-weight-bold text-center">
                        {{ actor.name }}
                      </div>
                      <div class="text-caption text-medium-emphasis text-center">
                        {{ actor.character }}
                      </div>
                    </div>
                  </div>
                </v-card-text>
              </v-card>

              <!-- Personal Notes -->
              <v-card elevation="2" class="mb-4" v-if="media.notes">
                <v-card-title class="text-h6">Your Notes</v-card-title>
                <v-card-text>
                  <p class="text-body-1">{{ media.notes }}</p>
                </v-card-text>
              </v-card>
            </div>

            <!-- EDIT MODE -->
            <div v-else>
              <v-card elevation="2" class="mb-4">
                <v-card-title class="text-h6">Edit Details</v-card-title>
                <v-card-text>
                  <v-select
                    v-model="editData.status"
                    :items="statusOptions"
                    label="Status"
                    variant="outlined"
                    class="mb-4"
                  />
                  
                  <div class="mb-4">
                    <div class="text-body-2 mb-2">Your Rating</div>
                    <v-rating
                      v-model="editData.rating"
                      color="amber"
                      hover
                    />
                  </div>
                  
                  <v-textarea
                    v-model="editData.notes"
                    label="Personal Notes"
                    variant="outlined"
                    rows="4"
                    placeholder="What did you think?"
                  />
                </v-card-text>
              </v-card>
              
              <!-- Mobile Edit Actions -->
              <v-card elevation="2" class="d-md-none">
                <v-card-actions class="pa-4">
                  <v-btn
                    color="primary"
                    size="large"
                    block
                    @click="saveChanges"
                    :loading="saving"
                    prepend-icon="mdi-content-save"
                    class="mb-2"
                  >
                    Save Changes
                  </v-btn>
                  
                  <v-btn
                    variant="outlined"
                    size="large"
                    block
                    @click="cancelEdit"
                  >
                    Cancel
                  </v-btn>
                </v-card-actions>
              </v-card>
            </div>
          </v-col>
        </v-row>
        
        <!-- Similar Content (Your Carousel Implementation) -->
        <similar-content 
          v-if="media && media.tmdbId"
          :tmdb-id="media.tmdbId"
          :media-type="media.mediaType"
        />
      </v-container>
    </div>

    <!-- Quick Mark as Watched Dialog -->
    <v-dialog v-model="showQuickWatchDialog" max-width="500">
      <v-card>
        <v-card-title>Mark as Watched</v-card-title>
        <v-card-text>
          <div class="mb-4">
            <div class="text-body-2 mb-2">Rate {{ media?.title }}</div>
            <v-rating
              v-model="quickWatchRating"
              color="amber"
              hover
              size="large"
            />
          </div>
          
          <v-textarea
            v-model="quickWatchNotes"
            label="Notes (optional)"
            variant="outlined"
            rows="3"
            placeholder="What did you think?"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="showQuickWatchDialog = false">
            Cancel
          </v-btn>
          <v-btn 
            color="success" 
            @click="confirmQuickWatch"
            :loading="saving"
          >
            Mark as Watched
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation -->
    <delete-confirm-dialog
      v-model="deleteDialog"
      :item-name="media?.title"
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
      loading: false,
      error: null,
      media: null,
      editMode: false,
      editData: {
        status: null,
        rating: null,
        notes: ''
      },
      saving: false,
      deleteDialog: false,
      showQuickWatchDialog: false,
      quickWatchRating: null,
      quickWatchNotes: '',
      statusOptions: [
        { title: 'Want to Watch', value: 'want_to_watch' },
        { title: 'Watched', value: 'watched' }
      ]
    };
  },
  
  computed: {
    statusLabel() {
      if (!this.media) return '';
      return this.media.status === 'want_to_watch' ? 'Watchlist' : 'Watched';
    },
    
    statusColor() {
      if (!this.media) return 'primary';
      return this.media.status === 'want_to_watch' ? 'info' : 'success';
    }
  },
  
  created() {
    this.loadMedia();
  },
  
  methods: {
    async loadMedia() {
      this.loading = true;
      this.error = null;
      
      try {
        const id = this.$route.params.id;
        this.media = await mediaAPI.getOne(id);
      } catch (err) {
        console.error('Error loading media:', err);
        this.error = 'Failed to load media. Please try again.';
      } finally {
        this.loading = false;
      }
    },
    
    quickMarkAsWatched() {
      this.quickWatchRating = null;
      this.quickWatchNotes = '';
      this.showQuickWatchDialog = true;
    },
    
    async confirmQuickWatch() {
      this.saving = true;
      
      try {
        const updateData = {
          status: 'watched',
          rating: this.quickWatchRating,
          notes: this.quickWatchNotes || this.media.notes
        };
        
        const updated = await mediaAPI.update(this.media.mediaId, updateData);
        this.media = updated;
        this.showQuickWatchDialog = false;
      } catch (err) {
        console.error('Error updating media:', err);
        alert('Failed to update. Please try again.');
      } finally {
        this.saving = false;
      }
    },
    
    cancelEdit() {
      this.editMode = false;
      this.editData = {
        status: null,
        rating: null,
        notes: ''
      };
    },
    
    async saveChanges() {
      this.saving = true;
      
      try {
        const updateData = {
          status: this.editData.status,
          rating: this.editData.rating,
          notes: this.editData.notes
        };
        
        const updated = await mediaAPI.update(this.media.mediaId, updateData);
        this.media = updated;
        this.editMode = false;
      } catch (err) {
        console.error('Error saving changes:', err);
        alert('Failed to save changes. Please try again.');
      } finally {
        this.saving = false;
      }
    },
    
    async handleDelete() {
      try {
        await mediaAPI.delete(this.media.mediaId);
        this.$router.push('/media');
      } catch (err) {
        console.error('Error deleting media:', err);
        alert('Failed to delete. Please try again.');
      }
    }
  },
  
  watch: {
    editMode(newVal) {
      if (newVal && this.media) {
        this.editData = {
          status: this.media.status,
          rating: this.media.rating,
          notes: this.media.notes || ''
        };
      }
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
  padding: 40px 0;
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
  margin-bottom: 8px;
}

.cast-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 16px;
}

.cast-member {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* MOBILE STYLES */
.mobile-hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  margin: -16px -16px 0 -16px;
}

.mobile-poster-wrapper {
  flex-shrink: 0;
}

.mobile-poster-placeholder {
  width: 120px;
  aspect-ratio: 2/3;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
}

.mobile-actions .gap-1 {
  gap: 4px;
}

/* RESPONSIVE */
@media (max-width: 960px) {
  .sticky-poster {
    position: static;
  }
  
  .hero-section {
    margin: -16px -16px 0 -16px;
  }
}

@media (min-width: 960px) {
  .mobile-hero {
    display: none !important;
  }
}
</style>
<template>
  <div class="random-picker">
    <v-row class="mb-6 align-center">
      <v-col>
        <h1 class="text-h3 font-weight-bold">What Should I Watch?</h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Let us pick something from your watchlist
        </p>
      </v-col>
    </v-row>

    <v-row v-if="loading" justify="center" class="my-12">
      <v-progress-circular indeterminate size="64" color="primary" />
    </v-row>

    <v-row v-else-if="watchlist.length === 0" justify="center" class="my-8">
      <v-col cols="12" md="10" lg="8">
        <v-sheet
          class="d-flex flex-column align-center justify-center text-center pa-10 pa-md-16 rounded-xl empty-dashed-border"
          color="surface-light"
        >
          <div class="icon-bg-circle mb-6">
            <v-icon icon="mdi-filmstrip-off" size="80" color="primary" />
          </div>
          
          <h2 class="text-h4 font-weight-bold mb-3">Your watchlist is looking a bit light</h2>
          
          <p class="text-body-1 text-medium-emphasis mb-8" style="max-width: 500px">
            We can't work our magic until you give us some options. 
            Add movies or TV shows you've been meaning to watch, and we'll help you decide.
          </p>

          <div class="d-flex flex-wrap justify-center gap-4">
            <v-btn
              color="primary"
              size="x-large"
              to="/media/new"
              prepend-icon="mdi-plus"
              elevation="4"
              class="px-8"
            >
              Add Media
            </v-btn>

            <v-btn
              variant="outlined"
              size="x-large"
              to="/discover"
              prepend-icon="mdi-compass-outline"
              class="px-8"
            >
              Browse Trending
            </v-btn>
          </div>
        </v-sheet>
      </v-col>
    </v-row>
    <div v-else>
      <v-card class="mb-6" elevation="2">
        <v-card-title class="text-h6">
          <v-icon start>mdi-filter</v-icon>
          Filters (Optional)
        </v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="12" sm="6" md="3">
              <v-select
                v-model="filters.type"
                :items="typeOptions"
                label="Type"
                variant="outlined"
                density="comfortable"
                clearable
              />
            </v-col>

            <v-col cols="12" sm="6" md="3">
              <v-select
                v-model="filters.genre"
                :items="availableGenres"
                label="Genre"
                variant="outlined"
                density="comfortable"
                clearable
              />
            </v-col>

            <v-col cols="12" sm="6" md="3">
              <v-select
                v-model="filters.runtime"
                :items="runtimeOptions"
                label="Runtime"
                variant="outlined"
                density="comfortable"
                clearable
                :disabled="filters.type === 'tv'"
              />
            </v-col>

            <v-col cols="12" sm="6" md="3">
              <v-select
                v-model="filters.decade"
                :items="decadeOptions"
                label="Decade"
                variant="outlined"
                density="comfortable"
                clearable
              />
            </v-col>
          </v-row>

          <div class="d-flex justify-space-between align-center">
            <v-chip v-if="hasActiveFilters" size="small">
              {{ filteredWatchlist.length }} matches
            </v-chip>
            <v-btn
              v-if="hasActiveFilters"
              variant="text"
              size="small"
              @click="clearFilters"
            >
              Clear Filters
            </v-btn>
          </div>
        </v-card-text>
      </v-card>

      <v-row v-if="!pickedMedia" justify="center" class="my-12">
        <v-col cols="12" sm="8" md="6" class="text-center">
          <v-btn
            color="primary"
            size="x-large"
            @click="pickRandom"
            :disabled="filteredWatchlist.length === 0"
            class="pick-button"
            elevation="8"
          >
            <div class="d-flex align-center justify-center">
              <v-icon start size="large">mdi-dice-5</v-icon>
              <span>Pick For Me</span>
            </div>
          </v-btn>
          <p v-if="filteredWatchlist.length === 0" class="text-caption text-error mt-4">
            No items match your filters
          </p>
        </v-col>
      </v-row>

      <v-card v-if="pickedMedia" class="picked-card mb-6" elevation="8">
        <v-row no-gutters>
          <v-col cols="12">
            <div class="picked-hero">
              <v-img
                v-if="pickedMedia.backdropUrl"
                :src="pickedMedia.backdropUrl"
                height="400"
                cover
                gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.8)"
              >
                <div class="picked-hero-content pa-8">
                  <v-chip 
                    :color="pickedMedia.mediaType === 'movie' ? 'primary' : 'secondary'" 
                    size="small" 
                    class="mb-2"
                  >
                    {{ pickedMedia.mediaType === 'movie' ? 'MOVIE' : 'TV SHOW' }}
                  </v-chip>
                  <h2 class="text-h2 font-weight-black text-white mb-2">
                    {{ pickedMedia.title }}
                  </h2>
                  <div class="d-flex flex-wrap gap-2">
                    <v-chip v-if="pickedMedia.releaseYear" color="white" variant="flat" size="small">
                      {{ pickedMedia.releaseYear }}
                    </v-chip>
                    <v-chip v-if="pickedMedia.runtime" color="white" variant="flat" size="small">
                      {{ pickedMedia.runtime }} min
                    </v-chip>
                    <v-chip v-if="pickedMedia.numberOfSeasons" color="white" variant="flat" size="small">
                      {{ pickedMedia.numberOfSeasons }} Seasons
                    </v-chip>
                    <v-chip v-if="pickedMedia.tmdbRating" color="amber" variant="flat" size="small">
                      <v-icon start size="small">mdi-star</v-icon>
                      {{ pickedMedia.tmdbRating.toFixed(1) }}
                    </v-chip>
                  </div>
                </div>
              </v-img>
              <div v-else class="picked-fallback pa-8">
                <v-chip 
                  :color="pickedMedia.mediaType === 'movie' ? 'primary' : 'secondary'" 
                  size="small" 
                  class="mb-2"
                >
                  {{ pickedMedia.mediaType === 'movie' ? 'MOVIE' : 'TV SHOW' }}
                </v-chip>
                <h2 class="text-h2 font-weight-black mb-2">
                  {{ pickedMedia.title }}
                </h2>
              </div>
            </div>
          </v-col>

          <v-col cols="12">
            <v-card-text class="pa-6">
              <p v-if="pickedMedia.plot" class="text-h6 mb-4" style="line-height: 1.6;">
                {{ pickedMedia.plot }}
              </p>

              <div v-if="pickedMedia.genres" class="mb-4">
                <v-chip
                  v-for="genre in getGenreArray(pickedMedia.genres)"
                  :key="genre"
                  size="small"
                  variant="tonal"
                  class="mr-2"
                >
                  {{ genre }}
                </v-chip>
              </div>

              <p v-if="pickedMedia.director" class="text-body-1 mb-2">
                <strong>{{ pickedMedia.mediaType === 'tv' ? 'Created by' : 'Director' }}:</strong> 
                {{ pickedMedia.director }}
              </p>

              <p v-if="pickedMedia.cast && pickedMedia.cast.length > 0" class="text-body-1 mb-4">
                <strong>Cast:</strong> 
                {{ pickedMedia.cast.slice(0, 5).map(c => c.name).join(', ') }}
              </p>

              <v-divider class="my-4" />
              <v-row>
                <v-col cols="12" sm="6">
                  <v-btn
                    color="success"
                    size="large"
                    block
                    @click="markAsWatched"
                    prepend-icon="mdi-check-circle"
                  >
                    I Watched This
                  </v-btn>
                </v-col>
                <v-col cols="12" sm="3">
                  <v-btn
                    variant="outlined"
                    size="large"
                    block
                    @click="viewDetails"
                    prepend-icon="mdi-information"
                  >
                    Details
                  </v-btn>
                </v-col>
                <v-col cols="12" sm="3">
                  <v-btn
                    color="primary"
                    size="large"
                    block
                    @click="pickAnother"
                    prepend-icon="mdi-refresh"
                  >
                    Pick Another
                  </v-btn>
                </v-col>
              </v-row>
            </v-card-text>
          </v-col>
        </v-row>
      </v-card>

      <v-row v-if="!pickedMedia">
        <v-col cols="12" sm="6" md="3">
          <v-card variant="outlined">
            <v-card-text class="text-center">
              <div class="text-h4 font-weight-bold text-primary">{{ watchlist.length }}</div>
              <div class="text-caption">Items on Watchlist</div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-card variant="outlined">
            <v-card-text class="text-center">
              <div class="text-h4 font-weight-bold text-secondary">{{ movieCount }}</div>
              <div class="text-caption">Movies</div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-card variant="outlined">
            <v-card-text class="text-center">
              <div class="text-h4 font-weight-bold text-secondary">{{ tvCount }}</div>
              <div class="text-caption">TV Shows</div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-card variant="outlined">
            <v-card-text class="text-center">
              <div class="text-h4 font-weight-bold text-info">{{ estimatedHours }}</div>
              <div class="text-caption">Hours to Watch</div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <v-dialog v-model="showRatingDialog" max-width="500">
      <v-card>
        <v-card-title>Rate {{ pickedMedia?.title }}</v-card-title>
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
            label="Notes (optional)"
            variant="outlined"
            rows="3"
            class="mt-4"
          />

          <v-text-field
            v-if="pickedMedia?.mediaType === 'tv' && pickedMedia?.numberOfSeasons"
            v-model.number="seasonsWatched"
            label="Seasons watched (optional)"
            type="number"
            variant="outlined"
            :max="pickedMedia.numberOfSeasons"
            min="1"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="showRatingDialog = false">Cancel</v-btn>
          <v-btn
            color="primary"
            @click="saveRating"
            :loading="saving"
            :disabled="!userRating"
          >
            Save & Mark Watched
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mediaAPI } from '@/services/api-production';

export default {
  name: 'RandomPickerView',
  
  data() {
    return {
      loading: false,
      watchlist: [],
      pickedMedia: null,
      
      // Filters
      filters: {
        type: null,
        genre: null,
        runtime: null,
        decade: null,
      },
      
      typeOptions: [
        { title: 'Movies', value: 'movie' },
        { title: 'TV Shows', value: 'tv' },
      ],
      
      runtimeOptions: [
        { title: 'Short (< 90 min)', value: 'short' },
        { title: 'Medium (90-120 min)', value: 'medium' },
        { title: 'Long (> 120 min)', value: 'long' },
      ],
      
      // Rating dialog
      showRatingDialog: false,
      userRating: null,
      userNotes: '',
      seasonsWatched: null,
      saving: false,
    };
  },
  
  computed: {
    filteredWatchlist() {
      let result = [...this.watchlist];
      
      // Type filter
      if (this.filters.type) {
        result = result.filter(m => m.mediaType === this.filters.type);
      }
      
      // Genre filter
      if (this.filters.genre) {
        result = result.filter(m => {
          if (!m.genres) return false;
          const genres = Array.isArray(m.genres) ? m.genres : m.genres.split(', ');
          return genres.includes(this.filters.genre);
        });
      }
      
      // Runtime filter (movies only)
      if (this.filters.runtime && (!this.filters.type || this.filters.type === 'movie')) {
        result = result.filter(m => {
          if (m.mediaType !== 'movie' || !m.runtime) return false;
          
          if (this.filters.runtime === 'short') return m.runtime < 90;
          if (this.filters.runtime === 'medium') return m.runtime >= 90 && m.runtime <= 120;
          if (this.filters.runtime === 'long') return m.runtime > 120;
          return true;
        });
      }
      
      // Decade filter
      if (this.filters.decade) {
        result = result.filter(m => {
          if (!m.releaseYear) return false;
          const decade = Math.floor(m.releaseYear / 10) * 10;
          return decade === parseInt(this.filters.decade);
        });
      }
      
      return result;
    },
    
    availableGenres() {
      const genreSet = new Set();
      this.watchlist.forEach(m => {
        if (m.genres) {
          const genres = Array.isArray(m.genres) ? m.genres : m.genres.split(', ');
          genres.forEach(g => genreSet.add(g));
        }
      });
      return Array.from(genreSet).sort();
    },
    
    decadeOptions() {
      const decades = new Set();
      this.watchlist.forEach(m => {
        if (m.releaseYear) {
          const decade = Math.floor(m.releaseYear / 10) * 10;
          decades.add(decade);
        }
      });
      return Array.from(decades)
        .sort((a, b) => b - a)
        .map(d => ({ title: `${d}s`, value: d }));
    },
    
    hasActiveFilters() {
      return Object.values(this.filters).some(v => v !== null);
    },
    
    movieCount() {
      return this.watchlist.filter(m => m.mediaType === 'movie').length;
    },
    
    tvCount() {
      return this.watchlist.filter(m => m.mediaType === 'tv').length;
    },
    
    estimatedHours() {
      let totalMinutes = 0;
      this.watchlist.forEach(m => {
        if (m.mediaType === 'movie' && m.runtime) {
          totalMinutes += m.runtime;
        } else if (m.mediaType === 'tv' && m.numberOfEpisodes) {
          totalMinutes += m.numberOfEpisodes * 45;
        }
      });
      return Math.round(totalMinutes / 60);
    },
  },
  
  created() {
    this.loadWatchlist();
  },

  async mounted() {
  // NEW: Auto-pick after watchlist loads
  if (this.watchlist.length > 0) {
    await this.$nextTick();
    this.pickRandom();
  }
},
  
  methods: {
    async loadWatchlist() {
      this.loading = true;
      try {
        const allMedia = await mediaAPI.getAll();
        this.watchlist = allMedia.filter(m => m.status === 'want_to_watch');
        
        // NEW: Auto-pick after loading
        if (this.watchlist.length > 0) {
          await this.$nextTick();
          this.pickRandom();
        }
      } catch (err) {
        console.error('Error loading watchlist:', err);
      } finally {
        this.loading = false;
      }
    },
    
    pickRandom() {
      if (this.filteredWatchlist.length === 0) return;
      
      const randomIndex = Math.floor(Math.random() * this.filteredWatchlist.length);
      this.pickedMedia = this.filteredWatchlist[randomIndex];
    },
    
    pickAnother() {
      this.pickRandom();
    },
    
    clearFilters() {
      this.filters = {
        type: null,
        genre: null,
        runtime: null,
        decade: null,
      },
      this.loadWatchlist();
    },
    
    markAsWatched() {
      this.showRatingDialog = true;
    },
    
    async saveRating() {
      if (!this.userRating) return;
      
      this.saving = true;
      
      try {
        const updateData = {
          status: 'watched',
          rating: this.userRating,
          notes: this.userNotes || null,
        };
        
        if (this.pickedMedia.mediaType === 'tv' && this.seasonsWatched) {
          updateData.seasonsWatched = this.seasonsWatched;
        }
        
        await mediaAPI.update(this.pickedMedia.mediaId, updateData);
        
        // Remove from watchlist
        this.watchlist = this.watchlist.filter(m => m.mediaId !== this.pickedMedia.mediaId);
        
        // Reset
        this.showRatingDialog = false;
        this.pickedMedia = null;
        this.userRating = null;
        this.userNotes = '';
        this.seasonsWatched = null;
        
      } catch (err) {
        console.error('Save error:', err);
      } finally {
        this.saving = false;
      }
    },
    
    viewDetails() {
      this.$router.push(`/media/${this.pickedMedia.mediaId}`);
    },
    
    getGenreArray(genres) {
      return Array.isArray(genres) ? genres : genres.split(', ');
    },
  },
};
</script>

<style scoped>
.random-picker {
  max-width: 1200px;
  margin: 0 auto;
}

/* NEW: Dashed border for empty state */
.empty-dashed-border {
  border: 2px dashed rgba(var(--v-theme-on-surface), 0.2) !important;
}

/* NEW: Background circle for icon */
.icon-bg-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background-color: rgba(var(--v-theme-primary), 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.gap-4 {
  gap: 16px;
}

/* FIXED: Button with centered text */
.pick-button {
  padding: 32px 64px !important;
  font-size: 1.5rem !important;
  font-weight: bold;
  min-height: 80px !important;
}

.pick-button .d-flex {
  width: 100%;
  height: 100%;
}

.picked-card {
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.picked-hero {
  position: relative;
}

.picked-hero-content {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
}

.picked-fallback {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 200px;
  color: white;
}

.gap-2 {
  gap: 8px;
}
</style>
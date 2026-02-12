<template>
  <v-dialog
    v-model="isOpen"
    max-width="1000"
    scrollable
    @click:outside="close"
  >
    <v-card>
      <v-card-title class="d-flex align-center pa-4 sticky-header">
        <v-icon class="mr-2">mdi-plus-circle</v-icon>
        <span class="text-h5">Add Media</span>
        <v-spacer />
        <v-btn icon variant="text" @click="close">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-divider />

      <!-- Search Section -->
      <v-card-text class="pa-4">
        <v-text-field
          v-model="searchQuery"
          label="Search for movies or TV shows..."
          prepend-inner-icon="mdi-magnify"
          variant="outlined"
          clearable
          autofocus
          @keyup.enter="search"
          @click:clear="clearSearch"
          hint="Press Enter to search"
          persistent-hint
          :loading="searching"
        />

        <!-- Loading State -->
        <div v-if="searching" class="text-center py-12">
          <v-progress-circular indeterminate size="64" color="primary" />
          <p class="text-body-1 mt-4">Searching TMDB...</p>
        </div>

        <!-- Empty State -->
        <v-empty-state
          v-else-if="!searchResults.length && searchQuery && !searching"
          icon="mdi-magnify-close"
          title="No Results"
          text="Try a different search term"
        />

        <!-- IMPROVED: Results with Quick Actions -->
        <div v-else-if="searchResults.length" class="mt-4">
          <p class="text-caption text-medium-emphasis mb-2">
            {{ searchResults.length }} results found
          </p>

          <!-- Desktop: Card Grid with Quick Actions -->
          <v-row v-if="!isMobile">
            <v-col
              v-for="item in searchResults"
              :key="item.tmdbId"
              cols="6"
              sm="4"
              md="3"
            >
              <v-card class="result-card" hover>
                <!-- Poster -->
                <v-img
                  v-if="item.posterUrl"
                  :src="item.posterUrl"
                  aspect-ratio="2/3"
                  cover
                  @click="viewDetails(item)"
                >
                  <!-- Already in collection badge -->
                  <div v-if="isInCollection(item.tmdbId)" class="collection-badge">
                    <v-chip size="small" color="success" variant="flat">
                      <v-icon start size="small">mdi-check</v-icon>
                      In Library
                    </v-chip>
                  </div>
                </v-img>

                <v-img
                  v-else
                  src="/placeholder-poster.png"
                  aspect-ratio="2/3"
                  @click="viewDetails(item)"
                >
                  <div class="d-flex align-center justify-center fill-height bg-grey-darken-3">
                    <v-icon size="64" color="grey">mdi-image-off</v-icon>
                  </div>
                </v-img>

                <!-- Title -->
                <v-card-text class="pa-2 pb-0">
                  <p class="text-caption font-weight-bold text-truncate mb-1">
                    {{ item.title }}
                  </p>
                  <p class="text-caption text-medium-emphasis">
                    {{ item.releaseYear }}
                  </p>
                </v-card-text>

                <!-- Quick Action Buttons -->
                <v-card-actions class="pa-2 pt-0">
                  <v-btn
                    v-if="!isInCollection(item.tmdbId)"
                    size="x-small"
                    color="info"
                    variant="tonal"
                    block
                    @click="quickAdd(item, 'want_to_watch')"
                    :loading="adding === `${item.tmdbId}-watchlist`"
                  >
                    <v-icon start size="14">mdi-bookmark-plus</v-icon>
                    Watchlist
                  </v-btn>
                  <v-btn
                    v-else
                    size="x-small"
                    variant="outlined"
                    block
                    @click="goToExisting(item.tmdbId)"
                  >
                    View
                  </v-btn>
                </v-card-actions>
                
                <v-card-actions class="pa-2 pt-0">
                  <v-btn
                    v-if="!isInCollection(item.tmdbId)"
                    size="x-small"
                    color="primary"
                    variant="tonal"
                    block
                    @click="openRatingDialog(item)"
                  >
                    <v-icon start size="14">mdi-star</v-icon>
                    Rate
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>

          <!-- Mobile: Compact List with Quick Actions -->
          <v-list v-else class="mobile-results">
            <v-list-item
              v-for="item in searchResults"
              :key="item.tmdbId"
              class="mb-2 result-list-item"
            >
              <template v-slot:prepend>
                <v-avatar size="80" rounded class="mr-3" @click="viewDetails(item)">
                  <v-img v-if="item.posterUrl" :src="item.posterUrl" cover />
                  <v-icon v-else size="40">mdi-movie-outline</v-icon>
                </v-avatar>
              </template>

              <v-list-item-title class="text-body-2 font-weight-bold">
                {{ item.title }}
                <v-chip
                  v-if="isInCollection(item.tmdbId)"
                  size="x-small"
                  color="success"
                  class="ml-1"
                >
                  In Library
                </v-chip>
              </v-list-item-title>
              
              <v-list-item-subtitle class="text-caption">
                {{ item.mediaType === 'movie' ? 'Movie' : 'TV' }} • {{ item.releaseYear }}
              </v-list-item-subtitle>

              <!-- Mobile Quick Actions -->
              <template v-slot:append>
                <div class="d-flex flex-column gap-1">
                  <v-btn
                    v-if="!isInCollection(item.tmdbId)"
                    size="x-small"
                    color="info"
                    icon
                    variant="tonal"
                    @click="quickAdd(item, 'want_to_watch')"
                    :loading="adding === `${item.tmdbId}-watchlist`"
                  >
                    <v-icon size="16">mdi-bookmark-plus</v-icon>
                  </v-btn>
                  <v-btn
                    v-if="!isInCollection(item.tmdbId)"
                    size="x-small"
                    color="primary"
                    icon
                    variant="tonal"
                    @click="openRatingDialog(item)"
                  >
                    <v-icon size="16">mdi-star</v-icon>
                  </v-btn>
                  <v-btn
                    v-if="isInCollection(item.tmdbId)"
                    size="x-small"
                    icon
                    variant="outlined"
                    @click="goToExisting(item.tmdbId)"
                  >
                    <v-icon size="16">mdi-eye</v-icon>
                  </v-btn>
                </div>
              </template>
            </v-list-item>
          </v-list>
        </div>

        <!-- Initial State -->
        <v-empty-state
          v-else
          icon="mdi-movie-search"
          title="Search TMDB"
          text="Search for any movie or TV show to add to your collection"
          class="my-8"
        />
      </v-card-text>
    </v-card>

    <!-- Rating Dialog (for "Rate" button) -->
    <v-dialog v-model="showRatingDialog" max-width="500">
      <v-card v-if="itemToRate">
        <v-card-title>Rate {{ itemToRate.title }}</v-card-title>
        <v-card-text>
          <div class="d-flex align-center mb-4">
            <v-avatar size="60" rounded class="mr-3">
              <v-img v-if="itemToRate.posterUrl" :src="itemToRate.posterUrl" />
            </v-avatar>
            <div>
              <p class="text-body-1 font-weight-bold mb-0">{{ itemToRate.title }}</p>
              <p class="text-caption text-medium-emphasis">
                {{ itemToRate.mediaType === 'movie' ? 'Movie' : 'TV Show' }} • {{ itemToRate.releaseYear }}
              </p>
            </div>
          </div>

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
            rows="2"
            class="mt-4"
            placeholder="What did you think?"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="closeRatingDialog">Cancel</v-btn>
          <v-btn
            color="primary"
            @click="saveWithRating"
            :loading="adding === `${itemToRate.tmdbId}-rated`"
            :disabled="!userRating"
          >
            Add to Library
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Success Snackbar -->
    <v-snackbar v-model="showSnackbar" :color="snackbarColor" timeout="3000">
      {{ snackbarMessage }}
    </v-snackbar>
  </v-dialog>
</template>

<script>
import { tmdbAPI, mediaAPI } from '@/services/api-production';

export default {
  name: 'AddMediaDialog',

  props: {
    modelValue: {
      type: Boolean,
      default: false
    }
  },

  emits: ['update:modelValue', 'media-added'],

  data() {
    return {
      searchQuery: '',
      searching: false,
      searchResults: [],
      adding: null, // Tracks which item is being added (tmdbId-action)
      userCollection: [],
      
      // Rating dialog
      showRatingDialog: false,
      itemToRate: null,
      userRating: null,
      userNotes: '',
      
      // Snackbar
      showSnackbar: false,
      snackbarMessage: '',
      snackbarColor: 'success'
    };
  },

  computed: {
    isOpen: {
      get() {
        return this.modelValue;
      },
      set(val) {
        this.$emit('update:modelValue', val);
      }
    },
    
    isMobile() {
      return this.$vuetify.display.mobile;
    }
  },

  watch: {
    isOpen(val) {
      if (val) {
        this.loadUserCollection();
      } else {
        this.reset();
      }
    }
  },

  methods: {
    async loadUserCollection() {
      try {
        this.userCollection = await mediaAPI.getAll();
      } catch (err) {
        console.error('Error loading collection:', err);
      }
    },

    async search() {
      if (!this.searchQuery || this.searchQuery.trim().length < 2) return;

      this.searching = true;

      try {
        this.searchResults = await tmdbAPI.search(this.searchQuery);
      } catch (err) {
        console.error('Search error:', err);
        this.searchResults = [];
        this.showMessage('Search failed. Please try again.', 'error');
      } finally {
        this.searching = false;
      }
    },

    // Quick add to watchlist (1-click)
    async quickAdd(item, status) {
      const addKey = `${item.tmdbId}-watchlist`;
      this.adding = addKey;

      try {
        const mediaData = {
          title: item.title,
          media_type: item.mediaType,
          tmdb_id: item.tmdbId,
          status: status,
          release_year: item.releaseYear,
          plot: item.plot,
          poster_url: item.posterUrl,
          backdrop_url: item.backdropUrl,
          tmdb_rating: item.tmdbRating
        };

        const created = await mediaAPI.create(mediaData);

        // Update local collection
        this.userCollection.push(created);

        // Show success message
        this.showMessage(`Added "${item.title}" to watchlist!`, 'success');

        // Emit event
        this.$emit('media-added', created);

      } catch (err) {
        console.error('Error adding media:', err);
        this.showMessage('Failed to add. Please try again.', 'error');
      } finally {
        this.adding = null;
      }
    },

    // Open rating dialog
    openRatingDialog(item) {
      this.itemToRate = item;
      this.userRating = null;
      this.userNotes = '';
      this.showRatingDialog = true;
    },

    closeRatingDialog() {
      this.showRatingDialog = false;
      this.itemToRate = null;
      this.userRating = null;
      this.userNotes = '';
    },

    // Save with rating
    async saveWithRating() {
      if (!this.itemToRate || !this.userRating) return;

      const addKey = `${this.itemToRate.tmdbId}-rated`;
      this.adding = addKey;

      try {
        const mediaData = {
          title: this.itemToRate.title,
          media_type: this.itemToRate.mediaType,
          tmdb_id: this.itemToRate.tmdbId,
          status: 'watched',
          rating: this.userRating,
          notes: this.userNotes || null,
          release_year: this.itemToRate.releaseYear,
          plot: this.itemToRate.plot,
          poster_url: this.itemToRate.posterUrl,
          backdrop_url: this.itemToRate.backdropUrl,
          tmdb_rating: this.itemToRate.tmdbRating
        };

        const created = await mediaAPI.create(mediaData);

        // Update collection
        this.userCollection.push(created);

        // Close dialogs
        this.closeRatingDialog();
        this.close();

        // used to navigate to detail page now stays on page
        this.showMessage(`Rated "${this.itemToRate.title}" - ${this.userRating} stars!`, 'success');
        this.closeRatingDialog();
        

      } catch (err) {
        console.error('Error adding media:', err);
        this.showMessage('Failed to add. Please try again.', 'error');
      } finally {
        this.adding = null;
      }
    },

    // View full details (optional enhancement)
    viewDetails(item) {
      // Could show expanded modal with full plot, cast, etc.
      // For now, just opens rating dialog
      this.openRatingDialog(item);
    },

    isInCollection(tmdbId) {
      return this.userCollection.some(m => m.tmdbId === tmdbId);
    },

    goToExisting(tmdbId) {
      const existing = this.userCollection.find(m => m.tmdbId === tmdbId);
      if (existing) {
        this.$router.push(`/media/${existing.mediaId}`);
        this.close();
      }
    },

    clearSearch() {
      this.searchQuery = '';
      this.searchResults = [];
    },

    reset() {
      this.searchQuery = '';
      this.searchResults = [];
      this.searching = false;
      this.adding = null;
      this.closeRatingDialog();
    },

    close() {
      this.isOpen = false;
    },

    showMessage(message, color = 'success') {
      this.snackbarMessage = message;
      this.snackbarColor = color;
      this.showSnackbar = true;
    }
  }
};
</script>

<style scoped>
.sticky-header {
  position: sticky;
  top: 0;
  z-index: 10;
  background: rgb(var(--v-theme-surface));
}

.result-card {
  cursor: pointer;
  transition: all 0.2s ease;
}

.result-card:hover {
  transform: translateY(-4px);
}

.collection-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  right: 8px;
  display: flex;
  justify-content: center;
}

.mobile-results {
  background: transparent;
}

.result-list-item {
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  border-radius: 8px;
  background: rgb(var(--v-theme-surface));
}

.gap-1 {
  gap: 4px;
}
/* Added to dialog */
:deep(.add-media-dialog) {
  align-self: flex-start !important;
  margin-top: 80px !important; /* Below header */
}
</style>
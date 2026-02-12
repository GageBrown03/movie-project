<template>
  <v-dialog
    v-model="isOpen"
    max-width="900"
    scrollable
    @click:outside="close"
  >
    <v-card>
      <v-card-title class="d-flex align-center pa-4">
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

        <!-- Results Grid -->
        <v-row v-else-if="searchResults.length" class="mt-4">
          <v-col
            v-for="item in searchResults"
            :key="item.id"
            cols="6"
            sm="4"
            md="3"
          >
            <v-card
              :class="['result-card', { 'result-card--selected': isInCollection(item.id) }]"
              @click="selectItem(item)"
              hover
            >
              <v-img
                v-if="item.poster_path"
                :src="`https://image.tmdb.org/t/p/w342${item.poster_path}`"
                aspect-ratio="2/3"
                cover
              >
                <template v-slot:placeholder>
                  <div class="d-flex align-center justify-center fill-height">
                    <v-progress-circular indeterminate color="primary" />
                  </div>
                </template>

                <!-- Already in collection badge -->
                <div v-if="isInCollection(item.id)" class="collection-badge">
                  <v-chip size="small" color="success" variant="flat">
                    <v-icon start size="small">mdi-check</v-icon>
                    In Collection
                  </v-chip>
                </div>
              </v-img>

              <v-img
                v-else
                src="/placeholder-poster.png"
                aspect-ratio="2/3"
                cover
              >
                <div class="d-flex align-center justify-center fill-height bg-grey-darken-3">
                  <v-icon size="64" color="grey">mdi-image-off</v-icon>
                </div>
              </v-img>

              <v-card-text class="pa-2">
                <p class="text-caption font-weight-bold text-truncate mb-1">
                  {{ item.title || item.name }}
                </p>
                <p class="text-caption text-medium-emphasis">
                  {{ getReleaseYear(item) }}
                </p>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Initial State -->
        <v-empty-state
          v-else
          icon="mdi-movie-search"
          title="Search TMDB"
          text="Search for any movie or TV show to add to your collection"
          class="my-8"
        />
      </v-card-text>

      <!-- Quick Add Actions (when item selected) -->
      <v-card-actions v-if="selectedItem" class="pa-4 bg-surface-light">
        <div class="w-100">
          <div class="d-flex align-center mb-3">
            <v-avatar size="48" rounded class="mr-3">
              <v-img
                v-if="selectedItem.poster_path"
                :src="`https://image.tmdb.org/t/p/w92${selectedItem.poster_path}`"
              />
            </v-avatar>
            <div class="flex-grow-1">
              <p class="text-body-1 font-weight-bold mb-0">
                {{ selectedItem.title || selectedItem.name }}
              </p>
              <p class="text-caption text-medium-emphasis">
                {{ selectedItem.media_type === 'movie' ? 'Movie' : 'TV Show' }} • {{ getReleaseYear(selectedItem) }}
              </p>
            </div>
          </div>

          <div class="d-flex gap-2">
            <v-btn
              color="primary"
              variant="flat"
              prepend-icon="mdi-eye-check"
              @click="quickAdd('watched')"
              :loading="adding"
              block
            >
              Mark as Watched
            </v-btn>
            <v-btn
              color="info"
              variant="flat"
              prepend-icon="mdi-bookmark-plus"
              @click="quickAdd('want_to_watch')"
              :loading="adding"
              block
            >
              Add to Watchlist
            </v-btn>
          </div>
        </div>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { tmdbAPI } from '@/services/tmdb';
import { mediaAPI } from '@/services/api-production';

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
      selectedItem: null,
      adding: false,
      userCollection: []
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
      this.selectedItem = null;

      try {
        const results = await tmdbAPI.searchMulti(this.searchQuery);
        // Filter to only movies and TV shows
        this.searchResults = results.filter(
          item => item.media_type === 'movie' || item.media_type === 'tv'
        ).slice(0, 12); // Limit to 12 results
      } catch (err) {
        console.error('Search error:', err);
        this.searchResults = [];
      } finally {
        this.searching = false;
      }
    },

    selectItem(item) {
      // If already in collection, navigate to it
      if (this.isInCollection(item.id)) {
        const existing = this.userCollection.find(m => m.tmdbId === item.id);
        if (existing) {
          this.$router.push(`/movies/${existing.mediaId}`);
          this.close();
        }
        return;
      }

      this.selectedItem = item;
    },

    async quickAdd(status) {
      if (!this.selectedItem) return;

      this.adding = true;

      try {
        const mediaData = {
          title: this.selectedItem.title || this.selectedItem.name,
          media_type: this.selectedItem.media_type,
          tmdb_id: this.selectedItem.id,
          status: status,
          release_year: this.getReleaseYear(this.selectedItem),
          plot: this.selectedItem.overview,
          poster_url: this.selectedItem.poster_path
            ? `https://image.tmdb.org/t/p/w342${this.selectedItem.poster_path}`
            : null,
          backdrop_url: this.selectedItem.backdrop_path
            ? `https://image.tmdb.org/t/p/w1280${this.selectedItem.backdrop_path}`
            : null,
          tmdb_rating: this.selectedItem.vote_average
        };

        const created = await mediaAPI.create(mediaData);

        // Emit success event
        this.$emit('media-added', created);

        // Navigate to the new media page
        this.$router.push(`/movies/${created.mediaId}`);
        this.close();

      } catch (err) {
        console.error('Error adding media:', err);
        alert('Failed to add media. Please try again.');
      } finally {
        this.adding = false;
      }
    },

    isInCollection(tmdbId) {
      return this.userCollection.some(m => m.tmdbId === tmdbId);
    },

    getReleaseYear(item) {
      const date = item.release_date || item.first_air_date;
      return date ? new Date(date).getFullYear() : 'N/A';
    },

    clearSearch() {
      this.searchQuery = '';
      this.searchResults = [];
      this.selectedItem = null;
    },

    reset() {
      this.searchQuery = '';
      this.searchResults = [];
      this.selectedItem = null;
      this.searching = false;
    },

    close() {
      this.isOpen = false;
    }
  }
};
</script>

<style scoped>
.result-card {
  cursor: pointer;
  transition: all 0.2s ease;
}

.result-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.result-card--selected {
  border: 2px solid rgb(var(--v-theme-primary));
}

.collection-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  right: 8px;
  display: flex;
  justify-content: center;
}

.gap-2 {
  gap: 8px;
}
</style>
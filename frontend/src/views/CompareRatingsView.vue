<template>
  <div class="compare-ratings-view">
    <!-- Header -->
    <v-row class="mb-6 align-center">
      <v-col>
        <v-btn
          variant="text"
          prepend-icon="mdi-arrow-left"
          @click="$router.back()"
        >
          Back
        </v-btn>
        
        <h1 class="text-h3 font-weight-bold mt-4">
          Compare Ratings
          <span v-if="friendData" class="text-medium-emphasis">
            with {{ friendData.username }}
          </span>
        </h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          See how your tastes align
        </p>
      </v-col>
    </v-row>

    <!-- Loading State -->
    <v-row v-if="loading" justify="center" class="my-12">
      <v-progress-circular indeterminate size="64" color="primary" />
    </v-row>

    <!-- Error State -->
    <v-alert v-else-if="error" type="error" variant="tonal" class="mb-6">
      {{ error }}
    </v-alert>

    <div v-else-if="comparison">
      <!-- Stats Cards -->
      <v-row class="mb-6">
        <v-col cols="6" sm="3">
          <v-card>
            <v-card-text class="text-center">
              <div class="text-h3 font-weight-bold text-primary">
                {{ comparison.stats.totalCommon }}
              </div>
              <div class="text-caption text-medium-emphasis">
                Media in Common
              </div>
            </v-card-text>
          </v-card>
        </v-col>
        
        <v-col cols="6" sm="3">
          <v-card>
            <v-card-text class="text-center">
              <div class="text-h3 font-weight-bold" :class="agreementColor">
                {{ comparison.stats.agreementRate }}%
              </div>
              <div class="text-caption text-medium-emphasis">
                Agreement Rate
              </div>
            </v-card-text>
          </v-card>
        </v-col>
        
        <v-col cols="6" sm="3">
          <v-card>
            <v-card-text class="text-center">
              <div class="text-h3 font-weight-bold text-success">
                {{ comparison.stats.bothLovedCount }}
              </div>
              <div class="text-caption text-medium-emphasis">
                Both Loved (5★)
              </div>
            </v-card-text>
          </v-card>
        </v-col>
        
        <v-col cols="6" sm="3">
          <v-card>
            <v-card-text class="text-center">
              <div class="text-h3 font-weight-bold text-warning">
                {{ comparison.biggestDisagreements.length }}
              </div>
              <div class="text-caption text-medium-emphasis">
                Big Disagreements
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Filter & Sort -->
      <v-card class="mb-6">
        <v-card-text>
          <v-row class="align-center">
            <v-col cols="12" md="6">
              <v-select
                v-model="filterType"
                :items="filterOptions"
                label="Filter"
                variant="outlined"
                density="comfortable"
              />
            </v-col>
            
            <v-col cols="12" md="6">
              <v-select
                v-model="sortBy"
                :items="sortOptions"
                label="Sort by"
                variant="outlined"
                density="comfortable"
              />
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Comparisons List -->
      <div v-if="filteredComparisons.length > 0">
        <v-card
          v-for="item in filteredComparisons"
          :key="item.tmdbId"
          class="mb-4 comparison-card"
        >
          <v-row no-gutters>
            <!-- Poster -->
            <v-col cols="auto">
              <v-img
                v-if="item.posterUrl"
                :src="item.posterUrl"
                width="100"
                aspect-ratio="2/3"
                cover
              />
              <div v-else class="poster-placeholder">
                <v-icon size="large">mdi-movie-outline</v-icon>
              </div>
            </v-col>
            
            <!-- Content -->
            <v-col>
              <v-card-text>
                <!-- Title -->
                <h3 class="text-h6 mb-2">
                  {{ item.title }}
                  <v-chip
                    v-if="item.releaseYear"
                    size="small"
                    variant="tonal"
                    class="ml-2"
                  >
                    {{ item.releaseYear }}
                  </v-chip>
                </h3>

                <!-- Ratings -->
                <v-row class="mt-4">
                  <!-- Your Rating -->
                  <v-col cols="5">
                    <div class="text-caption text-medium-emphasis mb-1">
                      Your Rating
                    </div>
                    <div class="d-flex align-center">
                      <v-rating
                        :model-value="item.myRating"
                        readonly
                        density="compact"
                        color="amber"
                        size="small"
                      />
                    </div>
                  </v-col>

                  <!-- Difference -->
                  <v-col cols="2" class="text-center d-flex align-center justify-center">
                    <v-chip
                      :color="getDifferenceColor(item.difference)"
                      variant="tonal"
                    >
                      {{ item.difference > 0 ? '+' : '' }}{{ item.difference }}
                    </v-chip>
                  </v-col>

                  <!-- Friend's Rating -->
                  <v-col cols="5">
                    <div class="text-caption text-medium-emphasis mb-1">
                      {{ friendData.username }}'s
                    </div>
                    <div class="d-flex align-center">
                      <v-rating
                        :model-value="item.friendRating"
                        readonly
                        density="compact"
                        color="amber"
                        size="small"
                      />
                      
                    </div>
                  </v-col>
                </v-row>

                <!-- Agreement Indicator -->
                <div class="mt-3">
                  <v-chip
                    v-if="item.agreement"
                    color="success"
                    size="small"
                    variant="tonal"
                    prepend-icon="mdi-check"
                  >
                    You agree!
                  </v-chip>
                  <v-chip
                    v-else
                    color="error"
                    size="small"
                    variant="tonal"
                    prepend-icon="mdi-close"
                  >
                    {{ getDifferenceText(item.difference) }}
                  </v-chip>
                </div>
              </v-card-text>
            </v-col>
          </v-row>
        </v-card>
      </div>

      <!-- Empty State -->
      <v-card v-else class="text-center pa-12">
        <v-icon size="64" color="grey">mdi-filter-off</v-icon>
        <h3 class="text-h5 mt-4">No matches</h3>
        <p class="text-body-2 text-medium-emphasis">Try adjusting your filters</p>
      </v-card>

      <!-- Recommendations Section - WITH WORKING QUICK ADD -->
      <v-row class="mt-6" v-if="comparison.recommendationsForMe.length > 0">
        <v-col cols="12">
          <h2 class="text-h5 font-weight-bold mb-4">
            <v-icon color="primary" class="mr-2">mdi-lightbulb</v-icon>
            {{ friendData.username }} Recommends for You
          </h2>
          <p class="text-body-2 text-medium-emphasis mb-4">
            Media {{ friendData.username }} loved (4-5★) that you haven't seen yet
          </p>

          <v-row>
            <v-col
              v-for="rec in comparison.recommendationsForMe.slice(0, 6)"
              :key="rec.tmdbId"
              cols="6"
              sm="4"
              md="2"
            >
              <v-card hover class="recommendation-card">
                <v-img
                  v-if="rec.posterUrl"
                  :src="rec.posterUrl"
                  aspect-ratio="2/3"
                  cover
                />
                <v-card-text class="pa-2">
                  <div class="text-caption font-weight-bold text-truncate" :title="rec.title">
                    {{ rec.title }}
                  </div>
                  <v-rating
                    :model-value="rec.rating"
                    readonly
                    density="compact"
                    color="amber"
                    size="x-small"
                  />
                </v-card-text>
                
                <!-- Quick Add Buttons -->
                <v-card-actions class="pa-2 pt-0">
                  <v-btn
                    v-if="!isInCollection(rec.tmdbId)"
                    size="x-small"
                    color="info"
                    variant="tonal"
                    block
                    @click="quickAddToWatchlist(rec)"
                    :loading="loadingStates[rec.tmdbId] === 'watchlist'"
                  >
                    <v-icon start size="14">mdi-bookmark-plus</v-icon>
                    Watchlist
                  </v-btn>
                  <v-btn
                    v-else
                    size="x-small"
                    variant="outlined"
                    block
                    @click="goToExisting(rec.tmdbId)"
                  >
                    View
                  </v-btn>
                </v-card-actions>
                <v-card-actions class="pa-2 pt-0">
                  <v-btn
                    v-if="!isInCollection(rec.tmdbId)"
                    size="x-small"
                    color="primary"
                    variant="tonal"
                    block
                    @click="openRatingDialog(rec)"
                  >
                    <v-icon start size="14">mdi-star</v-icon>
                    Rate
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </div>

    <!-- Rating Dialog -->
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
                Movie • {{ itemToRate.releaseYear }}
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
            :loading="savingRating"
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
      <template v-slot:actions>
        <v-btn variant="text" @click="showSnackbar = false">Close</v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
// FIXED: Added missing imports
import { compareAPI, tmdbAPI, mediaAPI } from '@/services/api-production';

export default {
  name: 'CompareRatingsView',
  
  data() {
    return {
      loading: false,
      error: null,
      comparison: null,
      friendData: null,
      
      filterType: 'all',
      filterOptions: [
        { title: 'All Comparisons', value: 'all' },
        { title: 'Agreements (within 1★)', value: 'agreements' },
        { title: 'Disagreements (3+ stars)', value: 'disagreements' },
        { title: 'Both Loved (5★)', value: 'both_loved' },
      ],
      
      sortBy: 'difference',
      sortOptions: [
        { title: 'Biggest Difference', value: 'difference' },
        { title: 'Highest Rated (Me)', value: 'my_rating' },
        { title: 'Highest Rated (Friend)', value: 'friend_rating' },
        { title: 'Title (A-Z)', value: 'title' },
      ],

      // Quick add functionality
      userCollection: [],
      loadingStates: {},
      showRatingDialog: false,
      itemToRate: null,
      userRating: null,
      userNotes: '',
      savingRating: false,

      // Snackbar
      showSnackbar: false,
      snackbarMessage: '',
      snackbarColor: 'success'
    };
  },
  
  computed: {
    friendUsername() {
      return this.$route.params.username;
    },
    
    agreementColor() {
      if (!this.comparison) return '';
      const rate = this.comparison.stats.agreementRate;
      if (rate >= 70) return 'text-success';
      if (rate >= 40) return 'text-warning';
      return 'text-error';
    },
    
    filteredComparisons() {
      if (!this.comparison) return [];
      
      let filtered = [...this.comparison.comparisons];
      
      // Apply filter
      switch (this.filterType) {
        case 'agreements':
          filtered = filtered.filter(c => c.agreement);
          break;
        case 'disagreements':
          filtered = filtered.filter(c => Math.abs(c.difference) >= 3);
          break;
        case 'both_loved':
          filtered = filtered.filter(c => c.myRating === 5 && c.friendRating === 5);
          break;
      }
      
      // Apply sort
      switch (this.sortBy) {
        case 'difference':
          filtered.sort((a, b) => Math.abs(b.difference) - Math.abs(a.difference));
          break;
        case 'my_rating':
          filtered.sort((a, b) => b.myRating - a.myRating);
          break;
        case 'friend_rating':
          filtered.sort((a, b) => b.friendRating - a.friendRating);
          break;
        case 'title':
          filtered.sort((a, b) => a.title.localeCompare(b.title));
          break;
      }
      
      return filtered;
    }
  },
  
  created() {
    this.loadComparison();
    this.loadUserCollection();
  },
  
  methods: {
    async loadComparison() {
      this.loading = true;
      this.error = null;
      
      try {
        this.comparison = await compareAPI.getRatings(this.friendUsername);
        this.friendData = this.comparison.friend;
      } catch (err) {
        console.error('Error loading comparison:', err);
        this.error = err.message || 'Failed to load comparison';
      } finally {
        this.loading = false;
      }
    },

    // NEW: Load user collection
    async loadUserCollection() {
      try {
        this.userCollection = await mediaAPI.getAll();
      } catch (err) {
        console.error('Error loading collection:', err);
      }
    },

    // NEW: Check if in collection
    isInCollection(tmdbId) {
      return this.userCollection.some(m => m.tmdbId === tmdbId);
    },
    
    getDifferenceColor(difference) {
      const abs = Math.abs(difference);
      if (abs === 0) return 'success';
      if (abs === 1) return 'info';
      if (abs === 2) return 'warning';
      return 'error';
    },
    
    getDifferenceText(difference) {
      if (difference > 0) {
        return `You liked it ${difference} star${difference > 1 ? 's' : ''} more`;
      } else {
        return `They liked it ${Math.abs(difference)} star${Math.abs(difference) > 1 ? 's' : ''} more`;
      }
    },

    // FIXED: Complete quick add implementation with proper media type handling
    async quickAddToWatchlist(item) {
      this.loadingStates[item.tmdbId] = 'watchlist';
      const mediaTitle = item.title;

      try {
        // Get media type from item (backend now includes it)
        const mediaType = item.mediaType || item.media_type || 'movie';
        
        // Fetch FULL details from TMDB based on correct type
        let fullDetails;
        try {
          if (mediaType === 'tv') {
            fullDetails = await tmdbAPI.getTVDetails(item.tmdbId);
          } else {
            fullDetails = await tmdbAPI.getMovieDetails(item.tmdbId);
          }
        } catch (tmdbError) {
          console.warn('Could not fetch TMDB details:', tmdbError.message);
          throw new Error('Failed to fetch media details');
        }

        // Extract cast data
        const castData = Array.isArray(fullDetails?.cast) ? fullDetails.cast : [];

        // Build complete media data
        const mediaData = {
          title: mediaTitle,
          media_type: mediaType,
          tmdb_id: item.tmdbId,
          status: 'want_to_watch',
          release_year: fullDetails.release_year || item.releaseYear,
          plot: fullDetails.plot || fullDetails.overview,
          poster_url: fullDetails.poster_url || item.posterUrl,
          backdrop_url: fullDetails.backdrop_url,
          tmdb_rating: fullDetails.tmdb_rating || fullDetails.vote_average,
          genres: fullDetails.genres,
          cast: castData
        };

        // Add type-specific fields
        if (mediaType === 'movie') {
          mediaData.director = fullDetails.director;
          mediaData.runtime = fullDetails.runtime;
        } else if (mediaType === 'tv') {
          mediaData.number_of_seasons = fullDetails.number_of_seasons;
          mediaData.number_of_episodes = fullDetails.number_of_episodes;
          mediaData.show_status = fullDetails.status;
        }

        const created = await mediaAPI.create(mediaData);
        
        if (!created || typeof created !== 'object') {
          throw new Error('Invalid response from server');
        }

        this.userCollection.push(created);
        this.showMessage(`Added "${mediaTitle}" to watchlist!`, 'success');

      } catch (err) {
        console.error('Error adding to watchlist:', err);
        const errorMsg = err.message || 'Unknown error';
        this.showMessage(`Failed to add: ${errorMsg}`, 'error');
      } finally {
        delete this.loadingStates[item.tmdbId];
      }
    },
    
    // FIXED: Complete rating dialog
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
    
    // FIXED: Complete save with rating with proper media type handling
    async saveWithRating() {
      if (!this.itemToRate || !this.userRating) return;

      const mediaTitle = this.itemToRate.title;
      const rating = this.userRating;
      const notes = this.userNotes;
      const tmdbId = this.itemToRate.tmdbId;

      this.savingRating = true;

      try {
        // Get media type from item
        const mediaType = this.itemToRate.mediaType || this.itemToRate.media_type || 'movie';
        
        // Fetch FULL details from TMDB based on correct type
        let fullDetails;
        try {
          if (mediaType === 'tv') {
            fullDetails = await tmdbAPI.getTVDetails(tmdbId);
          } else {
            fullDetails = await tmdbAPI.getMovieDetails(tmdbId);
          }
        } catch (tmdbError) {
          console.warn('Could not fetch TMDB details:', tmdbError.message);
          throw new Error('Failed to fetch media details');
        }

        // Extract cast data
        const castData = Array.isArray(fullDetails?.cast) ? fullDetails.cast : [];

        // Build complete media data
        const mediaData = {
          title: mediaTitle,
          media_type: mediaType,
          tmdb_id: tmdbId,
          status: 'watched',
          rating: rating,
          notes: notes || null,
          release_year: fullDetails.release_year || this.itemToRate.releaseYear,
          plot: fullDetails.plot || fullDetails.overview,
          poster_url: fullDetails.poster_url || this.itemToRate.posterUrl,
          backdrop_url: fullDetails.backdrop_url,
          tmdb_rating: fullDetails.tmdb_rating || fullDetails.vote_average,
          genres: fullDetails.genres,
          cast: castData
        };

        // Add type-specific fields
        if (mediaType === 'movie') {
          mediaData.director = fullDetails.director;
          mediaData.runtime = fullDetails.runtime;
        } else if (mediaType === 'tv') {
          mediaData.number_of_seasons = fullDetails.number_of_seasons;
          mediaData.number_of_episodes = fullDetails.number_of_episodes;
          mediaData.show_status = fullDetails.status;
        }

        const created = await mediaAPI.create(mediaData);
        
        if (!created || typeof created !== 'object') {
          throw new Error('Invalid response from server');
        }

        this.userCollection.push(created);

        this.closeRatingDialog();
        this.showMessage(`Rated "${mediaTitle}" - ${rating} stars!`, 'success');

      } catch (err) {
        console.error('Error saving rating:', err);
        const errorMsg = err.message || 'Unknown error';
        this.showMessage(`Failed to save: ${errorMsg}`, 'error');
      } finally {
        this.savingRating = false;
      }
    },

    // NEW: Go to existing media
    goToExisting(tmdbId) {
      const existing = this.userCollection.find(m => m.tmdbId === tmdbId);
      if (existing) {
        this.$router.push(`/media/${existing.mediaId}`);
      }
    },

    // NEW: Show message
    showMessage(message, color = 'success') {
      this.snackbarMessage = message;
      this.snackbarColor = color;
      this.showSnackbar = true;
    }
  }
};
</script>

<style scoped>
.compare-ratings-view {
  max-width: 1200px;
  margin: 0 auto;
}

.comparison-card {
  transition: transform 0.2s ease;
}

.comparison-card:hover {
  transform: translateY(-2px);
}

.poster-placeholder {
  width: 100px;
  aspect-ratio: 2/3;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.1);
}

.recommendation-card {
  transition: transform 0.2s ease;
}

.recommendation-card:hover {
  transform: translateY(-4px);
}
</style>
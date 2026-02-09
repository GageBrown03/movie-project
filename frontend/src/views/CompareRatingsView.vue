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
          See how your movie tastes align
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
                Movies in Common
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
          <v-row align="center">
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
                      <span class="text-h6 ml-2">{{ item.myRating }}</span>
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
                      {{ friendData.username }}'s Rating
                    </div>
                    <div class="d-flex align-center">
                      <v-rating
                        :model-value="item.friendRating"
                        readonly
                        density="compact"
                        color="amber"
                        size="small"
                      />
                      <span class="text-h6 ml-2">{{ item.friendRating }}</span>
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
      <v-empty-state
        v-else
        icon="mdi-filter-off"
        title="No matches"
        text="Try adjusting your filters"
      />

      <!-- Recommendations Section -->
      <v-row class="mt-6" v-if="comparison.recommendationsForMe.length > 0">
        <v-col cols="12">
          <h2 class="text-h5 font-weight-bold mb-4">
            <v-icon color="primary" class="mr-2">mdi-lightbulb</v-icon>
            {{ friendData.username }} Recommends for You
          </h2>
          <p class="text-body-2 text-medium-emphasis mb-4">
            Movies {{ friendData.username }} loved (4-5★) that you haven't seen yet
          </p>

          <v-row>
            <v-col
              v-for="rec in comparison.recommendationsForMe.slice(0, 6)"
              :key="rec.tmdbId"
              cols="6"
              sm="4"
              md="2"
            >
              <v-card hover>
                <v-img
                  v-if="rec.posterUrl"
                  :src="rec.posterUrl"
                  aspect-ratio="2/3"
                  cover
                />
                <v-card-text class="pa-2">
                  <div class="text-caption font-weight-bold text-truncate">
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
              </v-card>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
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
  },
  
  methods: {
    async loadComparison() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await fetch(`/api/compare/${this.friendUsername}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        if (response.ok) {
          this.comparison = await response.json();
          this.friendData = this.comparison.friend;
        } else {
          const errorData = await response.json();
          this.error = errorData.error || 'Failed to load comparison';
        }
      } catch (err) {
        console.error('Error loading comparison:', err);
        this.error = 'Failed to load comparison';
      } finally {
        this.loading = false;
      }
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
</style>
<template>
  <div class="home">
    <div class="hero-section">
      <h1 class="text-h2 font-weight-bold mb-4">Welcome to Your Digital Library</h1>
      <p class="text-h6 text-medium-emphasis mb-8">
        Track and rate your favorite Movies and TV Shows in your Personal Digital Library!
      </p>
      
      <!-- Quick Action Buttons -->
      <div class="actions">
        <v-btn 
          color="primary" 
          size="x-large" 
          to="/media/new"
          prepend-icon="mdi-plus"
          elevation="4"
          class="px-8"
        >
          Add New Media
        </v-btn>
        <v-btn 
          color="secondary" 
          size="x-large" 
          to="/media"
          prepend-icon="mdi-view-grid"
          variant="outlined"
          class="ml-4"
        >
          Browse Collection
        </v-btn>
      </div>
    </div>
    
    <!-- Quick Stats Cards (Optional - shows if user has data) -->
    <v-row v-if="stats.total > 0" class="mt-12">
      <v-col cols="12">
        <h2 class="text-h4 mb-6 text-center">Quick Stats</h2>
      </v-col>
      
      <v-col cols="12" sm="6" md="3">
        <v-card elevation="2" class="text-center pa-4">
          <v-icon size="48" color="primary" class="mb-2">mdi-film</v-icon>
          <div class="text-h4 font-weight-bold">{{ stats.total }}</div>
          <div class="text-caption text-medium-emphasis">Total Items</div>
        </v-card>
      </v-col>
      
      <v-col cols="12" sm="6" md="3">
        <v-card elevation="2" class="text-center pa-4">
          <v-icon size="48" color="success" class="mb-2">mdi-check-circle</v-icon>
          <div class="text-h4 font-weight-bold">{{ stats.watched }}</div>
          <div class="text-caption text-medium-emphasis">Watched</div>
        </v-card>
      </v-col>
      
      <v-col cols="12" sm="6" md="3">
        <v-card elevation="2" class="text-center pa-4">
          <v-icon size="48" color="info" class="mb-2">mdi-bookmark</v-icon>
          <div class="text-h4 font-weight-bold">{{ stats.watchlist }}</div>
          <div class="text-caption text-medium-emphasis">Watchlist</div>
        </v-card>
      </v-col>
      
      <v-col cols="12" sm="6" md="3">
        <v-card elevation="2" class="text-center pa-4">
          <v-icon size="48" color="amber" class="mb-2">mdi-star</v-icon>
          <div class="text-h4 font-weight-bold">
            {{ stats.averageRating ? stats.averageRating.toFixed(1) : 'N/A' }}
          </div>
          <div class="text-caption text-medium-emphasis">Avg Rating</div>
        </v-card>
      </v-col>
      
      <!-- Quick Action Cards -->
      <v-col cols="12" class="mt-8">
        <v-row>
          <v-col cols="12" md="6">
            <v-card 
              elevation="4" 
              hover 
              to="/analytics"
              class="pa-6 text-center quick-action-card"
            >
              <v-icon size="64" color="primary" class="mb-4">mdi-chart-line</v-icon>
              <h3 class="text-h5 mb-2">View Analytics</h3>
              <p class="text-body-2 text-medium-emphasis">
                Dive deep into your watching habits and stats
              </p>
            </v-card>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-card 
              elevation="4" 
              hover 
              to="/random"
              class="pa-6 text-center quick-action-card"
            >
              <v-icon size="64" color="secondary" class="mb-4">mdi-dice-5</v-icon>
              <h3 class="text-h5 mb-2">What to Watch?</h3>
              <p class="text-body-2 text-medium-emphasis">
                Let us pick something from your watchlist
              </p>
            </v-card>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mediaAPI } from '@/services/api-production';

export default {
  name: 'HomeView',
  
  data() {
    return {
      stats: {
        total: 0,
        watched: 0,
        watchlist: 0,
        averageRating: 0,
      }
    };
  },
  
  created() {
    this.loadStats();
  },
  
  methods: {
    async loadStats() {
      try {
        const mediaList = await mediaAPI.getAll();
        
        this.stats.total = mediaList.length;
        this.stats.watched = mediaList.filter(m => m.status === 'watched').length;
        this.stats.watchlist = mediaList.filter(m => m.status === 'want_to_watch').length;
        
        const ratedMedia = mediaList.filter(m => m.rating);
        this.stats.averageRating = ratedMedia.length > 0
          ? ratedMedia.reduce((sum, m) => sum + m.rating, 0) / ratedMedia.length
          : 0;
          
      } catch (err) {
        // User might not have any media yet - that's OK
        console.log('No media yet or error loading:', err);
      }
    }
  }
};
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 20px;
}

.hero-section {
  text-align: center;
  padding: 40px 0;
}

.actions {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 16px;
}

.quick-action-card {
  cursor: pointer;
  transition: transform 0.2s ease;
}

.quick-action-card:hover {
  transform: translateY(-4px);
}

@media (max-width: 600px) {
  .actions {
    flex-direction: column;
    align-items: stretch;
  }
  
  .actions .v-btn {
    margin: 0 !important;
  }
}
</style>
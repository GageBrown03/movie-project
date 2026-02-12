<template>
  <div class="home">
    <!-- Hero Section -->
    <div class="hero-section">
      <h1 class="text-h3 font-weight-bold mb-2">
        Welcome back{{ currentUser ? ', ' + currentUser.username : '' }}!
      </h1>
      <div v-if="activityStats" class="stats-summary text-h6 text-medium-emphasis mb-4">
        <span class="stat-item">
          <v-icon size="small" class="mr-1">mdi-film</v-icon>
          {{ activityStats.totalRated }}
        </span>
        <span class="stat-divider">•</span>
        <span class="stat-item">
          <v-icon size="small" class="mr-1">mdi-bookmark</v-icon>
          {{ activityStats.totalWatchlist }}
        </span>
        <span class="stat-divider">•</span>
        <span class="stat-item">
          <v-icon size="small" class="mr-1">mdi-account-group</v-icon>
          {{ activityStats.totalFriends }}
        </span>
      </div>
    </div>

    <!-- Activity Feed Section -->
    <v-row class="mt-6">
      <v-col cols="12">
        <activity-feed 
          ref="activityFeed"
          @add-media="openAddDialog"
        />
      </v-col>
    </v-row>

    <!-- Quick Stats Cards (Below Feed) -->
    <v-row v-if="stats.total > 0" class="mt-8">
      <v-col cols="12">
        <h2 class="text-h5 mb-4">Quick Stats</h2>
      </v-col>
      
      <!-- Total Items -->
      <v-col cols="6" sm="6" md="3">
        <v-card 
          elevation="2" 
          class="stat-card text-center pa-4" 
          hover
          @click="$router.push('/media')"
        >
          <v-icon size="40" color="primary" class="mb-2">mdi-film</v-icon>
          <div class="text-h5 font-weight-bold">{{ stats.total }}</div>
          <div class="text-caption text-medium-emphasis">Total Items</div>
        </v-card>
      </v-col>
      
      <!-- Watched -->
      <v-col cols="6" sm="6" md="3">
        <v-card 
          elevation="2" 
          class="stat-card text-center pa-4" 
          hover
          @click="$router.push('/media')"
        >
          <v-icon size="40" color="success" class="mb-2">mdi-check-circle</v-icon>
          <div class="text-h5 font-weight-bold">{{ stats.watched }}</div>
          <div class="text-caption text-medium-emphasis">Watched</div>
        </v-card>
      </v-col>
      
      <!-- Watchlist -->
      <v-col cols="6" sm="6" md="3">
        <v-card 
          elevation="2" 
          class="stat-card text-center pa-4" 
          hover
          @click="$router.push('/random')"
        >
          <v-icon size="40" color="info" class="mb-2">mdi-bookmark</v-icon>
          <div class="text-h5 font-weight-bold">{{ stats.watchlist }}</div>
          <div class="text-caption text-medium-emphasis">Watchlist</div>
        </v-card>
      </v-col>
      
      <!-- Average Rating -->
      <v-col cols="6" sm="6" md="3">
        <v-card 
          elevation="2" 
          class="stat-card text-center pa-4" 
          hover
          @click="$router.push('/analytics')"
        >
          <v-icon size="40" color="amber" class="mb-2">mdi-star</v-icon>
          <div class="text-h5 font-weight-bold">
            {{ stats.averageRating ? stats.averageRating.toFixed(1) : 'N/A' }}
          </div>
          <div class="text-caption text-medium-emphasis">Avg Rating</div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Quick Action Cards -->
    <v-row v-if="stats.total > 0" class="mt-6 mb-8">
      <v-col cols="12" md="6">
        <v-card 
          elevation="4" 
          hover 
          to="/analytics"
          class="pa-6 text-center quick-action-card"
        >
          <v-icon size="56" color="primary" class="mb-3">mdi-chart-line</v-icon>
          <h3 class="text-h6 mb-2">View Analytics</h3>
          <p class="text-body-2 text-medium-emphasis">
            Dive deep into your watching habits
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
          <v-icon size="56" color="secondary" class="mb-3">mdi-dice-5</v-icon>
          <h3 class="text-h6 mb-2">What to Watch?</h3>
          <p class="text-body-2 text-medium-emphasis">
            Pick something from your watchlist
          </p>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mediaAPI, activityAPI } from '@/services/api-production';
import ActivityFeed from '@/components/ActivityFeed.vue';

export default {
  name: 'HomeView',
  
  components: {
    ActivityFeed
  },

  data() {
    return {
      stats: {
        total: 0,
        watched: 0,
        watchlist: 0,
        averageRating: 0,
      },
      activityStats: null,
      currentUser: null
    };
  },
  
  created() {
    this.loadStats();
    this.loadActivityStats();
    this.loadCurrentUser();
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
        console.log('No media yet or error loading:', err);
      }
    },

    async loadActivityStats() {
      try {
        this.activityStats = await activityAPI.getStats();
      } catch (err) {
        console.log('Error loading activity stats:', err);
      }
    },

    loadCurrentUser() {
      const userStr = localStorage.getItem('user');
      if (userStr) {
        try {
          this.currentUser = JSON.parse(userStr);
        } catch (err) {
          console.error('Error parsing user:', err);
        }
      }
    },

    openAddDialog() {
      // Emit event to parent (App.vue) to open add dialog
      this.$root.$emit('open-add-media-dialog');
    },

    // Public method to refresh feed (call after adding media)
    refreshFeed() {
      if (this.$refs.activityFeed) {
        this.$refs.activityFeed.refresh();
      }
      this.loadStats();
      this.loadActivityStats();
    }
  }
};
</script>

<style scoped>
.home {
  max-width: 1400px;
  margin: 0 auto;
  padding: 40px 20px;
}

.hero-section {
  text-align: center;
  padding: 20px 0 40px;
}

.stats-summary {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.stat-item {
  display: inline-flex;
  align-items: center;
}

.stat-divider {
  opacity: 0.5;
}

.stat-card {
  cursor: pointer;
  transition: all 0.3s ease;
  height: 100%;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15) !important;
}

.quick-action-card {
  cursor: pointer;
  transition: transform 0.2s ease;
}

.quick-action-card:hover {
  transform: translateY(-4px);
}

/* Mobile Optimizations */
@media (max-width: 960px) {
  .home {
    padding: 20px 16px;
  }

  .hero-section {
    padding: 16px 0 24px;
  }

  .hero-section h1 {
    font-size: 1.75rem !important;
  }

  .stats-summary {
    font-size: 0.875rem;
  }

  .stat-card .v-icon {
    font-size: 32px !important;
  }

  .stat-card .text-h5 {
    font-size: 1.25rem !important;
  }

  .quick-action-card {
    padding: 20px !important;
  }

  .quick-action-card .v-icon {
    font-size: 48px !important;
  }
}

@media (max-width: 600px) {
  .stats-summary {
    flex-direction: row;
    justify-content: center;
  }

  .stat-divider {
    display: inline;
  }
}
</style>
<template>
  <v-card elevation="4" class="collection-card">
    <v-card-title class="text-h6 d-flex align-center justify-space-between">
      <span>
        <v-icon start color="primary">mdi-chart-box</v-icon>
        Your Collection in Review
      </span>
      <v-btn
        icon="mdi-download"
        variant="text"
        size="small"
        @click="downloadCard"
        :loading="downloading"
      />
    </v-card-title>
    
    <v-card-text v-if="loading">
      <v-skeleton-loader type="article, article, article" />
    </v-card-text>

    <v-card-text v-else-if="!hasStats" class="text-center py-8">
      <v-icon size="48" color="grey">mdi-chart-box-outline</v-icon>
      <p class="text-body-2 text-medium-emphasis mt-2">
        No stats yet - start adding media!
      </p>
    </v-card-text>
    
    <v-card-text v-else ref="cardContent" class="stats-card-content">
      <!-- Header Stats -->
      <div class="text-center mb-6 stats-header">
        <div class="text-h3 font-weight-bold text-primary mb-2">
          {{ stats.totalItems }}
        </div>
        <div class="text-h6 text-medium-emphasis">
          {{ stats.totalItems === 1 ? 'Item' : 'Items' }} in Your Collection
        </div>
        <v-divider class="my-4" />
        <div class="text-body-1">
          <strong>{{ stats.totalWatched }}</strong> watched • 
          <strong>{{ stats.totalRated }}</strong> rated
        </div>
      </div>

      <!-- Key Stats Grid -->
      <v-row class="mb-4">
        <!-- Average Rating -->
        <v-col v-if="stats.averageRating" cols="6">
          <div class="stat-box">
            <v-icon color="amber" size="large" class="mb-2">mdi-star</v-icon>
            <div class="text-h4 font-weight-bold">{{ stats.averageRating }}</div>
            <div class="text-caption text-medium-emphasis">Average Rating</div>
          </div>
        </v-col>

        <!-- Top Genre -->
        <v-col v-if="stats.topGenre" cols="6">
          <div class="stat-box">
            <v-icon color="primary" size="large" class="mb-2">mdi-movie-open</v-icon>
            <div class="text-h6 font-weight-bold">{{ stats.topGenre }}</div>
            <div class="text-caption text-medium-emphasis">
              Top Genre ({{ stats.topGenreCount }})
            </div>
          </div>
        </v-col>

        <!-- Favorite Actor -->
        <v-col v-if="stats.favoriteActor" cols="6">
          <div class="stat-box">
            <v-icon color="secondary" size="large" class="mb-2">mdi-account-star</v-icon>
            <div class="text-body-1 font-weight-bold line-clamp-2">
              {{ stats.favoriteActor }}
            </div>
            <div class="text-caption text-medium-emphasis">
              Favorite Actor ({{ stats.favoriteActorCount }})
            </div>
          </div>
        </v-col>

        <!-- Favorite Decade -->
        <v-col v-if="stats.favoriteDecade" cols="6">
          <div class="stat-box">
            <v-icon color="indigo" size="large" class="mb-2">mdi-calendar-star</v-icon>
            <div class="text-h6 font-weight-bold">{{ stats.favoriteDecade }}</div>
            <div class="text-caption text-medium-emphasis">
              Favorite Era ({{ stats.favoriteDecadeCount }})
            </div>
          </div>
        </v-col>
      </v-row>

      <!-- TMDB Comparison -->
      <v-alert
        v-if="stats.tmdbDifference !== undefined"
        :color="stats.tmdbDifference > 0 ? 'success' : 'error'"
        variant="tonal"
        class="mb-4"
      >
        <div class="d-flex align-center">
          <v-icon 
            :icon="stats.tmdbDifference > 0 ? 'mdi-heart' : 'mdi-gavel'" 
            size="large"
            class="mr-3"
          />
          <div>
            <div class="font-weight-bold">
              {{ stats.tmdbDifference > 0 ? '+' : '' }}{{ stats.tmdbDifference }}★ 
              vs TMDB
            </div>
            <div class="text-caption">
              You're {{ stats.tmdbDifference > 0 ? 'more generous' : 'a harsher critic' }} 
              than the average
            </div>
          </div>
        </div>
      </v-alert>

      <!-- Footer -->
      <v-divider class="my-4" />
      <div class="text-center text-caption text-medium-emphasis">
        CineSphere Collection • {{ currentDate }}
      </div>
    </v-card-text>

    <v-card-actions v-if="hasStats">
      <v-spacer />
      <v-btn
        variant="tonal"
        color="primary"
        @click="shareCard"
        prepend-icon="mdi-share-variant"
      >
        Share
      </v-btn>
      <v-btn
        variant="flat"
        color="primary"
        @click="downloadCard"
        prepend-icon="mdi-download"
        :loading="downloading"
      >
        Download
      </v-btn>
    </v-card-actions>

    <!-- Share Dialog -->
    <v-dialog v-model="showShareDialog" max-width="400">
      <v-card>
        <v-card-title>Share Your Collection</v-card-title>
        <v-card-text>
          <p class="text-body-2 mb-4">
            Share your collection stats with friends!
          </p>
          <v-text-field
            :model-value="shareUrl"
            readonly
            label="Share URL"
            variant="outlined"
            append-inner-icon="mdi-content-copy"
            @click:append-inner="copyShareUrl"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="showShareDialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar -->
    <v-snackbar v-model="showSnackbar" :color="snackbarColor" timeout="3000">
      {{ snackbarMessage }}
    </v-snackbar>
  </v-card>
</template>

<script>
import html2canvas from 'html2canvas';

export default {
  name: 'CollectionCard',
  
  props: {
    stats: {
      type: Object,
      default: () => ({})
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  
  data() {
    return {
      downloading: false,
      showShareDialog: false,
      showSnackbar: false,
      snackbarMessage: '',
      snackbarColor: 'success'
    };
  },
  
  computed: {
    hasStats() {
      return this.stats.totalItems > 0;
    },
    
    currentDate() {
      return new Date().toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long',
        day: 'numeric'
      });
    },
    
    shareUrl() {
      return window.location.origin + '/analytics';
    }
  },
  
  methods: {
    async downloadCard() {
      this.downloading = true;
      
      try {
        const element = this.$refs.cardContent;
        if (!element) {
          throw new Error('Card content not found');
        }

        const canvas = await html2canvas(element, {
          backgroundColor: '#ffffff',
          scale: 2,
          logging: false
        });
        
        const link = document.createElement('a');
        link.download = `cinesphere-collection-${Date.now()}.png`;
        link.href = canvas.toDataURL();
        link.click();
        
        this.showMessage('Card downloaded!', 'success');
      } catch (err) {
        console.error('Download error:', err);
        this.showMessage('Failed to download', 'error');
      } finally {
        this.downloading = false;
      }
    },
    
    shareCard() {
      if (navigator.share) {
        navigator.share({
          title: 'My CineSphere Collection',
          text: `I have ${this.stats.totalItems} items in my collection!`,
          url: this.shareUrl
        }).catch(() => {
          // Fallback to dialog if share fails
          this.showShareDialog = true;
        });
      } else {
        this.showShareDialog = true;
      }
    },
    
    async copyShareUrl() {
      try {
        await navigator.clipboard.writeText(this.shareUrl);
        this.showMessage('URL copied to clipboard!', 'success');
      } catch {
        this.showMessage('Failed to copy', 'error');
      }
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
.collection-card {
  max-width: 600px;
  margin: 0 auto;
}

.stats-card-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 8px;
  padding: 24px;
}

.stats-header {
  padding: 16px 0;
}

.stat-box {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  backdrop-filter: blur(10px);
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
<template>
  <div class="analytics-view">
    <!-- Header -->
    <v-row class="mb-6 align-center">
      <v-col>
        <h1 class="text-h3 font-weight-bold">Your Analytics</h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Insights from your {{ totalMedia }} {{ totalMedia === 1 ? 'item' : 'items' }}
        </p>
      </v-col>
    </v-row>

    <!-- Loading State -->
    <v-row v-if="loading" justify="center" class="my-12">
      <v-progress-circular indeterminate size="64" color="primary" />
    </v-row>

    <!-- Empty State -->
    <v-empty-state
      v-else-if="totalMedia === 0"
      icon="mdi-chart-box-outline"
      title="No Data Yet"
      text="Start adding movies and TV shows to see your analytics"
    >
      <template v-slot:actions>
        <v-btn color="primary" size="large" to="/movies/new">
          Add Your First Title
        </v-btn>
      </template>
    </v-empty-state>

    <!-- Analytics Content -->
    <div v-else>
      <!-- Stats Cards Row -->
      <v-row class="mb-6">
        <!-- Total Media -->
        <v-col cols="12" sm="6" md="4">
          <v-card class="stat-card" elevation="2">
            <v-card-text>
              <div class="d-flex align-center mb-2">
                <v-icon color="primary" size="32" class="mr-3">mdi-film</v-icon>
                <div>
                  <div class="text-h4 font-weight-bold">{{ totalMedia }}</div>
                  <div class="text-caption text-medium-emphasis">Total Items</div>
                </div>
              </div>
              <v-divider class="my-2" />
              <div class="text-body-2">
                <span class="font-weight-bold">{{ stats.movies }}</span> movies • 
                <span class="font-weight-bold">{{ stats.tvShows }}</span> TV shows
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Watched vs Watchlist -->
        <v-col cols="12" sm="6" md="4">
          <v-card class="stat-card" elevation="2">
            <v-card-text>
              <div class="d-flex align-center mb-2">
                <v-icon color="success" size="32" class="mr-3">mdi-check-circle</v-icon>
                <div>
                  <div class="text-h4 font-weight-bold">{{ stats.watched }}</div>
                  <div class="text-caption text-medium-emphasis">Watched</div>
                </div>
              </div>
              <v-divider class="my-2" />
              <div class="text-body-2">
                <span class="font-weight-bold text-info">{{ stats.watchlist }}</span> on watchlist
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Average Rating -->
        <v-col cols="12" sm="6" md="4">
          <v-card class="stat-card" elevation="2">
            <v-card-text>
              <div class="d-flex align-center mb-2">
                <v-icon color="amber" size="32" class="mr-3">mdi-star</v-icon>
                <div>
                  <div class="text-h4 font-weight-bold">
                    {{ stats.averageRating ? stats.averageRating.toFixed(1) : 'N/A' }}
                  </div>
                  <div class="text-caption text-medium-emphasis">Average Rating</div>
                </div>
              </div>
              <v-divider class="my-2" />
              <div class="text-body-2">
                Out of 5 stars
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Total Watch Time -->
        <v-col cols="12" sm="6" md="4">
          <v-card class="stat-card" elevation="2">
            <v-card-text>
              <div class="d-flex align-center mb-2">
                <v-icon color="purple" size="32" class="mr-3">mdi-clock-outline</v-icon>
                <div>
                  <div class="text-h4 font-weight-bold">{{ stats.totalHours }}</div>
                  <div class="text-caption text-medium-emphasis">Hours Watched</div>
                </div>
              </div>
              <v-divider class="my-2" />
              <div class="text-body-2">
                {{ stats.totalDays }} days total
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Favorite Genre -->
        <v-col cols="12" sm="6" md="4">
          <v-card class="stat-card" elevation="2">
            <v-card-text>
              <div class="d-flex align-center mb-2">
                <v-icon color="indigo" size="32" class="mr-3">mdi-movie-open</v-icon>
                <div>
                  <div class="text-h6 font-weight-bold text-truncate">
                    {{ stats.favoriteGenre || 'N/A' }}
                  </div>
                  <div class="text-caption text-medium-emphasis">Favorite Genre</div>
                </div>
              </div>
              <v-divider class="my-2" />
              <div class="text-body-2">
                Most watched
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Your Rating vs TMDB -->
        <v-col cols="12" sm="6" md="4">
          <v-card class="stat-card" elevation="2">
            <v-card-text>
              <div class="d-flex align-center mb-2">
                <v-icon :color="stats.ratingDiff > 0 ? 'success' : 'error'" size="32" class="mr-3">
                  {{ stats.ratingDiff > 0 ? 'mdi-thumb-up' : 'mdi-thumb-down' }}
                </v-icon>
                <div>
                  <div class="text-h5 font-weight-bold">
                    {{ stats.ratingDiff > 0 ? '+' : '' }}{{ stats.ratingDiff }}
                  </div>
                  <div class="text-caption text-medium-emphasis">vs TMDB</div>
                </div>
              </div>
              <v-divider class="my-2" />
              <div class="text-body-2">
                {{ stats.ratingDiff > 0 ? 'More generous' : 'Harsher critic' }}
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Charts Row -->
      <v-row>
        <!-- Rating Distribution -->
        <v-col cols="12" md="6">
          <v-card elevation="2">
            <v-card-title class="text-h6">
              <v-icon start>mdi-chart-bar</v-icon>
              Rating Distribution
            </v-card-title>
            <v-card-text>
              <div class="rating-chart">
                <div 
                  v-for="rating in [5, 4, 3, 2, 1]" 
                  :key="rating"
                  class="rating-bar-row"
                >
                  <div class="rating-label">
                    <v-icon color="amber" size="small">mdi-star</v-icon>
                    {{ rating }}
                  </div>
                  <div class="rating-bar-container">
                    <div 
                      class="rating-bar"
                      :style="{ width: getRatingPercentage(rating) + '%' }"
                    >
                      <span class="rating-count">{{ stats.ratingDistribution[rating] || 0 }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Genre Breakdown -->
        <v-col cols="12" md="6">
          <v-card elevation="2">
            <v-card-title class="text-h6">
              <v-icon start>mdi-chart-pie</v-icon>
              Top Genres
            </v-card-title>
            <v-card-text>
              <div class="genre-list">
                <div 
                  v-for="(genre, index) in stats.topGenres.slice(0, 8)" 
                  :key="genre.name"
                  class="genre-item"
                >
                  <div class="d-flex align-center justify-space-between mb-2">
                    <span class="genre-name">{{ genre.name }}</span>
                    <span class="genre-count">{{ genre.count }}</span>
                  </div>
                  <v-progress-linear
                    :model-value="(genre.count / stats.topGenres[0].count) * 100"
                    :color="genreColors[index % genreColors.length]"
                    height="8"
                    rounded
                  />
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Recent Activity -->
        <v-col cols="12">
          <v-card elevation="2">
            <v-card-title class="text-h6">
              <v-icon start>mdi-history</v-icon>
              Recent Activity
            </v-card-title>
            <v-card-text>
              <v-list lines="two" class="bg-transparent">
                <v-list-item
                  v-for="media in recentMedia"
                  :key="media.mediaId"
                  :to="`/movies/${media.mediaId}`"
                  link
                >
                  <template v-slot:prepend>
                    <v-avatar size="60" rounded class="mr-4">
                      <v-img v-if="media.posterUrl" :src="media.posterUrl" cover />
                      <v-icon v-else>mdi-movie-outline</v-icon>
                    </v-avatar>
                  </template>

                  <v-list-item-title>
                    {{ media.title }}
                    <v-chip size="x-small" :color="media.mediaType === 'movie' ? 'primary' : 'secondary'" class="ml-2">
                      {{ media.mediaType.toUpperCase() }}
                    </v-chip>
                  </v-list-item-title>

                  <v-list-item-subtitle>
                    <v-rating
                      v-if="media.rating"
                      :model-value="media.rating"
                      size="x-small"
                      color="amber"
                      density="compact"
                      readonly
                    />
                    <span v-else class="text-info">Watchlist</span>
                  </v-list-item-subtitle>

                  <template v-slot:append>
                    <span class="text-caption text-medium-emphasis">
                      {{ timeAgo(media.createdAt) }}
                    </span>
                  </template>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
import { mediaAPI } from '@/services/api-production';

export default {
  name: 'AnalyticsView',
  
  data() {
    return {
      loading: false,
      mediaList: [],
      genreColors: ['primary', 'secondary', 'success', 'warning', 'error', 'info', 'purple', 'indigo'],
    };
  },
  
  computed: {
    totalMedia() {
      return this.mediaList.length;
    },
    
    stats() {
      if (this.mediaList.length === 0) return {};
      
      const watched = this.mediaList.filter(m => m.status === 'watched');
      const watchlist = this.mediaList.filter(m => m.status === 'want_to_watch');
      const movies = this.mediaList.filter(m => m.mediaType === 'movie');
      const tvShows = this.mediaList.filter(m => m.mediaType === 'tv');
      
      // Average rating
      const ratedMedia = this.mediaList.filter(m => m.rating);
      const averageRating = ratedMedia.length > 0
        ? ratedMedia.reduce((sum, m) => sum + m.rating, 0) / ratedMedia.length
        : 0;
      
      // Rating distribution
      const ratingDistribution = {};
      for (let i = 1; i <= 5; i++) {
        ratingDistribution[i] = this.mediaList.filter(m => m.rating === i).length;
      }
      
      // Total watch time (movies only, estimate TV as 45min per episode)
      let totalMinutes = 0;
      this.mediaList.forEach(m => {
        if (m.mediaType === 'movie' && m.runtime) {
          totalMinutes += m.runtime;
        } else if (m.mediaType === 'tv' && m.numberOfEpisodes) {
          totalMinutes += m.numberOfEpisodes * 45; // Estimate 45min per episode
        }
      });
      const totalHours = Math.round(totalMinutes / 60);
      const totalDays = (totalMinutes / 60 / 24).toFixed(1);
      
      // Top genres
      const genreCounts = {};
      this.mediaList.forEach(m => {
        if (m.genres) {
          const genres = Array.isArray(m.genres) ? m.genres : m.genres.split(', ');
          genres.forEach(g => {
            genreCounts[g] = (genreCounts[g] || 0) + 1;
          });
        }
      });
      const topGenres = Object.entries(genreCounts)
        .map(([name, count]) => ({ name, count }))
        .sort((a, b) => b.count - a.count);
      
      const favoriteGenre = topGenres[0]?.name || null;
      
      // Your rating vs TMDB average
      const mediaWithBothRatings = this.mediaList.filter(m => m.rating && m.tmdbRating);
      let ratingDiff = 0;
      if (mediaWithBothRatings.length > 0) {
        const yourAvg = mediaWithBothRatings.reduce((sum, m) => sum + m.rating, 0) / mediaWithBothRatings.length;
        const tmdbAvg = mediaWithBothRatings.reduce((sum, m) => sum + (m.tmdbRating / 2), 0) / mediaWithBothRatings.length; // Convert TMDB 10-point to 5-point
        ratingDiff = (yourAvg - tmdbAvg).toFixed(1);
      }
      
      return {
        movies: movies.length,
        tvShows: tvShows.length,
        watched: watched.length,
        watchlist: watchlist.length,
        averageRating,
        ratingDistribution,
        totalHours,
        totalDays,
        topGenres,
        favoriteGenre,
        ratingDiff: parseFloat(ratingDiff),
      };
    },
    
    recentMedia() {
      return [...this.mediaList]
        .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
        .slice(0, 5);
    },
  },
  
  created() {
    this.loadMedia();
  },
  
  methods: {
    async loadMedia() {
      this.loading = true;
      try {
        this.mediaList = await mediaAPI.getAll();
      } catch (err) {
        console.error('Error loading media:', err);
      } finally {
        this.loading = false;
      }
    },
    
    getRatingPercentage(rating) {
      const count = this.stats.ratingDistribution[rating] || 0;
      const maxCount = Math.max(...Object.values(this.stats.ratingDistribution));
      return maxCount > 0 ? (count / maxCount) * 100 : 0;
    },
    
    timeAgo(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      const now = new Date();
      const diffMs = now - date;
      const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
      
      if (diffDays === 0) return 'Today';
      if (diffDays === 1) return 'Yesterday';
      if (diffDays < 7) return `${diffDays} days ago`;
      if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
      if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`;
      return `${Math.floor(diffDays / 365)} years ago`;
    },
  },
};
</script>

<style scoped>
.analytics-view {
  max-width: 1600px;
  margin: 0 auto;
}

.stat-card {
  height: 100%;
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
}

/* Rating Distribution Chart */
.rating-chart {
  padding: 16px 0;
}

.rating-bar-row {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.rating-label {
  width: 60px;
  display: flex;
  align-items: center;
  font-weight: bold;
}

.rating-bar-container {
  flex: 1;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  height: 32px;
  position: relative;
}

.rating-bar {
  background: linear-gradient(90deg, #FFC107, #FF9800);
  height: 100%;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 12px;
  transition: width 0.3s ease;
  min-width: 40px;
}

.rating-count {
  color: white;
  font-weight: bold;
  font-size: 14px;
}

/* Genre List */
.genre-list {
  padding: 8px 0;
}

.genre-item {
  margin-bottom: 16px;
}

.genre-name {
  font-weight: 500;
}

.genre-count {
  color: rgba(0, 0, 0, 0.6);
  font-weight: bold;
}
</style>
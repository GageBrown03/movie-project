<template>
  <v-card elevation="2">
    <v-card-title class="text-h6">
      <v-icon start color="indigo">mdi-calendar-range</v-icon>
      Decade Preferences
    </v-card-title>
    
    <v-card-text v-if="loading">
      <v-skeleton-loader type="image" height="300" />
    </v-card-text>

    <v-card-text v-else-if="decades.length === 0" class="text-center py-8">
      <v-icon size="48" color="grey">mdi-calendar-blank</v-icon>
      <p class="text-body-2 text-medium-emphasis mt-2">
        No decade data yet
      </p>
    </v-card-text>
    
    <v-card-text v-else>
      <!-- Favorite Decade Highlight -->
      <v-alert
        v-if="favorite"
        :color="getDecadeColor(favorite.label)"
        variant="tonal"
        class="mb-4"
        prominent
      >
        <div class="d-flex align-center">
          <v-icon start size="large">mdi-trophy</v-icon>
          <div>
            <div class="text-h6">{{ favorite.label }}</div>
            <div class="text-body-2">
              Your favorite era with {{ favorite.count }} {{ favorite.count === 1 ? 'movie' : 'movies' }}
            </div>
          </div>
        </div>
      </v-alert>

      <!-- Decade Bars -->
      <div class="decade-chart">
        <div 
          v-for="decade in sortedDecades" 
          :key="decade.label"
          class="decade-bar-row"
        >
          <div class="decade-label">
            <v-icon 
              :color="getDecadeColor(decade.label)" 
              size="small" 
              class="mr-2"
            >
              mdi-calendar
            </v-icon>
            <span class="font-weight-bold">{{ decade.label }}</span>
          </div>
          
          <div class="decade-bar-container">
            <div 
              class="decade-bar"
              :style="{ 
                width: getDecadePercentage(decade) + '%',
                backgroundColor: getDecadeColorValue(decade.label)
              }"
            >
              <span class="decade-count">{{ decade.count }}</span>
            </div>
          </div>
          
          <div class="decade-rating">
            <v-chip
              v-if="decade.averageRating"
              size="small"
              variant="flat"
              :color="getRatingColor(decade.averageRating)"
            >
              <v-icon start size="x-small">mdi-star</v-icon>
              {{ decade.averageRating }}
            </v-chip>
          </div>
        </div>
      </div>

      <!-- Era Insights -->
      <v-divider class="my-4" />
      
      <div class="text-body-2 text-medium-emphasis">
        <v-icon size="small" class="mr-1">mdi-lightbulb-on</v-icon>
        <strong>Era Insights:</strong>
        <span v-if="hasClassicTaste">
          You appreciate classic cinema! 
        </span>
        <span v-else-if="hasModernTaste">
          You prefer modern releases! 
        </span>
        <span v-else>
          You have diverse decade preferences! 
        </span>
        <span v-if="bestRatedDecade">
          You rate {{ bestRatedDecade.label }} movies highest ({{ bestRatedDecade.averageRating }}★).
        </span>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'DecadePreferences',
  
  props: {
    decades: {
      type: Array,
      default: () => []
    },
    favorite: {
      type: Object,
      default: null
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  
  computed: {
    sortedDecades() {
      // Sort from oldest to newest
      return [...this.decades].sort((a, b) => a.decade - b.decade);
    },
    
    maxCount() {
      return Math.max(...this.decades.map(d => d.count), 1);
    },
    
    hasClassicTaste() {
      // More than 50% from pre-2000
      const pre2000 = this.decades
        .filter(d => d.decade < 2000)
        .reduce((sum, d) => sum + d.count, 0);
      const total = this.decades.reduce((sum, d) => sum + d.count, 0);
      return pre2000 / total > 0.5;
    },
    
    hasModernTaste() {
      // More than 50% from 2010s and 2020s
      const modern = this.decades
        .filter(d => d.decade >= 2010)
        .reduce((sum, d) => sum + d.count, 0);
      const total = this.decades.reduce((sum, d) => sum + d.count, 0);
      return modern / total > 0.5;
    },
    
    bestRatedDecade() {
      const ratedDecades = this.decades.filter(d => d.averageRating);
      if (ratedDecades.length === 0) return null;
      return ratedDecades.reduce((best, d) => 
        d.averageRating > (best?.averageRating || 0) ? d : best
      );
    }
  },
  
  methods: {
    getDecadePercentage(decade) {
      return (decade.count / this.maxCount) * 100;
    },
    
    getDecadeColor(label) {
      const colors = {
        '1920s': 'brown',
        '1930s': 'grey',
        '1940s': 'blue-grey',
        '1950s': 'indigo',
        '1960s': 'deep-purple',
        '1970s': 'purple',
        '1980s': 'pink',
        '1990s': 'red',
        '2000s': 'orange',
        '2010s': 'green',
        '2020s': 'teal'
      };
      return colors[label] || 'primary';
    },
    
    getDecadeColorValue(label) {
      const colorMap = {
        '1920s': '#795548',
        '1930s': '#9E9E9E',
        '1940s': '#607D8B',
        '1950s': '#3F51B5',
        '1960s': '#673AB7',
        '1970s': '#9C27B0',
        '1980s': '#E91E63',
        '1990s': '#F44336',
        '2000s': '#FF9800',
        '2010s': '#4CAF50',
        '2020s': '#009688'
      };
      return colorMap[label] || '#2196F3';
    },
    
    getRatingColor(rating) {
      if (rating >= 4.5) return 'success';
      if (rating >= 4.0) return 'primary';
      if (rating >= 3.5) return 'info';
      if (rating >= 3.0) return 'warning';
      return 'error';
    }
  }
};
</script>

<style scoped>
.decade-chart {
  padding: 16px 0;
}

.decade-bar-row {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  gap: 12px;
}

.decade-label {
  width: 100px;
  display: flex;
  align-items: center;
  font-size: 14px;
}

.decade-bar-container {
  flex: 1;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  height: 36px;
  position: relative;
  min-width: 100px;
}

.decade-bar {
  height: 100%;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 12px;
  transition: width 0.3s ease;
  min-width: 40px;
}

.decade-count {
  color: white;
  font-weight: bold;
  font-size: 14px;
  text-shadow: 0 1px 2px rgba(0,0,0,0.3);
}

.decade-rating {
  width: 60px;
  display: flex;
  justify-content: flex-end;
}
</style>
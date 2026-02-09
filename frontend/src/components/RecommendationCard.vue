<template>
  <v-card 
    class="recommendation-card" 
    hover
    @click="$emit('click')"
  >
    <!-- Poster -->
    <v-img
      v-if="item.posterUrl"
      :src="item.posterUrl"
      aspect-ratio="2/3"
      cover
      class="recommendation-poster"
    >
      <!-- In Collection Badge -->
      <div v-if="isInCollection" class="poster-overlay">
        <v-chip 
          color="success"
          size="x-small"
          class="in-collection-chip"
        >
          <v-icon start size="x-small">mdi-check</v-icon>
          In Collection
        </v-chip>
      </div>
      
      <!-- Rating Badge -->
      <div v-if="item.tmdbRating" class="rating-badge">
        <v-chip 
          color="amber"
          size="x-small"
          variant="flat"
        >
          <v-icon start size="x-small">mdi-star</v-icon>
          {{ item.tmdbRating.toFixed(1) }}
        </v-chip>
      </div>
    </v-img>
    
    <!-- Placeholder if no poster -->
    <div v-else class="poster-placeholder">
      <v-icon size="64" color="grey">mdi-movie-outline</v-icon>
    </div>
    
    <!-- Card Content -->
    <v-card-text class="pa-3">
      <div class="text-body-2 font-weight-bold text-truncate mb-1">
        {{ item.title }}
      </div>
      <div class="text-caption text-medium-emphasis">
        {{ item.releaseYear || 'N/A' }}
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'RecommendationCard',
  
  props: {
    item: {
      type: Object,
      required: true
    },
    isInCollection: {
      type: Boolean,
      default: false
    }
  },
  
  emits: ['click']
};
</script>

<style scoped>
.recommendation-card {
  cursor: pointer;
  transition: all 0.2s ease;
  height: 100%;
}

.recommendation-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.recommendation-poster {
  position: relative;
}

.poster-overlay {
  position: absolute;
  top: 8px;
  left: 8px;
}

.rating-badge {
  position: absolute;
  top: 8px;
  right: 8px;
}

.in-collection-chip {
  backdrop-filter: blur(8px);
  background: rgba(76, 175, 80, 0.9) !important;
}

.poster-placeholder {
  aspect-ratio: 2/3;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(0,0,0,0.05) 0%, rgba(0,0,0,0.1) 100%);
}
</style>
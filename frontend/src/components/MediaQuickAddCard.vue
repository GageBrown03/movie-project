<template>
  <!-- Desktop Card View -->
  <v-card v-if="!isMobile" class="media-quick-card" hover>
    <v-img
      v-if="item.posterUrl"
      :src="item.posterUrl"
      aspect-ratio="2/3"
      cover
      @click="$emit('view-details', item)"
    >
      <!-- In collection badge -->
      <div v-if="isInCollection" class="collection-badge">
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
      @click="$emit('view-details', item)"
    >
      <div class="d-flex align-center justify-center fill-height bg-grey-darken-3">
        <v-icon size="64" color="grey">mdi-image-off</v-icon>
      </div>
    </v-img>

    <!-- Title -->
    <v-card-text class="pa-2 pb-0">
      <p class="text-caption font-weight-bold text-truncate mb-1" :title="item.title">
        {{ item.title }}
      </p>
      <p class="text-caption text-medium-emphasis">
        {{ item.releaseYear || 'N/A' }}
      </p>
    </v-card-text>

    <!-- Quick Actions -->
    <v-card-actions v-if="!isInCollection" class="pa-2 pt-0 flex-column gap-1">
      <v-btn
        size="x-small"
        color="info"
        variant="tonal"
        block
        @click="$emit('quick-add-watchlist', item)"
        :loading="loading === 'watchlist'"
      >
        <v-icon start size="14">mdi-bookmark-plus</v-icon>
        Watchlist
      </v-btn>
      
      <v-btn
        size="x-small"
        color="primary"
        variant="tonal"
        block
        @click="$emit('quick-add-rated', item)"
        :loading="loading === 'rated'"
      >
        <v-icon start size="14">mdi-star</v-icon>
        Rate
      </v-btn>
    </v-card-actions>

    <!-- Already in collection -->
    <v-card-actions v-else class="pa-2 pt-0">
      <v-btn
        size="x-small"
        variant="outlined"
        block
        @click="$emit('view-existing', item)"
      >
        View in Library
      </v-btn>
    </v-card-actions>
  </v-card>

  <!-- Mobile List View -->
  <v-list-item v-else class="mobile-quick-item mb-2 rounded-lg border">
    <template v-slot:prepend>
      <v-avatar size="80" rounded class="mr-3" @click="$emit('view-details', item)">
        <v-img v-if="item.posterUrl" :src="item.posterUrl" cover />
        <v-icon v-else size="40">mdi-movie-outline</v-icon>
      </v-avatar>
    </template>

    <v-list-item-title class="text-body-2 font-weight-bold">
      {{ item.title }}
      <v-chip
        v-if="isInCollection"
        size="x-small"
        color="success"
        class="ml-1"
      >
        In Library
      </v-chip>
    </v-list-item-title>
    
    <v-list-item-subtitle class="text-caption">
      {{ item.mediaType === 'movie' ? 'Movie' : 'TV' }} • {{ item.releaseYear || 'N/A' }}
    </v-list-item-subtitle>

    <!-- Mobile Quick Actions -->
    <template v-slot:append>
      <div class="d-flex flex-column gap-1">
        <v-btn
          v-if="!isInCollection"
          size="x-small"
          color="info"
          icon
          variant="tonal"
          @click="$emit('quick-add-watchlist', item)"
          :loading="loading === 'watchlist'"
        >
          <v-icon size="16">mdi-bookmark-plus</v-icon>
        </v-btn>
        
        <v-btn
          v-if="!isInCollection"
          size="x-small"
          color="primary"
          icon
          variant="tonal"
          @click="$emit('quick-add-rated', item)"
          :loading="loading === 'rated'"
        >
          <v-icon size="16">mdi-star</v-icon>
        </v-btn>
        
        <v-btn
          v-if="isInCollection"
          size="x-small"
          icon
          variant="outlined"
          @click="$emit('view-existing', item)"
        >
          <v-icon size="16">mdi-eye</v-icon>
        </v-btn>
      </div>
    </template>
  </v-list-item>
</template>

<script>
export default {
  name: 'MediaQuickAddCard',

  props: {
    item: {
      type: Object,
      required: true
    },
    isInCollection: {
      type: Boolean,
      default: false
    },
    loading: {
      type: String, // 'watchlist' | 'rated' | null
      default: null
    },
    isMobile: {
      type: Boolean,
      default: false
    }
  },

  emits: [
    'quick-add-watchlist',
    'quick-add-rated',
    'view-details',
    'view-existing'
  ]
};
</script>

<style scoped>
.media-quick-card {
  cursor: pointer;
  transition: all 0.2s ease;
}

.media-quick-card:hover {
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

.mobile-quick-item {
  background: rgb(var(--v-theme-surface));
}

.gap-1 {
  gap: 4px;
}
</style>
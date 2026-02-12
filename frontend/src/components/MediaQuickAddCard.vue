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
      <div v-if="isInCollection" class="collection-badge">
        <v-chip size="small" :color="collectionStatus.color" variant="flat">
          <v-icon start size="small">{{ collectionStatus.icon }}</v-icon>
          {{ collectionStatus.label }}
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

    <v-card-text class="pa-2 pb-0">
      <p class="text-caption font-weight-bold text-truncate mb-1" :title="item.title">
        {{ item.title }}
      </p>
      <p class="text-caption text-medium-emphasis">
        {{ item.releaseYear || 'N/A' }}
      </p>
    </v-card-text>

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

  <!-- IMPROVED: Mobile Card View with Title -->
  <v-card v-else class="media-quick-card-mobile" hover @click="handleMobileClick">
    <v-img
      v-if="item.posterUrl"
      :src="item.posterUrl"
      :aspect-ratio="0.7"
      cover
      class="mobile-poster"
    >
      <!-- Status badge on poster -->
      <div v-if="isInCollection" class="collection-badge-mobile">
        <v-chip size="x-small" :color="collectionStatus.color" variant="flat">
          <v-icon size="12">{{ collectionStatus.icon }}</v-icon>
        </v-chip>
      </div>
    </v-img>

    <v-img
      v-else
      src="/placeholder-poster.png"
      :aspect-ratio="0.7"
      class="mobile-poster"
    >
      <div class="d-flex align-center justify-center fill-height bg-grey-darken-3">
        <v-icon size="48" color="grey">mdi-image-off</v-icon>
      </div>
    </v-img>

    <!-- Title underneath poster -->
    <v-card-text class="pa-2">
      <p class="text-caption font-weight-bold mobile-title" :title="item.title">
        {{ item.title }}
      </p>
      <p class="text-caption text-medium-emphasis">
        {{ item.releaseYear || 'N/A' }}
      </p>
    </v-card-text>

    <!-- Quick action buttons -->
    <v-card-actions v-if="!isInCollection" class="pa-2 pt-0 justify-center gap-1">
      <v-btn
        size="x-small"
        color="info"
        icon
        variant="tonal"
        @click.stop="$emit('quick-add-watchlist', item)"
        :loading="loading === 'watchlist'"
      >
        <v-icon size="16">mdi-bookmark-plus</v-icon>
      </v-btn>
      
      <v-btn
        size="x-small"
        color="primary"
        icon
        variant="tonal"
        @click.stop="$emit('quick-add-rated', item)"
        :loading="loading === 'rated'"
      >
        <v-icon size="16">mdi-star</v-icon>
      </v-btn>
    </v-card-actions>

    <v-card-actions v-else class="pa-2 pt-0">
      <v-btn
        size="x-small"
        variant="outlined"
        block
        @click.stop="$emit('view-existing', item)"
      >
        View
      </v-btn>
    </v-card-actions>
  </v-card>
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
    collectionInfo: {
      type: Object,
      default: null
    },
    loading: {
      type: String,
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
  ],

  computed: {
    collectionStatus() {
      if (!this.collectionInfo) {
        return { icon: 'mdi-check', label: 'In Library', color: 'success' };
      }

      if (this.collectionInfo.type === 'rated') {
        return {
          icon: 'mdi-star',
          label: `${this.collectionInfo.rating}★`,
          color: 'success'
        };
      } else if (this.collectionInfo.type === 'watchlist') {
        return {
          icon: 'mdi-bookmark',
          label: 'Watchlist',
          color: 'info'
        };
      }

      return { icon: 'mdi-check', label: 'In Library', color: 'success' };
    }
  },

  methods: {
    handleMobileClick() {
      if (!this.isInCollection) {
        this.$emit('quick-add-rated', this.item);
      } else {
        this.$emit('view-existing', this.item);
      }
    }
  }
};
</script>

<style scoped>
/* Desktop card */
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

.gap-1 {
  gap: 4px;
}

/* IMPROVED: Mobile card styling */
.media-quick-card-mobile {
  cursor: pointer;
  transition: all 0.2s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.media-quick-card-mobile:active {
  transform: scale(0.98);
}

.mobile-poster {
  border-radius: 8px 8px 0 0;
}

.collection-badge-mobile {
  position: absolute;
  top: 6px;
  right: 6px;
}

.mobile-title {
  /* Show 2 lines max on mobile */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.3;
  min-height: 2.6em;
}
</style>
<template>
  <div class="all-media">
    <v-row class="mb-4 align-center" no-gutters>
      <v-col cols="12" sm="8" md="6">
        <v-text-field
          v-model="searchQuery"
          prepend-inner-icon="mdi-magnify"
          label="Search your collection..."
          variant="solo-filled"
          flat
          density="comfortable"
          clearable
          hide-details
          class="search-bar"
        />
      </v-col>
      <v-spacer />
    </v-row>

    <v-row class="mb-6 align-center" no-gutters>
      <div class="d-flex flex-wrap align-center gap-3 w-100">
        <v-select
          v-model="filterType"
          :items="typeOptions"
          label="Type"
          variant="outlined"
          density="compact"
          hide-details
          clearable
          style="max-width: 130px;"
        />
        <v-select
          v-model="filterRating"
          :items="ratingOptions"
          label="Rating"
          variant="outlined"
          density="compact"
          hide-details
          clearable
          style="max-width: 130px;"
        />
        <v-select
          v-model="sortBy"
          :items="sortOptions"
          label="Sort"
          variant="outlined"
          density="compact"
          hide-details
          style="max-width: 170px;"
        />

        <v-btn 
          v-if="hasActiveFilters" 
          variant="text" 
          color="grey" 
          size="small" 
          prepend-icon="mdi-filter-off-outline"
          @click="clearFilters"
          class="text-none"
        >
          Reset
        </v-btn>

        <v-spacer />

        <div class="d-flex align-center">
          <span class="text-caption text-grey mr-4">{{ filteredMedia.length }} items</span>
          <v-btn-toggle v-model="viewMode" mandatory density="compact" color="primary">
            <v-btn value="grid" icon="mdi-view-grid-outline" size="small" />
            <v-btn value="list" icon="mdi-view-list" size="small" />
          </v-btn-toggle>
        </div>
      </div>
    </v-row>
    
    <v-row v-if="loading" justify="center" class="my-12">
      <v-progress-circular indeterminate size="64" color="primary" />
    </v-row>
    
    <v-alert v-else-if="error" type="error" variant="tonal" class="mb-4">
      {{ error }}
      <template v-slot:append>
        <v-btn @click="getAllMedia" variant="text">Retry</v-btn>
      </template>
    </v-alert>
    
    <v-empty-state
      v-else-if="mediaList.length === 0"
      class="empty-state-cinematic"
    >
      <template v-slot:media>
        <div class="empty-icon-wrapper">
          <svg width="180" height="180" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="film-reel-svg">
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1" />
            <circle cx="12" cy="12" r="2" fill="currentColor" />
            <circle cx="12" cy="6" r="1.5" fill="currentColor" opacity="0.5" />
            <circle cx="12" cy="18" r="1.5" fill="currentColor" opacity="0.5" />
            <circle cx="6" cy="12" r="1.5" fill="currentColor" opacity="0.5" />
            <circle cx="18" cy="12" r="1.5" fill="currentColor" opacity="0.5" />
            <path d="M19 12C19 12 21 13 22 16" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-dasharray="2 2" />
          </svg>
        </div>
      </template>

      <template v-slot:title>
        <h2 class="text-h4 font-weight-black text-white mt-6">Your Premiere Awaits</h2>
      </template>

      <template v-slot:text>
        <p class="text-body-1 text-grey-lighten-1 mx-auto" style="max-width: 500px;">
          Your collection is currently a blank script. Start adding movies and shows to build your personal library.
        </p>
      </template>

      <template v-slot:actions>
        <v-btn color="primary" size="x-large" to="/movies/new" class="mt-4 px-10 font-weight-bold" elevation="8">
          Add Your First Title
        </v-btn>
      </template>
    </v-empty-state>

    <div v-else>
      <!-- Grid View -->
      <v-row v-if="viewMode === 'grid'">
        <v-col
          v-for="media in filteredMedia"
          :key="media.mediaId"
          cols="4"
          sm="3"
          md="3"
          lg="2"
          xl="2"
        >
          <v-card
            class="media-card"
            flat
            @mouseenter="startHover(media)"
            @mouseleave="cancelHover"
            @click="handleCardClick(media)"
          >
            <div class="poster-container">
              <v-img
                v-if="media.posterUrl"
                :src="media.posterUrl"
                aspect-ratio="2/3"
                cover
              >
                <!-- Slim top scrim -->
                <div class="top-scrim"></div>

                <!-- Corner badges -->
                <div class="overlay-content">
                  <!-- Top-left: Type badge -->
                  <div
                    class="badge-type"
                    :class="media.mediaType === 'movie' ? 'badge-type--movie' : 'badge-type--tv'"
                  >
                    {{ media.mediaType === 'movie' ? 'M' : 'TV' }}
                  </div>

                  <!-- Top-right: Rating or Watchlist -->
                  <div class="badge-corner-right">
                    <!-- Rating badge -->
                    <div v-if="media.rating" class="badge-rating">
                      <v-icon class="badge-rating__star" color="#FFC107">
                        mdi-star
                      </v-icon>
                      <span class="badge-rating__value">
                        {{ Number(media.rating).toFixed(1).replace('.0','') }}
                      </span>
                    </div>

                    <!-- Watchlist badge (icon only) -->
                    <div v-else class="badge-watchlist">
                      <v-icon class="badge-watchlist__icon">mdi-bookmark</v-icon>
                    </div>
                  </div>
                </div>
              </v-img>
            </div>
          </v-card>
        </v-col>
      </v-row>

      <!-- List View -->
      <v-list v-else lines="two" class="bg-transparent">
        <v-list-item
          v-for="media in filteredMedia"
          :key="media.mediaId"
          @click="handleCardClick(media)"
          @mouseenter="startHover(media)"
          @mouseleave="cancelHover"
          link
          class="mb-2 rounded-lg border list-item-hoverable"
        >
          <!-- Poster -->
          <template v-slot:prepend>
            <v-avatar size="80" rounded class="mr-3 list-avatar">
              <v-img v-if="media.posterUrl" :src="media.posterUrl" cover />
            </v-avatar>
          </template>

          <!-- Content -->
          <div class="w-100">
            <!-- Title -->
            <v-list-item-title class="list-title text-subtitle-1 font-weight-bold">
              {{ media.title }}
            </v-list-item-title>

            <!-- Mobile meta row (under title on mobile only) -->
            <div v-if="isMobile" class="list-meta-row">
              <v-chip
                size="x-small"
                :color="media.mediaType === 'movie' ? '#1976D2' : '#7B1FA2'"
                class="text-white"
                label
              >
                {{ media.mediaType.toUpperCase() }}
              </v-chip>

              <div class="spacer"></div>

              <!-- Rating compact -->
              <v-chip
                v-if="media.rating"
                size="x-small"
                color="#121212"
                variant="flat"
                class="rating-chip-mobile"
              >
                <span class="gold-text font-weight-bold">
                  {{ Number(media.rating).toFixed(1).replace('.0','') }}/5
                </span>
              </v-chip>

              <!-- Watchlist icon -->
              <v-chip
                v-else
                size="x-small"
                color="info"
                variant="flat"
                title="Watchlist"
              >
                <v-icon start size="16">mdi-bookmark</v-icon>
              </v-chip>
            </div>
          </div>

          <!-- Desktop append -->
          <template v-slot:append>
            <div v-if="!isMobile" class="d-flex align-center gap-2">
              <!-- Type chip on desktop -->
              <v-chip
                size="small"
                :color="media.mediaType === 'movie' ? '#1976D2' : '#7B1FA2'"
                class="text-white"
                label
              >
                {{ media.mediaType === 'movie' ? 'MOVIE' : 'TV' }}
              </v-chip>

              <!-- Rating with star -->
              <v-chip
                v-if="media.rating"
                color="#121212"
                variant="flat"
                size="small"
                class="rating-chip-desktop"
              >
                <v-icon start color="#FFC107" size="18">mdi-star</v-icon>
                <span class="gold-text font-weight-bold">
                  {{ Number(media.rating).toFixed(1).replace('.0','') }}/5
                </span>
              </v-chip>

              <!-- Watchlist (icon only - no WL text) -->
              <v-chip
                v-else
                color="info"
                variant="flat"
                size="small"
                title="Watchlist"
              >
                <v-icon size="18">mdi-bookmark</v-icon>
              </v-chip>
            </div>
          </template>
        </v-list-item>
      </v-list>
    </div>

    <!-- Hover Modal - Desktop Only -->
    <v-dialog
      v-model="showHoverModal"
      max-width="900"
      :scrim="false"
      transition="scale-transition"
      @click:outside="closeHoverModal"
    >
      <v-card 
        v-if="hoveredMedia" 
        class="hover-preview-large" 
        @click="goToMedia(hoveredMedia.mediaId)"
        @mouseenter="keepModalOpen"
        @mouseleave="startCloseTimeout"
      >
        <v-img
          :src="hoveredMedia.backdropUrl || hoveredMedia.posterUrl"
          height="450"
          cover
          class="align-end"
          gradient="to top, rgba(18,18,18,1) 0%, rgba(18,18,18,0.7) 20%, rgba(18,18,18,0) 100%"
        >
          <div class="pa-8">
            <div class="d-flex align-center mb-2">
              <v-chip 
                size="small" 
                :color="hoveredMedia.mediaType === 'movie' ? '#1976D2' : '#7B1FA2'" 
                class="mr-3 text-white font-weight-black" 
                label
              >
                {{ hoveredMedia.mediaType.toUpperCase() }}
              </v-chip>
              <span v-if="hoveredMedia.releaseYear" class="text-h5 text-grey-lighten-1">
                {{ hoveredMedia.releaseYear }}
              </span>
            </div>
            <h2 class="text-h2 font-weight-black text-white mb-2">{{ hoveredMedia.title }}</h2>
          </div>
        </v-img>

        <v-card-text class="pa-8 bg-surface">
          <v-row>
            <v-col cols="12" md="8">
              <div class="d-flex align-center mb-6">
                <v-chip 
                  v-if="hoveredMedia.rating" 
                  color="#121212" 
                  class="mr-4 rating-label" 
                  size="large" 
                  variant="flat"
                >
                  <v-icon start color="#FFC107">mdi-star</v-icon>
                  <span class="gold-text font-weight-black text-h6">{{ hoveredMedia.rating }}/5</span>
                </v-chip>
                <v-chip 
                  v-else 
                  color="info" 
                  class="mr-4 watchlist-label" 
                  size="large" 
                  variant="flat"
                >
                  <v-icon start>mdi-bookmark</v-icon>
                  <span class="font-weight-bold">Watchlist</span>
                </v-chip>
                <v-chip v-if="hoveredMedia.tmdbRating" variant="outlined" class="mr-2">
                  TMDB {{ hoveredMedia.tmdbRating.toFixed(1) }}
                </v-chip>
              </div>
              <p class="text-h6 font-weight-regular text-grey-lighten-1 mb-6" style="line-height: 1.6;">
                {{ hoveredMedia.plot || 'No plot description available.' }}
              </p>
              <div class="d-flex flex-wrap gap-2">
                <v-chip 
                  v-for="genre in hoveredMedia.genres" 
                  :key="genre" 
                  size="small" 
                  variant="tonal" 
                  class="mr-2"
                >
                  {{ genre }}
                </v-chip>
              </div>
            </v-col>
            <v-col cols="12" md="4" class="border-s-sm border-opacity-10">
              <div class="text-overline text-grey-darken-1 mb-2">Cast</div>
              <div class="text-body-1 mb-6">
                {{ hoveredMedia.cast?.slice(0, 5).map(c => c.name).join(', ') || 'N/A' }}
              </div>
            </v-col>
          </v-row>
        </v-card-text>

        <v-divider></v-divider>
        <v-card-actions class="pa-6 justify-center">
          <v-btn color="primary" variant="flat" size="large" block>
            View Full Details <v-icon end>mdi-chevron-right</v-icon>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <delete-confirm-dialog 
      :show="showDeleteDialog" 
      :movie-title="mediaToDelete?.title || ''" 
      :deleting="isDeleting" 
      @cancel="cancelDelete" 
      @confirm="handleDelete" 
    />
  </div>
</template>

<script>
import { mediaAPI } from '@/services/api-production';
import DeleteConfirmDialog from '@/components/DeleteConfirmDialog.vue';

export default {
  name: 'AllMediaView',
  components: { DeleteConfirmDialog },
  
  data() {
    return {
      mediaList: [],
      loading: false,
      error: null,
      searchQuery: '',
      filterType: null,
      filterRating: null,
      sortBy: 'dateAdded',
      viewMode: 'grid',
      showHoverModal: false,
      hoveredMedia: null,
      hoverTimeout: null,
      closeTimeout: null,
      showDeleteDialog: false,
      mediaToDelete: null,
      isDeleting: false,
      typeOptions: [
        { title: 'Movies', value: 'movie' }, 
        { title: 'TV Shows', value: 'tv' }
      ],
      ratingOptions: [5, 4, 3, 2, 1].map(r => ({ title: `${r} Stars`, value: r })),
      sortOptions: [
        { title: 'Recently Added', value: 'dateAdded' }, 
        { title: 'Title (A-Z)', value: 'titleAsc' }, 
        { title: 'Rating (High to Low)', value: 'ratingDesc' }
      ],
    };
  },
  
  computed: {
    hasActiveFilters() { 
      return this.searchQuery || this.filterType || this.filterRating; 
    },
    
    filteredMedia() {
      let result = [...this.mediaList];
      
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(m => m.title.toLowerCase().includes(query));
      }
      
      if (this.filterType) {
        result = result.filter(m => m.mediaType === this.filterType);
      }
      
      if (this.filterRating !== null) {
        result = result.filter(m => m.rating === this.filterRating);
      }
      
      switch (this.sortBy) {
        case 'titleAsc': 
          result.sort((a, b) => a.title.localeCompare(b.title)); 
          break;
        case 'ratingDesc': 
          result.sort((a, b) => (b.rating || 0) - (a.rating || 0)); 
          break;
        default: 
          result.sort((a, b) => new Date(b.createdAt || 0) - new Date(a.createdAt || 0));
      }
      
      return result;
    },
    
    isMobile() { 
      return this.$vuetify.display.mobile; 
    }
  },
  
  methods: {
    async getAllMedia() {
      this.loading = true;
      try { 
        this.mediaList = await mediaAPI.getAll(); 
      } catch (err) { 
        this.error = 'Failed to load media.'; 
      } finally { 
        this.loading = false; 
      }
    },
    
    // Desktop hover modal
    startHover(media) {
      if (this.isMobile) return;
      
      this.clearCloseTimeout();
      this.cancelHover();
      
      this.hoverTimeout = setTimeout(() => {
        this.hoveredMedia = media;
        this.showHoverModal = true;
      }, 500); // Slightly longer delay for better UX
    },
    
    cancelHover() { 
      if (this.hoverTimeout) { 
        clearTimeout(this.hoverTimeout); 
        this.hoverTimeout = null; 
      } 
    },
    
    startCloseTimeout() { 
      this.closeTimeout = setTimeout(() => { 
        this.showHoverModal = false;
        this.hoveredMedia = null;
      }, 200);
    },
    
    keepModalOpen() {
      this.clearCloseTimeout();
    },
    
    clearCloseTimeout() { 
      if (this.closeTimeout) { 
        clearTimeout(this.closeTimeout); 
        this.closeTimeout = null; 
      } 
    },
    
    closeHoverModal() {
      this.showHoverModal = false;
      this.hoveredMedia = null;
      this.clearCloseTimeout();
    },
    
    // Click handler for both mobile and desktop
    handleCardClick(media) {
      if (this.isMobile) {
        // Mobile: direct navigation
        this.goToMedia(media.mediaId);
      } else {
        // Desktop: modal is already shown on hover, click navigates
        this.goToMedia(media.mediaId);
      }
    },
    
    goToMedia(mediaId) { 
      this.closeHoverModal(); 
      this.$router.push(`/movies/${mediaId}`); 
    },
    
    confirmDelete(media) { 
      this.mediaToDelete = media; 
      this.showDeleteDialog = true; 
    },
    
    cancelDelete() { 
      this.showDeleteDialog = false; 
      this.mediaToDelete = null; 
    },
    
    async handleDelete() {
      if (!this.mediaToDelete) return;
      
      this.isDeleting = true;
      try {
        await mediaAPI.delete(this.mediaToDelete.mediaId);
        this.mediaList = this.mediaList.filter(m => m.mediaId !== this.mediaToDelete.mediaId);
        this.showDeleteDialog = false;
        this.closeHoverModal();
      } finally { 
        this.isDeleting = false; 
      }
    },
    
    clearFilters() { 
      this.searchQuery = ''; 
      this.filterType = null; 
      this.filterRating = null; 
      this.sortBy = 'dateAdded'; 
    }
  },
  
  created() { 
    this.getAllMedia(); 
  }
};
</script>

<style scoped>
/* === LAYOUT === */
.all-media { 
  max-width: 1600px; 
  margin: 0 auto; 
  padding-top: 16px; 
}

.gap-3 { gap: 12px; }

.search-bar :deep(.v-field__input) {
  padding-top: 10px !important;
  padding-bottom: 10px !important;
}

/* === EMPTY STATE === */
.empty-state-cinematic {
  background: radial-gradient(circle at center, rgba(var(--v-theme-primary), 0.08) 0%, transparent 75%);
  padding: 100px 0;
  border-radius: 24px;
}

.film-reel-svg {
  color: rgb(var(--v-theme-primary));
  filter: drop-shadow(0 0 15px rgba(var(--v-theme-primary), 0.4));
  animation: rotateReel 20s linear infinite;
}

@keyframes rotateReel { 
  from { transform: rotate(0deg); } 
  to { transform: rotate(360deg); } 
}

.empty-icon-wrapper { 
  perspective: 1000px; 
  display: flex; 
  justify-content: center; 
}

/* === GRID VIEW === */
.media-card { 
  cursor: pointer; 
  transition: transform 0.3s ease; 
  background: transparent !important; 
}

.media-card:hover { 
  transform: translateY(-8px); 
}

.poster-container { 
  position: relative; 
  aspect-ratio: 2/3; 
  border-radius: 12px; 
  overflow: hidden; 
  box-shadow: 0 4px 20px rgba(0,0,0,0.4); 
}

/* Scrim */
.top-scrim {
  position: absolute; 
  top: 0; 
  left: 0; 
  right: 0;
  height: 60px;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0.85) 0%,
    rgba(0, 0, 0, 0.4) 70%,
    rgba(0, 0, 0, 0) 100%
  );
  z-index: 1;
}

/* Badge overlay container */
.overlay-content {
  position: absolute; 
  top: 0; 
  left: 0; 
  right: 0;
  z-index: 2;
  pointer-events: none;
  padding: 8px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

/* === DESKTOP BADGES (Default - Large) === */
.badge-type {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 28px;
  min-width: 28px;
  padding: 0 8px;
  border-radius: 6px;
  font-size: 13px;
  line-height: 1;
  font-weight: 800;
  letter-spacing: 0.5px;
  color: #fff;
  box-shadow: 0 2px 10px rgba(0,0,0,0.7);
  border: 1.5px solid rgba(255,255,255,0.2);
}

.badge-type--movie { 
  background: #1976D2; 
}

.badge-type--tv { 
  background: #7B1FA2; 
}

.badge-corner-right {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

/* Rating badge - Desktop */
.badge-rating {
  display: inline-flex;
  align-items: center;
  height: 28px;
  padding: 0 8px;
  border-radius: 6px;
  border: 1.5px solid rgba(255,255,255,0.15);
  box-shadow: 0 2px 10px rgba(0,0,0,0.9);
  background: rgba(18, 18, 18, 0.95);
  backdrop-filter: blur(8px);
  gap: 4px;
}

.badge-rating__star {
  font-size: 18px !important;
}

.badge-rating__value {
  font-size: 14px;
  font-weight: 800;
  line-height: 1;
  color: #FFC107;
}

/* Watchlist badge - Icon only (NO "WL" text) */
.badge-watchlist {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 28px;
  width: 28px;
  padding: 0;
  border-radius: 6px;
  background: rgba(33, 150, 243, 0.2);
  border: 1.5px solid rgba(33, 150, 243, 0.4);
  box-shadow: 0 2px 8px rgba(0,0,0,0.8);
  backdrop-filter: blur(8px);
}

.badge-watchlist__icon {
  font-size: 18px !important;
  color: #2196F3 !important;
}

.gold-text { 
  color: #FFC107 !important; 
}

/* === LIST VIEW === */
.list-item-hoverable { 
  transition: background-color 0.2s ease; 
}

.list-item-hoverable:hover { 
  background-color: rgba(var(--v-theme-primary), 0.05); 
}

.list-avatar { 
  margin-right: 12px !important; 
}

.list-title { 
  line-height: 1.3; 
}

.rating-chip-desktop .v-chip__content {
  font-size: 14px;
  gap: 4px;
}

/* === MODAL === */
.hover-preview-large { 
  border-radius: 20px !important; 
  background-color: #121212 !important; 
  overflow: hidden;
  cursor: pointer;
}

:deep(.v-overlay__content) {
  margin: 0 !important;
  pointer-events: auto !important;
}

/* === MOBILE OPTIMIZATIONS === */
@media (max-width: 600px) {
  /* Smaller badges on mobile */
  .badge-type {
    height: 20px;
    min-width: 20px;
    padding: 0 5px;
    font-size: 10px;
    border-radius: 4px;
    border-width: 1px;
  }

  .badge-rating {
    height: 20px;
    padding: 0 5px;
    border-radius: 4px;
    gap: 2px;
  }

  .badge-rating__star {
    font-size: 14px !important;
  }

  .badge-rating__value {
    font-size: 11px;
  }

  .badge-watchlist {
    height: 20px;
    width: 20px;
    border-radius: 4px;
  }

  .badge-watchlist__icon {
    font-size: 14px !important;
  }

  /* Tighter scrim on mobile */
  .top-scrim {
    height: 40px;
  }

  .overlay-content {
    padding: 4px;
  }

  /* List view mobile meta row */
  .list-meta-row {
    display: flex; 
    align-items: center;
    margin-top: 6px; 
    gap: 6px;
  }

  .list-meta-row .spacer { 
    flex: 1 1 auto; 
  }

  .rating-chip-mobile .v-chip__content {
    font-size: 12px;
  }

  /* Touch-friendly hover */
  .media-card:active { 
    transform: scale(0.98); 
  }
}

/* === TABLET (601px - 960px) === */
@media (min-width: 601px) and (max-width: 960px) {
  /* Medium-sized badges for tablets */
  .badge-type {
    height: 24px;
    min-width: 24px;
    font-size: 11px;
  }

  .badge-rating {
    height: 24px;
  }

  .badge-rating__star {
    font-size: 16px !important;
  }

  .badge-rating__value {
    font-size: 12px;
  }

  .badge-watchlist {
    height: 24px;
    width: 24px;
  }

  .badge-watchlist__icon {
    font-size: 16px !important;
  }
}
</style>
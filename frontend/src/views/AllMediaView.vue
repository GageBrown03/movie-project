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
    </v-row>

    <!-- IMPROVED: Mobile-friendly filters -->
    <v-row class="mb-6 align-center" no-gutters>
      <v-col cols="12">
        <div class="filters-container">
          <!-- IMPROVED: Horizontal scroll on mobile, flex-wrap on desktop -->
          <div :class="['filters-row', { 'filters-mobile': isMobile }]">
            <v-select
              v-model="filterType"
              :items="typeOptions"
              label="Type"
              variant="outlined"
              density="compact"
              hide-details
              clearable
              class="filter-select"
            />

            <!-- NEW: Status Filter -->
            <v-select
              v-model="filterStatus"
              :items="statusOptions"
              label="Status"
              variant="outlined"
              density="compact"
              hide-details
              clearable
              class="filter-select"
            />

            <v-select
              v-model="filterRating"
              :items="ratingOptions"
              label="Rating"
              variant="outlined"
              density="compact"
              hide-details
              clearable
              class="filter-select"
            />

            <v-select
              v-model="sortBy"
              :items="sortOptions"
              label="Sort"
              variant="outlined"
              density="compact"
              hide-details
              class="filter-select"
            />

            <v-btn 
              v-if="hasActiveFilters" 
              variant="text" 
              color="grey" 
              size="small" 
              prepend-icon="mdi-filter-off-outline"
              @click="clearFilters"
              class="text-none filter-reset"
            >
              Reset
            </v-btn>
          </div>

          <v-spacer v-if="!isMobile" />

          <!-- View toggle, count & Add button -->
          <div class="view-controls">
            <span class="text-caption text-grey mr-3">{{ filteredMedia.length }} items</span>
            <v-btn-toggle v-model="viewMode" mandatory density="compact" color="primary" class="mr-3">
              <v-btn value="grid" icon="mdi-view-grid-outline" size="small" />
              <v-btn value="list" icon="mdi-view-list" size="small" />
            </v-btn-toggle>
            <v-btn
              color="primary"
              variant="flat"
              size="small"
              prepend-icon="mdi-plus"
              class="font-weight-bold text-none add-media-btn"
              @click="openAddDialog"
            >
              <span class="d-none d-sm-inline">Add</span>
            </v-btn>
          </div>
        </div>
      </v-col>
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
    
    <!-- GRAND EMPTY STATE -->
    <div v-else-if="mediaList.length === 0" class="grand-empty">
      <div class="grand-empty__bg" />

      <!-- Film strip top -->
      <div class="filmstrip filmstrip--top" aria-hidden="true">
        <span v-for="n in 20" :key="'t'+n" class="filmstrip__frame" />
      </div>

      <div class="grand-empty__content">
        <!-- Spinning reel -->
        <div class="reel-wrap">
          <svg class="reel-svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <circle cx="50" cy="50" r="46" stroke="currentColor" stroke-width="1.5" fill="none" opacity="0.2"/>
            <circle cx="50" cy="50" r="30" stroke="currentColor" stroke-width="1" fill="none" opacity="0.15"/>
            <circle cx="50" cy="50" r="6" fill="currentColor" opacity="0.6"/>
            <circle cx="50" cy="16" r="5" fill="currentColor" opacity="0.35"/>
            <circle cx="50" cy="84" r="5" fill="currentColor" opacity="0.35"/>
            <circle cx="16" cy="50" r="5" fill="currentColor" opacity="0.35"/>
            <circle cx="84" cy="50" r="5" fill="currentColor" opacity="0.35"/>
            <circle cx="26" cy="26" r="4" fill="currentColor" opacity="0.25"/>
            <circle cx="74" cy="26" r="4" fill="currentColor" opacity="0.25"/>
            <circle cx="26" cy="74" r="4" fill="currentColor" opacity="0.25"/>
            <circle cx="74" cy="74" r="4" fill="currentColor" opacity="0.25"/>
          </svg>
        </div>

        <p class="grand-empty__overline">EST. TODAY</p>
        <h1 class="grand-empty__headline">
          Nothing to see here.<br />
          <span class="grand-empty__headline--dim">Literally.</span>
        </h1>
        <p class="grand-empty__body">
          Your library has fewer titles than a silent film.<br />
          Time to fix that — where do you want to start?
        </p>

        <!-- Two-path choice -->
        <div class="grand-paths">
          <!-- Path 1: Log something -->
          <button class="grand-path grand-path--log" @click="openAddDialog">
            <span class="grand-path__stripe-bar" aria-hidden="true">
              <span v-for="n in 6" :key="n" class="grand-path__stripe" />
            </span>
            <span class="grand-path__inner">
              <span class="grand-path__emoji">🎬</span>
              <span class="grand-path__text">
                <span class="grand-path__label">Log Something I've Seen</span>
                <span class="grand-path__sub">Search by title, rate it, add your review</span>
              </span>
              <span class="grand-path__arrow"><i class="mdi mdi-arrow-right"></i></span>
            </span>
          </button>

          <div class="grand-paths__or"><span>or</span></div>

          <!-- Path 2: Discover -->
          <button class="grand-path grand-path--discover" @click="$router.push('/discover')">
            <span class="grand-path__stripe-bar" aria-hidden="true">
              <span v-for="n in 6" :key="n" class="grand-path__stripe" />
            </span>
            <span class="grand-path__inner">
              <span class="grand-path__emoji">🧭</span>
              <span class="grand-path__text">
                <span class="grand-path__label">Find My Next Watch</span>
                <span class="grand-path__sub">Curated picks, genres, trending & hidden gems</span>
              </span>
              <span class="grand-path__arrow"><i class="mdi mdi-arrow-right"></i></span>
            </span>
          </button>
        </div>

        <p class="grand-empty__footnote">No popcorn required, but recommended.</p>
      </div>

      <!-- Film strip bottom -->
      <div class="filmstrip filmstrip--bottom" aria-hidden="true">
        <span v-for="n in 20" :key="'b'+n" class="filmstrip__frame" />
      </div>
    </div>

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
                <div class="top-scrim"></div>

                <div class="overlay-content">
                  <div
                    class="badge-type"
                    :class="media.mediaType === 'movie' ? 'badge-type--movie' : 'badge-type--tv'"
                  >
                    {{ media.mediaType === 'movie' ? 'M' : 'TV' }}
                  </div>

                  <div class="badge-corner-right">
                    <div v-if="media.rating" class="badge-rating">
                      <v-icon class="badge-rating__star" color="#FFC107">
                        mdi-star
                      </v-icon>
                      <span class="badge-rating__value">
                        {{ Number(media.rating).toFixed(1).replace('.0','') }}
                      </span>
                    </div>

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
          <template v-slot:prepend>
            <v-avatar size="80" rounded class="mr-3 list-avatar">
              <v-img v-if="media.posterUrl" :src="media.posterUrl" cover />
            </v-avatar>
          </template>

          <div class="w-100">
            <v-list-item-title class="list-title text-subtitle-1 font-weight-bold">
              {{ media.title }}
            </v-list-item-title>

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

          <template v-slot:append>
            <div v-if="!isMobile" class="d-flex align-center gap-2">
              <v-chip
                size="small"
                :color="media.mediaType === 'movie' ? '#1976D2' : '#7B1FA2'"
                class="text-white"
                label
              >
                {{ media.mediaType === 'movie' ? 'MOVIE' : 'TV' }}
              </v-chip>

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

    <!-- Hover Modal -->
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
      filterStatus: null, // NEW
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
      // NEW: Status filter options
      statusOptions: [
        { title: 'Watched', value: 'watched' },
        { title: 'Watchlist', value: 'want_to_watch' }
      ],
      ratingOptions: [5, 4, 3, 2, 1].map(r => ({ title: `${r} Stars`, value: r })),
      // IMPROVED: Shortened mobile labels
      sortOptions: [
        { title: isMobile => isMobile ? 'Recent' : 'Recently Added', value: 'dateAdded' }, 
        { title: 'Title (A-Z)', value: 'titleAsc' }, 
        { title: isMobile => isMobile ? 'Rating' : 'Rating (High to Low)', value: 'ratingDesc' }
      ].map(opt => ({
        title: typeof opt.title === 'function' ? opt.title(this.$vuetify?.display?.mobile) : opt.title,
        value: opt.value
      })),
    };
  },
  
  computed: {
    hasActiveFilters() { 
      return this.searchQuery || this.filterType || this.filterStatus || this.filterRating; 
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

      // NEW: Status filter
      if (this.filterStatus) {
        result = result.filter(m => m.status === this.filterStatus);
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
    
    startHover(media) {
      if (this.isMobile) return;
      
      this.clearCloseTimeout();
      this.cancelHover();
      
      this.hoverTimeout = setTimeout(() => {
        this.hoveredMedia = media;
        this.showHoverModal = true;
      }, 500);
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
    
    handleCardClick(media) {
      if (this.isMobile) {
        this.goToMedia(media.mediaId);
      } else {
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
      this.filterStatus = null;
      this.filterRating = null; 
      this.sortBy = 'dateAdded'; 
    },

    openAddDialog() {
      window.dispatchEvent(new CustomEvent('open-add-media-dialog'));
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

/* IMPROVED: Mobile-friendly filters */
.filters-container {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
}

.filters-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

/* Mobile: Horizontal scroll */
.filters-mobile {
  flex-wrap: nowrap;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE/Edge */
}

.filters-mobile::-webkit-scrollbar {
  display: none; /* Chrome/Safari */
}

.filter-select {
  min-width: 110px;
  flex-shrink: 0;
}

.add-media-btn {
  flex-shrink: 0;
}

.filter-reset {
  flex-shrink: 0;
}

.view-controls {
  display: flex;
  align-items: center;
  flex-shrink: 0;
  margin-left: auto;
}

@media (max-width: 600px) {
  .filters-container {
    flex-direction: column;
    align-items: stretch;
  }

  .view-controls {
    justify-content: space-between;
    margin-left: 0;
    margin-top: 8px;
  }
}

.search-bar :deep(.v-field__input) {
  padding-top: 10px !important;
  padding-bottom: 10px !important;
}

/* ═══════════════════════════════════════
   GRAND EMPTY STATE
═══════════════════════════════════════ */
.grand-empty {
  position: relative;
  min-height: 72vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  border-radius: 20px;
  margin-top: 8px;
}

.grand-empty__bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 60% 50% at 50% 40%, rgba(var(--v-theme-primary), 0.08) 0%, transparent 70%),
    repeating-linear-gradient(
      0deg,
      transparent,
      transparent 39px,
      rgba(var(--v-theme-on-surface), 0.02) 39px,
      rgba(var(--v-theme-on-surface), 0.02) 40px
    );
  pointer-events: none;
  z-index: 0;
}

/* Film strip bars */
.filmstrip {
  position: absolute;
  left: 0; right: 0;
  height: 48px;
  display: flex;
  z-index: 1;
  background: rgba(var(--v-theme-on-surface), 0.05);
  border-top: 1px solid rgba(var(--v-theme-on-surface), 0.07);
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.07);
  overflow: hidden;
}

.filmstrip--top { top: 0; }
.filmstrip--bottom { bottom: 0; }

.filmstrip__frame {
  flex: 1;
  display: block;
  border-left: 1px solid rgba(var(--v-theme-on-surface), 0.08);
  margin: 8px 0;
}

.filmstrip__frame::before {
  content: '';
  display: block;
  margin: 2px 4px;
  height: calc(100% - 4px);
  border-radius: 2px;
  background: rgba(var(--v-theme-on-surface), 0.04);
}

/* Main content */
.grand-empty__content {
  position: relative;
  z-index: 2;
  text-align: center;
  padding: 72px 32px;
  max-width: 560px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Spinning reel */
.reel-wrap {
  width: 110px;
  height: 110px;
  color: rgb(var(--v-theme-primary));
  margin-bottom: 24px;
  filter: drop-shadow(0 0 18px rgba(var(--v-theme-primary), 0.3));
}

.reel-svg {
  width: 100%;
  height: 100%;
  animation: spinReel 14s linear infinite;
}

@keyframes spinReel {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}

.grand-empty__overline {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: rgb(var(--v-theme-primary));
  margin: 0 0 12px;
}

.grand-empty__headline {
  font-size: clamp(1.9rem, 4.5vw, 2.8rem);
  font-weight: 900;
  line-height: 1.1;
  letter-spacing: -0.02em;
  margin: 0 0 14px;
}

.grand-empty__headline--dim {
  opacity: 0.3;
  font-style: italic;
}

.grand-empty__body {
  font-size: 0.95rem;
  color: rgba(var(--v-theme-on-surface), 0.5);
  line-height: 1.65;
  margin: 0 0 32px;
}

/* ── Two-path grand buttons ── */
.grand-paths {
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 0;
  margin-bottom: 24px;
}

.grand-path {
  position: relative;
  display: flex;
  flex-direction: column;
  border: none;
  padding: 0;
  cursor: pointer;
  background: none;
  overflow: hidden;
  border-radius: 14px;
  box-shadow: 0 6px 28px rgba(0, 0, 0, 0.25);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.grand-path:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
}

.grand-path:active {
  transform: scale(0.98);
}

/* Clapperboard-style stripe bar on each button */
.grand-path__stripe-bar {
  display: flex;
  height: 14px;
  overflow: hidden;
  border-bottom: 1.5px solid rgba(0,0,0,0.3);
}

.grand-path__stripe {
  flex: 1;
}

.grand-path--log .grand-path__stripe-bar {
  background: #1a1a1a;
}

.grand-path--log .grand-path__stripe:nth-child(odd)  { background: #fff; opacity: 0.9; }
.grand-path--log .grand-path__stripe:nth-child(even) { background: #1a1a1a; }

.grand-path--discover .grand-path__stripe-bar {
  background: #1a1a1a;
}

.grand-path--discover .grand-path__stripe:nth-child(odd)  { background: #7C4DFF; opacity: 0.85; }
.grand-path--discover .grand-path__stripe:nth-child(even) { background: #1a1a1a; }

/* Inner content row */
.grand-path__inner {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px 20px;
}

.grand-path--log .grand-path__inner {
  background: rgb(var(--v-theme-primary));
}

.grand-path--discover .grand-path__inner {
  background: #5E35B1;
}

.grand-path__emoji {
  font-size: 1.6rem;
  line-height: 1;
  flex-shrink: 0;
}

.grand-path__text {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
  text-align: left;
}

.grand-path__label {
  font-size: 0.95rem;
  font-weight: 800;
  color: #fff;
  line-height: 1.2;
  letter-spacing: 0.01em;
}

.grand-path__sub {
  font-size: 0.75rem;
  color: rgba(255,255,255,0.65);
  line-height: 1.3;
}

.grand-path__arrow {
  flex-shrink: 0;
  color: rgba(255,255,255,0.5);
  font-size: 18px;
  transition: transform 0.2s ease, color 0.2s ease;
}

.grand-path:hover .grand-path__arrow {
  transform: translateX(4px);
  color: #fff;
}

.grand-paths__or {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  color: rgba(var(--v-theme-on-surface), 0.3);
  font-size: 0.72rem;
  font-style: italic;
  letter-spacing: 0.05em;
}

.grand-paths__or::before,
.grand-paths__or::after {
  content: '';
  flex: 1;
  height: 1px;
  background: rgba(var(--v-theme-on-surface), 0.08);
}

.grand-empty__footnote {
  font-size: 0.75rem;
  color: rgba(var(--v-theme-on-surface), 0.25);
  font-style: italic;
  margin: 0;
}

@media (max-width: 600px) {
  .grand-empty__content {
    padding: 56px 16px;
  }

  .reel-wrap {
    width: 84px;
    height: 84px;
  }

  .filmstrip {
    height: 36px;
  }

  .grand-path__inner {
    padding: 14px 16px;
    gap: 12px;
  }

  .grand-path__emoji {
    font-size: 1.3rem;
  }
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

  .top-scrim {
    height: 40px;
  }

  .overlay-content {
    padding: 4px;
  }

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

  .media-card:active { 
    transform: scale(0.98); 
  }
}

/* === TABLET (601px - 960px) === */
@media (min-width: 601px) and (max-width: 960px) {
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
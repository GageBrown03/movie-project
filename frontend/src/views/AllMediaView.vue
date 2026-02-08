<template>
  <div class="all-media">
    <v-row class="mb-6 align-center">
      <v-col>
        <h1 class="text-h3 font-weight-bold">My Collection</h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          {{ filteredMedia.length }} {{ filteredMedia.length === 1 ? 'item' : 'items' }}
        </p>
      </v-col>
      <v-col cols="auto">
        <v-btn color="primary" size="large" to="/movies/new" prepend-icon="mdi-plus">
          Add Movie/TV
        </v-btn>
      </v-col>
    </v-row>

    <v-card class="mb-6" elevation="2">
      <v-card-text>
        <v-row>
          <v-col cols="12" md="4">
            <v-text-field
              v-model="searchQuery"
              prepend-inner-icon="mdi-magnify"
              label="Search..."
              variant="outlined"
              density="comfortable"
              clearable
              hide-details
            />
          </v-col>
          <v-col cols="12" md="2">
            <v-select v-model="filterType" :items="typeOptions" label="Type" variant="outlined" density="comfortable" clearable hide-details />
          </v-col>
          <v-col cols="12" md="2">
            <v-select v-model="filterStatus" :items="statusOptions" label="Status" variant="outlined" density="comfortable" clearable hide-details />
          </v-col>
          <v-col cols="12" md="2">
            <v-select v-model="filterRating" :items="ratingOptions" label="Rating" variant="outlined" density="comfortable" clearable hide-details />
          </v-col>
          <v-col cols="12" md="2">
            <v-select v-model="sortBy" :items="sortOptions" label="Sort by" variant="outlined" density="comfortable" hide-details />
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
    
    <v-row v-if="loading" justify="center" class="my-12">
      <v-progress-circular indeterminate size="64" color="primary" />
    </v-row>
    
    <v-alert v-else-if="error" type="error" variant="tonal" class="mb-4">
      {{ error }}
      <template v-slot:append>
        <v-btn @click="getAllMedia" variant="text">Retry</v-btn>
      </template>
    </v-alert>
    
    <v-empty-state v-else-if="mediaList.length === 0" icon="mdi-movie-open-outline" title="No media yet" text="Start building your collection">
      <template v-slot:actions>
        <v-btn color="primary" size="large" to="/movies/new">Add Your First Movie or Show</v-btn>
      </template>
    </v-empty-state>

    <div v-else>
      <v-row class="mb-4 align-center">
        <v-col>
          <v-chip variant="text">{{ filteredMedia.length }} results</v-chip>
        </v-col>
        <v-col cols="auto">
          <v-btn-toggle v-model="viewMode" mandatory density="compact">
            <v-btn value="grid" icon="mdi-view-grid" />
            <v-btn value="list" icon="mdi-view-list" />
          </v-btn-toggle>
        </v-col>
      </v-row>

      <v-row v-if="viewMode === 'grid'">
        <v-col v-for="media in filteredMedia" :key="media.mediaId" cols="12" sm="6" md="4" lg="3">
          <v-card
            class="media-card"
            flat
            @mouseenter="startHover(media)"
            @mouseleave="cancelHover"
            @click="goToMedia(media.mediaId)"
          >
            <div class="poster-container">
              <v-img v-if="media.posterUrl" :src="media.posterUrl" aspect-ratio="2/3" cover class="poster-image">
                <div class="top-scrim"></div>
                <div class="overlay-content pa-2">
                  <div class="d-flex justify-space-between align-center">
                    <v-chip size="x-small" :color="media.mediaType === 'movie' ? '#1976D2' : '#7B1FA2'" class="type-label font-weight-black text-white" variant="flat" label>
                      {{ media.mediaType.toUpperCase() }}
                    </v-chip>
                    <v-chip v-if="media.rating" size="small" color="#121212" class="rating-label font-weight-black" variant="flat">
                      <v-icon start size="14" color="#FFC107">mdi-star</v-icon>
                      <span class="gold-text">{{ media.rating }}/5</span>
                    </v-chip>
                    <v-chip v-else size="small" color="#121212" class="rating-label font-weight-black text-white" variant="flat">
                      <v-icon start size="14" color="white">mdi-bookmark</v-icon> WATCH
                    </v-chip>
                  </div>
                </div>
              </v-img>
            </div>
            <v-card-text class="px-1 py-3 text-center">
              <div class="text-subtitle-1 font-weight-bold text-truncate">{{ media.title }}</div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-list v-else lines="two" class="bg-transparent">
        <v-list-item v-for="media in filteredMedia" :key="media.mediaId" @click="goToMedia(media.mediaId)" link class="mb-2 rounded-lg border">
          <template v-slot:prepend>
            <v-avatar size="80" rounded class="mr-4">
              <v-img v-if="media.posterUrl" :src="media.posterUrl" cover />
            </v-avatar>
          </template>
          <v-list-item-title class="text-h6 font-weight-bold">
            {{ media.title }}
            <v-chip :color="media.mediaType === 'movie' ? '#1976D2' : '#7B1FA2'" size="x-small" class="ml-2 text-white" label>{{ media.mediaType.toUpperCase() }}</v-chip>
          </v-list-item-title>
          <template v-slot:append>
            <v-chip v-if="media.rating" color="#121212" variant="flat" class="rating-label">
              <v-icon start color="#FFC107" size="small">mdi-star</v-icon>
              <span class="gold-text font-weight-bold">{{ media.rating }}/5</span>
            </v-chip>
          </template>
        </v-list-item>
      </v-list>
    </div>

    <v-dialog
      v-model="showHoverModal"
      max-width="900"
      :scrim="false"
      transition="scale-transition"
      persistent
      @click:outside="closeHoverModalImmediately"
      class="hover-dialog-clean"
    >
      <div 
        class="modal-capture-area"
        @mouseenter="clearCloseTimeout" 
        @mouseleave="startCloseTimeout"
      >
        <v-card v-if="hoveredMedia" class="hover-preview-large" @click="goToMedia(hoveredMedia.mediaId)">
          <v-img
            :src="hoveredMedia.backdropUrl || hoveredMedia.posterUrl"
            height="450"
            cover
            class="align-end"
            :image-props="{ class: 'zoom-animation' }"
            gradient="to top, rgba(18,18,18,1) 0%, rgba(18,18,18,0.7) 20%, rgba(18,18,18,0) 100%"
          >
            <div class="pa-8">
              <div class="d-flex align-center mb-2">
                <v-chip size="small" :color="hoveredMedia.mediaType === 'movie' ? '#1976D2' : '#7B1FA2'" class="mr-3 text-white font-weight-black" label>
                  {{ hoveredMedia.mediaType.toUpperCase() }}
                </v-chip>
                <span v-if="hoveredMedia.releaseYear" class="text-h5 text-grey-lighten-1">{{ hoveredMedia.releaseYear }}</span>
              </div>
              <h2 class="text-h2 font-weight-black text-white mb-2">{{ hoveredMedia.title }}</h2>
            </div>
          </v-img>

          <v-card-text class="pa-8 bg-surface">
            <v-row>
              <v-col cols="12" md="8">
                <div class="d-flex align-center mb-6">
                  <v-chip v-if="hoveredMedia.rating" color="#121212" class="mr-4 rating-label" size="large" variant="flat">
                    <v-icon start color="#FFC107">mdi-star</v-icon>
                    <span class="gold-text font-weight-black text-h6">{{ hoveredMedia.rating }}/5</span>
                  </v-chip>
                  <v-chip v-if="hoveredMedia.tmdbRating" variant="outlined" class="mr-2">TMDB {{ hoveredMedia.tmdbRating.toFixed(1) }}</v-chip>
                </div>
                <p class="text-h6 font-weight-regular text-grey-lighten-1 mb-6" style="line-height: 1.6;">{{ hoveredMedia.plot || 'No plot description available.' }}</p>
                <div class="d-flex flex-wrap gap-2">
                  <v-chip v-for="genre in hoveredMedia.genres" :key="genre" size="small" variant="tonal" class="mr-2">{{ genre }}</v-chip>
                </div>
              </v-col>
              <v-col cols="12" md="4" class="border-s-sm border-opacity-10">
                <div class="text-overline text-grey-darken-1 mb-2">Cast</div>
                <div class="text-body-1 mb-6">{{ hoveredMedia.cast?.slice(0, 5).map(c => c.name).join(', ') || 'N/A' }}</div>
              </v-col>
            </v-row>
          </v-card-text>

          <v-divider></v-divider>
          <v-card-actions class="pa-6">
            <v-btn variant="text" color="grey" @click.stop="goToEdit(hoveredMedia.mediaId)"><v-icon start>mdi-pencil</v-icon> Edit</v-btn>
            <v-spacer />
            <v-btn color="primary" variant="flat" size="large">Full Details <v-icon end>mdi-chevron-right</v-icon></v-btn>
          </v-card-actions>
        </v-card>
      </div>
    </v-dialog>

    <delete-confirm-dialog :show="showDeleteDialog" :movie-title="mediaToDelete?.title || ''" :deleting="isDeleting" @cancel="cancelDelete" @confirm="handleDelete" />
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
      filterStatus: null,
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
      typeOptions: [{ title: 'Movies', value: 'movie' }, { title: 'TV Shows', value: 'tv' }],
      statusOptions: [{ title: 'Watched', value: 'watched' }, { title: 'Watchlist', value: 'want_to_watch' }, { title: 'Watching', value: 'watching' }],
      ratingOptions: [5, 4, 3, 2, 1].map(r => ({ title: `${r} Stars`, value: r })),
      sortOptions: [{ title: 'Recently Added', value: 'dateAdded' }, { title: 'Title (A-Z)', value: 'titleAsc' }, { title: 'Rating (High to Low)', value: 'ratingDesc' }],
    };
  },
  computed: {
    filteredMedia() {
      let result = [...this.mediaList];
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(m => m.title.toLowerCase().includes(query));
      }
      if (this.filterType) result = result.filter(m => m.mediaType === this.filterType);
      if (this.filterStatus) result = result.filter(m => m.status === this.filterStatus);
      if (this.filterRating !== null) result = result.filter(m => m.rating === this.filterRating);
      
      switch (this.sortBy) {
        case 'titleAsc': result.sort((a, b) => a.title.localeCompare(b.title)); break;
        case 'ratingDesc': result.sort((a, b) => (b.rating || 0) - (a.rating || 0)); break;
        default: result.sort((a, b) => new Date(b.createdAt || 0) - new Date(a.createdAt || 0));
      }
      return result;
    },
    isMobile() { return this.$vuetify.display.mobile; }
  },
  methods: {
    async getAllMedia() {
      this.loading = true;
      try { this.mediaList = await mediaAPI.getAll(); } 
      catch (err) { this.error = 'Failed to load media.'; } 
      finally { this.loading = false; }
    },
    startHover(media) {
      if (this.isMobile) return;
      this.clearCloseTimeout();
      this.cancelHover();
      this.hoverTimeout = setTimeout(() => {
        this.hoveredMedia = media;
        this.showHoverModal = true;
      }, 450);
    },
    cancelHover() {
      if (this.hoverTimeout) { clearTimeout(this.hoverTimeout); this.hoverTimeout = null; }
    },
    startCloseTimeout() {
      // 250ms Grace Period
      this.closeTimeout = setTimeout(() => { this.showHoverModal = false; }, 250);
    },
    clearCloseTimeout() {
      if (this.closeTimeout) { clearTimeout(this.closeTimeout); this.closeTimeout = null; }
    },
    closeHoverModalImmediately() {
      this.showHoverModal = false;
      this.clearCloseTimeout();
    },
    goToMedia(mediaId) {
      this.closeHoverModalImmediately();
      this.$router.push(`/movies/${mediaId}`);
    },
    goToEdit(mediaId) {
      this.closeHoverModalImmediately();
      this.$router.push(`/movies/${mediaId}/edit`);
    },
    confirmDelete(media) { this.mediaToDelete = media; this.showDeleteDialog = true; },
    cancelDelete() { this.showDeleteDialog = false; this.mediaToDelete = null; },
    async handleDelete() {
      if (!this.mediaToDelete) return;
      this.isDeleting = true;
      try {
        await mediaAPI.delete(this.mediaToDelete.mediaId);
        this.mediaList = this.mediaList.filter(m => m.mediaId !== this.mediaToDelete.mediaId);
        this.showDeleteDialog = false;
        this.closeHoverModalImmediately();
      } finally { this.isDeleting = false; }
    },
    clearFilters() { this.searchQuery = ''; this.filterType = this.filterStatus = this.filterRating = null; this.sortBy = 'dateAdded'; }
  },
  created() { this.getAllMedia(); }
};
</script>

<style scoped>
/* Scoped deep selectors for Vuetify dialog cleanup */
:deep(.v-overlay__content) {
  margin: 0 !important;
  pointer-events: auto !important;
}

.modal-capture-area {
  padding: 30px; /* Invisible buffer zone */
  margin: -30px; /* Offset to keep card centered */
  display: block;
}

.all-media { max-width: 1600px; margin: 0 auto; }
.media-card { cursor: pointer; transition: transform 0.3s ease; background: transparent !important; }
.media-card:hover { transform: translateY(-8px); }
.poster-container { position: relative; aspect-ratio: 2/3; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.4); }
.top-scrim { position: absolute; top: 0; left: 0; right: 0; height: 60px; background: linear-gradient(to bottom, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0) 100%); z-index: 1; }
.overlay-content { position: absolute; top: 0; left: 0; right: 0; z-index: 2; }
.gold-text { color: #FFC107 !important; }
.rating-label { border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 2px 8px rgba(0,0,0,0.8); }

.hover-preview-large { 
  border-radius: 20px !important; 
  background-color: #121212 !important; 
  overflow: hidden; 
}

/* Cinematic Zoom Animation */
.zoom-animation {
  animation: scaleBackground 12s linear infinite;
  transform-origin: center;
}
@keyframes scaleBackground {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}
.gap-2 { gap: 8px; }
</style>
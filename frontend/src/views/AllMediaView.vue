<template>
  <div class="all-media">
    <!-- Header with actions -->
    <v-row class="mb-6 align-center">
      <v-col>
        <h1 class="text-h3">My Collection</h1>
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

    <!-- Filters Bar -->
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
            <v-select
              v-model="filterType"
              :items="typeOptions"
              label="Type"
              variant="outlined"
              density="comfortable"
              clearable
              hide-details
            />
          </v-col>
          <v-col cols="12" md="2">
            <v-select
              v-model="filterStatus"
              :items="statusOptions"
              label="Status"
              variant="outlined"
              density="comfortable"
              clearable
              hide-details
            />
          </v-col>
          <v-col cols="12" md="2">
            <v-select
              v-model="filterRating"
              :items="ratingOptions"
              label="Rating"
              variant="outlined"
              density="comfortable"
              clearable
              hide-details
            />
          </v-col>
          <v-col cols="12" md="2">
            <v-select
              v-model="sortBy"
              :items="sortOptions"
              label="Sort by"
              variant="outlined"
              density="comfortable"
              hide-details
            />
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
    
    <!-- Loading state -->
    <v-row v-if="loading" justify="center" class="my-12">
      <v-progress-circular indeterminate size="64" color="primary" />
    </v-row>
    
    <!-- Error state -->
    <v-alert v-else-if="error" type="error" variant="tonal" class="mb-4">
      {{ error }}
      <template v-slot:append>
        <v-btn @click="getAllMedia" variant="text">Retry</v-btn>
      </template>
    </v-alert>
    
    <!-- Empty state -->
    <v-empty-state
      v-else-if="mediaList.length === 0"
      icon="mdi-movie-open-outline"
      title="No media yet"
      text="Start building your collection"
    >
      <template v-slot:actions>
        <v-btn color="primary" size="large" to="/movies/new">
          Add Your First Movie or Show
        </v-btn>
      </template>
    </v-empty-state>

    <!-- No results from search/filter -->
    <v-empty-state
      v-else-if="filteredMedia.length === 0"
      icon="mdi-movie-search-outline"
      title="No results found"
      text="Try adjusting your search or filters"
    >
      <template v-slot:actions>
        <v-btn @click="clearFilters" variant="text">Clear Filters</v-btn>
      </template>
    </v-empty-state>
    
    <!-- Media Grid/List View -->
    <div v-else>
      <!-- View Toggle -->
      <v-row class="mb-4 align-center">
        <v-col>
          <v-chip variant="text">
            {{ filteredMedia.length }} {{ filteredMedia.length === 1 ? 'result' : 'results' }}
          </v-chip>
        </v-col>
        <v-col cols="auto">
          <v-btn-toggle v-model="viewMode" mandatory density="compact">
            <v-btn value="grid" icon="mdi-view-grid" />
            <v-btn value="list" icon="mdi-view-list" />
          </v-btn-toggle>
        </v-col>
      </v-row>

      <!-- Grid View -->
      <v-row v-if="viewMode === 'grid'">
        <v-col
          v-for="media in filteredMedia"
          :key="media.mediaId"
          cols="12"
          sm="6"
          md="4"
          lg="3"
        >
          <v-card
            class="media-card"
            hover
            @click="goToMedia(media.mediaId)"
            @mouseenter="startHover(media)"
            @mouseleave="cancelHover"
          >
            <div class="poster-container">
              <v-img
                v-if="media.posterUrl"
                :src="media.posterUrl"
                aspect-ratio="2/3"
                cover
                class="poster-image"
              >
                <div class="poster-scrim"></div>

                <template v-slot:placeholder>
                  <v-row class="fill-height ma-0 align-center justify-center">
                    <v-progress-circular indeterminate color="grey-lighten-5" />
                  </v-row>
                </template>
              </v-img>
              
              <div v-else class="poster-placeholder">
                <v-icon size="64" color="grey-lighten-1">mdi-movie-outline</v-icon>
                <p class="text-caption mt-2">No poster</p>
              </div>
              
              <div class="badge-wrapper left">
                <v-chip
                  :color="media.mediaType === 'movie' ? 'blue-darken-2' : 'purple-darken-2'"
                  size="x-small"
                  class="type-chip"
                  variant="flat"
                >
                  {{ media.mediaType === 'movie' ? 'MOVIE' : 'TV' }}
                </v-chip>
              </div>
              
              <div v-if="!media.rating" class="badge-wrapper right">
                <v-chip
                  color="surface"
                  size="x-small"
                  class="watchlist-chip"
                  variant="flat"
                >
                  <v-icon start size="10">mdi-bookmark</v-icon>
                  WATCHLIST
                </v-chip>
              </div>
            </div>

            <v-card-text class="pa-3">
              <div class="d-flex justify-space-between align-start">
                <div class="text-subtitle-1 font-weight-bold text-truncate pr-2" style="flex: 1;">
                  {{ media.title }}
                </div>
                
                <div v-if="media.rating" class="d-flex align-center pt-1" style="white-space: nowrap;">
                  <v-icon color="amber-darken-1" size="small" class="mr-1">mdi-star</v-icon>
                  <span class="text-body-2 font-weight-black">{{ media.rating }}</span>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- List View -->
      <v-list v-else lines="two">
        <v-list-item
          v-for="media in filteredMedia"
          :key="media.mediaId"
          @click="goToMedia(media.mediaId)"
          @mouseenter="startHover(media)"
          @mouseleave="cancelHover"
          link
        >
          <template v-slot:prepend>
            <v-avatar size="80" rounded class="mr-4">
              <v-img v-if="media.posterUrl" :src="media.posterUrl" cover />
              <v-icon v-else size="40">mdi-movie-outline</v-icon>
            </v-avatar>
          </template>

          <v-list-item-title class="text-h6">
            {{ media.title }}
            <v-chip 
              :color="media.mediaType === 'movie' ? 'primary' : 'secondary'" 
              size="x-small" 
              class="ml-2"
            >
              {{ media.mediaType === 'movie' ? 'MOVIE' : 'TV' }}
            </v-chip>
          </v-list-item-title>

          <v-list-item-subtitle v-if="media.cast && media.cast.length > 0">
            {{ media.cast.slice(0, 3).map(c => c.name).join(', ') }}
          </v-list-item-subtitle>
          <v-list-item-subtitle v-else-if="media.director">
            {{ media.director }}
          </v-list-item-subtitle>

          <template v-slot:append>
            <div class="d-flex flex-column align-end">
              <v-chip v-if="media.rating" color="amber" size="small">
                <v-icon start size="small">mdi-star</v-icon>
                {{ media.rating }}/5
              </v-chip>
              <v-chip v-else color="info" size="small">
                <v-icon start size="small">mdi-bookmark</v-icon>
                Watchlist
              </v-chip>
            </div>
          </template>
        </v-list-item>
      </v-list>
    </div>

    <!-- Hover Preview Modal -->
    <v-dialog
      v-model="showHoverModal"
      max-width="600"
      :scrim="false"
      persistent
      @click:outside="closeHoverModal"
    >
      <v-card v-if="hoveredMedia" class="hover-preview">
        <v-img
          v-if="hoveredMedia.backdropUrl"
          :src="hoveredMedia.backdropUrl"
          height="200"
          cover
          gradient="to bottom, rgba(0,0,0,.3), rgba(0,0,0,.7)"
        >
          <v-card-title class="text-h5 text-white">
            {{ hoveredMedia.title }}
            <span v-if="hoveredMedia.releaseYear" class="text-h6 ml-2">
              ({{ hoveredMedia.releaseYear }})
            </span>
            <v-chip 
              :color="hoveredMedia.mediaType === 'movie' ? 'primary' : 'secondary'" 
              size="small" 
              class="ml-2"
            >
              {{ hoveredMedia.mediaType === 'movie' ? 'MOVIE' : 'TV' }}
            </v-chip>
          </v-card-title>
        </v-img>
        <v-card-title v-else>
          {{ hoveredMedia.title }}
          <span v-if="hoveredMedia.releaseYear" class="text-subtitle-1 ml-2">
            ({{ hoveredMedia.releaseYear }})
          </span>
          <v-chip 
            :color="hoveredMedia.mediaType === 'movie' ? 'primary' : 'secondary'" 
            size="small" 
            class="ml-2"
          >
            {{ hoveredMedia.mediaType === 'movie' ? 'MOVIE' : 'TV' }}
          </v-chip>
        </v-card-title>

        <v-card-text>
          <div class="mb-3">
            <v-chip v-if="hoveredMedia.rating" size="small" class="mr-2" color="amber">
              <v-icon start size="small">mdi-star</v-icon>
              {{ hoveredMedia.rating }}/5 (You)
            </v-chip>
            <v-chip v-else size="small" class="mr-2" color="info">
              <v-icon start size="small">mdi-bookmark</v-icon>
              Watchlist
            </v-chip>
            <v-chip v-if="hoveredMedia.tmdbRating" size="small" class="mr-2">
              {{ hoveredMedia.tmdbRating.toFixed(1) }} TMDB
            </v-chip>
            <v-chip v-if="hoveredMedia.imdbRating" size="small" class="mr-2">
              {{ hoveredMedia.imdbRating.toFixed(1) }} IMDb
            </v-chip>
          </div>

          <!-- Cast -->
          <p v-if="hoveredMedia.cast && hoveredMedia.cast.length > 0" class="text-subtitle-2 mb-2">
            <strong>Cast:</strong> {{ hoveredMedia.cast.slice(0, 3).map(c => c.name).join(', ') }}
          </p>
          <p v-else-if="hoveredMedia.director" class="text-subtitle-2 mb-2">
            <strong>{{ hoveredMedia.mediaType === 'tv' ? 'Created by' : 'Director' }}:</strong> {{ hoveredMedia.director }}
          </p>

          <!-- TV-specific info -->
          <p v-if="hoveredMedia.mediaType === 'tv' && hoveredMedia.numberOfSeasons" class="text-subtitle-2 mb-2">
            <strong>Seasons:</strong> {{ hoveredMedia.numberOfSeasons }}
            <span v-if="hoveredMedia.seasonsWatched"> (Watched {{ hoveredMedia.seasonsWatched }})</span>
          </p>

          <div v-if="hoveredMedia.genres && hoveredMedia.genres.length > 0" class="mb-3">
            <v-chip
              v-for="genre in hoveredMedia.genres"
              :key="genre"
              size="small"
              variant="outlined"
              class="mr-1"
            >
              {{ genre }}
            </v-chip>
          </div>

          <p v-if="hoveredMedia.plot" class="text-body-2">
            {{ truncateText(hoveredMedia.plot, 200) }}
          </p>
        </v-card-text>

        <v-card-actions>
          <v-btn
            variant="text"
            color="primary"
            @click.stop="goToEdit(hoveredMedia.mediaId)"
          >
            <v-icon start>mdi-pencil</v-icon>
            Edit
          </v-btn>
          <v-btn
            variant="text"
            color="error"
            @click.stop="confirmDelete(hoveredMedia)"
          >
            <v-icon start>mdi-delete</v-icon>
            Delete
          </v-btn>
          <v-spacer />
          <v-btn
            color="primary"
            @click.stop="goToMedia(hoveredMedia.mediaId)"
          >
            Full Details
            <v-icon end>mdi-arrow-right</v-icon>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation -->
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
  
  components: {
    DeleteConfirmDialog
  },
  
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
      
      // Hover modal
      showHoverModal: false,
      hoveredMedia: null,
      hoverTimeout: null,
      
      // Delete
      showDeleteDialog: false,
      mediaToDelete: null,
      isDeleting: false,
      
      typeOptions: [
        { title: 'Movies', value: 'movie' },
        { title: 'TV Shows', value: 'tv' },
      ],
      
      statusOptions: [
        { title: 'Watched', value: 'watched' },
        { title: 'Watchlist', value: 'want_to_watch' },
        { title: 'Watching', value: 'watching' },
      ],
      
      ratingOptions: [
        { title: '5 Stars', value: 5 },
        { title: '4 Stars', value: 4 },
        { title: '3 Stars', value: 3 },
        { title: '2 Stars', value: 2 },
        { title: '1 Star', value: 1 },
      ],
      
      sortOptions: [
        { title: 'Recently Added', value: 'dateAdded' },
        { title: 'Title (A-Z)', value: 'titleAsc' },
        { title: 'Title (Z-A)', value: 'titleDesc' },
        { title: 'Rating (High to Low)', value: 'ratingDesc' },
        { title: 'Rating (Low to High)', value: 'ratingAsc' },
      ],
    };
  },
  
  computed: {
    filteredMedia() {
      let result = [...this.mediaList];
      
      // Search filter
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(m =>
          m.title.toLowerCase().includes(query) ||
          (m.director && m.director.toLowerCase().includes(query)) ||
          (m.plot && m.plot.toLowerCase().includes(query)) ||
          (m.cast && m.cast.some(c => c.name.toLowerCase().includes(query)))
        );
      }
      
      // Type filter
      if (this.filterType) {
        result = result.filter(m => m.mediaType === this.filterType);
      }
      
      // Status filter
      if (this.filterStatus) {
        result = result.filter(m => m.status === this.filterStatus);
      }
      
      // Rating filter
      if (this.filterRating !== null) {
        result = result.filter(m => m.rating === this.filterRating);
      }
      
      // Sorting
      switch (this.sortBy) {
        case 'titleAsc':
          result.sort((a, b) => a.title.localeCompare(b.title));
          break;
        case 'titleDesc':
          result.sort((a, b) => b.title.localeCompare(a.title));
          break;
        case 'ratingDesc':
          result.sort((a, b) => (b.rating || 0) - (a.rating || 0));
          break;
        case 'ratingAsc':
          result.sort((a, b) => (a.rating || 0) - (b.rating || 0));
          break;
        case 'dateAdded':
        default:
          result.sort((a, b) => {
            const dateA = a.createdAt ? new Date(a.createdAt) : new Date(0);
            const dateB = b.createdAt ? new Date(b.createdAt) : new Date(0);
            return dateB - dateA;
          });
      }
      
      return result;
    },
    
    isMobile() {
      return this.$vuetify.display.mobile;
    }
  },
  
  created() {
    this.getAllMedia();
    const savedView = localStorage.getItem('mediaViewMode');
    if (savedView) {
      this.viewMode = savedView;
    }
  },
  
  watch: {
    viewMode(newMode) {
      localStorage.setItem('mediaViewMode', newMode);
    }
  },
  
  methods: {
    async getAllMedia() {
      this.loading = true;
      this.error = null;
      
      try {
        this.mediaList = await mediaAPI.getAll();
      } catch (err) {
        console.error('Error loading media:', err);
        this.error = 'Failed to load media. Please try again.';
      } finally {
        this.loading = false;
      }
    },
    
    startHover(media) {
      if (this.isMobile) return;
      
      this.cancelHover();
      this.hoverTimeout = setTimeout(() => {
        this.hoveredMedia = media;
        this.showHoverModal = true;
      }, 300);
    },
    
    cancelHover() {
      if (this.hoverTimeout) {
        clearTimeout(this.hoverTimeout);
        this.hoverTimeout = null;
      }
    },
    
    closeHoverModal() {
      this.showHoverModal = false;
      this.hoveredMedia = null;
    },
    
    goToMedia(mediaId) {
      this.closeHoverModal();
      this.$router.push(`/movies/${mediaId}`);
    },
    
    goToEdit(mediaId) {
      this.closeHoverModal();
      this.$router.push(`/movies/${mediaId}/edit`);
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
        this.showHoverModal = false;
        this.mediaToDelete = null;
      } catch (err) {
        console.error('Delete error:', err);
        this.error = 'Failed to delete. Please try again.';
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
    
    truncateText(text, maxLength) {
      if (!text) return '';
      return text.length > maxLength
        ? text.substring(0, maxLength) + '...'
        : text;
    }
  }
};
</script>

<style scoped>
.all-media {
  max-width: 1400px;
  margin: 0 auto;
}

.media-card {
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  overflow: hidden;
  border-radius: 12px;
}

.media-card:hover {
  transform: translateY(-6px);
}

.poster-container {
  position: relative;
  aspect-ratio: 2/3;
  background: #1a1a1a;
  overflow: hidden;
}

/* Subtle dark gradient at the top to ensure badges are visible on light posters */
.poster-scrim {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 40%;
  background: linear-gradient(to bottom, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0) 100%);
  z-index: 1;
}

.badge-wrapper {
  position: absolute;
  top: 8px;
  z-index: 2;
}

.badge-wrapper.left { left: 8px; }
.badge-wrapper.right { right: 8px; }

/* Glassmorphism/Flat style for chips to make them feel modern */
.type-chip, .watchlist-chip {
  font-weight: 800 !important;
  letter-spacing: 0.5px;
  opacity: 0.9;
}

.watchlist-chip {
  background: rgba(var(--v-theme-surface), 0.8) !important;
  backdrop-filter: blur(4px);
}

.poster-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.poster-image {
  width: 100%;
  height: 100%;
}
</style>
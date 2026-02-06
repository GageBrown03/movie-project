<template>
  <div class="all-movies">
    <!-- Header with actions -->
    <v-row align="center" class="mb-6">
      <v-col>
        <h1 class="text-h3">My Movies</h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          {{ movies.length }} {{ movies.length === 1 ? 'movie' : 'movies' }} in your collection
        </p>
      </v-col>
      <v-col cols="auto">
        <v-btn color="primary" size="large" to="/movies/new" prepend-icon="mdi-plus">
          Add Movie
        </v-btn>
      </v-col>
    </v-row>

    <!-- Search and Filter Bar -->
    <v-card class="mb-6" elevation="2">
      <v-card-text>
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="searchQuery"
              prepend-inner-icon="mdi-magnify"
              label="Search movies..."
              variant="outlined"
              density="comfortable"
              clearable
              hide-details
            />
          </v-col>
          <v-col cols="12" md="3">
            <v-select
              v-model="filterRating"
              :items="ratingOptions"
              label="Filter by Rating"
              variant="outlined"
              density="comfortable"
              clearable
              hide-details
            />
          </v-col>
          <v-col cols="12" md="3">
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
        <v-btn @click="getAllMovies" variant="text">Retry</v-btn>
      </template>
    </v-alert>
    
    <!-- Empty state -->
    <v-empty-state
      v-else-if="movies.length === 0"
      icon="mdi-movie-open-outline"
      title="No movies yet"
      text="Start building your personal movie collection"
    >
      <template v-slot:actions>
        <v-btn color="primary" size="large" to="/movies/new">
          Add Your First Movie
        </v-btn>
      </template>
    </v-empty-state>

    <!-- No results from search/filter -->
    <v-empty-state
      v-else-if="filteredMovies.length === 0"
      icon="mdi-movie-search-outline"
      title="No movies found"
      text="Try adjusting your search or filters"
    >
      <template v-slot:actions>
        <v-btn @click="clearFilters" variant="text">Clear Filters</v-btn>
      </template>
    </v-empty-state>
    
    <!-- Movie Grid/List View -->
    <div v-else>
      <!-- View Toggle -->
      <v-row class="mb-4 align-center">
        <v-col>
          <v-chip variant="text">
            {{ filteredMovies.length }} {{ filteredMovies.length === 1 ? 'result' : 'results' }}
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
          v-for="movie in filteredMovies"
          :key="movie.movieId"
          cols="12"
          sm="6"
          md="4"
          lg="3"
        >
          <v-card
            class="movie-card"
            hover
            @click="goToMovie(movie.movieId)"
            @mouseenter="startHover(movie)"
            @mouseleave="cancelHover"
          >
            <!-- Movie Poster -->
            <div class="poster-container">
              <v-img
                v-if="movie.posterUrl"
                :src="movie.posterUrl"
                aspect-ratio="2/3"
                cover
                class="poster-image"
              >
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
              
              <!-- Personal Rating Badge -->
              <v-chip
                class="rating-badge"
                color="primary"
                size="small"
                label
              >
                <v-icon start size="small">mdi-star</v-icon>
                {{ movie.rating }}/5
              </v-chip>
            </div>

            <v-card-title class="text-subtitle-1">
              {{ movie.title }}
            </v-card-title>

            <v-card-subtitle v-if="movie.director">
              {{ movie.director }}
            </v-card-subtitle>
          </v-card>
        </v-col>
      </v-row>

      <!-- List View -->
      <v-list v-else lines="two">
        <v-list-item
          v-for="movie in filteredMovies"
          :key="movie.movieId"
          @click="goToMovie(movie.movieId)"
          @mouseenter="startHover(movie)"
          @mouseleave="cancelHover"
          link
        >
          <template v-slot:prepend>
            <v-avatar size="80" rounded class="mr-4">
              <v-img v-if="movie.posterUrl" :src="movie.posterUrl" cover />
              <v-icon v-else size="40">mdi-movie-outline</v-icon>
            </v-avatar>
          </template>

          <v-list-item-title class="text-h6">
            {{ movie.title }}
          </v-list-item-title>

          <v-list-item-subtitle v-if="movie.director">
            Directed by {{ movie.director }}
          </v-list-item-subtitle>

          <template v-slot:append>
            <div class="d-flex flex-column align-end">
              <v-chip color="primary" size="small">
                <v-icon start size="small">mdi-star</v-icon>
                {{ movie.rating }}/5
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
      <v-card v-if="hoveredMovie" class="hover-preview">
        <v-img
          v-if="hoveredMovie.backdropUrl"
          :src="hoveredMovie.backdropUrl"
          height="200"
          cover
          gradient="to bottom, rgba(0,0,0,.3), rgba(0,0,0,.7)"
        >
          <v-card-title class="text-h5 text-white">
            {{ hoveredMovie.title }}
            <span v-if="hoveredMovie.releaseYear" class="text-h6 ml-2">
              ({{ hoveredMovie.releaseYear }})
            </span>
          </v-card-title>
        </v-img>
        <v-card-title v-else>
          {{ hoveredMovie.title }}
          <span v-if="hoveredMovie.releaseYear" class="text-subtitle-1 ml-2">
            ({{ hoveredMovie.releaseYear }})
          </span>
        </v-card-title>

        <v-card-text>
          <div class="mb-3">
            <v-chip size="small" class="mr-2" color="primary">
              <v-icon start size="small">mdi-star</v-icon>
              {{ hoveredMovie.rating }}/5 (You)
            </v-chip>
            <v-chip v-if="hoveredMovie.tmdbRating" size="small" class="mr-2">
              {{ hoveredMovie.tmdbRating.toFixed(1) }} TMDB
            </v-chip>
            <v-chip v-if="hoveredMovie.imdbRating" size="small" class="mr-2">
              {{ hoveredMovie.imdbRating.toFixed(1) }} IMDb
            </v-chip>
          </div>

          <p v-if="hoveredMovie.director" class="text-subtitle-2 mb-2">
            <strong>Director:</strong> {{ hoveredMovie.director }}
          </p>

          <div v-if="hoveredMovie.genres && hoveredMovie.genres.length > 0" class="mb-3">
            <v-chip
              v-for="genre in hoveredMovie.genres"
              :key="genre"
              size="small"
              variant="outlined"
              class="mr-1"
            >
              {{ genre }}
            </v-chip>
          </div>

          <p v-if="hoveredMovie.plot" class="text-body-2">
            {{ truncateText(hoveredMovie.plot, 200) }}
          </p>
        </v-card-text>

        <v-card-actions>
          <v-btn
            variant="text"
            color="primary"
            @click.stop="goToEdit(hoveredMovie.movieId)"
          >
            <v-icon start>mdi-pencil</v-icon>
            Edit
          </v-btn>
          <v-btn
            variant="text"
            color="error"
            @click.stop="confirmDelete(hoveredMovie)"
          >
            <v-icon start>mdi-delete</v-icon>
            Delete
          </v-btn>
          <v-spacer />
          <v-btn
            color="primary"
            @click.stop="goToMovie(hoveredMovie.movieId)"
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
      :movie-title="movieToDelete?.title || ''"
      :deleting="isDeleting"
      @cancel="cancelDelete"
      @confirm="handleDelete"
    />
  </div>
</template>

<script>
import { movieAPI } from '@/services/api-production';
import DeleteConfirmDialog from '@/components/DeleteConfirmDialog.vue';

export default {
  name: 'AllMoviesView',
  
  components: {
    DeleteConfirmDialog
  },
  
  data() {
    return {
      movies: [],
      loading: false,
      error: null,
      searchQuery: '',
      filterRating: null,
      sortBy: 'dateAdded',
      viewMode: 'grid',
      
      // Hover modal
      showHoverModal: false,
      hoveredMovie: null,
      hoverTimeout: null,
      
      // Delete
      showDeleteDialog: false,
      movieToDelete: null,
      isDeleting: false,
      
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
        { title: 'Director (A-Z)', value: 'directorAsc' },
      ],
    };
  },
  
  computed: {
    filteredMovies() {
      let result = [...this.movies];
      
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(movie =>
          movie.title.toLowerCase().includes(query) ||
          (movie.director && movie.director.toLowerCase().includes(query)) ||
          (movie.plot && movie.plot.toLowerCase().includes(query))
        );
      }
      
      if (this.filterRating !== null) {
        result = result.filter(movie => movie.rating === this.filterRating);
      }
      
      switch (this.sortBy) {
        case 'titleAsc':
          result.sort((a, b) => a.title.localeCompare(b.title));
          break;
        case 'titleDesc':
          result.sort((a, b) => b.title.localeCompare(a.title));
          break;
        case 'ratingDesc':
          result.sort((a, b) => b.rating - a.rating);
          break;
        case 'ratingAsc':
          result.sort((a, b) => a.rating - b.rating);
          break;
        case 'directorAsc':
          result.sort((a, b) => (a.director || '').localeCompare(b.director || ''));
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
    this.getAllMovies();
    const savedView = localStorage.getItem('movieViewMode');
    if (savedView) {
      this.viewMode = savedView;
    }
  },
  
  watch: {
    viewMode(newMode) {
      localStorage.setItem('movieViewMode', newMode);
    }
  },
  
  methods: {
    async getAllMovies() {
      this.loading = true;
      this.error = null;
      
      try {
        this.movies = await movieAPI.getAll();
      } catch (err) {
        console.error('Error loading movies:', err);
        this.error = 'Failed to load movies. Please try again.';
      } finally {
        this.loading = false;
      }
    },
    
    startHover(movie) {
      if (this.isMobile) return; // Skip hover on mobile
      
      this.cancelHover(); // Clear any existing timeout
      this.hoverTimeout = setTimeout(() => {
        this.hoveredMovie = movie;
        this.showHoverModal = true;
      }, 300); // 0.3s delay
    },
    
    cancelHover() {
      if (this.hoverTimeout) {
        clearTimeout(this.hoverTimeout);
        this.hoverTimeout = null;
      }
    },
    
    closeHoverModal() {
      this.showHoverModal = false;
      this.hoveredMovie = null;
    },
    
    goToMovie(movieId) {
      this.closeHoverModal();
      this.$router.push(`/movies/${movieId}`);
    },
    
    goToEdit(movieId) {
      this.closeHoverModal();
      this.$router.push(`/movies/${movieId}/edit`);
    },
    
    confirmDelete(movie) {
      this.movieToDelete = movie;
      this.showDeleteDialog = true;
    },
    
    cancelDelete() {
      this.showDeleteDialog = false;
      this.movieToDelete = null;
    },
    
    async handleDelete() {
      if (!this.movieToDelete) return;
      
      this.isDeleting = true;
      
      try {
        await movieAPI.delete(this.movieToDelete.movieId);
        
        // Remove from local array
        this.movies = this.movies.filter(m => m.movieId !== this.movieToDelete.movieId);
        
        // Close dialogs
        this.showDeleteDialog = false;
        this.showHoverModal = false;
        this.movieToDelete = null;
        
      } catch (err) {
        console.error('Delete error:', err);
        this.error = 'Failed to delete movie. Please try again.';
      } finally {
        this.isDeleting = false;
      }
    },
    
    clearFilters() {
      this.searchQuery = '';
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
.all-movies {
  max-width: 1400px;
  margin: 0 auto;
}

.movie-card {
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.movie-card:hover {
  transform: translateY(-4px);
}

.poster-container {
  position: relative;
  aspect-ratio: 2/3;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.poster-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.05);
}

.rating-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  font-weight: bold;
}

.poster-image {
  width: 100%;
  height: 100%;
}

.hover-preview {
  user-select: none;
}
</style>
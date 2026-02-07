<template>
  <div class="all-movies">
    <v-row class="mb-6 align-center">
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

    <v-card class="mb-6" elevation="2">
      <v-card-text>
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="searchQuery"
              prepend-inner-icon="mdi-magnify"
              label="Search your movies..."
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
    
    <v-row v-if="loading" justify="center" class="my-12">
      <v-progress-circular indeterminate size="64" color="primary" />
    </v-row>
    
    <v-alert v-else-if="error" type="error" variant="tonal" class="mb-4">
      {{ error }}
      <template v-slot:append>
        <v-btn @click="getAllMovies" variant="text">Retry</v-btn>
      </template>
    </v-alert>
    
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
    
    <div v-else>
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

      <v-row v-if="viewMode === 'grid'">
        <v-col
          v-for="movie in filteredMovies"
          :key="movie.movieId"
          cols="12" sm="6" md="4" lg="3"
        >
          <v-menu
            open-on-hover
            :open-delay="400"
            location="center"
            transition="scale-transition"
            :disabled="isMobile"
            max-width="450"
          >
            <template v-slot:activator="{ props }">
              <v-card
                v-bind="props"
                class="movie-card"
                hover
                @click="goToMovie(movie.movieId)"
              >
                <div class="poster-container">
                  <v-img
                    v-if="movie.posterUrl"
                    :src="movie.posterUrl"
                    aspect-ratio="2/3"
                    cover
                  />
                  <div v-else class="poster-placeholder">
                    <v-icon size="64" color="grey-lighten-1">mdi-movie-outline</v-icon>
                  </div>
                  
                  <v-chip class="rating-badge" color="primary" size="small" label>
                    <v-icon start size="small">mdi-star</v-icon>
                    {{ movie.rating }}/5
                  </v-chip>
                </div>
                <v-card-title class="text-subtitle-1">{{ movie.title }}</v-card-title>
                <v-card-subtitle v-if="movie.director">{{ movie.director }}</v-card-subtitle>
              </v-card>
            </template>

            <v-card class="elevation-12 rounded-lg overflow-hidden">
              <v-img
                v-if="movie.backdropUrl"
                :src="movie.backdropUrl"
                height="180"
                cover
                gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.8)"
              >
                <v-card-title class="text-white align-end fill-height d-flex">
                  <div>
                    <div class="text-h6">{{ movie.title }}</div>
                    <div class="text-caption" v-if="movie.releaseYear">({{ movie.releaseYear }})</div>
                  </div>
                </v-card-title>
              </v-img>
              
              <v-card-text class="pt-4">
                <div class="d-flex mb-3 gap-2">
                  <v-chip size="x-small" color="primary">Your Rating: {{ movie.rating }}/5</v-chip>
                  <v-chip v-if="movie.tmdbRating" size="x-small">{{ movie.tmdbRating.toFixed(1) }} TMDB</v-chip>
                </div>
                <p class="text-body-2 text-medium-emphasis mb-3">
                  {{ truncateText(movie.plot, 160) }}
                </p>
                <div v-if="movie.genres" class="d-flex flex-wrap gap-1">
                  <v-chip v-for="g in movie.genres" :key="g" size="x-small" variant="tonal">{{ g }}</v-chip>
                </div>
              </v-card-text>

              <v-divider />

              <v-card-actions class="bg-surface-variant">
                <v-btn icon="mdi-pencil" size="small" variant="text" @click.stop="goToEdit(movie.movieId)" />
                <v-btn icon="mdi-delete" size="small" color="error" variant="text" @click.stop="confirmDelete(movie)" />
                <v-spacer />
                <v-btn variant="elevated" color="primary" size="small" @click.stop="goToMovie(movie.movieId)">
                  Details
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-menu>
        </v-col>
      </v-row>

      <v-list v-else lines="two">
        <v-list-item
          v-for="movie in filteredMovies"
          :key="movie.movieId"
          @click="goToMovie(movie.movieId)"
          link
        >
          <template v-slot:prepend>
            <v-avatar size="80" rounded class="mr-4">
              <v-img v-if="movie.posterUrl" :src="movie.posterUrl" cover />
              <v-icon v-else size="40">mdi-movie-outline</v-icon>
            </v-avatar>
          </template>
          <v-list-item-title class="text-h6">{{ movie.title }}</v-list-item-title>
          <v-list-item-subtitle v-if="movie.director">Directed by {{ movie.director }}</v-list-item-subtitle>
          <template v-slot:append>
            <v-chip color="primary" size="small">
              <v-icon start size="small">mdi-star</v-icon>
              {{ movie.rating }}/5
            </v-chip>
          </template>
        </v-list-item>
      </v-list>
    </div>

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
  components: { DeleteConfirmDialog },
  
  data: () => ({
    movies: [],
    loading: false,
    error: null,
    searchQuery: '',
    filterRating: null,
    sortBy: 'dateAdded',
    viewMode: 'grid',
    
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
    ],
  }),

  computed: {
    filteredMovies() {
      let result = [...this.movies];
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(m => m.title.toLowerCase().includes(query));
      }
      if (this.filterRating !== null) {
        result = result.filter(m => m.rating === this.filterRating);
      }
      // Sort logic remains same...
      return result;
    },
    isMobile() {
      return this.$vuetify.display.mobile;
    }
  },

  created() {
    this.getAllMovies();
    this.viewMode = localStorage.getItem('movieViewMode') || 'grid';
  },

  methods: {
    async getAllMovies() {
      this.loading = true;
      try {
        this.movies = await movieAPI.getAll();
      } catch (err) {
        this.error = 'Failed to load movies.';
      } finally {
        this.loading = false;
      }
    },
    goToMovie(id) { this.$router.push(`/movies/${id}`); },
    goToEdit(id) { this.$router.push(`/movies/${id}/edit`); },
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
        this.movies = this.movies.filter(m => m.movieId !== this.movieToDelete.movieId);
        this.showDeleteDialog = false;
      } catch (err) {
        this.error = 'Failed to delete movie.';
      } finally {
        this.isDeleting = false;
      }
    },
    clearFilters() {
      this.searchQuery = '';
      this.filterRating = null;
    },
    truncateText(text, maxLength) {
      if (!text) return '';
      return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
    }
  }
};
</script>

<style scoped>
.all-movies { max-width: 1400px; margin: 0 auto; }
.movie-card { cursor: pointer; transition: transform 0.2s ease; }
.movie-card:hover { transform: translateY(-4px); }
.poster-container { position: relative; aspect-ratio: 2/3; background: #eee; }
.rating-badge { position: absolute; top: 8px; right: 8px; font-weight: bold; }
.gap-1 { gap: 4px; }
.gap-2 { gap: 8px; }
</style>
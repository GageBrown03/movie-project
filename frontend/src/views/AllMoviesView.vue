<template>
  <div class="all-movies">
    <!-- Header with actions -->
    <v-row align-content="center" class="mb-6 align-center">
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
      <v-row class="mb-4" align-content="center">
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
            @click="$router.push(`/movies/${movie.movieId}`)"
          >
            <!-- Movie Poster Placeholder -->
            <div class="poster-container">
              <v-img
                v-if="movie.imageUrl"
                :src="movie.imageUrl"
                aspect-ratio="2/3"
                cover
                class="poster-image"
              >
                <template v-slot:placeholder>
                  <v-row class="fill-height ma-0" align-content="center" justify="center">
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

            <v-card-subtitle>
              {{ movie.director }}
            </v-card-subtitle>

            <!-- Placeholder for future features -->
            <v-card-text v-if="movie.description" class="text-body-2">
              {{ truncateText(movie.description, 80) }}
            </v-card-text>

            <v-card-actions>
              <v-spacer />
              <v-btn
                size="small"
                variant="text"
                @click.stop="$router.push(`/movies/${movie.movieId}/edit`)"
              >
                Edit
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>

      <!-- List View -->
      <v-list v-else lines="two">
        <v-list-item
          v-for="movie in filteredMovies"
          :key="movie.movieId"
          @click="$router.push(`/movies/${movie.movieId}`)"
          link
        >
          <template v-slot:prepend>
            <v-avatar size="80" rounded class="mr-4">
              <v-img v-if="movie.imageUrl" :src="movie.imageUrl" cover />
              <v-icon v-else size="40">mdi-movie-outline</v-icon>
            </v-avatar>
          </template>

          <v-list-item-title class="text-h6">
            {{ movie.title }}
          </v-list-item-title>

          <v-list-item-subtitle>
            Directed by {{ movie.director }}
          </v-list-item-subtitle>

          <template v-slot:append>
            <div class="d-flex flex-column align-end">
              <v-chip color="primary" size="small">
                <v-icon start size="small">mdi-star</v-icon>
                {{ movie.rating }}/5
              </v-chip>
              <v-btn
                size="small"
                variant="text"
                icon="mdi-pencil"
                @click.stop="$router.push(`/movies/${movie.movieId}/edit`)"
                class="mt-2"
              />
            </div>
          </template>
        </v-list-item>
      </v-list>
    </div>
  </div>
</template>

<script>
import { movieAPI } from '@/services/api-production';

export default {
  name: 'AllMoviesView',
  
  data() {
    return {
      movies: [],
      loading: false,
      error: null,
      searchQuery: '',
      filterRating: null,
      sortBy: 'dateAdded',
      viewMode: 'grid', // 'grid' or 'list'
      
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
      
      // Apply search filter
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(movie =>
          movie.title.toLowerCase().includes(query) ||
          movie.director.toLowerCase().includes(query) ||
          (movie.description && movie.description.toLowerCase().includes(query))
        );
      }
      
      // Apply rating filter
      if (this.filterRating !== null) {
        result = result.filter(movie => movie.rating === this.filterRating);
      }
      
      // Apply sorting
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
          result.sort((a, b) => a.director.localeCompare(b.director));
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
    }
  },
  
  created() {
    this.getAllMovies();
    // Load saved view preference
    const savedView = localStorage.getItem('movieViewMode');
    if (savedView) {
      this.viewMode = savedView;
    }
  },
  
  watch: {
    viewMode(newMode) {
      // Save view preference
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
</style>
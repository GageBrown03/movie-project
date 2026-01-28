<template>
  <div class="single-movie">
    <!-- NEW: Show loading state -->
    <v-progress-circular v-if="loading" indeterminate class="mt-4" />
    
    <!-- NEW: Show error state -->
    <v-alert v-else-if="error" type="error" class="mt-4">
      {{ error }}
      <v-btn @click="$router.push('/movies')" class="mt-2">Back to Movies</v-btn>
    </v-alert>
    
    <!-- UPDATED: Only show if movie exists and not loading -->
    <template v-else-if="movie">
      <h1>{{ movie.title }}</h1>

      <v-btn flat @click="handleEditClick">Edit</v-btn>
      <v-btn 
        flat 
        color="error" 
        :loading="isDeleting" 
        @click="handleDeleteClick"
      >
        Delete
      </v-btn>

      <h2 class="mt-2">Directed by {{ movie.director }}</h2>  <!-- FIXED: Changed from "Written by" -->
      <p class="mt-3">Rated {{ movie.rating }} out of 5</p>
    </template>
  </div>
</template>

<script>
// NEW: Import the API service
import { movieAPI } from '@/services/api';

export default {
  name: 'SingleMovieView',  // FIXED: Changed from 'SingleMoviesView'

  data() {
    return {
      movie: null,
      loading: false,      // NEW: Track loading state
      isDeleting: false,   // NEW: Track delete operation
      error: null          // NEW: Track errors
    };
  },

  computed: {
    movieId() {
      return this.$route.params.movieId;
    }
  },

  created() {
    this.getMovie();
  },

  methods: {
    // UPDATED: Replaced the entire method
    async getMovie() {
      this.loading = true;
      this.error = null;
      
      try {
        // REPLACED: Old fetch call with API service
        // OLD CODE (DELETE THIS):
        // const res = await fetch(`http://localhost:5000/movies/${this.movieId}`);
        // const data = await res.json();
        // this.movie = data;
        
        // NEW CODE:
        this.movie = await movieAPI.getOne(this.movieId);
        
      } catch (err) {
        console.error('Error loading movie:', err);
        this.error = 'Failed to load movie. It may have been deleted.';
      } finally {
        this.loading = false;
      }
    },

    handleEditClick() {
      this.$router.push(`/movies/${this.movie.movieId}/edit`);
    },

    // UPDATED: Replaced the entire method
    async handleDeleteClick() {
      // NEW: Add confirmation dialog
      if (!confirm(`Are you sure you want to delete "${this.movie.title}"?`)) {
        return;  // User cancelled
      }
      
      this.isDeleting = true;
      
      try {
        // REPLACED: Old fetch call with API service
        // OLD CODE (DELETE THIS):
        // await fetch(`http://localhost:5000/movies/${this.movieId}`, {
        //   method: 'DELETE'
        // });
        // this.$router.push('/movies');
        
        // NEW CODE:
        await movieAPI.delete(this.movieId);
        
        // Redirect to movies list
        this.$router.push('/movies');
        
      } catch (err) {
        console.error('Error deleting movie:', err);
        this.error = 'Failed to delete movie. Please try again.';
        this.isDeleting = false;
      }
    }
  }
};
</script>
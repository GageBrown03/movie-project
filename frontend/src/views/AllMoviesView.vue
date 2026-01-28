<template>
  <div class="all-movies">
    <h1>All movies</h1>
    
    <!-- NEW: Add loading state -->
    <v-progress-circular v-if="loading" indeterminate class="mt-10" />
    
    <!-- NEW: Add error state -->
    <v-alert v-else-if="error" type="error" class="mt-4">
      {{ error }}
    </v-alert>
    
    <!-- UPDATED: Only show table if we have movies and not loading -->
    <v-table v-else-if="movies.length > 0" class="mt-10">
      <thead>
        <th class="text-left">Title</th>
        <th class="text-left">Director</th> <!-- FIXED: Changed from "Author" to "Director" -->
        <th class="text-left">Rating</th>
      </thead>
      <tbody>
        <tr v-for="movie of movies" :key="movie.movieId">
          <td><router-link :to="`/movies/${movie.movieId}`">{{ movie.title }}</router-link></td>
          <td>{{ movie.director }}</td> <!-- FIXED: Changed from movie.author to movie.director -->
          <td>{{ movie.rating }}</td>
        </tr>
      </tbody>
    </v-table>
    
    <!-- NEW: Add empty state -->
    <div v-else class="empty-state mt-10">
      <p>No movies yet! Add your first one.</p>
      <v-btn color="primary" to="/movies/new">Add Movie</v-btn>
    </div>
  </div>
</template>

<script>
// NEW: Import the API service
import { movieAPI } from '@/services/api';

export default {
  name: 'AllMoviesView',
  data() {
    return {
      movies: [],
      loading: false,    // NEW: Track loading state
      error: null        // NEW: Track error state
    };
  },
  created() {
    this.getAllMovies();
  },
  methods: {
    // UPDATED: Replaced the entire method
    async getAllMovies() {
      this.loading = true;    // NEW: Set loading to true when starting
      this.error = null;      // NEW: Clear any previous errors
      
      try {
        // REPLACED: Old fetch call with API service
        // OLD CODE (DELETE THIS):
        // const res = await fetch('http://localhost:5000/movies')
        // const data = await res.json();
        // this.movies = data;
        
        // NEW CODE:
        this.movies = await movieAPI.getAll();
        
      } catch (err) {
        // NEW: Handle errors gracefully
        console.error('Error loading movies:', err);
        this.error = 'Failed to load movies. Please try again.';
      } finally {
        // NEW: Always turn off loading when done
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.empty-state {
  text-align: center;
  padding: 40px;
}
</style>
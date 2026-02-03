<template>
  <div class="edit-movie">  <!-- FIXED: Changed from "edit-book" to "edit-movie" -->
    <h1>Edit Movie</h1>  <!-- FIXED: Changed from "Edit Book" to "Edit Movie" -->
    
    <!-- NEW: Show loading while fetching movie data -->
    <v-progress-circular v-if="loading" indeterminate class="mt-4" />
    
    <!-- NEW: Show error if fetch/update fails -->
    <v-alert v-if="error" type="error" class="mb-4">
      {{ error }}
    </v-alert>
    
    <!-- Only show form once movie data is loaded -->
    <v-form v-if="!loading" class="mt-4">
      <v-text-field
        v-model="title"
        label="Movie Title"  
        required
      />
      <v-text-field
        v-model="director"
        label="Movie Director"  
        required
      />
      <v-select
        v-model="rating"
        :items="ratingDropdownData"
        label="Rating"
        :rules="[v => !!v || 'Rating is required']"
        required
      />
      <!-- UPDATED: Better button states -->
      <v-btn 
        :disabled="!isValid || isSubmitting" 
        :loading="isSubmitting"
        @click="handleUpdateMovie" 
      >
        Update  <!-- FIXED: Changed from "Create" to "Update" -->
      </v-btn>
      <v-btn @click="handleCancelClick">Cancel</v-btn>
    </v-form>
  </div>
</template>

<script>
// NEW: Import the API service
import { movieAPI } from '@/services/api-production';

export default {
  name: 'EditMovieView',  // FIXED: Changed from 'EditBooksView'
  data() {
    return {
      title: '',
      director: '',      // FIXED: Changed from 'author' to 'director'
      rating: 1,
      loading: false,    // NEW: Track loading state
      isSubmitting: false,  // NEW: Track submission state
      error: null        // NEW: Track errors
    };
  },
  computed: {
    movieId() {  // FIXED: Changed from bookId to movieId
      return this.$route.params.movieId;  // FIXED: Changed from bookId
    },
    ratingDropdownData() {
      return [1, 2, 3, 4, 5];
    },
    isValid() {
      return !!this.title && !!this.director;  // FIXED: Changed from author
    },
  },
  // NEW: Fetch movie data when component loads
  created() {
    this.fetchMovieData();
  },
  methods: {
    // NEW METHOD: Fetch existing movie data to populate form
    async fetchMovieData() {
      this.loading = true;
      this.error = null;
      
      try {
        const movie = await movieAPI.getOne(this.movieId);
        
        // Populate form with existing data
        this.title = movie.title;
        this.director = movie.director;
        this.rating = movie.rating;
        
      } catch (err) {
        console.error('Error loading movie:', err);
        this.error = 'Failed to load movie data.';
      } finally {
        this.loading = false;
      }
    },
    
    // COMPLETELY REPLACED this method
    async handleUpdateMovie() {  // FIXED: Changed from handleUpdateBook
      this.isSubmitting = true;
      this.error = null;
      
      try {
        // REPLACED: Old fetch call with API service
        // OLD CODE (DELETE ALL OF THIS):
        // const res = await fetch(`http://localhost:5000/books/${this.bookId}`, {
        //   method: 'post',
        //   headers: {
        //     'Content-Type': 'application/json'
        //   },
        //   body: JSON.stringify({
        //     title: this.title,
        //     author: this.author,
        //     rating: this.rating,
        //   }),
        // });
        // this.$router.push(`/books/${this.bookId}`);
        
        // NEW CODE (REPLACE WITH THIS):
        await movieAPI.update(this.movieId, {
          title: this.title,
          director: this.director,
          rating: this.rating,
        });
        
        // Redirect back to movie detail page
        this.$router.push(`/movies/${this.movieId}`);
        
      } catch (err) {
        console.error('Error updating movie:', err);
        this.error = 'Failed to update movie. Please try again.';
      } finally {
        this.isSubmitting = false;
      }
    },
    
    handleCancelClick() {
      this.$router.push(`/movies/${this.movieId}`);  // FIXED: Changed from books
    },
  },
};
</script>
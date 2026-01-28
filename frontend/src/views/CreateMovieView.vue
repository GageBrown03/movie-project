<template>
  <div class="create-movie">
    <h1>New movie</h1>
    
    <!-- NEW: Show error message if create fails -->
    <v-alert v-if="error" type="error" class="mb-4">
      {{ error }}
    </v-alert>
    
    <v-form class="mt-4">
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
      <!-- UPDATED: Disable button while submitting -->
      <v-btn 
        :disabled="!isValid || isSubmitting" 
        :loading="isSubmitting"
        @click="handleCreateMovie"
      >
        Create
      </v-btn>
    </v-form>
  </div>
</template>

<script>
// NEW: Import the API service
import { movieAPI } from '@/services/api';

export default {
  name: 'CreateMovieView',  // FIXED: Changed from 'CreatemovieView' to 'CreateMovieView'
  data() {
    return {
      title: '',
      director: '',
      rating: 1,
      isSubmitting: false,  // NEW: Track submission state
      error: null           // NEW: Track errors
    };
  },
  computed: {
    ratingDropdownData() {
      return [1, 2, 3, 4, 5];
    },
    isValid() {
      return !!this.title && !!this.director;
    },
  },
  methods: {
    // COMPLETELY REPLACED this method
    async handleCreateMovie() {  // FIXED: Changed from handleCreatemovie to handleCreateMovie
      this.isSubmitting = true;  // NEW: Disable button while submitting
      this.error = null;         // NEW: Clear previous errors
      
      try {
        // REPLACED: Old fetch call with API service
        // OLD CODE (DELETE ALL OF THIS):
        // await fetch('http://localhost:5000/movies', {
        //   method: 'post',
        //   headers: {
        //     'Content-Type': 'application/json'
        //   },
        //   body: JSON.stringify({
        //     title: this.title,
        //     director: this.director,
        //     rating: this.rating,
        //   }),
        // });
        // const createdmovie = await res.json();
        // this.$router.push(`/movies/${createdmovie.movieId}`);
        
        // NEW CODE (REPLACE WITH THIS):
        const createdMovie = await movieAPI.create({
          title: this.title,
          director: this.director,
          rating: this.rating,
        });
        
        // Redirect to the newly created movie
        this.$router.push(`/movies/${createdMovie.movieId}`);
        
      } catch (err) {
        // NEW: Show error to user
        console.error('Error creating movie:', err);
        this.error = 'Failed to create movie. Please try again.';
      } finally {
        // NEW: Re-enable button
        this.isSubmitting = false;
      }
    },
  },
};
</script>
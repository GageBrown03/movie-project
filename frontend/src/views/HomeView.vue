<template>
  <div class="home">
    <h1>Welcome to Your Movie Library</h1>  <!-- UPDATED: Better title -->
    <p class="mt-3">Track and rate your favorite movies in this personal movie journal!</p>  <!-- UPDATED: Better description -->
    
    <!-- NEW: Add quick action buttons -->
    <div class="actions mt-6">
      <v-btn color="primary" size="large" to="/movies/new">
        Add New Movie
      </v-btn>
      <v-btn color="secondary" size="large" to="/movies" class="ml-2">
        View Your Movies
      </v-btn>
    </div>
    
    <!-- OPTIONAL: You could add stats here in the future -->
    <!-- Example:
    <div class="stats mt-10">
      <h2>Your Stats</h2>
      <p>Total movies watched: {{ totalMovies }}</p>
      <p>Average rating: {{ averageRating }}</p>
    </div>
    -->
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  
  // OPTIONAL: Add data for future stats feature
  // data() {
  //   return {
  //     totalMovies: 0,
  //     averageRating: 0
  //   };
  // },
  
  // OPTIONAL: Fetch stats when component loads
  // created() {
  //   this.loadStats();
  // },
  
  // methods: {
  //   async loadStats() {
  //     // Fetch all movies and calculate stats
  //     const movies = await movieAPI.getAll();
  //     this.totalMovies = movies.length;
  //     this.averageRating = movies.reduce((sum, m) => sum + m.rating, 0) / movies.length;
  //   }
  // }
};
</script>

<style scoped>
.home {
  text-align: center;
  padding: 40px 20px;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 10px;
}
</style>
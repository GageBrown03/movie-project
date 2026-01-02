<template>
    <div class="all-movies">
      <h1>All movies</h1>
      <v-table class="mt-10">
        <thead>
          <th class="text-left">Title</th>
          <th class="text-left">Author</th>
          <th class="text-left">Rating</th>
        </thead>
        <tbody>
          <tr v-for="movie of movies" :key="movie.movieId">
            <td><router-link :to="`/movies/${movie.movieId}`">{{ movie.title }}</router-link></td>
            <td>{{ movie.author }}</td>
            <td>{{ movie.rating }}</td>
          </tr>
        </tbody>
      </v-table>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AllmoviesView',
    data() {
      return {
        movies: []
      };
    },
    created() {
      this.getAllmovies();
    },
    methods: {
      async getAllmovies(){
        const res = await fetch('http://localhost:5000/movies')
        const data = await res.json();
        this.movies = data;
      }
    }
  };
  
  </script>
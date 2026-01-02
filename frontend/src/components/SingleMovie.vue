<template>
    <div class="single-movie">
      <template v-if="movie">
        <h1>{{ movie.title }}</h1>
        <v-btn flat @click="handleEditClick">Edit</v-btn>
        <v-btn flat @click="handleDeleteClick">Delete</v-btn>
        <h2 class="mt-2">Written by {{ movie.director }}</h2>
        <p class="mt-3">Rated {{ movie.rating }} out of 5</p>
      </template>
    </div>
  </template>
  
  <script>
  export default {
    name: 'SinglemoviesView',
    data() {
      return {
        movie: null
      };
    },
    computed: {
      movieId() {
        return this.$route.params.movieId;
      },
    },
    created() {
      this.getmovie();
    },
    methods: {
      async getmovie() {
        const res = await fetch(`http://localhost:5000/movies/${this.movieId}`);
        const data = res.json();
      this.movie = data;
      },
      handleEditClick() {
        this.$router.push(`/movies/${this.movie.movieId}/edit`);
      },
      async handleDeleteClick() {
        const res = await fetch(`http://localhost:5000/movies/${this.movieId}`, {
          method: 'delete'
        })
        this.$router.push('/movies');
      },
    },
  };
  </script>
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
  name: 'SingleMoviesView',

  data() {
    return {
      movie: null
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
    async getMovie() {
      const res = await fetch(`http://localhost:5000/movies/${this.movieId}`);
      const data = await res.json();
      this.movie = data;
    },

    handleEditClick() {
      this.$router.push(`/movies/${this.movie.movieId}/edit`);
    },

    async handleDeleteClick() {
      await fetch(`http://localhost:5000/movies/${this.movieId}`, {
        method: 'DELETE'
      });

      this.$router.push('/movies');
    }
  }
};
</script>

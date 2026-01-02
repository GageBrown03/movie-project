<template>
    <div class="create-movie">
      <h1>New movie</h1>
      <v-form class="mt-4">
        <v-text-field
          v-model="title"
          label="movie Title"
          required
        />
        <v-text-field
          v-model="director"
          label="movie director"
          required
        />
        <v-select
          v-model="rating"
          :items="ratingDropdownData"
          :rules="[v => !!v || 'Item is required']"
          required
        />
        <v-btn :disabled="!isValid" @click="handleCreatemovie">Create</v-btn>
      </v-form>
    </div>
  </template>
  
  <script>
  export default {
    name: 'CreatemovieView',
    data() {
      return {
        title: '',
        director: '',
        rating: 1,
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
      async handleCreatemovie() {
        await fetch('http://localhost:5000/movies', {
          method: 'post',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            title: this.title,
            director: this.director,
            rating: this.rating,
          }),
        });
        const createdmovie = await res.json();
        this.$router.push(`/movies/${createdmovie.movieId}`);
  
      },
    },
  };
  </script>
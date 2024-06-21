<template>
  <h1>{{ title }}</h1> 

  <ul>
    <li v-for="(movie, index) in movies" :key="index" @click="openModal(movie)">
      {{ movie.title }}
    </li>
  </ul>

  <button @click="toggleModal">Add Movie</button>

  <div v-if="showModal">  
    <movieModal v-if="currentMovie" :movie="currentMovie" @close="toggleModal" />
    <div v-else>
      <form @submit.prevent="addMovie">
        <input v-model="newMovie.title" placeholder="Title" required />
        <input v-model="newMovie.description" placeholder="Description" required />
        <input v-model="newMovie.director" placeholder="Director" required />
        <input type="file" @change="uploadImage" required />
        <button type="submit">Add</button>
      </form>
    </div>
  </div>
</template>

<script>
import movieModal from './components/movieModal.vue'

export default {
  name: 'App',
  components: { movieModal },
  data() {
    return {
      title: "Movie Rating app",
      showModal: false,
      movies: [],
      newMovie: { title: '', description: '', director: '', image: null },
      currentMovie: null
    }
  },
  methods: {
    toggleModal() {
      this.showModal = !this.showModal;
      this.currentMovie = null;
    },
    openModal(movie) {
      this.showModal = true;
      this.currentMovie = movie;
    },
    addMovie() {
      this.movies.push({ ...this.newMovie });
      this.newMovie = { title: '', description: '', director: '', image: null };
      this.toggleModal();
    },
    uploadImage(event) {
      this.newMovie.image = event.target.files[0];
    }
  }
}
</script>


<style>
#app {
  font-family: Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

h1 {
  border-bottom: 1px solid #ddd;
  display: inline-block;
  padding-bottom: 10px;
}
</style>

<!-- movieModal.vue -->
<!-- NOTE: This component currently doesn't integrate with your backend -->
<!-- It appears to be from an earlier iteration of your app -->

<template>
  <div class="backdrop" @click.self="closeModal">
    <div class="modal" :class="{fav: theme === 'fav'}">
      <h3>{{ movie.title }}</h3>
      <img :src="movie.image" alt="Movie poster" />
      <p>{{ movie.description }}</p>
      <p>Directed by: {{ movie.director }}</p>
      <input type="number" v-model.number="movie.rating" min="0" max="10" placeholder="Rate this movie" />
    </div>
  </div> 
</template>

<script>
export default {
  props: ['movie'],
  methods: {
    closeModal() {
      this.$emit('close');
    }
  }
}
</script>

<style>
h2 {
  border-bottom: 1px solid #ddd;
  display: inline-block;
  padding-bottom: 10px;
}
.modal {
  width: 400px;
  padding: 20px;
  margin: 100px auto;
  background : white;
  border-radius: 10px;
}
.backdrop {
  top: 0;
  position: fixed;
  background: rgba(0,0,0,0.5);
  width: 100%;
  height: 100%;
}
.modal.fav {
  background: #b1b0b0;
  color: black;
}
</style>

<!-- 
RECOMMENDATIONS FOR THIS COMPONENT:

1. This modal doesn't save changes to the backend
2. The rating input allows 0-10 but your backend expects 1-5
3. You're not using this component in your router views

OPTIONS:
A) DELETE THIS FILE if you're not using it
B) UPDATE IT to work with your current app:
   - Add save button that calls movieAPI.update()
   - Change rating to 1-5 scale
   - Use it as a detail view modal

C) REPLACE IT with Vuetify's dialog component for consistency:
   <v-dialog> is more aligned with your Vuetify UI
-->
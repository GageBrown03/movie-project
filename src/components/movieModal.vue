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
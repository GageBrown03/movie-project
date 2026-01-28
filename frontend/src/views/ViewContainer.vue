<template>
  <div class="view-container">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'ViewContainer'
};
</script>

<style scoped>
.view-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}
</style>

<!-- 
NOTE: This is a simple wrapper component for your router views.
It's perfectly fine as-is! The added padding/max-width styling
will make your content look better on wide screens.
-->
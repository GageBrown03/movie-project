<template>
  <div class="top-rated-movies">
    <v-row v-if="topRated.length > 0">
      <v-col
        v-for="media in topRated"
        :key="media.mediaId"
        cols="6"
        sm="4"
        md="3"
        lg="2"
      >
        <v-card hover class="poster-card">
          <v-img
            v-if="media.posterUrl"
            :src="media.posterUrl"
            aspect-ratio="2/3"
            cover
          >
            <!-- Rating Badge -->
            <div class="rating-badge">
              <v-chip color="amber" size="small">
                <v-icon start size="small">mdi-star</v-icon>
                {{ media.rating }}
              </v-chip>
            </div>
          </v-img>
          <div v-else class="poster-placeholder">
            <v-icon size="64" color="grey">mdi-movie-outline</v-icon>
          </div>

          <v-card-text class="pa-3">
            <div class="text-subtitle-2 font-weight-bold text-truncate" :title="media.title">
              {{ media.title }}
            </div>
            <div class="text-caption text-medium-emphasis">
              {{ media.releaseYear }}
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Empty State -->
    <v-empty-state
      v-else
      icon="mdi-star-off"
      :title="`${username} hasn't rated anything yet`"
      text="No rated movies or shows to display"
    />
  </div>
</template>

<script>
export default {
  name: 'TopRatedMovies',

  props: {
    mediaList: {
      type: Array,
      required: true
    },
    username: {
      type: String,
      required: true
    }
  },

  computed: {
    topRated() {
      return [...this.mediaList]
        .filter(m => m.rating)
        .sort((a, b) => {
          // Sort by rating (desc), then by date (desc)
          if (b.rating !== a.rating) {
            return b.rating - a.rating;
          }
          return new Date(b.createdAt) - new Date(a.createdAt);
        })
        .slice(0, 30); // Top 30
    }
  }
};
</script>

<style scoped>
.poster-card {
  height: 100%;
}

.rating-badge {
  position: absolute;
  top: 8px;
  right: 8px;
}

.poster-placeholder {
  aspect-ratio: 2/3;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.1);
}
</style>
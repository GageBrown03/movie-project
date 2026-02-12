<template>
  <div class="user-collection">
    <!-- Filters -->
    <v-card class="mb-4" elevation="2">
      <v-card-text>
        <v-row>
          <v-col cols="12" md="4">
            <v-select
              v-model="filterType"
              :items="typeOptions"
              label="Media Type"
              variant="outlined"
              density="comfortable"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
              v-model="filterStatus"
              :items="statusOptions"
              label="Status"
              variant="outlined"
              density="comfortable"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
              v-model="sortBy"
              :items="sortOptions"
              label="Sort by"
              variant="outlined"
              density="comfortable"
            />
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Media Grid -->
    <v-row v-if="filteredMedia.length > 0">
      <v-col
        v-for="media in filteredMedia"
        :key="media.mediaId"
        cols="6"
        sm="4"
        md="3"
        lg="2"
      >
        <v-card hover class="media-card">
          <v-img
            v-if="media.posterUrl"
            :src="media.posterUrl"
            aspect-ratio="2/3"
            cover
          >
            <!-- Status Badge -->
            <div class="status-badge">
              <v-chip
                v-if="media.status === 'watched' && media.rating && canViewRatings"
                color="amber"
                size="small"
              >
                <v-icon start size="small">mdi-star</v-icon>
                {{ media.rating }}
              </v-chip>
              <v-chip
                v-else-if="media.status === 'want_to_watch'"
                color="info"
                size="small"
              >
                <v-icon start size="small">mdi-bookmark</v-icon>
                Watchlist
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
            <v-chip
              size="x-small"
              :color="media.mediaType === 'movie' ? 'primary' : 'secondary'"
              class="mt-1"
            >
              {{ media.mediaType.toUpperCase() }}
            </v-chip>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Empty State -->
    <v-card v-else class="text-center pa-12">
      <v-icon size="64" color="grey">mdi-filter-off</v-icon>
      <h3 class="text-h5 mt-4">No matches</h3>
      <p class="text-body-2 text-medium-emphasis">Try adjusting your filters</p>
    </v-card>
  </div>
</template>

<script>
export default {
  name: 'UserCollection',

  props: {
    mediaList: {
      type: Array,
      required: true
    },
    username: {
      type: String,
      required: true
    },
    canViewRatings: {
      type: Boolean,
      default: false
    }
  },

  data() {
    return {
      filterType: 'all',
      typeOptions: [
        { title: 'All Types', value: 'all' },
        { title: 'Movies Only', value: 'movie' },
        { title: 'TV Shows Only', value: 'tv' }
      ],
      filterStatus: 'all',
      statusOptions: [
        { title: 'All Status', value: 'all' },
        { title: 'Watched', value: 'watched' },
        { title: 'Watchlist', value: 'want_to_watch' }
      ],
      sortBy: 'date_desc',
      sortOptions: [
        { title: 'Recently Added', value: 'date_desc' },
        { title: 'Oldest First', value: 'date_asc' },
        { title: 'Title (A-Z)', value: 'title_asc' },
        { title: 'Title (Z-A)', value: 'title_desc' },
        { title: 'Rating (High to Low)', value: 'rating_desc' },
        { title: 'Rating (Low to High)', value: 'rating_asc' },
        { title: 'Release Year (New)', value: 'year_desc' },
        { title: 'Release Year (Old)', value: 'year_asc' }
      ]
    };
  },

  computed: {
    filteredMedia() {
      let filtered = [...this.mediaList];

      // Filter by type
      if (this.filterType !== 'all') {
        filtered = filtered.filter(m => m.mediaType === this.filterType);
      }

      // Filter by status
      if (this.filterStatus !== 'all') {
        filtered = filtered.filter(m => m.status === this.filterStatus);
      }

      // Sort
      switch (this.sortBy) {
        case 'date_desc':
          filtered.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
          break;
        case 'date_asc':
          filtered.sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt));
          break;
        case 'title_asc':
          filtered.sort((a, b) => a.title.localeCompare(b.title));
          break;
        case 'title_desc':
          filtered.sort((a, b) => b.title.localeCompare(a.title));
          break;
        case 'rating_desc':
          filtered.sort((a, b) => (b.rating || 0) - (a.rating || 0));
          break;
        case 'rating_asc':
          filtered.sort((a, b) => (a.rating || 0) - (b.rating || 0));
          break;
        case 'year_desc':
          filtered.sort((a, b) => (b.releaseYear || 0) - (a.releaseYear || 0));
          break;
        case 'year_asc':
          filtered.sort((a, b) => (a.releaseYear || 0) - (b.releaseYear || 0));
          break;
      }

      return filtered;
    }
  }
};
</script>

<style scoped>
.media-card {
  height: 100%;
}

.status-badge {
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
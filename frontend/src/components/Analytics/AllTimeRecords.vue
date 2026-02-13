<template>
  <v-card elevation="2">
    <v-card-title class="text-h6">
      <v-icon start color="amber">mdi-trophy</v-icon>
      Personal Records
    </v-card-title>
    
    <v-card-text v-if="loading">
      <v-row>
        <v-col v-for="i in 6" :key="i" cols="12" sm="6" md="4">
          <v-skeleton-loader type="card" />
        </v-col>
      </v-row>
    </v-card-text>

    <v-card-text v-else-if="!hasRecords" class="text-center py-8">
      <v-icon size="48" color="grey">mdi-trophy-outline</v-icon>
      <p class="text-body-2 text-medium-emphasis mt-2">
        No records yet - keep watching!
      </p>
    </v-card-text>
    
    <v-card-text v-else>
      <v-row>
        <!-- Highest Rated -->
        <v-col v-if="records.highestRated" cols="12" sm="6" md="4">
          <v-card 
            variant="tonal" 
            color="success" 
            class="record-card"
            @click="goToMedia(records.highestRated.mediaId)"
            link
          >
            <v-card-text>
              <div class="d-flex align-center mb-2">
                <v-icon color="success" size="32" class="mr-2">
                  mdi-thumb-up
                </v-icon>
                <div class="text-caption text-medium-emphasis">
                  Highest Rated
                </div>
              </div>
              
              <div class="d-flex align-center">
                <v-avatar v-if="records.highestRated.posterUrl" size="60" rounded class="mr-3">
                  <v-img :src="records.highestRated.posterUrl" cover />
                </v-avatar>
                
                <div class="flex-grow-1">
                  <div class="text-body-2 font-weight-bold line-clamp-2">
                    {{ records.highestRated.title }}
                  </div>
                  <v-rating
                    :model-value="records.highestRated.rating"
                    readonly
                    density="compact"
                    color="amber"
                    size="small"
                  />
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Lowest Rated -->
        <v-col v-if="records.lowestRated" cols="12" sm="6" md="4">
          <v-card 
            variant="tonal" 
            color="error" 
            class="record-card"
            @click="goToMedia(records.lowestRated.mediaId)"
            link
          >
            <v-card-text>
              <div class="d-flex align-center mb-2">
                <v-icon color="error" size="32" class="mr-2">
                  mdi-thumb-down
                </v-icon>
                <div class="text-caption text-medium-emphasis">
                  Lowest Rated
                </div>
              </div>
              
              <div class="d-flex align-center">
                <v-avatar v-if="records.lowestRated.posterUrl" size="60" rounded class="mr-3">
                  <v-img :src="records.lowestRated.posterUrl" cover />
                </v-avatar>
                
                <div class="flex-grow-1">
                  <div class="text-body-2 font-weight-bold line-clamp-2">
                    {{ records.lowestRated.title }}
                  </div>
                  <v-rating
                    :model-value="records.lowestRated.rating"
                    readonly
                    density="compact"
                    color="amber"
                    size="small"
                  />
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Genre Champion -->
        <v-col v-if="records.genreChampion" cols="12" sm="6" md="4">
          <v-card variant="tonal" color="purple" class="record-card">
            <v-card-text>
              <div class="d-flex align-center mb-2">
                <v-icon color="purple" size="32" class="mr-2">
                  mdi-crown
                </v-icon>
                <div class="text-caption text-medium-emphasis">
                  Genre Champion
                </div>
              </div>
              
              <div class="text-h5 font-weight-bold">
                {{ records.genreChampion.genre }}
              </div>
              <div class="text-body-2">
                {{ records.genreChampion.count }} {{ records.genreChampion.count === 1 ? 'movie' : 'movies' }}
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Best Genre (Highest Average Rating) -->
        <v-col v-if="records.bestGenre" cols="12" sm="6" md="4">
          <v-card variant="tonal" color="indigo" class="record-card">
            <v-card-text>
              <div class="d-flex align-center mb-2">
                <v-icon color="indigo" size="32" class="mr-2">
                  mdi-star-circle
                </v-icon>
                <div class="text-caption text-medium-emphasis">
                  Best Genre (Avg Rating)
                </div>
              </div>
              
              <div class="text-h5 font-weight-bold">
                {{ records.bestGenre.genre }}
              </div>
              <div class="text-body-2">
                {{ records.bestGenre.averageRating }}★ average ({{ records.bestGenre.count }} rated)
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- TMDB Contrarian -->
        <v-col v-if="records.tmdbContrarian" cols="12" sm="6" md="4">
          <v-card 
            variant="tonal" 
            :color="records.tmdbContrarian.type === 'generous' ? 'teal' : 'orange'" 
            class="record-card"
          >
            <v-card-text>
              <div class="d-flex align-center mb-2">
                <v-icon 
                  :color="records.tmdbContrarian.type === 'generous' ? 'teal' : 'orange'" 
                  size="32" 
                  class="mr-2"
                >
                  {{ records.tmdbContrarian.type === 'generous' ? 'mdi-heart' : 'mdi-gavel' }}
                </v-icon>
                <div class="text-caption text-medium-emphasis">
                  vs TMDB
                </div>
              </div>
              
              <div class="text-h5 font-weight-bold">
                {{ records.tmdbContrarian.difference > 0 ? '+' : '' }}{{ records.tmdbContrarian.difference }}★
              </div>
              <div class="text-body-2">
                {{ records.tmdbContrarian.type === 'generous' ? 'More generous' : 'Harsher critic' }} than TMDB
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Collection Milestone -->
        <v-col v-if="records.collectionMilestone" cols="12" sm="6" md="4">
          <v-card variant="tonal" color="primary" class="record-card">
            <v-card-text>
              <div class="d-flex align-center mb-2">
                <v-icon color="primary" size="32" class="mr-2">
                  mdi-flag-checkered
                </v-icon>
                <div class="text-caption text-medium-emphasis">
                  Collection Milestone
                </div>
              </div>
              
              <div class="text-h5 font-weight-bold">
                {{ records.collectionMilestone.total }} Items
              </div>
              <div class="text-body-2 mb-2">
                <v-icon size="small">mdi-check</v-icon>
                Reached {{ records.collectionMilestone.reached }}
              </div>
              
              <div v-if="records.collectionMilestone.next">
                <v-progress-linear
                  :model-value="records.collectionMilestone.progress"
                  color="primary"
                  height="8"
                  rounded
                  class="mb-1"
                />
                <div class="text-caption">
                  {{ records.collectionMilestone.next - records.collectionMilestone.total }} 
                  to reach {{ records.collectionMilestone.next }}
                </div>
              </div>
              <div v-else class="text-caption">
                <v-icon size="small" color="amber">mdi-trophy</v-icon>
                Max milestone reached!
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'AllTimeRecords',
  
  props: {
    records: {
      type: Object,
      default: () => ({})
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  
  computed: {
    hasRecords() {
      return Object.keys(this.records).length > 0;
    }
  },
  
  methods: {
    goToMedia(mediaId) {
      if (mediaId) {
        this.$router.push(`/media/${mediaId}`);
      }
    }
  }
};
</script>

<style scoped>
.record-card {
  cursor: pointer;
  transition: transform 0.2s ease;
  height: 100%;
}

.record-card:hover {
  transform: translateY(-4px);
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
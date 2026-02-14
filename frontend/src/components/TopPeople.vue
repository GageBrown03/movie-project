<template>
  <v-row>
    <!-- Top Actors -->
    <v-col cols="12" md="6">
      <v-card elevation="2">
        <v-card-title class="text-h6">
          <v-icon start color="primary">mdi-account-star</v-icon>
          Your Favorite Actors
        </v-card-title>
        
        <v-card-text v-if="loading">
          <v-row>
            <v-col v-for="i in 5" :key="i" cols="12">
              <v-skeleton-loader type="list-item-avatar-two-line" />
            </v-col>
          </v-row>
        </v-card-text>

        <v-card-text v-else-if="actors.length === 0" class="text-center py-8">
          <v-icon size="48" color="grey">mdi-account-off</v-icon>
          <p class="text-body-2 text-medium-emphasis mt-2">
            No actor data yet
          </p>
        </v-card-text>
        
        <v-list v-else lines="two" class="bg-transparent">
          <v-list-item
            v-for="(actor, index) in displayedActors"
            :key="actor.id"
            @click="filterByActor(actor)"
            link
          >
            <template v-slot:prepend>
              <v-avatar size="56" class="mr-3">
                <v-img 
                  v-if="actor.photo" 
                  :src="actor.photo" 
                  cover
                />
                <v-icon v-else size="32">mdi-account</v-icon>
              </v-avatar>
            </template>

            <v-list-item-title class="font-weight-bold">
              {{ actor.name }}
            </v-list-item-title>

            <v-list-item-subtitle>
              {{ actor.count }} {{ actor.count === 1 ? 'movie' : 'movies' }}
            </v-list-item-subtitle>

            <template v-slot:append>
              <v-chip 
                :color="getRankColor(index)" 
                size="small"
                variant="tonal"
              >
                #{{ index + 1 }}
              </v-chip>
            </template>
          </v-list-item>
        </v-list>
        
        <!-- Show More/Less Button for Actors -->
        <v-card-actions v-if="actors.length > 5" class="justify-center">
          <v-btn
            variant="text"
            color="primary"
            @click="showAllActors = !showAllActors"
          >
            {{ showAllActors ? 'Show Less' : `Show More (${actors.length - 5} more)` }}
            <v-icon :icon="showAllActors ? 'mdi-chevron-up' : 'mdi-chevron-down'" end />
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-col>

    <!-- Top Directors -->
    <v-col cols="12" md="6">
      <v-card elevation="2">
        <v-card-title class="text-h6">
          <v-icon start color="secondary">mdi-movie-open-star</v-icon>
          Your Favorite Directors
        </v-card-title>
        
        <v-card-text v-if="loading">
          <v-row>
            <v-col v-for="i in 5" :key="i" cols="12">
              <v-skeleton-loader type="list-item-avatar-two-line" />
            </v-col>
          </v-row>
        </v-card-text>

        <v-card-text v-else-if="directors.length === 0" class="text-center py-8">
          <v-icon size="48" color="grey">mdi-account-off</v-icon>
          <p class="text-body-2 text-medium-emphasis mt-2">
            No director data yet
          </p>
        </v-card-text>
        
        <v-list v-else lines="two" class="bg-transparent">
          <v-list-item
            v-for="(director, index) in displayedDirectors"
            :key="director.id || director.name"
            @click="filterByDirector(director)"
            link
          >
            <template v-slot:prepend>
              <v-avatar size="56" class="mr-3">
                <v-img 
                  v-if="director.photo" 
                  :src="director.photo" 
                  cover
                />
                <v-icon v-else size="32">mdi-movie-open</v-icon>
              </v-avatar>
            </template>

            <v-list-item-title class="font-weight-bold">
              {{ director.name }}
            </v-list-item-title>

            <v-list-item-subtitle>
              {{ director.count }} {{ director.count === 1 ? 'movie' : 'movies' }}
            </v-list-item-subtitle>

            <template v-slot:append>
              <v-chip 
                :color="getRankColor(index)" 
                size="small"
                variant="tonal"
              >
                #{{ index + 1 }}
              </v-chip>
            </template>
          </v-list-item>
        </v-list>
        
        <!-- Show More/Less Button for Directors -->
        <v-card-actions v-if="directors.length > 5" class="justify-center">
          <v-btn
            variant="text"
            color="secondary"
            @click="showAllDirectors = !showAllDirectors"
          >
            {{ showAllDirectors ? 'Show Less' : `Show More (${directors.length - 5} more)` }}
            <v-icon :icon="showAllDirectors ? 'mdi-chevron-up' : 'mdi-chevron-down'" end />
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'TopPeople',
  
  props: {
    actors: {
      type: Array,
      default: () => []
    },
    directors: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  
  data() {
    return {
      showAllActors: false,
      showAllDirectors: false
    };
  },
  
  computed: {
    displayedActors() {
      return this.showAllActors ? this.actors : this.actors.slice(0, 5);
    },
    
    displayedDirectors() {
      return this.showAllDirectors ? this.directors : this.directors.slice(0, 5);
    }
  },
  
  emits: ['filter-by-actor', 'filter-by-director'],
  
  methods: {
    getRankColor(index) {
      if (index === 0) return 'amber';
      if (index === 1) return 'grey';
      if (index === 2) return 'orange';
      return 'primary';
    },
    
    filterByActor(actor) {
      this.$emit('filter-by-actor', actor);
    },
    
    filterByDirector(director) {
      this.$emit('filter-by-director', director);
    }
  }
};
</script>

<style scoped>
.v-list-item {
  transition: transform 0.2s ease;
}

.v-list-item:hover {
  transform: translateX(4px);
}
</style>
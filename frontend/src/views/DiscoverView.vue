<template>
  <div class="discover-view">
    <!-- Header -->
    <v-row class="mb-6 align-center">
      <v-col>
        <h1 class="text-h3 font-weight-bold">Discover</h1>
        
      </v-col>
    </v-row>

    <!-- Loading State -->
    <v-row v-if="loading" justify="center" class="my-12">
      <v-progress-circular indeterminate size="64" color="primary" />
    </v-row>

    <div v-else>
      <!-- Trending This Week -->
      <section class="mb-8">
        <div class="section-header mb-4">
          <h2 class="text-h5 font-weight-bold">
            <v-icon color="error" class="mr-2">mdi-trending-up</v-icon>
            Trending This Week
          </h2>
          
        </div>

        <v-row>
          <v-col 
            v-for="media in trendingRecommendations.slice(0, 6)" 
            :key="media.tmdbId"
            cols="6"
            sm="4"
            md="2"
          >
            <recommendation-card 
              :item="media"
              :is-in-collection="isInCollection(media.tmdbId)"
              @click="handleCardClick(media)"
            />
          </v-col>
        </v-row>
      </section>

      <!-- Based on Your Favorite Genre -->
      <section v-if="favoriteGenre" class="mb-8">
        <div class="section-header mb-4">
          <h2 class="text-h5 font-weight-bold">
            <v-icon color="primary" class="mr-2">mdi-movie-open</v-icon>
            More {{ favoriteGenre }}
          </h2>
          <p class="text-caption text-medium-emphasis">
            Your most-watched genre
          </p>
        </div>

        <v-row>
          <v-col 
            v-for="media in genreRecommendations.slice(0, 6)" 
            :key="media.tmdbId"
            cols="6"
            sm="4"
            md="2"
          >
            <recommendation-card 
              :item="media"
              :is-in-collection="isInCollection(media.tmdbId)"
              @click="handleCardClick(media)"
            />
          </v-col>
        </v-row>
      </section>

      <!-- Based on Your Ratings -->
      <section v-if="fiveStarMedia.length > 0" class="mb-8">
        <div class="section-header mb-4">
          <h2 class="text-h5 font-weight-bold">
            <v-icon color="amber" class="mr-2">mdi-star</v-icon>
            Based on What You Loved
          </h2>
          <p class="text-caption text-medium-emphasis">
            
          </p>
        </div>

        <v-row>
          <v-col 
            v-for="media in fiveStarRecommendations.slice(0, 6)" 
            :key="media.tmdbId"
            cols="6"
            sm="4"
            md="2"
          >
            <recommendation-card 
              :item="media"
              :is-in-collection="isInCollection(media.tmdbId)"
              @click="handleCardClick(media)"
            />
          </v-col>
        </v-row>
      </section>

      <!-- Based on Your Favorite Actors -->
      <section v-if="topActors.length > 0" class="mb-8">
        <div class="section-header mb-4">
          <h2 class="text-h5 font-weight-bold">
            <v-icon color="secondary" class="mr-2">mdi-account-star</v-icon>
            Featuring Your Favorite Actors
          </h2>
          
        </div>

        <v-row>
          <v-col 
            v-for="media in actorRecommendations.slice(0, 6)" 
            :key="media.tmdbId"
            cols="6"
            sm="4"
            md="2"
          >
            <recommendation-card 
              :item="media"
              :is-in-collection="isInCollection(media.tmdbId)"
              @click="handleCardClick(media)"
            />
          </v-col>
        </v-row>
      </section>

      
      <!-- Hidden Gems (High TMDB, Not in Your Collection) -->
      <section v-if="hiddenGems.length > 0" class="mb-8">
        <div class="section-header mb-4">
          <h2 class="text-h5 font-weight-bold">
            <v-icon color="info" class="mr-2">mdi-diamond-stone</v-icon>
            Hidden Gems
          </h2>
          
        </div>

        <v-row>
          <v-col 
            v-for="media in hiddenGems.slice(0, 6)" 
            :key="media.tmdbId"
            cols="6"
            sm="4"
            md="2"
          >
            <recommendation-card 
              :item="media"
              :is-in-collection="isInCollection(media.tmdbId)"
              @click="handleCardClick(media)"
            />
          </v-col>
        </v-row>
      </section>

      <!-- Empty State -->
      <v-empty-state
        v-if="!hasRecommendations"
        icon="mdi-lightbulb-outline"
        title="Build Your Collection"
        text="Rate some movies and TV shows to get personalized recommendations!"
      >
        <template v-slot:actions>
          <v-btn color="primary" size="large" to="/media/new">
            Add Media
          </v-btn>
        </template>
      </v-empty-state>
    </div>

    <!-- Quick Add Dialog -->
    <v-dialog v-model="showQuickAddDialog" max-width="700">
      <v-card v-if="selectedItem">
        <v-img
          v-if="selectedItem.backdropUrl"
          :src="selectedItem.backdropUrl"
          height="300"
          cover
          gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.8)"
        >
          <div class="pa-6" style="position: absolute; bottom: 0;">
            <v-chip 
              :color="selectedItem.mediaType === 'movie' ? 'primary' : 'secondary'"
              size="small"
              class="mb-2"
            >
              {{ selectedItem.mediaType === 'movie' ? 'MOVIE' : 'TV' }}
            </v-chip>
            <h2 class="text-h4 text-white">{{ selectedItem.title }}</h2>
          </div>
        </v-img>
        
        <v-card-text class="pt-6">
          <div class="d-flex gap-2 mb-4">
            <v-chip v-if="selectedItem.releaseYear" size="small">
              {{ selectedItem.releaseYear }}
            </v-chip>
            <v-chip v-if="selectedItem.tmdbRating" size="small">
              <v-icon start size="small">mdi-star</v-icon>
              {{ selectedItem.tmdbRating.toFixed(1) }}
            </v-chip>
          </div>
          
          <p v-if="selectedItem.plot" class="text-body-1">
            {{ selectedItem.plot }}
          </p>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="showQuickAddDialog = false">
            Cancel
          </v-btn>
          <v-btn color="info" @click="addToWatchlist" :loading="adding">
            <v-icon start>mdi-bookmark-plus</v-icon>
            Add to Watchlist
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { recommendationsAPI } from '@/services/recommendations';
import { mediaAPI } from '@/services/api-production';
import RecommendationCard from '@/components/RecommendationCard.vue';

export default {
  name: 'DiscoverView',
  
  components: {
    RecommendationCard
  },
  
  data() {
    return {
      loading: false,
      userCollection: [],
      
      // Recommendation categories
      fiveStarMedia: [],
      fiveStarRecommendations: [],
      favoriteGenre: null,
      genreRecommendations: [],
      topActors: [],
      actorRecommendations: [],
      trendingRecommendations: [],
      hiddenGems: [],
      
      // Quick add dialog
      showQuickAddDialog: false,
      selectedItem: null,
      adding: false,
    };
  },
  
  computed: {
    hasRecommendations() {
      return this.fiveStarRecommendations.length > 0 ||
             this.genreRecommendations.length > 0 ||
             this.actorRecommendations.length > 0 ||
             this.trendingRecommendations.length > 0;
    }
  },
  
  created() {
    this.loadRecommendations();
  },
  
  methods: {
    async loadRecommendations() {
      this.loading = true;
      
      try {
        // Load user collection
        this.userCollection = await mediaAPI.getAll();
        
        // Analyze collection
        await this.analyzeFavorites();
        
        // Load different recommendation types in parallel
        await Promise.all([
          this.loadFiveStarRecommendations(),
          this.loadGenreRecommendations(),
          this.loadActorRecommendations(),
          this.loadTrendingRecommendations(),
          this.loadHiddenGems()
        ]);
        
      } catch (err) {
        console.error('Error loading recommendations:', err);
      } finally {
        this.loading = false;
      }
    },
    
    analyzeFavorites() {
      // Get 5-star rated media
      this.fiveStarMedia = this.userCollection.filter(m => m.rating === 5);
      
      // Find favorite genre
      const genreCounts = {};
      this.userCollection.forEach(m => {
        if (m.genres) {
          const genres = Array.isArray(m.genres) ? m.genres : m.genres.split(', ');
          genres.forEach(g => {
            genreCounts[g] = (genreCounts[g] || 0) + 1;
          });
        }
      });
      
      const topGenre = Object.entries(genreCounts)
        .sort((a, b) => b[1] - a[1])[0];
      this.favoriteGenre = topGenre ? topGenre[0] : null;
      
      // Find top actors
      const actorCounts = {};
      this.userCollection.forEach(m => {
        if (m.cast && Array.isArray(m.cast)) {
          m.cast.forEach(actor => {
            if (!actorCounts[actor.actorId]) {
              actorCounts[actor.actorId] = {
                id: actor.actorId,
                name: actor.name,
                count: 0
              };
            }
            actorCounts[actor.actorId].count++;
          });
        }
      });
      
      this.topActors = Object.values(actorCounts)
        .sort((a, b) => b.count - a.count)
        .slice(0, 3);
    },
    
    async loadFiveStarRecommendations() {
      if (this.fiveStarMedia.length === 0) return;
      
      // Get similar content for random 5-star item
      const randomFiveStar = this.fiveStarMedia[
        Math.floor(Math.random() * this.fiveStarMedia.length)
      ];
      
      if (randomFiveStar.tmdbId) {
        try {
          const similar = await recommendationsAPI.getSimilar(
            randomFiveStar.tmdbId,
            randomFiveStar.mediaType
          );
          
          // Filter out items already in collection
          this.fiveStarRecommendations = similar.filter(
            item => !this.isInCollection(item.tmdbId)
          );
        } catch (err) {
          console.error('Error loading 5-star recommendations:', err);
        }
      }
    },
    
    async loadGenreRecommendations() {
      if (!this.favoriteGenre) return;
      
      const genreId = recommendationsAPI.genreMap[this.favoriteGenre];
      if (!genreId) return;
      
      try {
        const recommendations = await recommendationsAPI.getByGenre(genreId, 'movie');
        
        this.genreRecommendations = recommendations.filter(
          item => !this.isInCollection(item.tmdbId)
        );
      } catch (err) {
        console.error('Error loading genre recommendations:', err);
      }
    },
    
    async loadActorRecommendations() {
      if (this.topActors.length === 0) return;
      
      // Get recommendations for top actor
      const topActor = this.topActors[0];
      
      try {
        const recommendations = await recommendationsAPI.getByActor(topActor.id);
        
        this.actorRecommendations = recommendations.filter(
          item => !this.isInCollection(item.tmdbId)
        );
      } catch (err) {
        console.error('Error loading actor recommendations:', err);
      }
    },
    
    async loadTrendingRecommendations() {
      try {
        const trending = await recommendationsAPI.getTrending('all', 'week');
        
        this.trendingRecommendations = trending.filter(
          item => !this.isInCollection(item.tmdbId)
        );
      } catch (err) {
        console.error('Error loading trending:', err);
      }
    },
    
    async loadHiddenGems() {
      try {
        // Get highly rated movies not in collection
        const recommendations = await recommendationsAPI.getByGenre(18, 'movie'); // Drama genre
        
        this.hiddenGems = recommendations
          .filter(item => !this.isInCollection(item.tmdbId))
          .filter(item => item.tmdbRating >= 7.5)
          .slice(0, 12);
      } catch (err) {
        console.error('Error loading hidden gems:', err);
      }
    },
    
    isInCollection(tmdbId) {
      return this.userCollection.some(m => m.tmdbId === tmdbId);
    },
    
    handleCardClick(item) {
      if (this.isInCollection(item.tmdbId)) {
        const existing = this.userCollection.find(m => m.tmdbId === item.tmdbId);
        this.$router.push(`/media/${existing.mediaId}`);
      } else {
        this.selectedItem = item;
        this.showQuickAddDialog = true;
      }
    },
    
    async addToWatchlist() {
      if (!this.selectedItem) return;
      
      this.adding = true;
      
      try {
        const mediaData = {
          title: this.selectedItem.title,
          media_type: this.selectedItem.mediaType,
          tmdb_id: this.selectedItem.tmdbId,
          status: 'want_to_watch',
          release_year: this.selectedItem.releaseYear,
          plot: this.selectedItem.plot,
          poster_url: this.selectedItem.posterUrl,
          backdrop_url: this.selectedItem.backdropUrl,
          tmdb_rating: this.selectedItem.tmdbRating,
        };
        
        const created = await mediaAPI.create(mediaData);
        
        // Refresh collection
        this.userCollection = await mediaAPI.getAll();
        
        // Close dialog and navigate
        this.showQuickAddDialog = false;
        this.$router.push(`/media/${created.mediaId}`);
        
      } catch (err) {
        console.error('Error adding to watchlist:', err);
      } finally {
        this.adding = false;
      }
    },
  },
};
</script>

<style scoped>
.discover-view {
  max-width: 1600px;
  margin: 0 auto;
}

.section-header {
  border-left: 4px solid currentColor;
  padding-left: 16px;
}

.gap-2 {
  gap: 8px;
}
</style>
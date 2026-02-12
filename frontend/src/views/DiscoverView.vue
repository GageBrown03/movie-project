<template>
  <div class="discover-view">
    <v-row class="mb-6 align-center">
      <v-col>
        <h1 class="text-h3 font-weight-bold">Discover</h1>
      </v-col>
    </v-row>

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
            <media-quick-add-card
              :item="media"
              :is-in-collection="!!getLibraryStatus(media.tmdbId)"
              :collection-info="getLibraryStatus(media.tmdbId)"
              :loading="loadingStates[media.tmdbId]"
              :is-mobile="isMobile"
              @quick-add-watchlist="quickAddToWatchlist"
              @quick-add-rated="openRatingDialog"
              @view-existing="goToExisting"
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
            <media-quick-add-card
              :item="media"
              :is-in-collection="!!getLibraryStatus(media.tmdbId)"
              :collection-info="getLibraryStatus(media.tmdbId)"
              :loading="loadingStates[media.tmdbId]"
              :is-mobile="isMobile"
              @quick-add-watchlist="quickAddToWatchlist"
              @quick-add-rated="openRatingDialog"
              @view-existing="goToExisting"
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
        </div>

        <v-row>
          <v-col 
            v-for="media in fiveStarRecommendations.slice(0, 6)" 
            :key="media.tmdbId"
            cols="6"
            sm="4"
            md="2"
          >
            <media-quick-add-card
              :item="media"
              :is-in-collection="!!getLibraryStatus(media.tmdbId)"
              :collection-info="getLibraryStatus(media.tmdbId)"
              :loading="loadingStates[media.tmdbId]"
              :is-mobile="isMobile"
              @quick-add-watchlist="quickAddToWatchlist"
              @quick-add-rated="openRatingDialog"
              @view-existing="goToExisting"
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
            <media-quick-add-card
              :item="media"
              :is-in-collection="!!getLibraryStatus(media.tmdbId)"
              :collection-info="getLibraryStatus(media.tmdbId)"
              :loading="loadingStates[media.tmdbId]"
              :is-mobile="isMobile"
              @quick-add-watchlist="quickAddToWatchlist"
              @quick-add-rated="openRatingDialog"
              @view-existing="goToExisting"
            />
          </v-col>
        </v-row>
      </section>

      <!-- Hidden Gems -->
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
            <media-quick-add-card
              :item="media"
              :is-in-collection="!!getLibraryStatus(media.tmdbId)"
              :collection-info="getLibraryStatus(media.tmdbId)"
              :loading="loadingStates[media.tmdbId]"
              :is-mobile="isMobile"
              @quick-add-watchlist="quickAddToWatchlist"
              @quick-add-rated="openRatingDialog"
              @view-existing="goToExisting"
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
          <v-btn color="primary" size="large" @click="$emit('open-add-dialog')">
            Add Media
          </v-btn>
        </template>
      </v-empty-state>
    </div>

    <!-- Rating Dialog -->
    <v-dialog v-model="showRatingDialog" max-width="500">
      <v-card v-if="itemToRate">
        <v-card-title>Rate {{ itemToRate.title }}</v-card-title>
        <v-card-text>
          <div class="d-flex align-center mb-4">
            <v-avatar size="60" rounded class="mr-3">
              <v-img v-if="itemToRate.posterUrl" :src="itemToRate.posterUrl" />
            </v-avatar>
            <div>
              <p class="text-body-1 font-weight-bold mb-0">{{ itemToRate.title }}</p>
              <p class="text-caption text-medium-emphasis">
                {{ itemToRate.mediaType === 'movie' ? 'Movie' : 'TV Show' }} • {{ itemToRate.releaseYear }}
              </p>
            </div>
          </div>

          <v-rating
            v-model="userRating"
            color="primary"
            size="large"
            hover
          />
          <p class="text-caption mt-2">
            {{ userRating ? `${userRating} out of 5 stars` : 'Tap to rate' }}
          </p>

          <v-textarea
            v-model="userNotes"
            label="Personal notes (optional)"
            variant="outlined"
            rows="2"
            class="mt-4"
            placeholder="What did you think?"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="closeRatingDialog">Cancel</v-btn>
          <v-btn
            color="primary"
            @click="saveWithRating"
            :loading="savingRating"
            :disabled="!userRating"
          >
            Add to Library
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Success Snackbar -->
    <v-snackbar v-model="showSnackbar" :color="snackbarColor" timeout="3000">
      {{ snackbarMessage }}
      <template v-slot:actions>
        <v-btn variant="text" @click="showSnackbar = false">Close</v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import { recommendationsAPI } from '@/services/recommendations';
import { mediaAPI, tmdbAPI } from '@/services/api-production';
import MediaQuickAddCard from '@/components/MediaQuickAddCard.vue';

export default {
  name: 'DiscoverView',
  
  components: {
    MediaQuickAddCard
  },

  emits: ['open-add-dialog'],
  
  data() {
    return {
      loading: false,
      userCollection: [],
      loadingStates: {},
      
      fiveStarMedia: [],
      fiveStarRecommendations: [],
      favoriteGenre: null,
      genreRecommendations: [],
      topActors: [],
      actorRecommendations: [],
      trendingRecommendations: [],
      hiddenGems: [],
      
      showRatingDialog: false,
      itemToRate: null,
      userRating: null,
      userNotes: '',
      savingRating: false,

      showSnackbar: false,
      snackbarMessage: '',
      snackbarColor: 'success'
    };
  },
  
  computed: {
    hasRecommendations() {
      return this.fiveStarRecommendations.length > 0 ||
             this.genreRecommendations.length > 0 ||
             this.actorRecommendations.length > 0 ||
             this.trendingRecommendations.length > 0;
    },
    
    isMobile() {
      return this.$vuetify.display.mobile;
    }
  },
  
  created() {
    this.loadRecommendations();
  },
  
  methods: {
    async loadRecommendations() {
      this.loading = true;
      
      try {
        this.userCollection = await mediaAPI.getAll();
        await this.analyzeFavorites();
        
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
      this.fiveStarMedia = this.userCollection.filter(m => m.rating === 5);
      
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
      
      const randomFiveStar = this.fiveStarMedia[
        Math.floor(Math.random() * this.fiveStarMedia.length)
      ];
      
      if (randomFiveStar.tmdbId) {
        try {
          const similar = await recommendationsAPI.getSimilar(
            randomFiveStar.tmdbId,
            randomFiveStar.mediaType
          );
          
          this.fiveStarRecommendations = similar.filter(
            item => !this.getLibraryStatus(item.tmdbId)
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
          item => !this.getLibraryStatus(item.tmdbId)
        );
      } catch (err) {
        console.error('Error loading genre recommendations:', err);
      }
    },
    
    async loadActorRecommendations() {
      if (this.topActors.length === 0) return;
      
      const topActor = this.topActors[0];
      
      try {
        const recommendations = await recommendationsAPI.getByActor(topActor.id);
        
        this.actorRecommendations = recommendations.filter(
          item => !this.getLibraryStatus(item.tmdbId)
        );
      } catch (err) {
        console.error('Error loading actor recommendations:', err);
      }
    },
    
    async loadTrendingRecommendations() {
      try {
        const trending = await recommendationsAPI.getTrending('all', 'week');
        
        this.trendingRecommendations = trending.filter(
          item => !this.getLibraryStatus(item.tmdbId)
        );
      } catch (err) {
        console.error('Error loading trending:', err);
      }
    },
    
    async loadHiddenGems() {
      try {
        const recommendations = await recommendationsAPI.getByGenre(18, 'movie');
        
        this.hiddenGems = recommendations
          .filter(item => !this.getLibraryStatus(item.tmdbId))
          .filter(item => item.tmdbRating >= 7.5)
          .slice(0, 12);
      } catch (err) {
        console.error('Error loading hidden gems:', err);
      }
    },
    
    getLibraryStatus(tmdbId) {
      const existing = this.userCollection.find(m => m.tmdbId === tmdbId);
      if (!existing) return null;
      
      if (existing.status === 'watched' && existing.rating) {
        return { type: 'rated', rating: existing.rating };
      } else if (existing.status === 'want_to_watch') {
        return { type: 'watchlist' };
      }
      return { type: 'in-library' };
    },
    
    // FIXED: Fetch full details to get cast
    async quickAddToWatchlist(item) {
      this.loadingStates[item.tmdbId] = 'watchlist';

      try {
        // Fetch full details to get cast
        let fullDetails;
        try {
          fullDetails = item.mediaType === 'movie'
            ? await tmdbAPI.getMovieDetails(item.tmdbId)
            : await tmdbAPI.getTVDetails(item.tmdbId);
        } catch (err) {
          console.log('Could not fetch full details, using recommendation');
          fullDetails = item;
        }

        const mediaData = {
          title: item.title,
          media_type: item.mediaType,
          tmdb_id: item.tmdbId,
          status: 'want_to_watch',
          release_year: item.releaseYear,
          plot: item.plot,
          poster_url: item.posterUrl,
          backdrop_url: item.backdropUrl,
          tmdb_rating: item.tmdbRating,
          cast: fullDetails.cast || []  // FIXED: Include cast
        };

        const created = await mediaAPI.create(mediaData);
        this.userCollection.push(created);
        
        this.showMessage(`Added "${item.title}" to watchlist!`, 'success');

      } catch (err) {
        console.error('Error adding media:', err);
        this.showMessage('Failed to add. Please try again.', 'error');
      } finally {
        delete this.loadingStates[item.tmdbId];
      }
    },

    openRatingDialog(item) {
      this.itemToRate = item;
      this.userRating = null;
      this.userNotes = '';
      this.showRatingDialog = true;
    },

    closeRatingDialog() {
      this.showRatingDialog = false;
      this.itemToRate = null;
      this.userRating = null;
      this.userNotes = '';
    },

    // FIXED: Fetch full details to get cast + Store values before closing
    async saveWithRating() {
      if (!this.itemToRate || !this.userRating) return;

      this.savingRating = true;

      try {
        // Fetch full details to get cast
        let fullDetails;
        try {
          fullDetails = this.itemToRate.mediaType === 'movie'
            ? await tmdbAPI.getMovieDetails(this.itemToRate.tmdbId)
            : await tmdbAPI.getTVDetails(this.itemToRate.tmdbId);
        } catch (err) {
          console.log('Could not fetch full details, using recommendation');
          fullDetails = this.itemToRate;
        }

        // Store values BEFORE closing dialog
        const itemTitle = this.itemToRate.title;
        const itemRating = this.userRating;

        const mediaData = {
          title: itemTitle,
          media_type: this.itemToRate.mediaType,
          tmdb_id: this.itemToRate.tmdbId,
          status: 'watched',
          rating: itemRating,
          notes: this.userNotes || null,
          release_year: this.itemToRate.releaseYear,
          plot: this.itemToRate.plot,
          poster_url: this.itemToRate.posterUrl,
          backdrop_url: this.itemToRate.backdropUrl,
          tmdb_rating: this.itemToRate.tmdbRating,
          cast: fullDetails.cast || []  // FIXED: Include cast
        };

        const created = await mediaAPI.create(mediaData);
        this.userCollection.push(created);

        // Close dialog BEFORE showing message
        this.closeRatingDialog();
        
        // Use stored values
        this.showMessage(`Rated "${itemTitle}" - ${itemRating} stars!`, 'success');

      } catch (err) {
        console.error('Error adding media:', err);
        this.showMessage('Failed to add. Please try again.', 'error');
      } finally {
        this.savingRating = false;
      }
    },

    goToExisting(item) {
      const existing = this.userCollection.find(m => m.tmdbId === item.tmdbId);
      if (existing) {
        this.$router.push(`/media/${existing.mediaId}`);
      }
    },

    showMessage(message, color = 'success') {
      this.snackbarMessage = message;
      this.snackbarColor = color;
      this.showSnackbar = true;
    }
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
</style>
<template>
  <div class="similar-content">
    <!-- Loading -->
    <div v-if="loading" class="mb-6">
      <v-card elevation="2">
        <v-card-title class="text-h6">
          <v-icon start>mdi-lightbulb-on</v-icon>
          Loading Related Content...
        </v-card-title>
        <v-card-text>
          <v-row>
            <v-col v-for="i in 6" :key="i" cols="6" sm="4" md="2">
              <v-skeleton-loader type="image, article" />
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </div>

    <!-- Empty -->
    <v-card v-else-if="relatedItems.length === 0" elevation="2" class="mb-6">
      <v-card-title class="text-h6">
        <v-icon start>mdi-lightbulb-on</v-icon>
        Related Content
      </v-card-title>
      <v-card-text class="text-center py-6">
        <v-icon size="48" color="grey">mdi-filter-off</v-icon>
        <p class="text-body-2 text-medium-emphasis mt-2">
          No related content found
        </p>
      </v-card-text>
    </v-card>

    <!-- Sections -->
    <div v-else>
      <v-card
        v-for="section in sections"
        :key="section.id"
        elevation="2"
        class="mb-4"
      >
        <v-card-title class="text-h6">
          <v-icon start :color="section.color">{{ section.icon }}</v-icon>
          {{ section.title }}
        </v-card-title>

        <v-card-text>
          <div class="carousel-container">
            <v-btn
              icon="mdi-chevron-left"
              size="small"
              variant="elevated"
              class="carousel-nav carousel-nav-left"
              :disabled="scrollPositions[section.id] === 0"
              @click="scrollSection(section.id, -1)"
            />

            <div
              class="carousel-track"
              :ref="el => (carouselRefs[section.id] = el)"
            >
              <div
                v-for="item in section.items"
                :key="item.tmdbId"
                class="carousel-item"
              >
                <media-quick-add-card
                  :item="item"
                  :is-in-collection="!!getLibraryStatus(item.tmdbId)"
                  :collection-info="getLibraryStatus(item.tmdbId)"
                  :loading="loadingStates[item.tmdbId]"
                  :is-mobile="isMobile"
                  @quick-add-watchlist="quickAddToWatchlist"
                  @quick-add-rated="openRatingDialog"
                  @view-existing="goToExisting"
                />
              </div>
            </div>

            <v-btn
              icon="mdi-chevron-right"
              size="small"
              variant="elevated"
              class="carousel-nav carousel-nav-right"
              @click="scrollSection(section.id, 1)"
            />
          </div>
        </v-card-text>
      </v-card>
    </div>

    <!-- Rating Dialog -->
    <v-dialog v-model="showRatingDialog" max-width="500">
      <v-card v-if="itemToRate">
        <v-card-title>Rate {{ itemToRate.title }}</v-card-title>

        <v-card-text>
          <div class="d-flex align-center mb-4">
            <v-avatar size="60" rounded class="mr-3">
              <v-img
                v-if="itemToRate.posterUrl"
                :src="itemToRate.posterUrl"
              />
            </v-avatar>
            <div>
              <p class="text-body-1 font-weight-bold mb-0">
                {{ itemToRate.title }}
              </p>
              <p class="text-caption text-medium-emphasis">
                {{ itemToRate.mediaType === 'movie' ? 'Movie' : 'TV Show' }}
                • {{ itemToRate.releaseYear }}
              </p>
            </div>
          </div>

          <v-rating v-model="userRating" hover size="large" />
          <v-textarea
            v-model="userNotes"
            label="Notes (optional)"
            variant="outlined"
            rows="2"
            class="mt-4"
          />
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="closeRatingDialog">
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            :disabled="!userRating"
            :loading="savingRating"
            @click="saveWithRating"
          >
            Add to Library
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar -->
    <v-snackbar v-model="showSnackbar" :color="snackbarColor" timeout="3000">
      {{ snackbarMessage }}
    </v-snackbar>
  </div>
</template>

<script>
import { recommendationsAPI } from '@/services/recommendations';
import { mediaAPI } from '@/services/api-production';
import MediaQuickAddCard from '@/components/MediaQuickAddCard.vue';

export default {
  name: 'SimilarContent',
  components: { MediaQuickAddCard },

  props: {
    tmdbId: { type: Number, required: true },
    mediaType: {
      type: String,
      required: true,
      validator: v => ['movie', 'tv'].includes(v),
    },
  },

  data() {
    return {
      loading: false,
      relatedItems: [],
      userCollection: [],

      loadingStates: {},
      carouselRefs: {},
      scrollPositions: {
        collection: 0,
        recommended: 0,
        similar: 0,
        spinoff: 0,
      },

      showRatingDialog: false,
      itemToRate: null,
      userRating: null,
      userNotes: '',
      savingRating: false,

      showSnackbar: false,
      snackbarMessage: '',
      snackbarColor: 'success',
    };
  },

  computed: {
    isMobile() {
      return this.$vuetify.display.mobile;
    },

    collectionItems() {
      return this.relatedItems.filter(i => i.relationType === 'collection');
    },
    recommendedItems() {
      return this.relatedItems.filter(i => i.relationType === 'recommended');
    },
    similarItems() {
      return this.relatedItems.filter(i => i.relationType === 'similar');
    },
    spinoffItems() {
      return this.relatedItems.filter(i => i.relationType === 'spinoff');
    },

    sections() {
      return [
        {
          id: 'collection',
          title: 'More in This Series',
          icon: 'mdi-folder-multiple',
          color: 'primary',
          items: this.collectionItems,
        },
        {
          id: 'recommended',
          title: 'You Might Also Like',
          icon: 'mdi-thumb-up',
          color: 'success',
          items: this.recommendedItems,
        },
        {
          id: 'similar',
          title: `Similar ${this.mediaType === 'movie' ? 'Movies' : 'TV Shows'}`,
          icon: 'mdi-movie-filter',
          color: 'info',
          items: this.similarItems,
        },
        {
          id: 'spinoff',
          title: `Related ${this.mediaType === 'movie' ? 'TV Shows' : 'Movies'}`,
          icon: 'mdi-television-play',
          color: 'secondary',
          items: this.spinoffItems,
        },
      ].filter(s => s.items.length);
    },
  },

  created() {
    this.loadRelated();
    this.loadUserCollection();
  },

  methods: {
    async loadRelated() {
      this.loading = true;
      try {
        this.relatedItems = await recommendationsAPI.getRelatedContent(
          this.tmdbId,
          this.mediaType
        );
      } finally {
        this.loading = false;
      }
    },

    async loadUserCollection() {
      this.userCollection = await mediaAPI.getAll();
    },

    getLibraryStatus(tmdbId) {
      const item = this.userCollection.find(m => m.tmdbId === tmdbId);
      if (!item) return null;

      return {
        type: item.status === 'want_to_watch' ? 'watchlist' : 'rated',
        icon: item.status === 'want_to_watch' ? 'mdi-bookmark' : 'mdi-star',
        label:
          item.status === 'want_to_watch' ? 'Watchlist' : 'In Library',
        color: item.status === 'want_to_watch' ? 'info' : 'success',
        mediaId: item.mediaId,
      };
    },

    scrollSection(section, direction) {
      const el = this.carouselRefs[section];
      if (!el) return;

      el.scrollBy({ left: direction * 600, behavior: 'smooth' });
      setTimeout(() => {
        this.scrollPositions[section] = el.scrollLeft;
      }, 300);
    },

    goToExisting(item) {
      const status = this.getLibraryStatus(item.tmdbId);
      if (status) this.$router.push(`/media/${status.mediaId}`);
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
    },

    async saveWithRating() {
      this.savingRating = true;
      try {
        const created = await mediaAPI.create({
          ...this.itemToRate,
          rating: this.userRating,
          notes: this.userNotes,
          status: 'watched',
        });

        this.userCollection.push(created);
        this.showMessage(`Rated "${this.itemToRate.title}"!`);
        this.closeRatingDialog();
      } catch {
        this.showMessage('Failed to save rating', 'error');
      } finally {
        this.savingRating = false;
      }
    },

    async quickAddToWatchlist(item) {
      this.loadingStates[item.tmdbId] = true;
      try {
        const created = await mediaAPI.create({
          ...item,
          status: 'want_to_watch',
        });
        this.userCollection.push(created);
        this.showMessage(`Added ${item.title} to Watchlist`);
      } catch {
        this.showMessage('Failed to add to watchlist', 'error');
      } finally {
        delete this.loadingStates[item.tmdbId];
      }
    },

    showMessage(msg, color = 'success') {
      this.snackbarMessage = msg;
      this.snackbarColor = color;
      this.showSnackbar = true;
    },
  },
};
</script>

<style scoped>
.carousel-container {
  position: relative;
  padding: 0 40px;
}

.carousel-track {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  scroll-behavior: smooth;
  scrollbar-width: none;
}

.carousel-track::-webkit-scrollbar {
  display: none;
}

.carousel-item {
  flex: 0 0 auto;
  width: 160px;
}

.carousel-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 2;
}

.carousel-nav-left {
  left: 0;
}

.carousel-nav-right {
  right: 0;
}
</style>
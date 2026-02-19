<template>
  <div class="similar-content">
    <!-- Loading State -->
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

    <!-- Empty State -->
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

    <!-- Related Content by Type -->
    <div v-else>
      <!-- In Series / Collection -->
      <v-card v-if="collectionItems.length > 0" elevation="2" class="mb-4">
        <v-card-title class="text-h6">
          <v-icon start color="primary">mdi-folder-multiple</v-icon>
          More in This Series
        </v-card-title>
        <v-card-text>
          <div class="carousel-container">
            <v-btn
              icon="mdi-chevron-left"
              size="small"
              variant="elevated"
              class="carousel-nav carousel-nav-left"
              @click="scrollSection('collection', -1)"
              :disabled="scrollPositions.collection === 0"
            />
            
            <div class="carousel-track" :ref="el => carouselRefs.collection = el">
              <div 
                v-for="item in collectionItems" 
                :key="item.tmdbId"
                class="carousel-item"
                @click="handleItemClick(item)"
              >
                <!-- Inline Card -->
                <v-card class="similar-card" hover>
                  <v-img
                    v-if="item.posterUrl"
                    :src="item.posterUrl"
                    aspect-ratio="2/3"
                    cover
                    class="similar-poster"
                  >
                    <div class="poster-overlay">
                      <v-chip 
                        v-if="isInCollection(item.tmdbId)"
                        color="success"
                        size="x-small"
                        class="in-collection-chip"
                      >
                        <v-icon start size="x-small">mdi-check</v-icon>
                        In Library
                      </v-chip>
                    </div>
                  </v-img>
                  <div v-else class="poster-placeholder">
                    <v-icon size="48">mdi-movie-outline</v-icon>
                  </div>
                  
                  <v-card-text class="pa-2">
                    <div class="text-caption font-weight-bold text-truncate" :title="item.title">
                      {{ item.title }}
                    </div>
                    <div class="text-caption text-medium-emphasis">
                      {{ item.releaseYear }}
                      <v-icon v-if="item.tmdbRating" size="x-small" color="amber" class="ml-1">
                        mdi-star
                      </v-icon>
                      {{ item.tmdbRating ? item.tmdbRating.toFixed(1) : '' }}
                    </div>
                  </v-card-text>
                </v-card>
              </div>
            </div>
            
            <v-btn
              icon="mdi-chevron-right"
              size="small"
              variant="elevated"
              class="carousel-nav carousel-nav-right"
              @click="scrollSection('collection', 1)"
            />
          </div>
        </v-card-text>
      </v-card>

      <!-- Recommended (TMDB Algorithm) -->
      <v-card v-if="recommendedItems.length > 0" elevation="2" class="mb-4">
        <v-card-title class="text-h6">
          <v-icon start color="success">mdi-thumb-up</v-icon>
          You Might Also Like
        </v-card-title>
        <v-card-text>
          <div class="carousel-container">
            <v-btn
              icon="mdi-chevron-left"
              size="small"
              variant="elevated"
              class="carousel-nav carousel-nav-left"
              @click="scrollSection('recommended', -1)"
              :disabled="scrollPositions.recommended === 0"
            />
            
            <div class="carousel-track" :ref="el => carouselRefs.recommended = el">
              <div 
                v-for="item in recommendedItems" 
                :key="item.tmdbId"
                class="carousel-item"
                @click="handleItemClick(item)"
              >
                <!-- Inline Card -->
                <v-card class="similar-card" hover>
                  <v-img
                    v-if="item.posterUrl"
                    :src="item.posterUrl"
                    aspect-ratio="2/3"
                    cover
                    class="similar-poster"
                  >
                    <div class="poster-overlay">
                      <v-chip 
                        v-if="isInCollection(item.tmdbId)"
                        color="success"
                        size="x-small"
                        class="in-collection-chip"
                      >
                        <v-icon start size="x-small">mdi-check</v-icon>
                        In Library
                      </v-chip>
                    </div>
                  </v-img>
                  <div v-else class="poster-placeholder">
                    <v-icon size="48">mdi-movie-outline</v-icon>
                  </div>
                  
                  <v-card-text class="pa-2">
                    <div class="text-caption font-weight-bold text-truncate" :title="item.title">
                      {{ item.title }}
                    </div>
                    <div class="text-caption text-medium-emphasis">
                      {{ item.releaseYear }}
                      <v-icon v-if="item.tmdbRating" size="x-small" color="amber" class="ml-1">
                        mdi-star
                      </v-icon>
                      {{ item.tmdbRating ? item.tmdbRating.toFixed(1) : '' }}
                    </div>
                  </v-card-text>
                </v-card>
              </div>
            </div>
            
            <v-btn
              icon="mdi-chevron-right"
              size="small"
              variant="elevated"
              class="carousel-nav carousel-nav-right"
              @click="scrollSection('recommended', 1)"
            />
          </div>
        </v-card-text>
      </v-card>

      <!-- Similar Content -->
      <v-card v-if="similarItems.length > 0" elevation="2" class="mb-4">
        <v-card-title class="text-h6">
          <v-icon start color="info">mdi-movie-filter</v-icon>
          Similar {{ mediaType === 'movie' ? 'Movies' : 'TV Shows' }}
        </v-card-title>
        <v-card-text>
          <div class="carousel-container">
            <v-btn
              icon="mdi-chevron-left"
              size="small"
              variant="elevated"
              class="carousel-nav carousel-nav-left"
              @click="scrollSection('similar', -1)"
              :disabled="scrollPositions.similar === 0"
            />
            
            <div class="carousel-track" :ref="el => carouselRefs.similar = el">
              <div 
                v-for="item in similarItems" 
                :key="item.tmdbId"
                class="carousel-item"
                @click="handleItemClick(item)"
              >
                <!-- Inline Card -->
                <v-card class="similar-card" hover>
                  <v-img
                    v-if="item.posterUrl"
                    :src="item.posterUrl"
                    aspect-ratio="2/3"
                    cover
                    class="similar-poster"
                  >
                    <div class="poster-overlay">
                      <v-chip 
                        v-if="isInCollection(item.tmdbId)"
                        color="success"
                        size="x-small"
                        class="in-collection-chip"
                      >
                        <v-icon start size="x-small">mdi-check</v-icon>
                        In Library
                      </v-chip>
                    </div>
                  </v-img>
                  <div v-else class="poster-placeholder">
                    <v-icon size="48">mdi-movie-outline</v-icon>
                  </div>
                  
                  <v-card-text class="pa-2">
                    <div class="text-caption font-weight-bold text-truncate" :title="item.title">
                      {{ item.title }}
                    </div>
                    <div class="text-caption text-medium-emphasis">
                      {{ item.releaseYear }}
                      <v-icon v-if="item.tmdbRating" size="x-small" color="amber" class="ml-1">
                        mdi-star
                      </v-icon>
                      {{ item.tmdbRating ? item.tmdbRating.toFixed(1) : '' }}
                    </div>
                  </v-card-text>
                </v-card>
              </div>
            </div>
            
            <v-btn
              icon="mdi-chevron-right"
              size="small"
              variant="elevated"
              class="carousel-nav carousel-nav-right"
              @click="scrollSection('similar', 1)"
            />
          </div>
        </v-card-text>
      </v-card>

      <!-- Spinoffs (Related TV/Movies) -->
      <v-card v-if="spinoffItems.length > 0" elevation="2" class="mb-4">
        <v-card-title class="text-h6">
          <v-icon start color="secondary">mdi-television-play</v-icon>
          Related {{ mediaType === 'movie' ? 'TV Shows' : 'Movies' }}
        </v-card-title>
        <v-card-text>
          <div class="carousel-container">
            <v-btn
              icon="mdi-chevron-left"
              size="small"
              variant="elevated"
              class="carousel-nav carousel-nav-left"
              @click="scrollSection('spinoff', -1)"
              :disabled="scrollPositions.spinoff === 0"
            />
            
            <div class="carousel-track" :ref="el => carouselRefs.spinoff = el">
              <div 
                v-for="item in spinoffItems" 
                :key="item.tmdbId"
                class="carousel-item"
                @click="handleItemClick(item)"
              >
                <!-- Inline Card -->
                <v-card class="similar-card" hover>
                  <v-img
                    v-if="item.posterUrl"
                    :src="item.posterUrl"
                    aspect-ratio="2/3"
                    cover
                    class="similar-poster"
                  >
                    <div class="poster-overlay">
                      <v-chip 
                        v-if="isInCollection(item.tmdbId)"
                        color="success"
                        size="x-small"
                        class="in-collection-chip"
                      >
                        <v-icon start size="x-small">mdi-check</v-icon>
                        In Library
                      </v-chip>
                    </div>
                  </v-img>
                  <div v-else class="poster-placeholder">
                    <v-icon size="48">mdi-movie-outline</v-icon>
                  </div>
                  
                  <v-card-text class="pa-2">
                    <div class="text-caption font-weight-bold text-truncate" :title="item.title">
                      {{ item.title }}
                    </div>
                    <div class="text-caption text-medium-emphasis">
                      {{ item.releaseYear }}
                      <v-icon v-if="item.tmdbRating" size="x-small" color="amber" class="ml-1">
                        mdi-star
                      </v-icon>
                      {{ item.tmdbRating ? item.tmdbRating.toFixed(1) : '' }}
                    </div>
                  </v-card-text>
                </v-card>
              </div>
            </div>
            
            <v-btn
              icon="mdi-chevron-right"
              size="small"
              variant="elevated"
              class="carousel-nav carousel-nav-right"
              @click="scrollSection('spinoff', 1)"
            />
          </div>
        </v-card-text>
      </v-card>
    </div>

    <!-- Quick Add Dialog -->
    <v-dialog v-model="showQuickAddDialog" max-width="600">
      <v-card v-if="selectedItem">
        <v-card-title>{{ selectedItem.title }}</v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="4">
              <v-img
                v-if="selectedItem.posterUrl"
                :src="selectedItem.posterUrl"
                aspect-ratio="2/3"
                cover
              />
            </v-col>
            <v-col cols="8">
              <p v-if="selectedItem.plot" class="text-body-2 mb-4">
                {{ selectedItem.plot }}
              </p>
              <v-chip v-if="selectedItem.releaseYear" size="small" class="mr-2">
                {{ selectedItem.releaseYear }}
              </v-chip>
              <v-chip v-if="selectedItem.tmdbRating" size="small">
                <v-icon start size="small">mdi-star</v-icon>
                {{ selectedItem.tmdbRating.toFixed(1) }}
              </v-chip>
              <v-chip v-if="selectedItem.mediaType" size="small" class="ml-2">
                {{ selectedItem.mediaType === 'movie' ? 'Movie' : 'TV Show' }}
              </v-chip>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="showQuickAddDialog = false">
            Cancel
          </v-btn>
          <v-btn color="info" @click="addToWatchlist" :loading="adding">
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

export default {
  name: 'SimilarContent',
  
  components: {},
  
  props: {
    tmdbId: {
      type: Number,
      required: true
    },
    mediaType: {
      type: String,
      required: true,
      validator: (value) => ['movie', 'tv'].includes(value)
    }
  },
  
  data() {
    return {
      loading: false,
      relatedItems: [],
      userCollection: [],
      
      // Carousel refs and scroll positions
      carouselRefs: {
        collection: null,
        recommended: null,
        similar: null,
        spinoff: null
      },
      scrollPositions: {
        collection: 0,
        recommended: 0,
        similar: 0,
        spinoff: 0
      },
      
      // Quick add dialog
      showQuickAddDialog: false,
      selectedItem: null,
      adding: false,
    };
  },
  
  computed: {
    collectionItems() {
      return this.relatedItems.filter(item => item.relationType === 'collection');
    },
    
    recommendedItems() {
      return this.relatedItems.filter(item => item.relationType === 'recommended');
    },
    
    similarItems() {
      return this.relatedItems.filter(item => item.relationType === 'similar');
    },
    
    spinoffItems() {
      return this.relatedItems.filter(item => item.relationType === 'spinoff');
    }
  },
  
  created() {
    this.loadRelated();
    this.loadUserCollection();
  },
  
  methods: {
    async loadRelated() {
      this.loading = true;
      try {
        // NEW: Use comprehensive method instead
        this.relatedItems = await recommendationsAPI.getRelatedContent(this.tmdbId, this.mediaType);
        console.log('Related content loaded:', this.relatedItems.length);
        console.log('By type:', {
          collection: this.collectionItems.length,
          recommended: this.recommendedItems.length,
          similar: this.similarItems.length,
          spinoff: this.spinoffItems.length
        });
      } catch (err) {
        console.error('Error loading related content:', err);
      } finally {
        this.loading = false;
      }
    },
    
    async loadUserCollection() {
      try {
        this.userCollection = await mediaAPI.getAll();
      } catch (err) {
        console.error('Error loading collection:', err);
      }
    },
    
    isInCollection(tmdbId) {
      return this.userCollection.some(m => m.tmdbId === tmdbId);
    },
    
    scrollSection(section, direction) {
      const track = this.carouselRefs[section];
      if (!track) return;
      
      const scrollAmount = 300 * direction;
      
      track.scrollBy({ 
        left: scrollAmount, 
        behavior: 'smooth' 
      });
      
      // Update scroll position after animation
      setTimeout(() => {
        this.scrollPositions[section] = track.scrollLeft;
      }, 300);
    },
    
    handleItemClick(item) {
      // Check if already in collection
      if (this.isInCollection(item.tmdbId)) {
        // Navigate to existing media
        const existing = this.userCollection.find(m => m.tmdbId === item.tmdbId);
        this.$router.push(`/media/${existing.mediaId}`);
      } else {
        // Show quick add dialog
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
        await this.loadUserCollection();
        
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
.similar-content {
  margin-top: 32px;
}

.carousel-container {
  position: relative;
  padding: 0 40px;
}

.carousel-track {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  scroll-behavior: smooth;
  padding: 8px 0;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE/Edge */
}

.carousel-track::-webkit-scrollbar {
  display: none; /* Chrome/Safari */
}

.carousel-item {
  flex: 0 0 auto;
  width: 150px;
}

.carousel-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 2;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.carousel-nav-left {
  left: 0;
}

.carousel-nav-right {
  right: 0;
}

.similar-card {
  cursor: pointer;
  transition: transform 0.2s ease;
  height: 100%;
}

.similar-card:hover {
  transform: scale(1.05);
}

.similar-poster {
  position: relative;
}

.poster-overlay {
  position: absolute;
  top: 8px;
  right: 8px;
}

.in-collection-chip {
  backdrop-filter: blur(8px);
}

.poster-placeholder {
  aspect-ratio: 2/3;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.1);
}
</style>
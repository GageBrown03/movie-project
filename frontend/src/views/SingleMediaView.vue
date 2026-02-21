<template>
  <div class="single-media">
    <!-- Loading State -->
    <v-row v-if="loading" justify="center" class="my-12">
      <v-progress-circular indeterminate size="64" color="primary" />
    </v-row>

    <!-- Error State -->
    <v-alert v-else-if="error" type="error" variant="tonal" class="mb-4">
      {{ error }}
      <template v-slot:append>
        <v-btn to="/media" variant="text">Back to Collection</v-btn>
      </template>
    </v-alert>

    <!-- Media Content -->
    <div v-else-if="media">
      <!-- DESKTOP/TABLET: Hero Backdrop -->
      <div class="hero-section d-none d-md-block">
        <v-img
          v-if="media.backdropUrl"
          :src="media.backdropUrl"
          height="350"
          cover
          gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.8)"
          class="hero-backdrop"
        >
          <div class="hero-content">
            <v-container>
              <v-btn
                icon="mdi-arrow-left"
                variant="text"
                color="white"
                size="small"
                @click="$router.push('/media')"
                class="back-button"
              />
              
              <v-chip 
                :color="media.mediaType === 'movie' ? '#1976D2' : '#7B1FA2'" 
                size="small" 
                class="mb-2 text-white font-weight-black"
                variant="flat"
                label
              >
                {{ media.mediaType === 'movie' ? 'MOVIE' : 'TV' }}
              </v-chip>
              
              <h1 class="text-h3 text-white mb-2">{{ media.title }}</h1>
              
              <div class="hero-meta">
                <v-chip v-if="media.releaseYear" size="small" color="white" variant="flat" class="mr-2">
                  {{ media.releaseYear }}
                </v-chip>
                
                <v-chip v-if="media.mediaType === 'movie' && media.runtime" size="small" color="white" variant="flat" class="mr-2">
                  {{ media.runtime }} min
                </v-chip>
                
                <v-chip v-if="media.mediaType === 'tv' && media.numberOfSeasons" size="small" color="white" variant="flat" class="mr-2">
                  {{ media.numberOfSeasons }} {{ media.numberOfSeasons === 1 ? 'Season' : 'Seasons' }}
                </v-chip>
                
                <v-chip v-if="media.director" size="small" color="white" variant="flat">
                  {{ media.mediaType === 'tv' ? media.director : `Dir: ${media.director}` }}
                </v-chip>
              </div>
            </v-container>
          </div>
        </v-img>
        
        <div v-else class="hero-fallback">
          <v-container>
            <v-btn
              icon="mdi-arrow-left"
              variant="text"
              size="small"
              @click="$router.push('/media')"
              class="back-button mb-4"
            />
            
            <v-chip 
              :color="media.mediaType === 'movie' ? '#1976D2' : '#7B1FA2'" 
              size="small" 
              class="mb-2 text-white font-weight-black"
              variant="flat"
              label
            >
              {{ media.mediaType === 'movie' ? 'MOVIE' : 'TV' }}
            </v-chip>
            
            <h1 class="text-h3 mb-2">{{ media.title }}</h1>
            
            <div class="hero-meta">
              <v-chip v-if="media.releaseYear" size="small" class="mr-2">
                {{ media.releaseYear }}
              </v-chip>
              
              <v-chip v-if="media.mediaType === 'movie' && media.runtime" size="small" class="mr-2">
                {{ media.runtime }} min
              </v-chip>
              
              <v-chip v-if="media.mediaType === 'tv' && media.numberOfSeasons" size="small" class="mr-2">
                {{ media.numberOfSeasons }} {{ media.numberOfSeasons === 1 ? 'Season' : 'Seasons' }}
              </v-chip>
              
              <v-chip v-if="media.director" size="small">
                {{ media.director }}
              </v-chip>
            </div>
          </v-container>
        </div>
      </div>

      <!-- MOBILE: Centered Hero -->
      <div class="mobile-hero d-md-none">
        <v-container class="py-4">
          <!-- Back Button -->
          <v-btn
            icon="mdi-arrow-left"
            variant="text"
            size="small"
            color="white"
            @click="$router.push('/media')"
            class="mb-3"
          />
          
          <!-- Centered Content -->
          <div class="text-center">
            <!-- Type Badge -->
            <v-chip 
              :color="media.mediaType === 'movie' ? '#1976D2' : '#7B1FA2'" 
              size="small" 
              class="mb-3 text-white font-weight-black"
              variant="flat"
              label
            >
              {{ media.mediaType === 'movie' ? 'MOVIE' : 'TV' }}
            </v-chip>
            
            <!-- Title -->
            <h1 class="text-h5 mb-2 text-white">{{ media.title }}</h1>
            
            <!-- Meta Info - Centered -->
            <div class="mobile-meta mb-3">
              <span v-if="media.releaseYear" class="text-white">{{ media.releaseYear }}</span>
              <span v-if="media.mediaType === 'movie' && media.runtime" class="text-white">
                <v-icon size="x-small" color="white" class="mx-1">mdi-circle-small</v-icon>
                {{ media.runtime }} min
              </span>
              <span v-if="media.mediaType === 'tv' && media.numberOfSeasons" class="text-white">
                <v-icon size="x-small" color="white" class="mx-1">mdi-circle-small</v-icon>
                {{ media.numberOfSeasons }} {{ media.numberOfSeasons === 1 ? 'Season' : 'Seasons' }}
              </span>
            </div>
            
            <div v-if="media.director" class="text-caption text-white mb-4 opacity-90">
              {{ media.mediaType === 'tv' ? media.director : `Directed by ${media.director}` }}
            </div>
            
            <!-- Compact Poster -->
            <div class="mobile-poster-centered mx-auto mb-4">
              <v-img
                v-if="media.posterUrl"
                :src="media.posterUrl"
                aspect-ratio="2/3"
                width="140"
                cover
                class="rounded elevation-8"
              />
              <div v-else class="mobile-poster-placeholder">
                <v-icon size="48" color="white">mdi-movie-outline</v-icon>
              </div>
            </div>
            
            <!-- Compact Status & Rating Row -->
            <div class="mobile-status-row mb-3">
              <v-chip 
                :color="statusColor" 
                variant="flat"
                size="small"
                class="mr-2"
              >
                <v-icon start size="x-small">
                  {{ media.status === 'want_to_watch' ? 'mdi-bookmark' : 'mdi-check-circle' }}
                </v-icon>
                {{ statusLabel }}
              </v-chip>
              
              <v-chip
                v-if="media.rating"
                color="amber"
                variant="flat"
                size="small"
              >
                <v-icon start size="x-small">mdi-star</v-icon>
                {{ media.rating }}/5
              </v-chip>
            </div>
            
            <!-- Mobile Quick Actions -->
            <div class="mobile-actions-centered">
              <v-btn
                v-if="media.status === 'want_to_watch'"
                color="success"
                size="small"
                block
                @click="quickMarkAsWatched"
                prepend-icon="mdi-check"
                class="mb-2"
              >
                Mark Watched
              </v-btn>
              
              <div class="d-flex gap-2 justify-center">
                <v-btn
                  size="small"
                  variant="tonal"
                  @click="editMode = true"
                  prepend-icon="mdi-pencil"
                  class="flex-grow-1"
                >
                  Edit
                </v-btn>
                <v-btn
                  size="small"
                  variant="tonal"
                  color="error"
                  @click="deleteDialog = true"
                  icon="mdi-delete"
                />
              </div>
            </div>
          </div>
        </v-container>
      </div>

      <!-- Main Content -->
      <v-container class="mt-6">
        <v-row>
          <!-- DESKTOP/TABLET: Left Column with Poster + Actions -->
          <v-col cols="12" md="4" class="d-none d-md-block">
            <v-card elevation="4" class="sticky-poster">
              <v-img
                v-if="media.posterUrl"
                :src="media.posterUrl"
                aspect-ratio="2/3"
                cover
              />
              <div v-else class="poster-placeholder">
                <v-icon size="120" color="grey">mdi-movie-outline</v-icon>
              </div>

              <v-card-actions class="flex-column align-stretch pa-4">
                <template v-if="!editMode">
                  <v-btn
                    v-if="media.status === 'want_to_watch'"
                    color="success"
                    size="large"
                    block
                    @click="quickMarkAsWatched"
                    prepend-icon="mdi-check-circle"
                    class="mb-2"
                  >
                    Mark as Watched
                  </v-btn>
                  
                  <v-btn
                    variant="tonal"
                    size="large"
                    block
                    @click="editMode = true"
                    prepend-icon="mdi-pencil"
                    class="mb-2"
                  >
                    Edit Details
                  </v-btn>
                  
                  <v-btn
                    variant="tonal"
                    color="error"
                    size="large"
                    block
                    @click="deleteDialog = true"
                    prepend-icon="mdi-delete"
                  >
                    Delete
                  </v-btn>
                </template>
                
                <template v-else>
                  <v-btn
                    color="primary"
                    size="large"
                    block
                    @click="saveChanges"
                    :loading="saving"
                    prepend-icon="mdi-content-save"
                    class="mb-2"
                  >
                    Save Changes
                  </v-btn>
                  
                  <v-btn
                    variant="outlined"
                    size="large"
                    block
                    @click="cancelEdit"
                  >
                    Cancel
                  </v-btn>
                </template>
              </v-card-actions>
            </v-card>
          </v-col>

          <!-- Right Column: Details -->
          <v-col cols="12" md="8">
            <!-- VIEW MODE -->
            <div v-if="!editMode">
              <!-- Compact Status & Rating Bar (Desktop/Tablet only) -->
              <div class="d-none d-md-flex align-center gap-3 mb-4 pa-3 rounded" style="background: rgba(var(--v-theme-surface-variant), 0.5);">
                <v-chip 
                  :color="statusColor" 
                  variant="flat"
                  size="small"
                  prepend-icon="mdi-bookmark"
                >
                  {{ statusLabel }}
                </v-chip>
                
                <v-rating
                  v-if="media.rating"
                  :model-value="media.rating"
                  readonly
                  density="compact"
                  color="amber"
                  size="small"
                />
                <span v-if="media.rating" class="text-caption">Your Rating</span>
                
                <v-spacer />
                
                <v-chip
                  v-if="media.tmdbRating"
                  size="small"
                  variant="tonal"
                  prepend-icon="mdi-star"
                >
                  {{ media.tmdbRating.toFixed(1) }}/10 TMDB
                </v-chip>
              </div>

              <!-- Cast -->
              <v-card elevation="2" class="mb-4" v-if="media.cast && media.cast.length">
                <v-card-title class="text-h6">
                  <v-icon class="mr-2">mdi-account-group</v-icon>
                  Cast
                </v-card-title>
                <v-card-text>
                  <div class="cast-grid">
                    <div
                      v-for="actor in media.cast.slice(0, 6)"
                      :key="actor.actorId"
                      class="cast-member cast-member--clickable"
                      @click="openActorPanel(actor)"
                      :title="`See all of ${actor.name}'s work`"
                    >
                      <v-avatar size="64" class="mb-2 cast-avatar">
                        <v-img v-if="actor.profileUrl" :src="actor.profileUrl" />
                        <v-icon v-else size="36">mdi-account</v-icon>
                      </v-avatar>
                      <div class="text-caption font-weight-bold text-center">{{ actor.name }}</div>
                      <div class="text-caption text-medium-emphasis text-center">{{ actor.character }}</div>
                      <div class="cast-member__hint text-caption text-primary text-center mt-1">
                        <v-icon size="10">mdi-play-circle-outline</v-icon> Filmography
                      </div>
                    </div>
                  </div>
                </v-card-text>
              </v-card>

              <!-- Plot (Now below cast) -->
              <v-card elevation="2" class="mb-4" v-if="media.plot">
                <v-card-title class="text-h6">
                  <v-icon class="mr-2">mdi-text</v-icon>
                  Plot
                </v-card-title>
                <v-card-text>
                  <p class="text-body-2">{{ media.plot }}</p>
                </v-card-text>
              </v-card>

              <!-- Details Grid -->
              <v-card elevation="2" class="mb-4">
                <v-card-title class="text-h6">
                  <v-icon class="mr-2">mdi-information</v-icon>
                  Details
                </v-card-title>
                <v-card-text>
                  <v-row>
                    <v-col cols="12" sm="6" v-if="media.releaseYear">
                      <div class="detail-item">
                        <div class="text-caption text-medium-emphasis">Release Year</div>
                        <div class="text-body-1 font-weight-medium">{{ media.releaseYear }}</div>
                      </div>
                    </v-col>
                    
                    <v-col cols="12" sm="6" v-if="media.genres && media.genres.length">
                      <div class="detail-item">
                        <div class="text-caption text-medium-emphasis mb-1">Genres</div>
                        <div class="d-flex flex-wrap gap-1">
                          <v-chip 
                            v-for="genre in media.genres" 
                            :key="genre" 
                            size="small"
                            variant="tonal"
                          >
                            {{ genre }}
                          </v-chip>
                        </div>
                      </div>
                    </v-col>
                    
                    <v-col cols="12" sm="6" v-if="media.mediaType === 'movie' && media.runtime">
                      <div class="detail-item">
                        <div class="text-caption text-medium-emphasis">Runtime</div>
                        <div class="text-body-1 font-weight-medium">{{ media.runtime }} minutes</div>
                      </div>
                    </v-col>
                    
                    <v-col cols="12" sm="6" v-if="media.mediaType === 'tv' && media.numberOfSeasons">
                      <div class="detail-item">
                        <div class="text-caption text-medium-emphasis">Seasons</div>
                        <div class="text-body-1 font-weight-medium">{{ media.numberOfSeasons }}</div>
                      </div>
                    </v-col>
                    
                    <v-col cols="12" sm="6" v-if="media.mediaType === 'tv' && media.numberOfEpisodes">
                      <div class="detail-item">
                        <div class="text-caption text-medium-emphasis">Episodes</div>
                        <div class="text-body-1 font-weight-medium">{{ media.numberOfEpisodes }}</div>
                      </div>
                    </v-col>
                    
                    <v-col cols="12" sm="6" v-if="media.director">
                      <div class="detail-item">
                        <div class="text-caption text-medium-emphasis">
                          {{ media.mediaType === 'tv' ? 'Creator' : 'Director' }}
                        </div>
                        <div class="text-body-1 font-weight-medium">{{ media.director }}</div>
                      </div>
                    </v-col>
                    
                    <v-col cols="12" sm="6" v-if="media.tmdbRating">
                      <div class="detail-item">
                        <div class="text-caption text-medium-emphasis">TMDB Rating</div>
                        <div class="text-body-1 font-weight-medium">
                          <v-icon size="small" color="amber" class="mr-1">mdi-star</v-icon>
                          {{ media.tmdbRating.toFixed(1) }}/10
                        </div>
                      </div>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>

              <!-- Personal Notes -->
              <v-card elevation="2" class="mb-4" v-if="media.notes">
                <v-card-title class="text-h6">Your Notes</v-card-title>
                <v-card-text>
                  <p class="text-body-1">{{ media.notes }}</p>
                </v-card-text>
              </v-card>
            </div>

            <!-- EDIT MODE -->
            <div v-else>
              <v-card elevation="2" class="mb-4">
                <v-card-title class="text-h6">Edit Details</v-card-title>
                <v-card-text>
                  <v-select
                    v-model="editData.status"
                    :items="statusOptions"
                    label="Status"
                    variant="outlined"
                    class="mb-4"
                  />
                  
                  <div class="mb-4">
                    <div class="text-body-2 mb-2">Your Rating</div>
                    <v-rating
                      v-model="editData.rating"
                      color="amber"
                      hover
                    />
                  </div>
                  
                  <v-textarea
                    v-model="editData.notes"
                    label="Personal Notes"
                    variant="outlined"
                    rows="4"
                    placeholder="What did you think?"
                  />
                </v-card-text>
              </v-card>
              
              <!-- Mobile Edit Actions -->
              <v-card elevation="2" class="d-md-none">
                <v-card-actions class="pa-4">
                  <v-btn
                    color="primary"
                    size="large"
                    block
                    @click="saveChanges"
                    :loading="saving"
                    prepend-icon="mdi-content-save"
                    class="mb-2"
                  >
                    Save Changes
                  </v-btn>
                  
                  <v-btn
                    variant="outlined"
                    size="large"
                    block
                    @click="cancelEdit"
                  >
                    Cancel
                  </v-btn>
                </v-card-actions>
              </v-card>
            </div>
          </v-col>
        </v-row>
        
        <!-- Similar Content (Your Carousel Implementation) -->
        <similar-content 
          v-if="media && media.tmdbId"
          :tmdb-id="media.tmdbId"
          :media-type="media.mediaType"
        />
      </v-container>
    </div>

    <!-- ═══════════════════════════════════════
         ACTOR FILMOGRAPHY DRAWER
    ═══════════════════════════════════════ -->
    <v-navigation-drawer
      v-model="actorPanel.open"
      location="right"
      temporary
      width="420"
      class="actor-drawer"
    >
      <!-- Header -->
      <div class="actor-drawer__header">
        <v-btn icon="mdi-close" variant="text" size="small" @click="closeActorPanel" class="actor-drawer__close" />
        <div class="d-flex align-center gap-4 px-4 pb-4 pt-2">
          <v-avatar size="72" class="actor-drawer__avatar">
            <v-img v-if="actorPanel.actor?.profileUrl" :src="actorPanel.actor.profileUrl" />
            <v-icon v-else size="40">mdi-account</v-icon>
          </v-avatar>
          <div>
            <h2 class="text-h6 font-weight-black">{{ actorPanel.actor?.name }}</h2>
            <p class="text-caption text-medium-emphasis mb-0">
              as <em>{{ actorPanel.actor?.character }}</em>
            </p>
            <p class="text-caption text-medium-emphasis mt-1">
              {{ actorPanel.credits.length }} title{{ actorPanel.credits.length !== 1 ? 's' : '' }} found
            </p>
          </div>
        </div>

        <!-- Filter tabs -->
        <v-tabs
          v-model="actorPanel.filterTab"
          density="compact"
          class="px-4"
          color="primary"
        >
          <v-tab value="all">All</v-tab>
          <v-tab value="movie">Movies</v-tab>
          <v-tab value="tv">TV</v-tab>
          <v-tab value="inLibrary">In Library</v-tab>
        </v-tabs>
        <v-divider />
      </div>

      <!-- Loading -->
      <div v-if="actorPanel.loading" class="d-flex flex-column align-center justify-center pa-8">
        <v-progress-circular indeterminate color="primary" size="48" />
        <p class="text-body-2 text-medium-emphasis mt-4">Loading filmography…</p>
      </div>

      <!-- Error -->
      <div v-else-if="actorPanel.error" class="pa-6 text-center">
        <v-icon size="48" color="error" class="mb-3">mdi-alert-circle-outline</v-icon>
        <p class="text-body-2 text-medium-emphasis">{{ actorPanel.error }}</p>
        <v-btn size="small" variant="tonal" class="mt-3" @click="fetchActorFilmography(actorPanel.actor)">
          Retry
        </v-btn>
      </div>

      <!-- Empty -->
      <div v-else-if="actorPanel.credits.length === 0 && !actorPanel.loading" class="pa-6 text-center">
        <v-icon size="48" color="grey" class="mb-3">mdi-film-off</v-icon>
        <p class="text-body-2 text-medium-emphasis">No credits found</p>
      </div>

      <!-- Credits grid -->
      <div v-else class="actor-drawer__grid pa-3">
        <div
          v-for="credit in filteredCredits"
          :key="`${credit.mediaType}-${credit.tmdbId}`"
          class="actor-credit"
          :class="{ 'actor-credit--in-library': getLibraryEntry(credit.tmdbId) }"
          @click="handleCreditClick(credit)"
          :title="credit.title"
        >
          <!-- Poster -->
          <div class="actor-credit__poster-wrap">
            <v-img
              v-if="credit.posterUrl"
              :src="credit.posterUrl"
              aspect-ratio="0.667"
              cover
              class="actor-credit__poster"
            />
            <div v-else class="actor-credit__poster actor-credit__poster--empty">
              <v-icon color="grey" size="28">mdi-movie-outline</v-icon>
            </div>

            <!-- In-library badge -->
            <div v-if="getLibraryEntry(credit.tmdbId)" class="actor-credit__badge">
              <v-icon
                size="16"
                :color="getLibraryEntry(credit.tmdbId).status === 'want_to_watch' ? 'info' : 'success'"
              >
                {{ getLibraryEntry(credit.tmdbId).status === 'want_to_watch' ? 'mdi-bookmark' : 'mdi-star' }}
              </v-icon>
            </div>

            <!-- Media type pill -->
            <div class="actor-credit__type">
              {{ credit.mediaType === 'movie' ? 'M' : 'TV' }}
            </div>
          </div>

          <!-- Info -->
          <div class="actor-credit__info">
            <p class="actor-credit__title">{{ credit.title }}</p>
            <p class="actor-credit__year">{{ credit.releaseYear || '—' }}</p>
          </div>
        </div>

        <p v-if="filteredCredits.length === 0" class="text-caption text-medium-emphasis text-center pa-4 col-span-all">
          No {{ actorPanel.filterTab === 'inLibrary' ? 'library' : actorPanel.filterTab }} titles found.
        </p>
      </div>
    </v-navigation-drawer>

    <!-- Quick Mark as Watched Dialog -->
    <v-dialog v-model="showQuickWatchDialog" max-width="500">
      <v-card>
        <v-card-title>Mark as Watched</v-card-title>
        <v-card-text>
          <div class="mb-4">
            <div class="text-body-2 mb-2">Rate {{ media?.title }}</div>
            <v-rating
              v-model="quickWatchRating"
              color="amber"
              hover
              size="large"
            />
          </div>
          
          <v-textarea
            v-model="quickWatchNotes"
            label="Notes (optional)"
            variant="outlined"
            rows="3"
            placeholder="What did you think?"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="showQuickWatchDialog = false">
            Cancel
          </v-btn>
          <v-btn 
            color="success" 
            @click="confirmQuickWatch"
            :loading="saving"
          >
            Mark as Watched
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation -->
    <delete-confirm-dialog
      v-model="deleteDialog"
      :item-name="media?.title"
      @confirm="handleDelete"
    />
  </div>
</template>

<script>
import { mediaAPI } from '@/services/api-production';
import DeleteConfirmDialog from '@/components/DeleteConfirmDialog.vue';
import SimilarContent from '@/components/SimilarContent.vue';

export default {
  name: 'SingleMediaView',
  
  components: {
    DeleteConfirmDialog,
    SimilarContent
  },
  
  data() {
    return {
      loading: false,
      error: null,
      media: null,
      editMode: false,
      editData: {
        status: null,
        rating: null,
        notes: ''
      },
      saving: false,
      deleteDialog: false,
      showQuickWatchDialog: false,
      quickWatchRating: null,
      quickWatchNotes: '',
      statusOptions: [
        { title: 'Want to Watch', value: 'want_to_watch' },
        { title: 'Watched', value: 'watched' }
      ],

      // Actor filmography panel
      actorPanel: {
        open: false,
        actor: null,
        loading: false,
        error: null,
        credits: [],
        filterTab: 'all',
      },
      userCollection: [],  // For in-library detection in actor panel
    };
  },
  
  computed: {
    statusLabel() {
      if (!this.media) return '';
      return this.media.status === 'want_to_watch' ? 'Watchlist' : 'Watched';
    },
    statusColor() {
      if (!this.media) return 'primary';
      return this.media.status === 'want_to_watch' ? 'info' : 'success';
    },

    filteredCredits() {
      const { credits, filterTab } = this.actorPanel;
      if (filterTab === 'all') return credits;
      if (filterTab === 'movie') return credits.filter(c => c.mediaType === 'movie');
      if (filterTab === 'tv') return credits.filter(c => c.mediaType === 'tv');
      if (filterTab === 'inLibrary') return credits.filter(c => !!this.getLibraryEntry(c.tmdbId));
      return credits;
    },
  },
  
  created() {
    this.loadMedia();
    this.loadUserCollection();
  },

  watch: {
    // Fix: Vue Router reuses the component instance when navigating between
    // /media/123 → /media/456 (same route, different param). Without this
    // watch, created() never re-fires and the page stays frozen.
    '$route.params.mediaId'(newId, oldId) {
      if (newId && newId !== oldId) {
        this.loadMedia();
        this.closeActorPanel();
      }
    },

    'actorPanel.open'(val) {
      if (!val) this.closeActorPanel();
    },

    editMode(newVal) {
      if (newVal && this.media) {
        this.editData = {
          status: this.media.status,
          rating: this.media.rating,
          notes: this.media.notes || ''
        };
      }
    },
  },

  methods: {
    async loadMedia() {
      this.loading = true;
      this.error = null;
      try {
        const id = this.$route.params.mediaId;
        this.media = await mediaAPI.getOne(id);
      } catch (err) {
        console.error('Error loading media:', err);
        this.error = 'Failed to load media. Please try again.';
      } finally {
        this.loading = false;
      }
    },

    async loadUserCollection() {
      try {
        this.userCollection = await mediaAPI.getAll();
      } catch (err) {
        console.warn('Could not load user collection for actor panel:', err);
      }
    },

    // ── Actor panel ────────────────────────────────────────
    async openActorPanel(actor) {
      this.actorPanel.actor = actor;
      this.actorPanel.open = true;
      this.actorPanel.filterTab = 'all';
      this.actorPanel.credits = [];
      this.actorPanel.error = null;
      await this.fetchActorFilmography(actor);
    },

    closeActorPanel() {
      this.actorPanel.open = false;
      this.actorPanel.actor = null;
      this.actorPanel.credits = [];
      this.actorPanel.error = null;
      this.actorPanel.loading = false;
    },

    async fetchActorFilmography(actor) {
      if (!actor?.tmdbActorId) {
        this.actorPanel.error = 'No TMDB ID available for this actor.';
        return;
      }

      this.actorPanel.loading = true;
      this.actorPanel.error = null;

      try {
        const { recommendationsAPI } = await import('@/services/recommendations');
        const credits = await recommendationsAPI.getByActor(actor.tmdbActorId);

        // Sort by year descending (most recent first), nulls last
        this.actorPanel.credits = credits.sort((a, b) => {
          if (!a.releaseYear) return 1;
          if (!b.releaseYear) return -1;
          return b.releaseYear - a.releaseYear;
        });
      } catch (err) {
        console.error('Error fetching filmography:', err);
        this.actorPanel.error = 'Could not load filmography. Please try again.';
      } finally {
        this.actorPanel.loading = false;
      }
    },

    getLibraryEntry(tmdbId) {
      return this.userCollection.find(m => Number(m.tmdbId) === Number(tmdbId)) || null;
    },

    handleCreditClick(credit) {
      const existing = this.getLibraryEntry(credit.tmdbId);
      if (existing) {
        // Navigate to it — the route watch will handle the reload
        this.closeActorPanel();
        this.$router.push(`/media/${existing.mediaId}`);
      }
      // If not in library, do nothing — no add flow here,
      // user can use SimilarContent or DiscoverView for that
    },

    // ── Existing methods ────────────────────────────────────
    
    quickMarkAsWatched() {
      this.quickWatchRating = null;
      this.quickWatchNotes = '';
      this.showQuickWatchDialog = true;
    },
    
    async confirmQuickWatch() {
      this.saving = true;
      
      try {
        const updateData = {
          status: 'watched',
          rating: this.quickWatchRating,
          notes: this.quickWatchNotes || this.media.notes
        };
        
        const updated = await mediaAPI.update(this.media.mediaId, updateData);
        this.media = updated;
        this.showQuickWatchDialog = false;
      } catch (err) {
        console.error('Error updating media:', err);
        alert('Failed to update. Please try again.');
      } finally {
        this.saving = false;
      }
    },
    
    cancelEdit() {
      this.editMode = false;
      this.editData = {
        status: null,
        rating: null,
        notes: ''
      };
    },
    
    async saveChanges() {
      this.saving = true;
      
      try {
        const updateData = {
          status: this.editData.status,
          rating: this.editData.rating,
          notes: this.editData.notes
        };
        
        const updated = await mediaAPI.update(this.media.mediaId, updateData);
        this.media = updated;
        this.editMode = false;
      } catch (err) {
        console.error('Error saving changes:', err);
        alert('Failed to save changes. Please try again.');
      } finally {
        this.saving = false;
      }
    },
    
    async handleDelete() {
      try {
        await mediaAPI.delete(this.media.mediaId);
        this.$router.push('/media');
      } catch (err) {
        console.error('Error deleting media:', err);
        alert('Failed to delete. Please try again.');
      }
    }
  },
};
</script>

<style scoped>
.single-media {
  min-height: 100vh;
}

.hero-section {
  margin: -24px -24px 0 -24px;
}

.hero-backdrop {
  position: relative;
}

.hero-content {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 40px 0;
}

.hero-fallback {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 60px 0 40px 0;
  color: white;
}

.back-button {
  margin-bottom: 16px;
}

.hero-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}

.sticky-poster {
  position: sticky;
  top: 24px;
}

.poster-placeholder {
  aspect-ratio: 2/3;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.detail-item {
  margin-bottom: 8px;
}

.cast-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 16px;
}

.cast-member {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* MOBILE STYLES */
.mobile-hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  margin: -16px -16px 0 -16px;
  min-height: 400px;
  display: flex;
  align-items: center;
}

.mobile-meta {
  font-size: 0.875rem;
  line-height: 1.5;
}

.mobile-poster-centered {
  max-width: 140px;
}

.mobile-poster-placeholder {
  width: 140px;
  aspect-ratio: 2/3;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
}

.mobile-status-row {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.mobile-actions-centered {
  max-width: 300px;
  margin: 0 auto;
  width: 100%;
}

.mobile-actions-centered .gap-2 {
  gap: 8px;
}

/* RESPONSIVE */
@media (max-width: 960px) {
  .sticky-poster {
    position: static;
  }
  
  .hero-section {
    margin: -16px -16px 0 -16px;
  }
}

/* ── Clickable cast members ─────────────────────────── */
.cast-member--clickable {
  cursor: pointer;
  border-radius: 12px;
  padding: 8px 4px;
  transition: background 0.18s ease, transform 0.18s ease;
}

.cast-member--clickable:hover {
  background: rgba(var(--v-theme-primary), 0.07);
  transform: translateY(-3px);
}

.cast-member--clickable:hover .cast-avatar {
  box-shadow: 0 0 0 2px rgb(var(--v-theme-primary));
}

.cast-avatar {
  transition: box-shadow 0.18s ease;
}

.cast-member__hint {
  opacity: 0;
  transition: opacity 0.18s ease;
  font-size: 0.65rem;
  letter-spacing: 0.03em;
}

.cast-member--clickable:hover .cast-member__hint {
  opacity: 1;
}

/* ── Actor drawer ───────────────────────────────────── */
.actor-drawer__header {
  position: sticky;
  top: 0;
  z-index: 10;
  background: rgb(var(--v-theme-surface));
  padding-top: 12px;
  border-bottom: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}

.actor-drawer__close {
  position: absolute;
  top: 8px;
  right: 8px;
}

.actor-drawer__avatar {
  border: 2px solid rgba(var(--v-theme-primary), 0.3);
  flex-shrink: 0;
}

.actor-drawer__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  padding-top: 12px;
}

.col-span-all {
  grid-column: 1 / -1;
}

/* Individual credit card */
.actor-credit {
  cursor: default;
  border-radius: 8px;
  overflow: hidden;
  background: rgba(var(--v-theme-surface-variant), 0.3);
  transition: transform 0.18s ease, box-shadow 0.18s ease;
  position: relative;
}

.actor-credit--in-library {
  cursor: pointer;
}

.actor-credit--in-library:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
}

.actor-credit__poster-wrap {
  position: relative;
  aspect-ratio: 2 / 3;
}

.actor-credit__poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.actor-credit__poster--empty {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(var(--v-theme-on-surface), 0.05);
}

.actor-credit__badge {
  position: absolute;
  top: 5px;
  right: 5px;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.actor-credit__type {
  position: absolute;
  bottom: 4px;
  left: 4px;
  background: rgba(0, 0, 0, 0.65);
  color: #fff;
  font-size: 0.55rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  padding: 1px 4px;
  border-radius: 3px;
  line-height: 1.4;
}

.actor-credit__info {
  padding: 5px 6px 6px;
}

.actor-credit__title {
  font-size: 0.7rem;
  font-weight: 600;
  line-height: 1.25;
  margin: 0 0 2px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.actor-credit__year {
  font-size: 0.62rem;
  color: rgba(var(--v-theme-on-surface), 0.5);
  margin: 0;
}


</style>
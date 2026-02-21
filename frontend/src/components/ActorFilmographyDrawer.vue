<template>
  <v-navigation-drawer
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    location="right"
    temporary
    :width="drawerWidth"
  >
    <!-- Header -->
    <div class="afd-header">
      <v-btn
        icon="mdi-close"
        variant="text"
        size="small"
        class="afd-close"
        @click="$emit('update:modelValue', false)"
      />

      <div class="d-flex align-center gap-4 px-4 pb-4 pt-2">
        <v-avatar size="72" class="afd-avatar">
          <v-img v-if="actor?.photo" :src="actor.photo" cover />
          <v-icon v-else size="40">mdi-account</v-icon>
        </v-avatar>
        <div>
          <h2 class="text-h6 font-weight-black">{{ actor?.name }}</h2>
          <p v-if="actor?.character" class="text-caption text-medium-emphasis mb-0">
            as <em>{{ actor.character }}</em>
          </p>
          <p class="text-caption text-medium-emphasis mt-1">
            <template v-if="!loading && credits.length">
              {{ credits.length }} title{{ credits.length !== 1 ? 's' : '' }} found
            </template>
            <template v-else-if="!loading">No credits found</template>
            <template v-else>Loading…</template>
          </p>
        </div>
      </div>

      <!-- Filter tabs -->
      <v-tabs v-model="filterTab" density="compact" class="px-4" color="primary">
        <v-tab value="all">All</v-tab>
        <v-tab value="movie">Movies</v-tab>
        <v-tab value="tv">TV</v-tab>
        <v-tab value="inLibrary">
          In Library
          <v-badge
            v-if="inLibraryCount > 0"
            :content="inLibraryCount"
            color="primary"
            inline
            class="ml-1"
          />
        </v-tab>
      </v-tabs>

      <!-- Sort control -->
      <div class="d-flex align-center gap-2 px-4 py-2">
        <span class="text-caption text-medium-emphasis">Sort:</span>
        <v-btn-toggle v-model="sortBy" density="compact" variant="tonal" mandatory color="primary">
          <v-btn value="score" size="x-small">Best</v-btn>
          <v-btn value="rating" size="x-small">Rating</v-btn>
          <v-btn value="year" size="x-small">Year</v-btn>
        </v-btn-toggle>
        <span class="text-caption text-medium-emphasis ml-auto">
          {{ filteredCredits.length }} title{{ filteredCredits.length !== 1 ? 's' : '' }}
        </span>
      </div>

      <v-divider />
    </div>

    <!-- Loading -->
    <div v-if="loading" class="d-flex flex-column align-center justify-center pa-8">
      <v-progress-circular indeterminate color="primary" size="48" />
      <p class="text-body-2 text-medium-emphasis mt-4">Loading filmography…</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="pa-6 text-center">
      <v-icon size="48" color="error" class="mb-3">mdi-alert-circle-outline</v-icon>
      <p class="text-body-2 text-medium-emphasis">{{ error }}</p>
      <v-btn size="small" variant="tonal" class="mt-3" @click="load">Retry</v-btn>
    </div>

    <!-- Credits grid -->
    <div v-else class="afd-grid pa-3">
      <template v-if="filteredCredits.length">
        <div
          v-for="credit in filteredCredits"
          :key="`${credit.mediaType}-${credit.tmdbId}`"
          class="afd-credit"
          :class="{ 'afd-credit--in-library': getLibraryEntry(credit.tmdbId) }"
          :title="getLibraryEntry(credit.tmdbId) ? `Go to ${credit.title}` : credit.title"
          @click="handleCreditClick(credit)"
        >
          <!-- Poster -->
          <div class="afd-credit__poster-wrap">
            <v-img
              v-if="credit.posterUrl"
              :src="credit.posterUrl"
              aspect-ratio="0.667"
              cover
              class="afd-credit__poster"
            />
            <div v-else class="afd-credit__poster afd-credit__poster--empty">
              <v-icon color="grey" size="28">mdi-movie-outline</v-icon>
            </div>

            <!-- In-library badge -->
            <div v-if="getLibraryEntry(credit.tmdbId)" class="afd-credit__badge">
              <v-icon
                size="14"
                :color="getLibraryEntry(credit.tmdbId).status === 'want_to_watch' ? 'info' : 'success'"
              >
                {{ getLibraryEntry(credit.tmdbId).status === 'want_to_watch' ? 'mdi-bookmark' : 'mdi-star' }}
              </v-icon>
            </div>

            <!-- Media type pill -->
            <div class="afd-credit__type">
              {{ credit.mediaType === 'movie' ? 'M' : 'TV' }}
            </div>
          </div>

          <!-- Info -->
          <div class="afd-credit__info">
            <p class="afd-credit__title">{{ credit.title }}</p>
            <p class="afd-credit__year">{{ credit.releaseYear || '—' }}</p>
          </div>
        </div>
      </template>

      <p v-else class="text-caption text-medium-emphasis text-center pa-4 afd-empty">
        No {{ filterTab === 'inLibrary' ? 'library' : filterTab === 'all' ? '' : filterTab }} titles found.
      </p>
    </div>
  </v-navigation-drawer>
</template>

<script>
import { recommendationsAPI } from '@/services/recommendations';

export default {
  name: 'ActorFilmographyDrawer',

  props: {
    // v-model controls open/close
    modelValue: {
      type: Boolean,
      default: false,
    },
    // Normalised actor object:
    // { tmdbActorId, name, character?, photo }
    // SingleMediaView supplies tmdbActorId + character + photo (profileUrl mapped to photo)
    // AnalyticsView/TopPeople supplies tmdbActorId (= actor.id) + photo
    actor: {
      type: Object,
      default: null,
    },
    // Full user collection for in-library detection
    userCollection: {
      type: Array,
      default: () => [],
    },
  },

  emits: ['update:modelValue', 'navigate-to-media'],

  data() {
    return {
      loading: false,
      error: null,
      credits: [],
      filterTab: 'all',
      sortBy: 'score',       // 'score' | 'rating' | 'year'
      cachedActorId: null,
    };
  },

  computed: {
    drawerWidth() {
      // Responsive width: generous on desktop, full-ish on mobile
      if (typeof window === 'undefined') return 560;
      if (window.innerWidth >= 1280) return 640;
      if (window.innerWidth >= 960)  return 560;
      return Math.min(window.innerWidth - 32, 480);
    },

    filteredCredits() {
      let list = this.credits;

      // Filter
      if (this.filterTab === 'movie')     list = list.filter(c => c.mediaType === 'movie');
      else if (this.filterTab === 'tv')   list = list.filter(c => c.mediaType === 'tv');
      else if (this.filterTab === 'inLibrary') list = list.filter(c => !!this.getLibraryEntry(c.tmdbId));

      // Sort
      const sorted = [...list];
      if (this.sortBy === 'rating') {
        sorted.sort((a, b) => (b.tmdbRating || 0) - (a.tmdbRating || 0));
      } else if (this.sortBy === 'year') {
        sorted.sort((a, b) => {
          if (!a.releaseYear) return 1;
          if (!b.releaseYear) return -1;
          return b.releaseYear - a.releaseYear;
        });
      }
      // 'score' keeps the order from getByActor (already quality-sorted)

      return sorted;
    },

    inLibraryCount() {
      return this.credits.filter(c => !!this.getLibraryEntry(c.tmdbId)).length;
    },
  },

  watch: {
    // Fetch when drawer opens or actor changes
    modelValue(open) {
      if (open && this.actor) this.load();
    },
    actor(newActor) {
      if (this.modelValue && newActor) this.load();
    },
  },

  methods: {
    async load() {
      if (!this.actor?.tmdbActorId) {
        this.error = 'No TMDB ID available for this actor.';
        return;
      }

      // Skip re-fetch if same actor
      if (this.cachedActorId === this.actor.tmdbActorId && this.credits.length) return;

      this.loading = true;
      this.error = null;
      this.credits = [];
      this.filterTab = 'all';
      this.sortBy = 'score';

      try {
        const raw = await recommendationsAPI.getByActor(this.actor.tmdbActorId);

        // Sort newest first, nulls last
        this.credits = raw.sort((a, b) => {
          if (!a.releaseYear) return 1;
          if (!b.releaseYear) return -1;
          return b.releaseYear - a.releaseYear;
        });

        this.cachedActorId = this.actor.tmdbActorId;
      } catch (err) {
        console.error('ActorFilmographyDrawer: fetch error', err);
        this.error = 'Could not load filmography. Please try again.';
      } finally {
        this.loading = false;
      }
    },

    getLibraryEntry(tmdbId) {
      return this.userCollection.find(m => Number(m.tmdbId) === Number(tmdbId)) || null;
    },

    handleCreditClick(credit) {
      const existing = this.getLibraryEntry(credit.tmdbId);
      if (!existing) return; // not in library — no action

      this.$emit('update:modelValue', false);
      // Small delay so the drawer close animation doesn't fight navigation
      setTimeout(() => this.$emit('navigate-to-media', existing.mediaId), 150);
    },
  },
};
</script>

<style scoped>
/* ── Header ──────────────────────────────── */
.afd-header {
  position: sticky;
  top: 0;
  z-index: 10;
  background: rgb(var(--v-theme-surface));
  padding-top: 12px;
  border-bottom: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}

.afd-close {
  position: absolute;
  top: 8px;
  right: 8px;
}

.afd-avatar {
  flex-shrink: 0;
  border: 2px solid rgba(var(--v-theme-primary), 0.3);
}

/* ── Credits grid ────────────────────────── */
.afd-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  padding-top: 12px;
  align-content: start;
}

.afd-empty {
  grid-column: 1 / -1;
}

/* Individual credit card */
.afd-credit {
  border-radius: 8px;
  overflow: hidden;
  background: rgba(var(--v-theme-surface-variant), 0.3);
  transition: transform 0.18s ease, box-shadow 0.18s ease;
  position: relative;
  cursor: default;
}

.afd-credit--in-library {
  cursor: pointer;
}

.afd-credit--in-library:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
}

/* Faint ring on non-library items so user knows they're not clickable */
.afd-credit:not(.afd-credit--in-library) {
  opacity: 0.82;
}

.afd-credit__poster-wrap {
  position: relative;
  aspect-ratio: 2 / 3;
}

.afd-credit__poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.afd-credit__poster--empty {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(var(--v-theme-on-surface), 0.05);
}

.afd-credit__badge {
  position: absolute;
  top: 5px;
  right: 5px;
  background: rgba(0, 0, 0, 0.72);
  border-radius: 50%;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.afd-credit__type {
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

.afd-credit__info {
  padding: 5px 6px 6px;
}

.afd-credit__title {
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

.afd-credit__year {
  font-size: 0.62rem;
  color: rgba(var(--v-theme-on-surface), 0.5);
  margin: 0;
}
</style>
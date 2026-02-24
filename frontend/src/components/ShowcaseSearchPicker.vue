<template>
  <v-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    max-width="1000"
    scrollable
    attach="#app"
    :scrim="true"
  >
    <v-card>
      <v-card-title class="d-flex align-center pa-4">
        <v-icon class="mr-2">mdi-movie-search</v-icon>
        <span class="text-h6">{{ heading }}</span>
        <v-spacer />
        <v-btn icon variant="text" size="small" @click="close">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-divider />

      <v-card-text class="pa-4">
        <v-text-field
          v-model="query"
          :label="placeholder"
          prepend-inner-icon="mdi-magnify"
          variant="outlined"
          clearable
          autofocus
          @keyup.enter="search"
          @click:clear="clear"
          hint="Press Enter to search"
          persistent-hint
          :loading="loading"
        />

        <div v-if="loading" class="text-center py-12">
          <v-progress-circular indeterminate size="56" color="primary" />
          <p class="text-body-1 mt-4">Searching TMDB…</p>
        </div>

        <v-empty-state
          v-else-if="!filteredResults.length && query && !loading"
          icon="mdi-magnify-close"
          title="No Results"
          text="Try a different search term"
          class="my-8"
        />

        <v-empty-state
          v-else-if="!query && !loading"
          icon="mdi-movie-open-star"
          title="Search TMDB"
          :text="emptyText"
          class="my-8"
        />

        <div v-else class="mt-3">
          <p class="text-caption text-medium-emphasis mb-3">
            {{ filteredResults.length }} results
            <span v-if="mode !== 'any'"> ({{ mode.toUpperCase() }})</span>
          </p>

          <!-- Desktop grid -->
          <v-row v-if="!isMobile" dense>
            <v-col
              v-for="item in filteredResults"
              :key="item.tmdbId"
              cols="6" sm="4" md="3" lg="2"
            >
              <v-card class="result-card" hover @click="select(item)">
                <v-img
                  v-if="item.posterUrl"
                  :src="item.posterUrl"
                  aspect-ratio="2/3"
                  cover
                />
                <div v-else class="poster-fallback d-flex flex-column align-center justify-center">
                  <v-icon size="40">mdi-movie-outline</v-icon>
                </div>
                <v-card-text class="pa-2">
                  <p class="text-caption font-weight-bold text-truncate mb-1" :title="item.title">
                    {{ item.title }}
                  </p>
                  <p class="text-caption text-medium-emphasis">
                    {{ labelFor(item) }}
                  </p>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- Mobile list -->
          <v-list v-else lines="two">
            <v-list-item
              v-for="item in filteredResults"
              :key="item.tmdbId"
              class="mb-2 result-list-item"
              @click="select(item)"
            >
              <template #prepend>
                <v-avatar size="70" rounded class="mr-3">
                  <v-img v-if="item.posterUrl" :src="item.posterUrl" cover />
                  <v-icon v-else size="36">mdi-movie-outline</v-icon>
                </v-avatar>
              </template>
              <v-list-item-title class="text-body-2 font-weight-bold">
                {{ item.title }}
              </v-list-item-title>
              <v-list-item-subtitle class="text-caption">
                {{ labelFor(item) }}
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import { tmdbAPI } from '@/services/api-production';

export default {
  name: 'ShowcaseSearchPicker',
  props: {
    modelValue: { type: Boolean, default: false },
    /** 'movie' | 'tv' | 'any' */
    mode: { type: String, default: 'any' },
    heading: { type: String, default: 'Find Something Epic' },
  },
  emits: ['update:modelValue', 'selected'],
  data() {
    return {
      query: '',
      loading: false,
      results: [],
    };
  },
  computed: {
    isMobile() {
      return this.$vuetify?.display?.mobile;
    },
    placeholder() {
      if (this.mode === 'movie') return 'Search movies…';
      if (this.mode === 'tv') return 'Search TV shows…';
      return 'Search movies or TV shows…';
    },
    emptyText() {
      if (this.mode === 'movie') return 'Search for any movie to add to your showcase';
      if (this.mode === 'tv') return 'Search for any TV show to add to your showcase';
      return 'Search for a movie or TV show to add to your showcase';
    },
    filteredResults() {
      if (this.mode === 'any') return this.results;
      return this.results.filter(r => r.mediaType === this.mode);
    },
  },
  methods: {
    async search() {
      const q = (this.query || '').trim();
      if (q.length < 2) return;
      this.loading = true;
      try {
        const res = await tmdbAPI.search(q);
        // AddMediaDialog filters out items without poster; do the same for visual consistency
        this.results = (res || []).filter(r => !!r.posterUrl);
      } catch (e) {
        console.error('TMDB search failed:', e);
        this.results = [];
      } finally {
        this.loading = false;
      }
    },
    labelFor(item) {
      const type = item.mediaType === 'movie' ? 'Movie' : 'TV';
      return `${type} • ${item.releaseYear || '—'}`;
    },
    select(item) {
      this.$emit('selected', item);
      this.close();
    },
    clear() {
      this.query = '';
      this.results = [];
    },
    close() {
      this.$emit('update:modelValue', false);
      this.clear();
    },
  },
};
</script>

<style scoped>
.result-card { cursor: pointer; transition: transform .15s ease; }
.result-card:hover { transform: translateY(-3px); }
.poster-fallback { width: 100%; aspect-ratio: 2/3; background: rgba(255,255,255,0.05); }
.result-list-item {
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  border-radius: 8px;
  background: rgb(var(--v-theme-surface));
}
</style>
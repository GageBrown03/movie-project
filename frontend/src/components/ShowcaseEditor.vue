<template>
  <v-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    max-width="820px"
    persistent
  >
    <v-card>
      <v-card-title class="text-h6 d-flex align-center">
        Curate Your Showcase
        <v-spacer />
        <v-chip size="small" color="primary" variant="tonal">
          Keep it tight: 4 picks per row
        </v-chip>
      </v-card-title>

      <v-card-text>
        <!-- ACTIONS -->
        <div class="d-flex flex-wrap gap-2 mb-4">
          <v-btn color="primary" variant="tonal" prepend-icon="mdi-crown" @click="openPicker('movie', 'Crown a Top Movie 👑🎬')" :disabled="draft.topMovies.length >= 4">
            Crown a Top Movie
          </v-btn>
          <v-btn color="primary" variant="tonal" prepend-icon="mdi-television" @click="openPicker('tv', 'Add a Top TV Pick 📺✨')" :disabled="draft.topTv.length >= 4">
            Add a Top TV Pick
          </v-btn>
          <v-btn color="secondary" variant="tonal" prepend-icon="mdi-movie-roll" @click="openPicker('movie', 'Add a Legendary Movie Series 🎞️🌟')" :disabled="draft.favSeries.length >= 4">
            Add a Legendary Series
          </v-btn>
          <v-btn color="amber" variant="tonal" prepend-icon="mdi-diamond-stone" @click="openPicker('any', 'Choose Your Hidden Gem 💎')" :disabled="!!draft.hiddenGem.mediaId">
            Choose Your Hidden Gem
          </v-btn>
        </div>

        <!-- TOP MOVIES -->
        <section class="editor-section">
          <div class="d-flex align-center mb-2">
            <h3 class="section-title">Top Movies</h3>
            <v-spacer />
            <span class="text-caption text-medium-emphasis">{{ draft.topMovies.length }}/4</span>
          </div>
          <div v-if="!draft.topMovies.length" class="empty-row">Pick up to 4 all‑time favourites.</div>
          <div v-else class="row-list">
            <div
              v-for="(item, i) in draft.topMovies"
              :key="item.mediaId || i"
              class="row-item"
            >
              <v-img
                v-if="item.media?.posterUrl"
                :src="item.media.posterUrl"
                width="50"
                aspect-ratio="2/3"
                class="mr-3 rounded"
                cover
              />
              <div class="item-info">
                <div class="item-title">{{ item.media?.title }}</div>
                <div class="item-sub">{{ item.media?.releaseYear || '—' }}</div>
              </div>
              <div class="item-actions">
                <v-btn icon size="x-small" :disabled="i===0" @click="moveUp(draft.topMovies, i)">
                  <v-icon>mdi-arrow-up</v-icon>
                </v-btn>
                <v-btn icon size="x-small" :disabled="i===draft.topMovies.length-1" @click="moveDown(draft.topMovies, i)">
                  <v-icon>mdi-arrow-down</v-icon>
                </v-btn>
                <v-btn icon size="x-small" @click="removeAt(draft.topMovies, i)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </div>
            </div>
          </div>
        </section>

        <!-- TOP TV -->
        <section class="editor-section mt-6">
          <div class="d-flex align-center mb-2">
            <h3 class="section-title">Top TV</h3>
            <v-spacer />
            <span class="text-caption text-medium-emphasis">{{ draft.topTv.length }}/4</span>
          </div>
          <div v-if="!draft.topTv.length" class="empty-row">Pick up to 4 TV shows that define your taste.</div>
          <div v-else class="row-list">
            <div
              v-for="(item, i) in draft.topTv"
              :key="item.mediaId || i"
              class="row-item"
            >
              <v-img
                v-if="item.media?.posterUrl"
                :src="item.media.posterUrl"
                width="50"
                aspect-ratio="2/3"
                class="mr-3 rounded"
                cover
              />
              <div class="item-info">
                <div class="item-title">{{ item.media?.title }}</div>
                <div class="item-sub">{{ item.media?.releaseYear || '—' }}</div>
              </div>
              <div class="item-actions">
                <v-btn icon size="x-small" :disabled="i===0" @click="moveUp(draft.topTv, i)">
                  <v-icon>mdi-arrow-up</v-icon>
                </v-btn>
                <v-btn icon size="x-small" :disabled="i===draft.topTv.length-1" @click="moveDown(draft.topTv, i)">
                  <v-icon>mdi-arrow-down</v-icon>
                </v-btn>
                <v-btn icon size="x-small" @click="removeAt(draft.topTv, i)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </div>
            </div>
          </div>
        </section>

        <!-- FAV SERIES (Movie franchises) -->
        <section class="editor-section mt-6">
          <div class="d-flex align-center mb-2">
            <h3 class="section-title">Favourite Series</h3>
            <v-spacer />
            <span class="text-caption text-medium-emphasis">{{ draft.favSeries.length }}/4</span>
          </div>
          <div v-if="!draft.favSeries.length" class="empty-row">
            Choose up to 4 movie franchises (or a representative film).
          </div>
          <div v-else class="row-list">
            <div
              v-for="(item, i) in draft.favSeries"
              :key="item.mediaId || item.tmdbCollectionId || i"
              class="row-item"
            >
              <v-img
                v-if="item.media?.posterUrl"
                :src="item.media.posterUrl"
                width="50"
                aspect-ratio="2/3"
                class="mr-3 rounded"
                cover
              />
              <div class="item-info">
                <div class="item-title">
                  {{ item.tmdbCollectionName || item.media?.title }}
                </div>
                <div class="item-sub">
                  {{ item.media?.releaseYear || '—' }}
                </div>
              </div>
              <div class="item-actions">
                <v-btn icon size="x-small" :disabled="i===0" @click="moveUp(draft.favSeries, i)">
                  <v-icon>mdi-arrow-up</v-icon>
                </v-btn>
                <v-btn icon size="x-small" :disabled="i===draft.favSeries.length-1" @click="moveDown(draft.favSeries, i)">
                  <v-icon>mdi-arrow-down</v-icon>
                </v-btn>
                <v-btn icon size="x-small" @click="removeAt(draft.favSeries, i)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </div>
            </div>
          </div>
        </section>

        <!-- HIDDEN GEM (single) -->
        <section class="editor-section mt-6">
          <div class="d-flex align-center mb-2">
            <h3 class="section-title">Hidden Gem</h3>
            <v-spacer />
            <span class="text-caption text-medium-emphasis">{{ draft.hiddenGem.mediaId ? '1/1' : '0/1' }}</span>
          </div>

          <div v-if="!draft.hiddenGem.mediaId" class="empty-row">
            That one under‑the‑radar pick you want everyone to see.
          </div>

          <div v-else class="row-item">
            <v-img
              v-if="draft.hiddenGem.media?.posterUrl"
              :src="draft.hiddenGem.media.posterUrl"
              width="50"
              aspect-ratio="2/3"
              class="mr-3 rounded"
              cover
            />
            <div class="item-info">
              <div class="item-title">{{ draft.hiddenGem.media?.title }}</div>
              <div class="item-sub">{{ draft.hiddenGem.media?.releaseYear || '—' }}</div>
            </div>
            <div class="item-actions">
              <v-btn icon size="x-small" @click="clearGem">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </div>
          </div>

          <v-textarea
            v-model="draft.hiddenGem.note"
            label="Why is this your hidden gem?"
            rows="2"
            class="mt-3"
            variant="outlined"
            :disabled="!draft.hiddenGem.mediaId"
          />
        </section>
      </v-card-text>

      <v-divider />

      <v-card-actions class="pa-4">
        <v-btn variant="text" @click="close" :disabled="saving">Cancel</v-btn>
        <v-spacer />
        <v-btn color="primary" @click="save" :loading="saving">Save Showcase</v-btn>
      </v-card-actions>
    </v-card>

    <!-- Search picker -->
    <showcase-search-picker
      :model-value="pickerOpen"
      @update:model-value="pickerOpen = $event"
      :mode="pickerMode"
      :heading="pickerHeading"
      @selected="onPicked"
    />
  </v-dialog>
</template>

<script>
import ShowcaseSearchPicker from '@/components/ShowcaseSearchPicker.vue';
import { showcaseAPI } from '@/services/showcase-api';
import { mediaAPI, tmdbAPI } from '@/services/api-production';

export default {
  name: 'ShowcaseEditor',
  components: { ShowcaseSearchPicker },

  props: {
    modelValue: { type: Boolean, default: false },
    currentShowcase: {
      type: Object,
      default: () => ({
        topMovies: [],
        topTv: [],
        favSeries: [],
        hiddenGem: null,
      }),
    },
    /** Unused but preserved for compatibility with ShowcaseSection */
    mediaList: { type: Array, default: () => [] },
  },

  emits: ['update:modelValue', 'saved'],

  data() {
    return {
      draft: this.normalizeDraft(this.currentShowcase),
      pickerOpen: false,
      pickerMode: 'any',
      pickerHeading: 'Search',
      saving: false,
      userCollection: [],
    };
  },

  watch: {
    currentShowcase: {
      deep: true,
      handler(newVal) {
        this.draft = this.normalizeDraft(newVal);
      },
    },
    modelValue(val) {
      if (val) this.loadUserCollection();
    },
  },

  methods: {
    normalizeDraft(showcase) {
      const safe = {
        topMovies: Array.isArray(showcase?.topMovies) ? [...showcase.topMovies] : [],
        topTv: Array.isArray(showcase?.topTv) ? [...showcase.topTv] : [],
        favSeries: Array.isArray(showcase?.favSeries) ? [...showcase.favSeries] : [],
        hiddenGem: showcase?.hiddenGem
          ? { ...showcase.hiddenGem }
          : { mediaId: null, media: null, note: '' },
      };
      // Ensure each entry carries embedded media for preview if present
      for (const listName of ['topMovies', 'topTv', 'favSeries']) {
        safe[listName] = safe[listName].map(e => ({
          mediaId: e.mediaId ?? e.media?.mediaId ?? e.media_id ?? null,
          tmdbCollectionId: e.tmdbCollectionId ?? e.tmdb_collection_id ?? null,
          tmdbCollectionName: e.tmdbCollectionName ?? e.tmdb_collection_name ?? null,
          media: e.media || null,
        }));
      }
      if (safe.hiddenGem && typeof safe.hiddenGem === 'object') {
        safe.hiddenGem = {
          mediaId: safe.hiddenGem.mediaId ?? safe.hiddenGem.media?.mediaId ?? null,
          media: safe.hiddenGem.media || null,
          note: safe.hiddenGem.note || '',
        };
      }
      return safe;
    },

    async loadUserCollection() {
      try {
        // Pull the user's library so we can link picks to mediaId
        this.userCollection = await mediaAPI.getAll();
      } catch (e) {
        console.warn('Could not load user collection', e);
        this.userCollection = [];
      }
    },

    openPicker(mode, heading) {
      this.pickerMode = mode;
      this.pickerHeading = heading;
      this.pickerOpen = true;
    },

    async onPicked(tmdbItem) {
      // Ensure the item exists in the user's library and get the media object
      const media = await this.ensureInLibrary(tmdbItem);

      if (!media) return;

      if (this.pickerMode === 'movie') {
        // Decide which list to push into based on heading
        if (this.pickerHeading.includes('Top Movie')) {
          if (this.draft.topMovies.length >= 4) return;
          this.draft.topMovies.push({ mediaId: media.mediaId, media });
        } else {
          // Series uses representative movie; include collection fields if present
          if (this.draft.favSeries.length >= 4) return;
          this.draft.favSeries.push({
            mediaId: media.mediaId,
            media,
            tmdbCollectionId: media.tmdbCollectionId || null,
            tmdbCollectionName: media.tmdbCollectionName || null,
          });
        }
      } else if (this.pickerMode === 'tv') {
        if (this.draft.topTv.length >= 4) return;
        this.draft.topTv.push({ mediaId: media.mediaId, media });
      } else {
        // Hidden gem accepts either movie or TV
        if (this.draft.hiddenGem.mediaId) return; // only one allowed by backend
        this.draft.hiddenGem.mediaId = media.mediaId;
        this.draft.hiddenGem.media = media;
      }
    },

    // Find an existing media in library by tmdbId; if not present, create it
    async ensureInLibrary(tmdbItem) {
      const existing =
        this.userCollection.find(
          m => m.tmdbId === tmdbItem.tmdbId && m.mediaType === tmdbItem.mediaType
        ) || null;

      if (existing) return existing;

      try {
        // For better metadata (e.g., collection for movies), try to fetch full details
        let details = null;
        try {
          details =
            tmdbItem.mediaType === 'movie'
              ? await tmdbAPI.getMovieDetails(tmdbItem.tmdbId)
              : await tmdbAPI.getTVDetails(tmdbItem.tmdbId);
        } catch {
          // fallback to search result
          details = tmdbItem;
        }

        const payload = {
          title: tmdbItem.title,
          media_type: tmdbItem.mediaType,
          tmdb_id: tmdbItem.tmdbId,
          release_year: tmdbItem.releaseYear,
          plot: tmdbItem.plot,
          poster_url: tmdbItem.posterUrl,
          backdrop_url: tmdbItem.backdropUrl,
          tmdb_rating: tmdbItem.tmdbRating,
          // If details include collection, the backend Media model will store it
          tmdb_collection_id: details.tmdbCollectionId || details.tmdb_collection_id || null,
          tmdb_collection_name: details.tmdbCollectionName || details.tmdb_collection_name || null,
          // Let backend default status to WATCHED
        };

        const created = await mediaAPI.create(payload);
        this.userCollection.push(created);
        return created;
      } catch (e) {
        console.error('Failed creating media for showcase link', e);
        return null;
      }
    },

    moveUp(list, i) {
      if (i <= 0) return;
      [list[i - 1], list[i]] = [list[i], list[i - 1]];
    },
    moveDown(list, i) {
      if (i >= list.length - 1) return;
      [list[i + 1], list[i]] = [list[i], list[i + 1]];
    },
    removeAt(list, i) {
      list.splice(i, 1);
    },
    clearGem() {
      this.draft.hiddenGem = { mediaId: null, media: null, note: '' };
    },

    close() {
      this.$emit('update:modelValue', false);
    },

    buildPayload() {
      // Map lists to API shape with ranks (1..N)
      const mapRank = (arr) =>
        arr.slice(0, 4).map((e, idx) => ({
          mediaId: e.mediaId,
          rank: idx + 1,
        }));

      const payload = {
        topMovies: mapRank(this.draft.topMovies),
        topTv: mapRank(this.draft.topTv),
        favSeries: this.draft.favSeries.slice(0, 4).map((e, idx) => ({
          mediaId: e.mediaId || null,
          tmdbCollectionId: e.tmdbCollectionId || null,
          tmdbCollectionName: e.tmdbCollectionName || null,
          rank: idx + 1,
        })),
        hiddenGem: this.draft.hiddenGem?.mediaId
          ? {
            mediaId: this.draft.hiddenGem.mediaId,
            note: this.draft.hiddenGem.note || null,
            rank: 1,
          }
          : null,
      };

      return payload;
    },

    async save() {
      this.saving = true;
      try {
        const payload = this.buildPayload();
        await showcaseAPI.save(payload);

        // After save, fetch the owner’s full editable showcase so UI is in sync
        let updated;
        try {
          updated = await showcaseAPI.getMine();
        } catch {
          // Fallback to public version if needed
          updated = await showcaseAPI.getByUsername(localStorage.getItem('username'));
        }

        // Emit updated showcase back to ShowcaseSection
        this.$emit('saved', updated.showcase || updated);
        this.close();
      } catch (e) {
        console.error('Failed to save showcase', e);
      } finally {
        this.saving = false;
      }
    },
  },
};
</script>

<style scoped>

.section-title { font-weight: 800; font-size: 1rem; margin: 0; }
.empty-row {
  padding: 12px;
  border: 1px dashed rgba(var(--v-theme-on-surface), 0.15);
  border-radius: 10px;
  color: rgba(var(--v-theme-on-surface), 0.6);
  font-size: 0.9rem;
}
.row-list { display: flex; flex-direction: column; gap: 8px; }
.row-item {
  display: flex; align-items: center; gap: 10px;
  padding: 8px; border-radius: 10px;
  background: rgba(var(--v-theme-surface-variant), 0.25);
}
.item-info { flex: 1; min-width: 0; }
.item-title { font-weight: 700; font-size: .92rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.item-sub { font-size: .72rem; opacity: .7; }
.item-actions { display: flex; gap: 4px; }
.gap-2 { gap: 8px; }
</style>
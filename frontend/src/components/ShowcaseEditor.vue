<template>
  <v-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    max-width="820px"
    :fullscreen="$vuetify?.display?.mobile || false"
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

      <v-card-text class="editor-scroll">
        <!-- TOP MOVIES -->
        <section class="editor-section">
          <div class="section-head">
            <h3 class="section-title" @click="openPicker('movie','Crown a Top Movie 👑🎬')">Top Movies</h3>
            <div class="section-actions">
              <span class="count">{{ draft.topMovies.length }}/4</span>
              <v-btn
                size="small"
                variant="tonal"
                color="primary"
                prepend-icon="mdi-plus"
                @click="openPicker('movie','Crown a Top Movie 👑🎬')"
                :disabled="draft.topMovies.length >= 4"
              >
                Add
              </v-btn>
            </div>
          </div>

          <div v-if="!draft.topMovies.length" class="empty-row">
            Pick up to 4 all‑time favourites.
          </div>
          <div v-else class="row-list">
            <div v-for="(item, i) in draft.topMovies" :key="item.mediaId || i" class="row-item">
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
          <div class="section-head">
            <h3 class="section-title" @click="openPicker('tv','Add a Top TV Pick 📺✨')">Top TV</h3>
            <div class="section-actions">
              <span class="count">{{ draft.topTv.length }}/4</span>
              <v-btn
                size="small"
                variant="tonal"
                color="primary"
                prepend-icon="mdi-plus"
                @click="openPicker('tv','Add a Top TV Pick 📺✨')"
                :disabled="draft.topTv.length >= 4"
              >
                Add
              </v-btn>
            </div>
          </div>

          <div v-if="!draft.topTv.length" class="empty-row">
            Pick up to 4 TV shows that define your taste.
          </div>
          <div v-else class="row-list">
            <div v-for="(item, i) in draft.topTv" :key="item.mediaId || i" class="row-item">
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

        <!-- FAV SERIES -->
        <section class="editor-section mt-6">
          <div class="section-head">
            <h3 class="section-title" @click="openPicker('movie','Add a Legendary Movie Series 🎞️🌟')">Favourite Series</h3>
            <div class="section-actions">
              <span class="count">{{ draft.favSeries.length }}/4</span>
              <v-btn
                size="small"
                variant="tonal"
                color="secondary"
                prepend-icon="mdi-plus"
                @click="openPicker('movie','Add a Legendary Movie Series 🎞️🌟')"
                :disabled="draft.favSeries.length >= 4"
              >
                Add
              </v-btn>
            </div>
          </div>

          <div v-if="!draft.favSeries.length" class="empty-row">
            Choose up to 4 movie franchises (or a representative film).
          </div>
          <div v-else class="row-list">
            <div v-for="(item, i) in draft.favSeries" :key="item.mediaId || item.tmdbCollectionId || i" class="row-item">
              <v-img
                v-if="item.media?.posterUrl"
                :src="item.media.posterUrl"
                width="50"
                aspect-ratio="2/3"
                class="mr-3 rounded"
                cover
              />
              <div class="item-info">
                <div class="item-title">{{ item.tmdbCollectionName || item.media?.title }}</div>
                <div class="item-sub">{{ item.media?.releaseYear || '—' }}</div>
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

        <!-- HIDDEN GEM -->
        <section class="editor-section mt-6">
          <div class="section-head">
            <h3 class="section-title" @click="openPicker('any','Choose Your Hidden Gem 💎')">Hidden Gem</h3>
            <div class="section-actions">
              <span class="count">{{ draft.hiddenGem.mediaId ? '1/1' : '0/1' }}</span>
              <v-btn
                size="small"
                variant="tonal"
                color="amber"
                prepend-icon="mdi-plus"
                @click="openPicker('any','Choose Your Hidden Gem 💎')"
                :disabled="!!draft.hiddenGem.mediaId"
              >
                Pick
              </v-btn>
            </div>
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

      <!-- Sticky Save Bar -->
      <v-card-actions class="save-bar">
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

    <!-- Quick Rate Dialog -->
    <v-dialog v-model="quickRateOpen" max-width="480px">
      <v-card>
        <v-card-title class="text-h6 d-flex align-center">
          <v-avatar size="40" rounded class="mr-3" v-if="quickRateItem?.posterUrl">
            <v-img :src="quickRateItem.posterUrl" cover />
          </v-avatar>
          Rate {{ quickRateItem?.title }}
        </v-card-title>

        <v-card-text>
          <v-rating v-model="quickRateValue" hover size="36" color="amber" />
          <v-textarea v-model="quickRateNotes" label="Why do you like it?" auto-grow class="mt-3" />
        </v-card-text>

        <v-card-actions>
          <v-btn variant="text" @click="cancelQuickRate">Cancel</v-btn>
          <v-spacer />
          <v-btn color="secondary" variant="tonal" @click="skipAndAdd">Skip & Add</v-btn>
          <v-btn color="primary" @click="confirmQuickRate">Save Rating & Add</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Local Snackbar -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="3000">
      {{ snackbar.text }}
      <template #actions>
        <v-btn variant="text" @click="snackbar.show = false">Close</v-btn>
      </template>
    </v-snackbar>
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
      default: () => ({ topMovies: [], topTv: [], favSeries: [], hiddenGem: null }),
    },
    mediaList: { type: Array, default: () => [] },
  },

  emits: ['update:modelValue', 'saved'],

  data() {
    return {
      draft: this.normalizeDraft(this.currentShowcase),
      pickerOpen: false,
      pickerMode: 'any',
      pickerHeading: '',
      quickRateOpen: false,
      quickRateItem: null,
      quickRateValue: null,
      quickRateNotes: '',
      userCollection: [],
      saving: false,
      snackbar: { show: false, text: '', color: 'success' },
    };
  },

  watch: {
    modelValue(val) { if (val) this.loadUserCollection(); },
    currentShowcase: { deep: true, handler(newVal) { this.draft = this.normalizeDraft(newVal); } },
  },

  methods: {
    toast(text, color = 'success') { this.snackbar = { show: true, text, color }; },
    close() { this.$emit('update:modelValue', false); },

    normalizeDraft(showcase) {
      const safe = {
        topMovies: Array.isArray(showcase?.topMovies) ? [...showcase.topMovies] : [],
        topTv: Array.isArray(showcase?.topTv) ? [...showcase.topTv] : [],
        favSeries: Array.isArray(showcase?.favSeries) ? [...showcase.favSeries] : [],
        hiddenGem: showcase?.hiddenGem ? { ...showcase.hiddenGem } : { mediaId: null, media: null, note: '' },
      };
      for (const list of ['topMovies','topTv','favSeries']) {
        safe[list] = safe[list].map(e => ({
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
      try { this.userCollection = await mediaAPI.getAll(); }
      catch { this.userCollection = []; }
    },

    openPicker(mode, heading) { this.pickerMode = mode; this.pickerHeading = heading; this.pickerOpen = true; },

    async onPicked(tmdbItem) {
      this.pickerOpen = false;
      const existing = this.userCollection.find(m => m.tmdbId === tmdbItem.tmdbId && m.mediaType === tmdbItem.mediaType);
      if (existing) { this.toast(`Using your existing "${existing.title}".`); this.finishAdd(existing); return; }
      this.quickRateItem = tmdbItem; this.quickRateValue = null; this.quickRateNotes = ''; this.quickRateOpen = true;
    },

    cancelQuickRate() { this.quickRateOpen = false; this.quickRateItem = null; this.quickRateValue = null; this.quickRateNotes = ''; },

    async skipAndAdd() {
      const tmdbItem = this.quickRateItem; this.quickRateOpen = false;
      const created = await this.ensureInLibrary(tmdbItem);
      if (created) { this.toast(`Added "${created.title}" to your library ✨`); this.finishAdd(created); }
      this.cancelQuickRate();
    },

    async confirmQuickRate() {
      if (!this.quickRateItem) return;
      const created = await this.createRatedMedia(this.quickRateItem, this.quickRateValue, this.quickRateNotes);
      this.quickRateOpen = false;
      if (created) { this.toast(`Rated & added "${created.title}" ✔`); this.finishAdd(created); }
      this.cancelQuickRate();
    },

    async createRatedMedia(tmdbItem, rating, notes) {
      try {
        let details; try {
          details = tmdbItem.mediaType === 'movie' ? await tmdbAPI.getMovieDetails(tmdbItem.tmdbId) : await tmdbAPI.getTVDetails(tmdbItem.tmdbId);
        } catch { details = tmdbItem; }
        const payload = {
          title: tmdbItem.title, media_type: tmdbItem.mediaType, tmdb_id: tmdbItem.tmdbId,
          release_year: tmdbItem.releaseYear, plot: tmdbItem.plot, poster_url: tmdbItem.posterUrl,
          backdrop_url: tmdbItem.backdropUrl, tmdb_rating: tmdbItem.tmdbRating,
          rating: rating || null, notes: notes || null,
          tmdb_collection_id: details.tmdbCollectionId || details.tmdb_collection_id || null,
          tmdb_collection_name: details.tmdbCollectionName || details.tmdb_collection_name || null,
          cast: details.cast || [],
        };
        const created = await mediaAPI.create(payload);
        this.userCollection.push(created);
        return created;
      } catch { this.toast('Failed to save rating.', 'error'); return null; }
    },

    async ensureInLibrary(tmdbItem) {
      const existing = this.userCollection.find(m => m.tmdbId === tmdbItem.tmdbId && m.mediaType === tmdbItem.mediaType);
      if (existing) return existing;
      try {
        let details; try {
          details = tmdbItem.mediaType === 'movie' ? await tmdbAPI.getMovieDetails(tmdbItem.tmdbId) : await tmdbAPI.getTVDetails(tmdbItem.tmdbId);
        } catch { details = tmdbItem; }
        const payload = {
          title: tmdbItem.title, media_type: tmdbItem.mediaType, tmdb_id: tmdbItem.tmdbId,
          release_year: tmdbItem.releaseYear, plot: tmdbItem.plot, poster_url: tmdbItem.posterUrl,
          backdrop_url: tmdbItem.backdropUrl, tmdb_rating: tmdbItem.tmdbRating,
          tmdb_collection_id: details.tmdbCollectionId || details.tmdb_collection_id || null,
          tmdb_collection_name: details.tmdbCollectionName || details.tmdb_collection_name || null,
          cast: details.cast || [],
        };
        const created = await mediaAPI.create(payload);
        this.userCollection.push(created);
        return created;
      } catch { this.toast('Something went wrong adding to your library.', 'error'); return null; }
    },

    finishAdd(media) {
      if (this.pickerHeading.includes('Top Movie')) {
        if (this.draft.topMovies.length < 4) this.draft.topMovies.push({ mediaId: media.mediaId, media });
      } else if (this.pickerHeading.includes('Top TV')) {
        if (this.draft.topTv.length < 4) this.draft.topTv.push({ mediaId: media.mediaId, media });
      } else if (this.pickerHeading.includes('Legendary')) {
        if (this.draft.favSeries.length < 4) {
          this.draft.favSeries.push({
            mediaId: media.mediaId, media,
            tmdbCollectionId: media.tmdbCollectionId || null,
            tmdbCollectionName: media.tmdbCollectionName || null,
          });
        }
      } else if (this.pickerHeading.includes('Hidden Gem')) {
        if (!this.draft.hiddenGem.mediaId) { this.draft.hiddenGem.mediaId = media.mediaId; this.draft.hiddenGem.media = media; }
      }
    },

    moveUp(list, i) { if (i <= 0) return; [list[i - 1], list[i]] = [list[i], list[i - 1]]; },
    moveDown(list, i) { if (i >= list.length - 1) return; [list[i + 1], list[i]] = [list[i], list[i + 1]]; },
    removeAt(list, i) { list.splice(i, 1); },
    clearGem() { this.draft.hiddenGem = { mediaId: null, media: null, note: '' }; },

    async save() {
      this.saving = true;
      try {
        const payload = {
          topMovies: this.draft.topMovies.slice(0, 4).map((e, i) => ({ mediaId: e.mediaId, rank: i + 1 })),
          topTv: this.draft.topTv.slice(0, 4).map((e, i) => ({ mediaId: e.mediaId, rank: i + 1 })),
          favSeries: this.draft.favSeries.slice(0, 4).map((e, i) => ({
            mediaId: e.mediaId || null,
            tmdbCollectionId: e.tmdbCollectionId || null,
            tmdbCollectionName: e.tmdbCollectionName || null,
            rank: i + 1,
          })),
          hiddenGem: this.draft.hiddenGem?.mediaId ? { mediaId: this.draft.hiddenGem.mediaId, note: this.draft.hiddenGem.note || '', rank: 1 } : null,
        };
        await showcaseAPI.save(payload);
        let updated; try { updated = await showcaseAPI.getMine(); } catch { updated = { showcase: this.draft }; }
        this.$emit('saved', updated.showcase || this.draft);
        this.close();
        this.toast('Showcase saved!', 'success');
      } catch (e) {
        this.toast('Failed to save showcase', 'error');
      } finally { this.saving = false; }
    },
  },
};
</script>

<style scoped>
.editor-scroll { padding-bottom: 84px; }
.save-bar { position: sticky; bottom: 0; z-index: 5; background: rgb(var(--v-theme-surface)); border-top: 1px solid rgba(var(--v-border-color), var(--v-border-opacity)); padding: 12px; }

.section-head { display:flex; align-items:center; gap:12px; margin-bottom:8px; }
.section-title { font-weight: 800; font-size: 1rem; margin: 0; cursor:pointer; }
.section-actions { display:flex; align-items:center; gap:8px; }
.section-actions .count { font-size: .8rem; color: rgba(var(--v-theme-on-surface),.55); }

.empty-row { padding: 12px; border: 1px dashed rgba(var(--v-theme-on-surface), 0.15); border-radius: 10px; color: rgba(var(--v-theme-on-surface), 0.6); font-size: 0.9rem; }
.row-list { display: flex; flex-direction: column; gap: 8px; }
.row-item { display: flex; align-items: center; gap: 10px; padding: 8px; border-radius: 10px; background: rgba(var(--v-theme-surface-variant), 0.25); }
.item-info { flex: 1; min-width: 0; }
.item-title { font-weight: 700; font-size: .92rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.item-sub { font-size: .72rem; opacity: .7; }

@media (max-width:600px){ .editor-scroll{ padding-bottom: 92px; } }
</style>
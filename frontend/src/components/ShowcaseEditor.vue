<template>
  <v-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    :fullscreen="isMobile"
    max-width="680"
    scrollable
    persistent
  >
    <v-card class="editor-card">

      <!-- ── Title bar ── -->
      <div class="editor-titlebar">
        <div class="editor-titlebar__left">
          <span class="editor-titlebar__icon">✦</span>
          <span class="editor-titlebar__text">Edit Showcase</span>
        </div>
        <button class="editor-close-btn" @click="close" :disabled="saving">
          <v-icon size="20">mdi-close</v-icon>
        </button>
      </div>

      <!-- ── Scrollable body ── -->
      <v-card-text class="editor-body">

        <!-- TOP MOVIES -->
        <div class="ed-section">
          <div class="ed-section__head">
            <span class="ed-section__dot" style="background:#E8A838"></span>
            <span class="ed-section__title">Top Movies</span>
            <span class="ed-section__count">{{ draft.topMovies.length }}/{{ MAX }}</span>
            <button
              v-if="draft.topMovies.length < MAX"
              class="ed-add-btn ed-add-btn--gold"
              @click="openPicker('movie', 'TOP_MOVIES')"
            >+ Add</button>
          </div>
          <div v-if="!draft.topMovies.length" class="ed-empty">Pick up to {{ MAX }} all-time favourites.</div>
          <div v-else class="ed-list">
            <div v-for="(item, i) in draft.topMovies" :key="item.mediaId || i" class="ed-item">
              <span class="ed-item__rank" :class="{ 'ed-item__rank--gold': i === 0 }">
                {{ i === 0 ? '★' : i + 1 }}
              </span>
              <img v-if="item.media && item.media.posterUrl" :src="item.media.posterUrl" class="ed-item__poster" />
              <div v-else class="ed-item__poster ed-item__poster--empty">🎬</div>
              <div class="ed-item__info">
                <p class="ed-item__title">{{ item.media && item.media.title }}</p>
                <p class="ed-item__sub">{{ item.media && item.media.releaseYear || '—' }}</p>
              </div>
              <div class="ed-item__actions">
                <button class="ed-icon-btn" :disabled="i === 0" @click="moveUp(draft.topMovies, i)" title="Move up">
                  <v-icon size="16">mdi-chevron-up</v-icon>
                </button>
                <button class="ed-icon-btn" :disabled="i === draft.topMovies.length - 1" @click="moveDown(draft.topMovies, i)" title="Move down">
                  <v-icon size="16">mdi-chevron-down</v-icon>
                </button>
                <button class="ed-icon-btn ed-icon-btn--remove" @click="removeAt(draft.topMovies, i)" title="Remove">
                  <v-icon size="16">mdi-close</v-icon>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- TOP TV -->
        <div class="ed-section">
          <div class="ed-section__head">
            <span class="ed-section__dot" style="background:#5C9EFF"></span>
            <span class="ed-section__title">Top TV Shows</span>
            <span class="ed-section__count">{{ draft.topTv.length }}/{{ MAX }}</span>
            <button
              v-if="draft.topTv.length < MAX"
              class="ed-add-btn ed-add-btn--blue"
              @click="openPicker('tv', 'TOP_TV')"
            >+ Add</button>
          </div>
          <div v-if="!draft.topTv.length" class="ed-empty">Pick up to {{ MAX }} shows that define your taste.</div>
          <div v-else class="ed-list">
            <div v-for="(item, i) in draft.topTv" :key="item.mediaId || i" class="ed-item">
              <span class="ed-item__rank" :class="{ 'ed-item__rank--blue': i === 0 }">
                {{ i === 0 ? '★' : i + 1 }}
              </span>
              <img v-if="item.media && item.media.posterUrl" :src="item.media.posterUrl" class="ed-item__poster" />
              <div v-else class="ed-item__poster ed-item__poster--empty">📺</div>
              <div class="ed-item__info">
                <p class="ed-item__title">{{ item.media && item.media.title }}</p>
                <p class="ed-item__sub">{{ item.media && item.media.releaseYear || '—' }}</p>
              </div>
              <div class="ed-item__actions">
                <button class="ed-icon-btn" :disabled="i === 0" @click="moveUp(draft.topTv, i)">
                  <v-icon size="16">mdi-chevron-up</v-icon>
                </button>
                <button class="ed-icon-btn" :disabled="i === draft.topTv.length - 1" @click="moveDown(draft.topTv, i)">
                  <v-icon size="16">mdi-chevron-down</v-icon>
                </button>
                <button class="ed-icon-btn ed-icon-btn--remove" @click="removeAt(draft.topTv, i)">
                  <v-icon size="16">mdi-close</v-icon>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- FAVOURITE SERIES -->
        <div class="ed-section">
          <div class="ed-section__head">
            <span class="ed-section__dot" style="background:#A78BFA"></span>
            <span class="ed-section__title">Favourite Series</span>
            <span class="ed-section__count">{{ draft.favSeries.length }}/{{ MAX }}</span>
            <button
              v-if="draft.favSeries.length < MAX"
              class="ed-add-btn ed-add-btn--purple"
              @click="openPicker('movie', 'FAV_SERIES')"
            >+ Add</button>
          </div>
          <p class="ed-section__hint">Pick any film from a franchise — the series name auto-fills.</p>
          <div v-if="!draft.favSeries.length" class="ed-empty">Pick a film from any franchise or series.</div>
          <div v-else class="ed-list">
            <div v-for="(item, i) in draft.favSeries" :key="item.mediaId || item.tmdbCollectionId || i" class="ed-item">
              <span class="ed-item__rank" :class="{ 'ed-item__rank--purple': i === 0 }">
                {{ i === 0 ? '★' : i + 1 }}
              </span>
              <img v-if="item.media && item.media.posterUrl" :src="item.media.posterUrl" class="ed-item__poster" />
              <div v-else class="ed-item__poster ed-item__poster--empty">🎞️</div>
              <div class="ed-item__info">
                <p class="ed-item__title">{{ item.tmdbCollectionName || (item.media && item.media.title) }}</p>
                <p class="ed-item__sub">{{ (item.media && item.media.releaseYear) || '—' }} · Series</p>
              </div>
              <div class="ed-item__actions">
                <button class="ed-icon-btn" :disabled="i === 0" @click="moveUp(draft.favSeries, i)">
                  <v-icon size="16">mdi-chevron-up</v-icon>
                </button>
                <button class="ed-icon-btn" :disabled="i === draft.favSeries.length - 1" @click="moveDown(draft.favSeries, i)">
                  <v-icon size="16">mdi-chevron-down</v-icon>
                </button>
                <button class="ed-icon-btn ed-icon-btn--remove" @click="removeAt(draft.favSeries, i)">
                  <v-icon size="16">mdi-close</v-icon>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- HIDDEN GEM -->
        <div class="ed-section">
          <div class="ed-section__head">
            <span class="ed-section__dot" style="background:#F59E0B"></span>
            <span class="ed-section__title" style="color:#F59E0B">Hidden Gem</span>
            <span class="ed-section__count">{{ draft.hiddenGem.mediaId ? '1/1' : '0/1' }}</span>
            <button
              v-if="!draft.hiddenGem.mediaId"
              class="ed-add-btn ed-add-btn--amber"
              @click="openPicker('any', 'HIDDEN_GEM')"
            >+ Pick</button>
          </div>
          <p class="ed-section__hint">That one under-the-radar title you want everyone to discover.</p>

          <div v-if="!draft.hiddenGem.mediaId" class="ed-empty">No hidden gem selected yet.</div>
          <div v-else class="ed-gem-preview">
            <img v-if="draft.hiddenGem.media && draft.hiddenGem.media.backdropUrl" :src="draft.hiddenGem.media.backdropUrl" class="ed-gem-preview__bg" />
            <div v-else class="ed-gem-preview__bg ed-gem-preview__bg--fallback" />
            <div class="ed-gem-preview__scrim" />
            <div class="ed-gem-preview__body">
              <img v-if="draft.hiddenGem.media && draft.hiddenGem.media.posterUrl" :src="draft.hiddenGem.media.posterUrl" class="ed-gem-preview__poster" />
              <div class="ed-gem-preview__info">
                <p class="ed-gem-preview__title">{{ draft.hiddenGem.media && draft.hiddenGem.media.title }}</p>
                <p class="ed-gem-preview__year">{{ draft.hiddenGem.media && draft.hiddenGem.media.releaseYear }}</p>
              </div>
              <button class="ed-icon-btn ed-icon-btn--remove ed-icon-btn--overlay" @click="clearGem" title="Remove">
                <v-icon size="16">mdi-close</v-icon>
              </button>
            </div>
          </div>

          <!-- Note textarea — always visible so user can type when gem is set -->
          <div class="ed-gem-note-wrap">
            <v-textarea
              v-model="draft.hiddenGem.note"
              label="Why is this your hidden gem?"
              placeholder="A quiet masterpiece that nobody talks about…"
              rows="2"
              variant="outlined"
              density="compact"
              maxlength="200"
              counter
              class="mt-3"
              :disabled="!draft.hiddenGem.mediaId"
            />
          </div>
        </div>

      </v-card-text>

      <!-- ── Sticky save bar ── -->
      <div class="editor-save-bar">
        <button class="ed-cancel-btn" @click="close" :disabled="saving">Cancel</button>
        <button class="ed-save-btn" @click="save" :disabled="saving">
          <v-progress-circular v-if="saving" indeterminate size="14" width="2" class="mr-2" />
          Save Showcase
        </button>
      </div>

    </v-card>

    <!-- Search picker -->
    <showcase-search-picker
      :model-value="pickerOpen"
      @update:model-value="pickerOpen = $event"
      :mode="pickerMode"
      :heading="pickerHeading"
      @selected="onPicked"
    />

    <!-- Quick rate dialog -->
    <v-dialog v-model="quickRateOpen" max-width="480">
      <v-card>
        <v-card-title class="d-flex align-center pa-4">
          <v-avatar v-if="quickRateItem && quickRateItem.posterUrl" size="40" rounded class="mr-3">
            <v-img :src="quickRateItem.posterUrl" cover />
          </v-avatar>
          <span class="text-h6">Rate {{ quickRateItem && quickRateItem.title }}</span>
        </v-card-title>
        <v-card-text>
          <p class="text-body-2 text-medium-emphasis mb-3">
            This title isn't in your library yet. Rate it now, or just add it unrated.
          </p>
          <v-rating v-model="quickRateValue" hover size="36" color="amber" />
          <v-textarea v-model="quickRateNotes" label="Notes (optional)" auto-grow rows="2" variant="outlined" density="compact" class="mt-3" />
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-btn variant="text" @click="cancelQuickRate">Cancel</v-btn>
          <v-spacer />
          <v-btn variant="tonal" color="secondary" @click="skipAndAdd">Add Unrated</v-btn>
          <v-btn color="primary" @click="confirmQuickRate">Rate & Add</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="3000" location="bottom">
      {{ snackbar.text }}
      <template #actions>
        <v-btn variant="text" @click="snackbar.show = false">Dismiss</v-btn>
      </template>
    </v-snackbar>

  </v-dialog>
</template>

<script>
import ShowcaseSearchPicker from '@/components/ShowcaseSearchPicker.vue';
import { showcaseAPI } from '@/services/showcase-api';
import { mediaAPI, tmdbAPI } from '@/services/api-production';

const MAX = 5; // max items per ranked list

export default {
  name: 'ShowcaseEditor',
  components: { ShowcaseSearchPicker },

  props: {
    modelValue:       { type: Boolean, default: false },
    currentShowcase:  { type: Object,  default: () => ({ topMovies: [], topTv: [], favSeries: [], hiddenGem: null }) },
    mediaList:        { type: Array,   default: () => [] },
  },

  emits: ['update:modelValue', 'saved'],

  data() {
    return {
      MAX,
      draft: this.normalizeDraft(this.currentShowcase),

      // Picker state
      pickerOpen:    false,
      pickerMode:    'any',  // 'movie' | 'tv' | 'any'
      pickerHeading: '',
      pickerTarget:  null,   // 'TOP_MOVIES' | 'TOP_TV' | 'FAV_SERIES' | 'HIDDEN_GEM'

      // Quick-rate state
      quickRateOpen:  false,
      quickRateItem:  null,
      quickRateValue: null,
      quickRateNotes: '',

      userCollection: [],
      saving: false,
      snackbar: { show: false, text: '', color: 'success' },
    };
  },

  computed: {
    isMobile() {
      return this.$vuetify?.display?.smAndDown ?? false;
    },
    pickerHeadingMap() {
      return {
        TOP_MOVIES: 'Add a Top Movie 🎬',
        TOP_TV:     'Add a Top TV Show 📺',
        FAV_SERIES: 'Pick a Film from Your Favourite Series 🎞️',
        HIDDEN_GEM: 'Choose Your Hidden Gem 💎',
      };
    },
  },

  watch: {
    modelValue(val) {
      if (val) {
        this.draft = this.normalizeDraft(this.currentShowcase);
        this.loadUserCollection();
      }
    },
    currentShowcase: {
      deep: true,
      handler(v) { this.draft = this.normalizeDraft(v); },
    },
  },

  methods: {
    /* ── Helpers ── */
    toast(text, color = 'success') {
      this.snackbar = { show: true, text, color };
    },
    close() {
      this.$emit('update:modelValue', false);
    },

    normalizeDraft(showcase) {
      const safe = {
        topMovies: Array.isArray(showcase?.topMovies) ? [...showcase.topMovies] : [],
        topTv:     Array.isArray(showcase?.topTv)     ? [...showcase.topTv]     : [],
        favSeries: Array.isArray(showcase?.favSeries) ? [...showcase.favSeries] : [],
        hiddenGem: showcase?.hiddenGem
          ? { ...showcase.hiddenGem }
          : { mediaId: null, media: null, note: '' },
      };

      for (const key of ['topMovies', 'topTv', 'favSeries']) {
        safe[key] = safe[key].map(e => ({
          mediaId:            e.mediaId            ?? e.media?.mediaId ?? e.media_id ?? null,
          tmdbCollectionId:   e.tmdbCollectionId   ?? e.tmdb_collection_id   ?? null,
          tmdbCollectionName: e.tmdbCollectionName ?? e.tmdb_collection_name ?? null,
          media:              e.media              || null,
        }));
      }

      if (safe.hiddenGem) {
        safe.hiddenGem = {
          mediaId: safe.hiddenGem.mediaId ?? safe.hiddenGem.media?.mediaId ?? null,
          media:   safe.hiddenGem.media   || null,
          note:    safe.hiddenGem.note    || '',
        };
      }

      return safe;
    },

    async loadUserCollection() {
      try { this.userCollection = await mediaAPI.getAll(); }
      catch { this.userCollection = []; }
    },

    /* ── Picker ── */
    openPicker(mode, target) {
      this.pickerMode    = mode;
      this.pickerTarget  = target;
      this.pickerHeading = this.pickerHeadingMap[target] || 'Find Something';
      this.pickerOpen    = true;
    },

    async onPicked(tmdbItem) {
      this.pickerOpen = false;
      const existing = this.userCollection.find(
        m => m.tmdbId === tmdbItem.tmdbId && m.mediaType === tmdbItem.mediaType
      );
      if (existing) {
        this.toast(`Using your existing "${existing.title}".`);
        this.finishAdd(existing);
        return;
      }
      // Not in library → quick-rate
      this.quickRateItem  = tmdbItem;
      this.quickRateValue = null;
      this.quickRateNotes = '';
      this.quickRateOpen  = true;
    },

    cancelQuickRate() {
      this.quickRateOpen = false;
      this.quickRateItem = null;
    },

    async skipAndAdd() {
      const item = this.quickRateItem;
      this.quickRateOpen = false;
      const created = await this.ensureInLibrary(item);
      if (created) {
        this.toast(`Added "${created.title}" to your library.`);
        this.finishAdd(created);
      }
      this.cancelQuickRate();
    },

    async confirmQuickRate() {
      if (!this.quickRateItem) return;
      const created = await this.createRatedMedia(
        this.quickRateItem, this.quickRateValue, this.quickRateNotes
      );
      this.quickRateOpen = false;
      if (created) {
        this.toast(`Rated & added "${created.title}".`);
        this.finishAdd(created);
      }
      this.cancelQuickRate();
    },

    async createRatedMedia(tmdbItem, rating, notes) {
      try {
        let details;
        try {
          details = tmdbItem.mediaType === 'movie'
            ? await tmdbAPI.getMovieDetails(tmdbItem.tmdbId)
            : await tmdbAPI.getTVDetails(tmdbItem.tmdbId);
        } catch { details = tmdbItem; }

        const payload = {
          title: tmdbItem.title, media_type: tmdbItem.mediaType,
          tmdb_id: tmdbItem.tmdbId, release_year: tmdbItem.releaseYear,
          plot: tmdbItem.plot, poster_url: tmdbItem.posterUrl,
          backdrop_url: tmdbItem.backdropUrl, tmdb_rating: tmdbItem.tmdbRating,
          rating: rating || null, notes: notes || null,
          tmdb_collection_id:   details.tmdbCollectionId   || details.tmdb_collection_id   || null,
          tmdb_collection_name: details.tmdbCollectionName || details.tmdb_collection_name || null,
          cast: details.cast || [],
        };
        const created = await mediaAPI.create(payload);
        this.userCollection.push(created);
        return created;
      } catch {
        this.toast('Failed to save rating.', 'error');
        return null;
      }
    },

    async ensureInLibrary(tmdbItem) {
      const existing = this.userCollection.find(
        m => m.tmdbId === tmdbItem.tmdbId && m.mediaType === tmdbItem.mediaType
      );
      if (existing) return existing;
      try {
        let details;
        try {
          details = tmdbItem.mediaType === 'movie'
            ? await tmdbAPI.getMovieDetails(tmdbItem.tmdbId)
            : await tmdbAPI.getTVDetails(tmdbItem.tmdbId);
        } catch { details = tmdbItem; }

        const payload = {
          title: tmdbItem.title, media_type: tmdbItem.mediaType,
          tmdb_id: tmdbItem.tmdbId, release_year: tmdbItem.releaseYear,
          plot: tmdbItem.plot, poster_url: tmdbItem.posterUrl,
          backdrop_url: tmdbItem.backdropUrl, tmdb_rating: tmdbItem.tmdbRating,
          tmdb_collection_id:   details.tmdbCollectionId   || details.tmdb_collection_id   || null,
          tmdb_collection_name: details.tmdbCollectionName || details.tmdb_collection_name || null,
          cast: details.cast || [],
        };
        const created = await mediaAPI.create(payload);
        this.userCollection.push(created);
        return created;
      } catch {
        this.toast('Something went wrong adding to your library.', 'error');
        return null;
      }
    },

    finishAdd(media) {
      const target = this.pickerTarget;
      const entry = {
        mediaId:            media.mediaId,
        media,
        tmdbCollectionId:   media.tmdbCollectionId   || null,
        tmdbCollectionName: media.tmdbCollectionName || null,
      };

      if (target === 'TOP_MOVIES' && this.draft.topMovies.length < MAX) {
        this.draft.topMovies.push(entry);
      } else if (target === 'TOP_TV' && this.draft.topTv.length < MAX) {
        this.draft.topTv.push(entry);
      } else if (target === 'FAV_SERIES' && this.draft.favSeries.length < MAX) {
        this.draft.favSeries.push(entry);
      } else if (target === 'HIDDEN_GEM' && !this.draft.hiddenGem.mediaId) {
        this.draft.hiddenGem.mediaId = media.mediaId;
        this.draft.hiddenGem.media   = media;
      }
    },

    /* ── Reorder / remove ── */
    moveUp(list, i)   { if (i > 0)               [list[i-1], list[i]] = [list[i], list[i-1]]; },
    moveDown(list, i) { if (i < list.length - 1) [list[i+1], list[i]] = [list[i], list[i+1]]; },
    removeAt(list, i) { list.splice(i, 1); },
    clearGem()        { this.draft.hiddenGem = { mediaId: null, media: null, note: '' }; },

    /* ── Save ── */
    async save() {
      this.saving = true;
      try {
        const payload = {
          topMovies: this.draft.topMovies.slice(0, MAX).map((e, i) => ({ mediaId: e.mediaId, rank: i + 1 })),
          topTv:     this.draft.topTv.slice(0, MAX).map((e, i)     => ({ mediaId: e.mediaId, rank: i + 1 })),
          favSeries: this.draft.favSeries.slice(0, MAX).map((e, i) => ({
            mediaId:            e.mediaId            || null,
            tmdbCollectionId:   e.tmdbCollectionId   || null,
            tmdbCollectionName: e.tmdbCollectionName || null,
            rank: i + 1,
          })),
          hiddenGem: this.draft.hiddenGem?.mediaId
            ? { mediaId: this.draft.hiddenGem.mediaId, note: this.draft.hiddenGem.note || '', rank: 1 }
            : null,
        };

        await showcaseAPI.save(payload);

        let updated;
        try { updated = await showcaseAPI.getMine(); }
        catch { updated = { showcase: this.draft }; }

        this.$emit('saved', updated.showcase || this.draft);
        this.close();
        this.toast('Showcase saved!');
      } catch {
        this.toast('Failed to save showcase.', 'error');
      } finally {
        this.saving = false;
      }
    },
  },
};
</script>

<style scoped>
/* ── Card shell ──────────────────────────────────────── */
.editor-card {
  display: flex;
  flex-direction: column;
  max-height: 92vh;
}

/* ── Title bar ───────────────────────────────────────── */
.editor-titlebar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px 12px;
  border-bottom: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  flex-shrink: 0;
}
.editor-titlebar__left {
  display: flex;
  align-items: center;
  gap: 8px;
}
.editor-titlebar__icon {
  color: rgb(var(--v-theme-primary));
  font-size: 0.85rem;
}
.editor-titlebar__text {
  font-size: 1rem;
  font-weight: 800;
  letter-spacing: -0.01em;
}
.editor-close-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: rgba(var(--v-theme-on-surface), 0.07);
  color: rgba(var(--v-theme-on-surface), 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.15s;
}
.editor-close-btn:hover { background: rgba(var(--v-theme-on-surface), 0.14); }

/* ── Scrollable body ─────────────────────────────────── */
.editor-body {
  flex: 1;
  overflow-y: auto;
  padding: 16px 20px 8px !important;
}

/* ── Section ─────────────────────────────────────────── */
.ed-section {
  margin-bottom: 28px;
}
.ed-section__head {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}
.ed-section__dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
.ed-section__title {
  font-size: 0.85rem;
  font-weight: 800;
  letter-spacing: 0.01em;
  flex: 1;
}
.ed-section__count {
  font-size: 0.72rem;
  color: rgba(var(--v-theme-on-surface), 0.45);
  font-weight: 600;
}
.ed-section__hint {
  font-size: 0.73rem;
  color: rgba(var(--v-theme-on-surface), 0.45);
  margin: 0 0 8px;
  padding-left: 16px;
}

/* Add buttons */
.ed-add-btn {
  padding: 4px 10px;
  border-radius: 14px;
  border: none;
  font-size: 0.73rem;
  font-weight: 700;
  cursor: pointer;
  transition: opacity 0.15s;
}
.ed-add-btn:hover { opacity: 0.8; }
.ed-add-btn--gold   { background: rgba(232,168,56,0.15);  color: #E8A838; }
.ed-add-btn--blue   { background: rgba(92,158,255,0.15);  color: #5C9EFF; }
.ed-add-btn--purple { background: rgba(167,139,250,0.15); color: #A78BFA; }
.ed-add-btn--amber  { background: rgba(245,158,11,0.15);  color: #F59E0B; }

/* Empty hint */
.ed-empty {
  padding: 10px 12px;
  border: 1px dashed rgba(var(--v-theme-on-surface), 0.13);
  border-radius: 10px;
  font-size: 0.82rem;
  color: rgba(var(--v-theme-on-surface), 0.45);
}

/* ── List item ───────────────────────────────────────── */
.ed-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.ed-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  border-radius: 10px;
  background: rgba(var(--v-theme-surface-variant), 0.3);
}
.ed-item__rank {
  font-size: 0.68rem;
  font-weight: 900;
  width: 18px;
  text-align: center;
  color: rgba(var(--v-theme-on-surface), 0.35);
  flex-shrink: 0;
}
.ed-item__rank--gold   { color: #E8A838; font-size: 0.8rem; }
.ed-item__rank--blue   { color: #5C9EFF; font-size: 0.8rem; }
.ed-item__rank--purple { color: #A78BFA; font-size: 0.8rem; }

.ed-item__poster {
  width: 38px;
  aspect-ratio: 2/3;
  object-fit: cover;
  border-radius: 5px;
  flex-shrink: 0;
  background: rgba(var(--v-theme-on-surface), 0.07);
}
.ed-item__poster--empty {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
}
.ed-item__info {
  flex: 1;
  min-width: 0;
}
.ed-item__title {
  font-size: 0.82rem;
  font-weight: 700;
  margin: 0;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
.ed-item__sub {
  font-size: 0.68rem;
  color: rgba(var(--v-theme-on-surface), 0.5);
  margin: 1px 0 0;
}
.ed-item__actions {
  display: flex;
  gap: 2px;
  flex-shrink: 0;
}

/* Icon buttons */
.ed-icon-btn {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  border: none;
  background: transparent;
  color: rgba(var(--v-theme-on-surface), 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}
.ed-icon-btn:hover:not(:disabled) {
  background: rgba(var(--v-theme-on-surface), 0.09);
  color: rgba(var(--v-theme-on-surface), 0.9);
}
.ed-icon-btn:disabled { opacity: 0.25; cursor: default; }
.ed-icon-btn--remove:hover:not(:disabled) {
  background: rgba(var(--v-theme-error), 0.12);
  color: rgb(var(--v-theme-error));
}
.ed-icon-btn--overlay {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(0,0,0,0.5);
  color: #fff;
}
.ed-icon-btn--overlay:hover:not(:disabled) {
  background: rgba(var(--v-theme-error), 0.7);
}

/* ── Hidden Gem preview ──────────────────────────────── */
.ed-gem-preview {
  position: relative;
  height: 100px;
  border-radius: 10px;
  overflow: hidden;
}
.ed-gem-preview__bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.ed-gem-preview__bg--fallback {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
}
.ed-gem-preview__scrim {
  position: absolute;
  inset: 0;
  background: linear-gradient(to right, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.45) 60%, transparent 100%);
}
.ed-gem-preview__body {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
}
.ed-gem-preview__poster {
  flex-shrink: 0;
  width: 44px;
  aspect-ratio: 2/3;
  object-fit: cover;
  border-radius: 5px;
  box-shadow: 0 3px 10px rgba(0,0,0,0.5);
}
.ed-gem-preview__info { flex: 1; color: #fff; min-width: 0; }
.ed-gem-preview__title {
  font-size: 0.88rem;
  font-weight: 800;
  margin: 0;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
.ed-gem-preview__year { font-size: 0.7rem; opacity: 0.55; margin: 1px 0 0; }
.ed-gem-note-wrap { /* wrapper for textarea */ }

/* ── Save bar ────────────────────────────────────────── */
.editor-save-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  border-top: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  flex-shrink: 0;
  background: rgb(var(--v-theme-surface));
  gap: 12px;
}
.ed-cancel-btn {
  padding: 9px 18px;
  border-radius: 20px;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.2);
  background: transparent;
  color: rgba(var(--v-theme-on-surface), 0.7);
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}
.ed-cancel-btn:hover { background: rgba(var(--v-theme-on-surface), 0.07); }
.ed-cancel-btn:disabled { opacity: 0.4; cursor: default; }
.ed-save-btn {
  flex: 1;
  padding: 10px 20px;
  border-radius: 20px;
  border: none;
  background: rgb(var(--v-theme-primary));
  color: #fff;
  font-size: 0.88rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: opacity 0.15s;
}
.ed-save-btn:hover:not(:disabled) { opacity: 0.88; }
.ed-save-btn:disabled { opacity: 0.5; cursor: default; }

@media (min-width: 600px) {
  .ed-save-btn { flex: none; min-width: 160px; }
}
</style>
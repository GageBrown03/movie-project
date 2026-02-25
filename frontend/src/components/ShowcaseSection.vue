<template>
  <div class="sc" v-if="isOwn || hasAnyContent">

    <!-- ── Header ── -->
    <div class="sc__header">
      <div>
        <p class="sc__eyebrow">✦ Showcase</p>
        <h2 class="sc__title">{{ isOwn ? 'My Picks' : `${username}'s Picks` }}</h2>
      </div>
      <button v-if="isOwn" class="sc__edit-btn" @click="editorOpen = true">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
        </svg>
        Edit
      </button>
    </div>

    <!-- ── Empty CTA ── -->
    <div v-if="isOwn && !hasAnyContent" class="sc__empty">
      <div class="sc__empty-icon">🎬</div>
      <p class="sc__empty-title">Nothing here yet</p>
      <p class="sc__empty-sub">Curate your all-time favourites for the world to see.</p>
      <button class="sc__cta-btn" @click="editorOpen = true">+ Build My Showcase</button>
    </div>

    <template v-if="hasAnyContent">

      <!-- TOP MOVIES -->
      <div v-if="norm.topMovies.length" class="sc__section">
        <div class="sc__section-head">
          <span class="sc__dot" style="background:#E8A838"></span>
          <span class="sc__section-label">Top Movies</span>
          <span class="sc__section-count">{{ norm.topMovies.length }}</span>
        </div>
        <div class="sc__rail">
          <div
            v-for="(entry, i) in norm.topMovies"
            :key="'m-' + (entry.mediaId || i)"
            class="sc__card"
            @click="navigateTo(entry)"
          >
            <div class="sc__card-art" :class="i === 0 ? 'sc__card-art--gold' : ''">
              <img v-if="entry.media && entry.media.posterUrl" :src="entry.media.posterUrl" class="sc__card-img" loading="lazy" />
              <div v-else class="sc__card-placeholder">🎬</div>
              <span class="sc__badge" :class="i === 0 ? 'sc__badge--gold' : ''">{{ i === 0 ? '★' : i + 1 }}</span>
              <span v-if="entry.media && entry.media.rating" class="sc__user-rating">{{ entry.media.rating }}★</span>
            </div>
            <p class="sc__card-name">{{ (entry.media && entry.media.title) || '—' }}</p>
            <p class="sc__card-year">{{ (entry.media && entry.media.releaseYear) || '' }}</p>
          </div>
        </div>
      </div>

      <!-- TOP TV -->
      <div v-if="norm.topTv.length" class="sc__section">
        <div class="sc__section-head">
          <span class="sc__dot" style="background:#5C9EFF"></span>
          <span class="sc__section-label">Top TV Shows</span>
          <span class="sc__section-count">{{ norm.topTv.length }}</span>
        </div>
        <div class="sc__rail">
          <div
            v-for="(entry, i) in norm.topTv"
            :key="'tv-' + (entry.mediaId || i)"
            class="sc__card"
            @click="navigateTo(entry)"
          >
            <div class="sc__card-art" :class="i === 0 ? 'sc__card-art--blue' : ''">
              <img v-if="entry.media && entry.media.posterUrl" :src="entry.media.posterUrl" class="sc__card-img" loading="lazy" />
              <div v-else class="sc__card-placeholder">📺</div>
              <span class="sc__badge" :class="i === 0 ? 'sc__badge--blue' : ''">{{ i === 0 ? '★' : i + 1 }}</span>
              <span v-if="entry.media && entry.media.rating" class="sc__user-rating">{{ entry.media.rating }}★</span>
            </div>
            <p class="sc__card-name">{{ (entry.media && entry.media.title) || '—' }}</p>
            <p class="sc__card-year">{{ (entry.media && entry.media.releaseYear) || '' }}</p>
          </div>
        </div>
      </div>

      <!-- FAVOURITE SERIES -->
      <div v-if="norm.favSeries.length" class="sc__section">
        <div class="sc__section-head">
          <span class="sc__dot" style="background:#A78BFA"></span>
          <span class="sc__section-label">Favourite Series</span>
          <span class="sc__section-count">{{ norm.favSeries.length }}</span>
        </div>
        <div class="sc__rail">
          <div
            v-for="(entry, i) in norm.favSeries"
            :key="'s-' + (entry.tmdbCollectionId || entry.mediaId || i)"
            class="sc__card"
            @click="navigateTo(entry)"
          >
            <div class="sc__card-art" :class="i === 0 ? 'sc__card-art--purple' : ''">
              <img v-if="entry.media && entry.media.posterUrl" :src="entry.media.posterUrl" class="sc__card-img" loading="lazy" />
              <div v-else class="sc__card-placeholder">🎞️</div>
              <span class="sc__badge" :class="i === 0 ? 'sc__badge--purple' : ''">{{ i === 0 ? '★' : i + 1 }}</span>
            </div>
            <p class="sc__card-name">{{ entry.tmdbCollectionName || (entry.media && entry.media.title) || '—' }}</p>
            <p class="sc__card-year">Series</p>
          </div>
        </div>
      </div>

      <!-- HIDDEN GEM -->
      <div v-if="norm.hiddenGem && norm.hiddenGem.mediaId" class="sc__section">
        <div class="sc__section-head">
          <span class="sc__dot" style="background:#F59E0B"></span>
          <span class="sc__section-label sc__section-label--gem">Hidden Gem</span>
        </div>
        <div class="sc__gem" @click="navigateTo(norm.hiddenGem)">
          <img v-if="norm.hiddenGem.media && norm.hiddenGem.media.backdropUrl" :src="norm.hiddenGem.media.backdropUrl" class="sc__gem-bg" />
          <div v-else class="sc__gem-bg sc__gem-bg--fallback" />
          <div class="sc__gem-scrim" />
          <div class="sc__gem-body">
            <img v-if="norm.hiddenGem.media && norm.hiddenGem.media.posterUrl" :src="norm.hiddenGem.media.posterUrl" class="sc__gem-poster" />
            <div class="sc__gem-text">
              <p class="sc__gem-title">{{ norm.hiddenGem.media && norm.hiddenGem.media.title }}</p>
              <p class="sc__gem-year">{{ norm.hiddenGem.media && norm.hiddenGem.media.releaseYear }}</p>
              <p v-if="norm.hiddenGem.note" class="sc__gem-note">"{{ norm.hiddenGem.note }}"</p>
            </div>
          </div>
        </div>
      </div>

    </template>

    <!-- Editor (mounted only for owner) -->
    <showcase-editor
      v-if="isOwn"
      v-model="editorOpen"
      :current-showcase="norm"
      :media-list="mediaList"
      @saved="onSaved"
    />

  </div>
</template>

<script>
import ShowcaseEditor from '@/components/ShowcaseEditor.vue';

export default {
  name: 'ShowcaseSection',
  components: { ShowcaseEditor },

  props: {
    showcase:  { type: Object, default: () => ({}) },
    isOwn:     { type: Boolean, default: false },
    username:  { type: String,  default: '' },
    mediaList: { type: Array,   default: () => [] },
  },

  emits: ['navigate', 'showcase-saved'],

  data() {
    return { editorOpen: false };
  },

  computed: {
    norm() {
      const s   = this.showcase || {};
      const arr = (a, b) => (Array.isArray(a) ? a : Array.isArray(b) ? b : []);

      const mapE = e => ({
        mediaId:            e.mediaId            ?? e.media_id            ?? e.media?.mediaId ?? null,
        rank:               e.rank               ?? e.order               ?? null,
        tmdbCollectionId:   e.tmdbCollectionId   ?? e.tmdb_collection_id  ?? null,
        tmdbCollectionName: e.tmdbCollectionName ?? e.tmdb_collection_name ?? null,
        media:              e.media              || null,
      });

      const rawGem = s.hiddenGem ?? s.hidden_gem ?? null;
      let hiddenGem = null;
      if (rawGem && typeof rawGem === 'object') {
        const m   = rawGem.media || null;
        const mid = rawGem.mediaId ?? rawGem.media_id ?? m?.mediaId ?? null;
        if (mid) hiddenGem = { mediaId: mid, note: rawGem.note || null, media: m };
      }

      return {
        topMovies:  arr(s.topMovies,  s.top_movies ).map(mapE),
        topTv:      arr(s.topTv,      s.top_tv     ).map(mapE),
        favSeries:  arr(s.favSeries,  s.fav_series ).map(mapE),
        hiddenGem,
      };
    },

    hasAnyContent() {
      const n = this.norm;
      return n.topMovies.length > 0 || n.topTv.length > 0 ||
             n.favSeries.length > 0 || !!(n.hiddenGem?.mediaId);
    },
  },

  methods: {
    navigateTo(entry) {
      const id = entry?.mediaId ?? entry?.media?.mediaId;
      if (id) this.$emit('navigate', id);
    },
    onSaved(updated) {
      this.$emit('showcase-saved', updated);
      this.editorOpen = false;
    },
  },
};
</script>

<style scoped>
/* ── Shell ──────────────────────────────────────────── */
.sc { margin-bottom: 32px; }

/* ── Header ─────────────────────────────────────────── */
.sc__header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: 20px;
  gap: 12px;
}
.sc__eyebrow {
  font-size: 0.6rem;
  font-weight: 800;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: rgb(var(--v-theme-primary));
  margin: 0 0 3px;
}
.sc__title {
  font-size: 1.25rem;
  font-weight: 900;
  letter-spacing: -0.02em;
  margin: 0;
  line-height: 1.1;
}
.sc__edit-btn {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 6px 13px;
  border-radius: 20px;
  background: rgba(var(--v-theme-primary), 0.1);
  color: rgb(var(--v-theme-primary));
  border: 1px solid rgba(var(--v-theme-primary), 0.2);
  font-size: 0.72rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.15s;
  white-space: nowrap;
}
.sc__edit-btn:hover { background: rgba(var(--v-theme-primary), 0.2); }

/* ── Empty ──────────────────────────────────────────── */
.sc__empty {
  text-align: center;
  padding: 44px 20px;
  border: 2px dashed rgba(var(--v-theme-on-surface), 0.1);
  border-radius: 18px;
}
.sc__empty-icon { font-size: 2.4rem; margin-bottom: 10px; }
.sc__empty-title { font-size: 1rem; font-weight: 800; margin: 0 0 6px; }
.sc__empty-sub {
  font-size: 0.82rem;
  color: rgba(var(--v-theme-on-surface), 0.5);
  margin: 0 auto 18px;
  max-width: 280px;
}
.sc__cta-btn {
  padding: 9px 20px;
  border-radius: 20px;
  background: rgb(var(--v-theme-primary));
  color: #fff;
  border: none;
  font-size: 0.82rem;
  font-weight: 700;
  cursor: pointer;
  transition: opacity 0.15s;
}
.sc__cta-btn:hover { opacity: 0.85; }

/* ── Section ────────────────────────────────────────── */
.sc__section { margin-bottom: 20px; }

.sc__section-head {
  display: flex;
  align-items: center;
  gap: 7px;
  margin-bottom: 10px;
}
.sc__dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}
.sc__section-label {
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(var(--v-theme-on-surface), 0.6);
}
.sc__section-label--gem { color: #F59E0B; }
.sc__section-count {
  font-size: 0.62rem;
  font-weight: 700;
  padding: 1px 6px;
  border-radius: 20px;
  background: rgba(var(--v-theme-on-surface), 0.07);
  color: rgba(var(--v-theme-on-surface), 0.38);
}

/* ── Rail ───────────────────────────────────────────── */
.sc__rail {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding-bottom: 4px;
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.sc__rail::-webkit-scrollbar { display: none; }

/* ── Card ───────────────────────────────────────────── */
.sc__card {
  flex-shrink: 0;
  width: 88px;
  cursor: pointer;
  transition: transform 0.17s ease;
}
.sc__card:hover  { transform: translateY(-4px); }
.sc__card:active { transform: translateY(-1px); }

.sc__card-art {
  position: relative;
  width: 88px;
  aspect-ratio: 2 / 3;
  border-radius: 9px;
  overflow: hidden;
  background: rgba(var(--v-theme-on-surface), 0.07);
}

/* Accent rings on rank-1 cards */
.sc__card-art--gold   { box-shadow: 0 0 0 2px #E8A838, 0 4px 16px rgba(232,168,56,0.35); }
.sc__card-art--blue   { box-shadow: 0 0 0 2px #5C9EFF, 0 4px 16px rgba(92,158,255,0.3);  }
.sc__card-art--purple { box-shadow: 0 0 0 2px #A78BFA, 0 4px 16px rgba(167,139,250,0.3); }

.sc__card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.sc__card-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
}

/* Rank badge (top-left) */
.sc__badge {
  position: absolute;
  top: 5px;
  left: 5px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: rgba(0,0,0,0.72);
  color: rgba(255,255,255,0.6);
  font-size: 0.57rem;
  font-weight: 900;
  display: flex;
  align-items: center;
  justify-content: center;
}
.sc__badge--gold   { background: #E8A838; color: #1a0e00; }
.sc__badge--blue   { background: #5C9EFF; color: #fff; }
.sc__badge--purple { background: #A78BFA; color: #fff; }

/* User rating (bottom-right) */
.sc__user-rating {
  position: absolute;
  bottom: 4px;
  right: 4px;
  background: rgba(0,0,0,0.78);
  color: #FFC107;
  font-size: 0.55rem;
  font-weight: 800;
  padding: 2px 4px;
  border-radius: 4px;
  line-height: 1.3;
}

.sc__card-name {
  font-size: 0.68rem;
  font-weight: 700;
  margin: 5px 0 1px;
  line-height: 1.3;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  color: rgba(var(--v-theme-on-surface), 0.88);
}
.sc__card-year {
  font-size: 0.6rem;
  color: rgba(var(--v-theme-on-surface), 0.4);
  margin: 0;
}

@media (min-width: 960px) {
  .sc__card     { width: 108px; }
  .sc__card-art { width: 108px; }
  .sc__rail     { gap: 14px; }
}

/* ── Hidden Gem ─────────────────────────────────────── */
.sc__gem {
  position: relative;
  height: 148px;
  border-radius: 14px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s ease;
}
.sc__gem:hover { transform: scale(1.007); }

.sc__gem-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.sc__gem-bg--fallback {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
}
.sc__gem-scrim {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to right,
    rgba(0,0,0,0.9) 0%,
    rgba(0,0,0,0.55) 55%,
    rgba(0,0,0,0.08) 100%
  );
}
.sc__gem-body {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 18px;
}
.sc__gem-poster {
  flex-shrink: 0;
  width: 58px;
  aspect-ratio: 2/3;
  object-fit: cover;
  border-radius: 7px;
  box-shadow: 0 4px 14px rgba(0,0,0,0.55);
}
.sc__gem-text { flex: 1; color: #fff; min-width: 0; }
.sc__gem-title {
  font-size: 1rem;
  font-weight: 900;
  margin: 0 0 2px;
  text-shadow: 0 1px 4px rgba(0,0,0,0.7);
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
.sc__gem-year { font-size: 0.7rem; opacity: 0.5; margin: 0 0 6px; }
.sc__gem-note {
  font-size: 0.76rem;
  font-style: italic;
  opacity: 0.85;
  margin: 0;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
}

@media (min-width: 600px) {
  .sc__gem        { height: 168px; }
  .sc__gem-poster { width: 74px; }
  .sc__gem-title  { font-size: 1.15rem; }
}
</style>
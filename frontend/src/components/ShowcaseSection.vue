<template>
  <div class="showcase" v-if="hasAnyContent || isOwn">

    <!-- Section header -->
    <div class="showcase__header">
      <div class="showcase__title-group">
        <h2 class="showcase__title">
          <span class="showcase__title-icon">✦</span>
          {{ isOwn ? 'My Showcase' : `${username}'s Showcase` }}
        </h2>
        <p class="showcase__subtitle">Curated picks</p>
      </div>
      <v-btn
        v-if="isOwn"
        variant="tonal"
        color="primary"
        size="small"
        prepend-icon="mdi-pencil"
        @click="editorOpen = true"
      >
        Edit Showcase
      </v-btn>
    </div>

    <!-- Empty own showcase CTA -->
    <div v-if="isOwn && !hasAnyContent" class="showcase__empty-own">
      <div class="showcase__empty-icon">🎬</div>
      <p class="showcase__empty-title">Your showcase is empty</p>
      <p class="showcase__empty-sub">Pin your all-time favourites so friends can see what defines your taste.</p>
      <v-btn color="primary" prepend-icon="mdi-plus" @click="editorOpen = true">
        Build My Showcase
      </v-btn>
    </div>

    <template v-if="hasAnyContent">
      <!-- TOP MOVIES & TOP TV side by side -->
      <div class="showcase__row">
        <showcase-list
          v-if="showcase.topMovies?.length"
          title="Top Movies"
          icon="mdi-movie"
          accent="#E8A838"
          :items="showcase.topMovies"
          @item-click="navigateTo"
        />
        <showcase-list
          v-if="showcase.topTv?.length"
          title="Top TV"
          icon="mdi-television-play"
          accent="#5C9EFF"
          :items="showcase.topTv"
          @item-click="navigateTo"
        />
      </div>

      <!-- FAVORITE SERIES -->
      <showcase-list
        v-if="showcase.favSeries?.length"
        title="Favourite Series"
        icon="mdi-film-strip"
        accent="#A78BFA"
        :items="showcase.favSeries"
        layout="series"
        @item-click="navigateTo"
        class="mt-6"
      />

      <!-- HIDDEN GEM -->
      <div v-if="showcase.hiddenGem" class="showcase__gem mt-6">
        <div class="showcase__gem-label">
          <v-icon size="14" color="amber">mdi-diamond-stone</v-icon>
          Hidden Gem
        </div>
        <div class="showcase__gem-inner" @click="navigateTo(showcase.hiddenGem)">
          <v-img
            v-if="showcase.hiddenGem.media?.backdropUrl"
            :src="showcase.hiddenGem.media.backdropUrl"
            cover
            class="showcase__gem-backdrop"
          />
          <div class="showcase__gem-backdrop showcase__gem-backdrop--fallback"
               v-else />
          <div class="showcase__gem-overlay" />
          <div class="showcase__gem-content">
            <v-img
              v-if="showcase.hiddenGem.media?.posterUrl"
              :src="showcase.hiddenGem.media.posterUrl"
              width="72"
              class="showcase__gem-poster rounded elevation-4"
            />
            <div class="showcase__gem-text">
              <p class="showcase__gem-title">{{ showcase.hiddenGem.media?.title }}</p>
              <p class="showcase__gem-year">{{ showcase.hiddenGem.media?.releaseYear }}</p>
              <p v-if="showcase.hiddenGem.note" class="showcase__gem-note">
                <v-icon size="12" class="mr-1">mdi-format-quote-open</v-icon>
                {{ showcase.hiddenGem.note }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </template>
  <!-- Showcase Editor — lives here, opened by buttons above -->
  <showcase-editor
    v-if="isOwn"
    v-model="editorOpen"
    :current-showcase="showcase"
    :media-list="mediaList"
    @saved="onShowcaseSaved"
  />

  </div>
</template>

<script>
import ShowcaseEditor from '@/components/ShowcaseEditor.vue';

const ShowcaseList = {
  name: 'ShowcaseList',
  props: {
    title: String,
    icon: String,
    accent: String,
    items: Array,
    layout: { type: String, default: 'ranked' },
  },
  emits: ['item-click'],
  template: `
    <div class="sclist">
      <div class="sclist__header">
        <v-icon :color="accent" size="16" class="mr-1">{{ icon }}</v-icon>
        <span class="sclist__title" :style="{ color: accent }">{{ title }}</span>
      </div>
      <div class="sclist__items" :class="'sclist__items--' + layout">
        <div
          v-for="(entry, i) in items"
          :key="entry.id || i"
          class="sclist__item"
          :class="{ 'sclist__item--top': i === 0 }"
          @click="$emit('item-click', entry)"
          :title="entry.media?.title || entry.tmdbCollectionName"
        >
          <div class="sclist__rank" :style="i === 0 ? { color: accent } : {}">
            {{ i === 0 ? '★' : i + 1 }}
          </div>
          <div class="sclist__poster-wrap">
            <v-img
              v-if="entry.media?.posterUrl"
              :src="entry.media.posterUrl"
              cover
              class="sclist__poster"
              aspect-ratio="0.667"
            />
            <div v-else class="sclist__poster sclist__poster--empty">
              <v-icon color="grey" size="20">mdi-movie-outline</v-icon>
            </div>
            <div v-if="entry.media?.rating" class="sclist__rating">
              {{ entry.media.rating }}★
            </div>
          </div>
          <div class="sclist__info">
            <p class="sclist__name">
              {{ layout === 'series'
                ? (entry.tmdbCollectionName || entry.media?.title)
                : entry.media?.title }}
            </p>
            <p class="sclist__year">{{ entry.media?.releaseYear || '—' }}</p>
          </div>
        </div>
      </div>
    </div>
  `,
};

export default {
  name: 'ShowcaseSection',

  components: { ShowcaseList, ShowcaseEditor },

  props: {
    showcase: {
      type: Object,
      default: () => ({
        topMovies: [],
        topTv: [],
        favSeries: [],
        hiddenGem: null,
      }),
    },
    isOwn: { type: Boolean, default: false },
    username: { type: String, default: '' },
    mediaList: { type: Array, default: () => [] },
  },

  emits: ['navigate', 'showcase-saved'],

  data() {
    return {
      editorOpen: false,
    };
  },

  computed: {
    hasAnyContent() {
      if (!this.showcase) return false;
      return (
        this.showcase.topMovies?.length ||
        this.showcase.topTv?.length ||
        this.showcase.favSeries?.length ||
        this.showcase.hiddenGem
      );
    },
  },

  methods: {
    navigateTo(entry) {
      if (entry?.mediaId) {
        this.$emit('navigate', entry.mediaId);
      }
    },
    onShowcaseSaved(newShowcase) {
      this.$emit('showcase-saved', newShowcase);
      this.editorOpen = false;
    },
  },
};
</script>

<style scoped>
/* ── Section shell ───────────────────────────────────────── */
.showcase {
  margin-bottom: 32px;
}

.showcase__header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: 20px;
}

.showcase__title {
  font-size: 1.25rem;
  font-weight: 800;
  letter-spacing: -0.01em;
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
}

.showcase__title-icon {
  color: rgb(var(--v-theme-primary));
  font-size: 0.9rem;
}

.showcase__subtitle {
  font-size: 0.75rem;
  color: rgba(var(--v-theme-on-surface), 0.45);
  margin: 2px 0 0;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

/* ── Empty state (own profile) ───────────────────────────── */
.showcase__empty-own {
  text-align: center;
  padding: 48px 24px;
  border: 2px dashed rgba(var(--v-theme-on-surface), 0.12);
  border-radius: 16px;
}

.showcase__empty-icon { font-size: 3rem; margin-bottom: 12px; }
.showcase__empty-title {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 6px;
}
.showcase__empty-sub {
  color: rgba(var(--v-theme-on-surface), 0.5);
  font-size: 0.875rem;
  margin-bottom: 20px;
  max-width: 380px;
  margin-left: auto;
  margin-right: auto;
}

/* ── Row layout for Movies + TV ──────────────────────────── */
.showcase__row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 24px;
}

/* ── Showcase list sub-component ─────────────────────────── */
:deep(.sclist) {
  background: rgba(var(--v-theme-surface-variant), 0.35);
  border-radius: 16px;
  padding: 16px;
}

:deep(.sclist__header) {
  display: flex;
  align-items: center;
  margin-bottom: 14px;
}

:deep(.sclist__title) {
  font-size: 0.8rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

:deep(.sclist__items) {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

:deep(.sclist__items--series) {
  flex-direction: row;
  flex-wrap: wrap;
  gap: 12px;
}

:deep(.sclist__item) {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  border-radius: 10px;
  padding: 4px;
  transition: background 0.15s ease;
}

:deep(.sclist__item:hover) {
  background: rgba(var(--v-theme-on-surface), 0.06);
}

:deep(.sclist__items--series .sclist__item) {
  flex-direction: column;
  align-items: flex-start;
  width: 90px;
}

:deep(.sclist__item--top .sclist__rank) {
  font-size: 1rem;
}

:deep(.sclist__rank) {
  font-size: 0.75rem;
  font-weight: 800;
  width: 20px;
  text-align: center;
  color: rgba(var(--v-theme-on-surface), 0.35);
  flex-shrink: 0;
}

:deep(.sclist__poster-wrap) {
  position: relative;
  flex-shrink: 0;
}

:deep(.sclist__poster) {
  width: 44px;
  border-radius: 6px;
  overflow: hidden;
}

:deep(.sclist__items--series .sclist__poster) {
  width: 90px;
}

:deep(.sclist__poster--empty) {
  width: 44px;
  aspect-ratio: 2/3;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(var(--v-theme-on-surface), 0.07);
  border-radius: 6px;
}

:deep(.sclist__items--series .sclist__poster--empty) {
  width: 90px;
}

:deep(.sclist__rating) {
  position: absolute;
  bottom: 2px;
  right: 2px;
  background: rgba(0,0,0,0.7);
  color: #FFC107;
  font-size: 0.6rem;
  font-weight: 800;
  padding: 1px 4px;
  border-radius: 4px;
  line-height: 1.4;
}

:deep(.sclist__info) { flex: 1; min-width: 0; }

:deep(.sclist__name) {
  font-size: 0.82rem;
  font-weight: 600;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

:deep(.sclist__items--series .sclist__name) {
  white-space: normal;
  font-size: 0.72rem;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

:deep(.sclist__year) {
  font-size: 0.7rem;
  color: rgba(var(--v-theme-on-surface), 0.45);
  margin: 1px 0 0;
}

/* ── Hidden Gem ──────────────────────────────────────────── */
.showcase__gem-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.75rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #F59E0B;
  margin-bottom: 10px;
}

.showcase__gem-inner {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  height: 160px;
  transition: transform 0.2s ease;
}

.showcase__gem-inner:hover { transform: scale(1.01); }

.showcase__gem-backdrop {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.showcase__gem-backdrop--fallback {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
}

.showcase__gem-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to right,
    rgba(0,0,0,0.82) 0%,
    rgba(0,0,0,0.5) 60%,
    rgba(0,0,0,0.1) 100%
  );
}

.showcase__gem-content {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
}

.showcase__gem-poster {
  flex-shrink: 0;
  border-radius: 8px !important;
  overflow: hidden;
}

.showcase__gem-text { flex: 1; color: white; }

.showcase__gem-title {
  font-size: 1.15rem;
  font-weight: 800;
  margin: 0 0 2px;
  text-shadow: 0 1px 4px rgba(0,0,0,0.5);
}

.showcase__gem-year {
  font-size: 0.8rem;
  opacity: 0.65;
  margin: 0 0 8px;
}

.showcase__gem-note {
  font-size: 0.85rem;
  font-style: italic;
  opacity: 0.9;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
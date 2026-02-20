<template>
  <div class="home">

    <!-- ═══════════════════════════════════════════════ -->
    <!-- GUEST SPLASH (not logged in)                    -->
    <!-- ═══════════════════════════════════════════════ -->
    <div v-if="!isLoggedIn" class="splash">
      <div class="splash__hero">
        <div class="splash__glow" />
        <p class="splash__eyebrow">Your personal cinema</p>
        <h1 class="splash__headline">
          Track every title.<br />
          <span class="splash__headline--accent">Never forget what to watch.</span>
        </h1>
        <p class="splash__sub">
          Rate movies, build your watchlist, explore new picks, and see exactly what you've been watching.
        </p>
        <div class="splash__ctas">
          <v-btn
            to="/login"
            size="x-large"
            color="primary"
            variant="flat"
            class="splash__btn-primary font-weight-bold"
            elevation="8"
          >
            Sign In
          </v-btn>
          <v-btn
            to="/register"
            size="x-large"
            variant="outlined"
            class="splash__btn-secondary font-weight-medium"
          >
            Create Account
          </v-btn>
        </div>
      </div>

      <!-- Feature highlights -->
      <div class="splash__features">
        <div
          v-for="feat in guestFeatures"
          :key="feat.title"
          class="feat-card"
          :style="{ '--feat-color': feat.color }"
        >
          <div class="feat-card__icon-wrap">
            <v-icon size="32" :color="feat.color">{{ feat.icon }}</v-icon>
          </div>
          <h3 class="feat-card__title">{{ feat.title }}</h3>
          <p class="feat-card__desc">{{ feat.desc }}</p>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════ -->
    <!-- LOGGED IN                                       -->
    <!-- ═══════════════════════════════════════════════ -->
    <template v-else>

      <!-- Hero -->
      <div class="hero-section">
        <h1 class="text-h3 font-weight-bold mb-2">
          Welcome back{{ currentUser ? ', ' + currentUser.username : '' }}!
        </h1>
        <div v-if="activityStats" class="stats-summary text-h6 text-medium-emphasis mb-4">
          <span class="stat-item">
            <v-icon size="small" class="mr-1">mdi-film</v-icon>
            {{ activityStats.totalRated }}
          </span>
          <span class="stat-divider">•</span>
          <span class="stat-item">
            <v-icon size="small" class="mr-1">mdi-bookmark</v-icon>
            {{ activityStats.totalWatchlist }}
          </span>
          <span class="stat-divider">•</span>
          <span class="stat-item">
            <v-icon size="small" class="mr-1">mdi-account-group</v-icon>
            {{ activityStats.totalFriends }}
          </span>
        </div>
      </div>

      <!-- NEW USER EMPTY STATE -->
      <div v-if="!loading && stats.total === 0" class="new-user-empty">
        <div class="new-user-empty__glow" />
        <v-icon size="64" color="primary" class="mb-4" style="opacity:0.7">mdi-movie-open-star-outline</v-icon>
        <h2 class="text-h4 font-weight-black mb-3">Your collection is empty</h2>
        <p class="text-body-1 text-medium-emphasis mb-6" style="max-width:440px; margin-inline: auto;">
          Add your first movie or show to get started. Your ratings, watchlist, and stats will appear here.
        </p>
        <v-btn
          size="x-large"
          color="primary"
          variant="flat"
          prepend-icon="mdi-plus"
          class="font-weight-bold px-8"
          elevation="6"
          @click="openAddDialog"
        >
          Add Your First Title
        </v-btn>
      </div>

      <!-- RETURNING USER CONTENT -->
      <template v-else>
        <!-- Activity Feed -->
        <v-row class="mt-4">
          <v-col cols="12">
            <activity-feed
              ref="activityFeed"
              @add-media="openAddDialog"
            />
          </v-col>
        </v-row>

        <!-- ─── Feature Cards ─── -->
        <div class="feature-section mt-10 mb-8">
          <h2 class="text-overline text-medium-emphasis mb-5 feature-section__label">Explore</h2>
          <div class="feature-grid">
            <a
              v-for="feat in userFeatures"
              :key="feat.title"
              class="feature-tile"
              :style="{ '--tile-color': feat.color, '--tile-rgb': feat.rgb }"
              @click="$router.push(feat.route)"
            >
              <div class="feature-tile__accent" />
              <div class="feature-tile__body">
                <div class="feature-tile__icon-wrap">
                  <v-icon size="36" :style="{ color: feat.color }">{{ feat.icon }}</v-icon>
                </div>
                <div class="feature-tile__text">
                  <h3 class="feature-tile__title">{{ feat.title }}</h3>
                  <p class="feature-tile__desc">{{ feat.desc }}</p>
                </div>
              </div>
              <div class="feature-tile__arrow">
                <v-icon size="20" :style="{ color: feat.color }">mdi-arrow-right</v-icon>
              </div>
            </a>
          </div>
        </div>
      </template>

    </template>
  </div>
</template>

<script>
import { mediaAPI, activityAPI } from '@/services/api-production';
import ActivityFeed from '@/components/ActivityFeed.vue';

export default {
  name: 'HomeView',

  components: {
    ActivityFeed
  },

  data() {
    return {
      loading: true,
      stats: {
        total: 0,
        watched: 0,
        watchlist: 0,
        averageRating: 0,
      },
      activityStats: null,
      currentUser: null,

      // Guest feature highlights
      guestFeatures: [
        {
          icon: 'mdi-star-outline',
          title: 'Rate & Track',
          desc: 'Log every movie and show you watch. Rate them, mark status, and never lose track.',
          color: '#FFC107',
        },
        {
          icon: 'mdi-compass-outline',
          title: 'Discover',
          desc: 'Get personalised suggestions across genres — from hidden gems to new releases.',
          color: '#7C4DFF',
        },
        {
          icon: 'mdi-chart-line',
          title: 'Your Analytics',
          desc: 'See your watching habits, top genres, and ratings history at a glance.',
          color: '#00BCD4',
        },
      ],

      // Logged-in quick-access feature cards
      userFeatures: [
        {
          icon: 'mdi-chart-line',
          title: 'Analytics',
          desc: 'Deep dive into your watching habits and patterns',
          route: '/analytics',
          color: '#00BCD4',
          rgb: '0,188,212',
        },
        {
          icon: 'mdi-compass-outline',
          title: 'Discover',
          desc: 'Personalised picks across genres you love',
          route: '/discover',
          color: '#7C4DFF',
          rgb: '124,77,255',
        },
        {
          icon: 'mdi-dice-5',
          title: 'What to Watch?',
          desc: 'Let us randomly pick from your watchlist',
          route: '/random',
          color: '#FF6D00',
          rgb: '255,109,0',
        },
      ],
    };
  },

  computed: {
    isLoggedIn() {
      return !!localStorage.getItem('token');
    },
  },

  created() {
    if (this.isLoggedIn) {
      this.loadStats();
      this.loadActivityStats();
      this.loadCurrentUser();
    }
  },

  methods: {
    async loadStats() {
      this.loading = true;
      try {
        const mediaList = await mediaAPI.getAll();
        this.stats.total = mediaList.length;
        this.stats.watched = mediaList.filter(m => m.status === 'watched').length;
        this.stats.watchlist = mediaList.filter(m => m.status === 'want_to_watch').length;
        const ratedMedia = mediaList.filter(m => m.rating);
        this.stats.averageRating = ratedMedia.length > 0
          ? ratedMedia.reduce((sum, m) => sum + m.rating, 0) / ratedMedia.length
          : 0;
      } catch (err) {
        console.log('No media yet or error loading:', err);
      } finally {
        this.loading = false;
      }
    },

    async loadActivityStats() {
      try {
        this.activityStats = await activityAPI.getStats();
      } catch (err) {
        console.log('Error loading activity stats:', err);
      }
    },

    loadCurrentUser() {
      const userStr = localStorage.getItem('user');
      if (userStr) {
        try {
          this.currentUser = JSON.parse(userStr);
        } catch (err) {
          console.error('Error parsing user:', err);
        }
      }
    },

    openAddDialog() {
      window.dispatchEvent(new CustomEvent('open-add-media-dialog'));
    },

    refreshFeed() {
      if (this.$refs.activityFeed) {
        this.$refs.activityFeed.refresh();
      }
      this.loadStats();
      this.loadActivityStats();
    }
  }
};
</script>

<style scoped>
/* ─── Layout ──────────────────────────────────────────── */
.home {
  max-width: 1400px;
  margin: 0 auto;
  padding: 40px 20px;
}

/* ─── Guest Splash ────────────────────────────────────── */
.splash {
  min-height: calc(100vh - 120px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 60px 0 80px;
}

.splash__hero {
  position: relative;
  text-align: center;
  max-width: 680px;
  margin: 0 auto 80px;
}

.splash__glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -60%);
  width: 500px;
  height: 300px;
  background: radial-gradient(ellipse, rgba(var(--v-theme-primary), 0.15) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}

.splash__eyebrow {
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: rgb(var(--v-theme-primary));
  margin-bottom: 16px;
  position: relative;
  z-index: 1;
}

.splash__headline {
  font-size: clamp(2.2rem, 5vw, 3.5rem);
  font-weight: 900;
  line-height: 1.1;
  letter-spacing: -0.02em;
  margin-bottom: 20px;
  position: relative;
  z-index: 1;
}

.splash__headline--accent {
  color: rgb(var(--v-theme-primary));
}

.splash__sub {
  font-size: 1.1rem;
  color: rgba(var(--v-theme-on-surface), 0.65);
  max-width: 480px;
  margin: 0 auto 36px;
  line-height: 1.65;
  position: relative;
  z-index: 1;
}

.splash__ctas {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
  position: relative;
  z-index: 1;
}

.splash__btn-primary {
  min-width: 140px;
  letter-spacing: 0.03em;
}

.splash__btn-secondary {
  min-width: 140px;
  border-color: rgba(var(--v-theme-on-surface), 0.2) !important;
}

/* Guest feature cards */
.splash__features {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  max-width: 900px;
  margin: 0 auto;
}

.feat-card {
  background: rgba(var(--v-theme-surface-variant), 0.4);
  border: 1px solid rgba(var(--v-theme-on-surface), 0.08);
  border-radius: 16px;
  padding: 28px 24px;
  transition: border-color 0.25s, transform 0.25s;
}

.feat-card:hover {
  border-color: var(--feat-color);
  transform: translateY(-4px);
}

.feat-card__icon-wrap {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  background: color-mix(in srgb, var(--feat-color) 12%, transparent);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

.feat-card__title {
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 8px;
}

.feat-card__desc {
  font-size: 0.875rem;
  color: rgba(var(--v-theme-on-surface), 0.6);
  line-height: 1.55;
  margin: 0;
}

/* ─── Logged-in Hero ──────────────────────────────────── */
.hero-section {
  text-align: center;
  padding: 20px 0 32px;
}

.stats-summary {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.stat-item {
  display: inline-flex;
  align-items: center;
}

.stat-divider {
  opacity: 0.4;
}

/* ─── New User Empty State ────────────────────────────── */
.new-user-empty {
  position: relative;
  text-align: center;
  padding: 100px 20px;
  border-radius: 24px;
  background: rgba(var(--v-theme-surface-variant), 0.2);
  border: 1px dashed rgba(var(--v-theme-on-surface), 0.1);
  overflow: hidden;
}

.new-user-empty__glow {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at center, rgba(var(--v-theme-primary), 0.07) 0%, transparent 65%);
  pointer-events: none;
}

/* ─── Feature Section (Explore) ──────────────────────── */
.feature-section__label {
  display: block;
  font-size: 0.72rem;
  letter-spacing: 0.12em;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.feature-tile {
  position: relative;
  background: rgba(var(--v-theme-surface-variant), 0.35);
  border: 1px solid rgba(var(--v-theme-on-surface), 0.07);
  border-radius: 18px;
  padding: 28px 24px 24px;
  cursor: pointer;
  overflow: hidden;
  transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
  text-decoration: none;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Colored top accent bar */
.feature-tile__accent {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--tile-color);
  opacity: 0;
  transition: opacity 0.25s ease;
}

.feature-tile:hover .feature-tile__accent {
  opacity: 1;
}

.feature-tile:hover {
  transform: translateY(-5px);
  border-color: color-mix(in srgb, var(--tile-color) 30%, transparent);
  box-shadow: 0 12px 40px rgba(var(--tile-rgb), 0.12);
}

.feature-tile__body {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.feature-tile__icon-wrap {
  flex-shrink: 0;
  width: 60px;
  height: 60px;
  border-radius: 16px;
  background: rgba(var(--tile-rgb), 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.25s;
}

.feature-tile:hover .feature-tile__icon-wrap {
  background: rgba(var(--tile-rgb), 0.18);
}

.feature-tile__text {
  flex: 1;
}

.feature-tile__title {
  font-size: 1.05rem;
  font-weight: 700;
  margin-bottom: 6px;
  line-height: 1.2;
}

.feature-tile__desc {
  font-size: 0.85rem;
  color: rgba(var(--v-theme-on-surface), 0.58);
  line-height: 1.5;
  margin: 0;
}

.feature-tile__arrow {
  align-self: flex-end;
  opacity: 0;
  transform: translateX(-6px);
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.feature-tile:hover .feature-tile__arrow {
  opacity: 1;
  transform: translateX(0);
}

/* ─── Mobile ──────────────────────────────────────────── */
@media (max-width: 960px) {
  .home {
    padding: 20px 16px;
  }

  .splash {
    padding: 40px 0 60px;
    min-height: unset;
  }

  .splash__hero {
    margin-bottom: 48px;
  }

  .splash__features {
    grid-template-columns: 1fr;
    gap: 12px;
    max-width: 480px;
  }

  .feature-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .feature-tile {
    padding: 20px 18px;
  }

  .feature-tile__arrow {
    display: none;
  }
}

@media (min-width: 600px) and (max-width: 960px) {
  .splash__features {
    grid-template-columns: 1fr 1fr;
    max-width: 640px;
  }

  .feature-grid {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
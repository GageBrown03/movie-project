<template>
  <div class="user-profile-view">
    <!-- Back Button -->
    <v-btn
      variant="text"
      prepend-icon="mdi-arrow-left"
      @click="$router.back()"
      class="mb-4"
    >
      Back
    </v-btn>

    <!-- Loading State -->
    <v-row v-if="loading" justify="center" class="my-12">
      <v-progress-circular indeterminate size="64" color="primary" />
    </v-row>

    <!-- Error State -->
    <v-alert v-else-if="error" type="error" variant="tonal" class="mb-6">
      {{ error }}
      <template v-slot:append>
        <v-btn variant="text" @click="loadProfile">Retry</v-btn>
      </template>
    </v-alert>

    <!-- Profile Content -->
    <div v-else-if="profile">
      <!-- Profile Header -->
      <v-card class="mb-6" elevation="2">
        <v-card-text>
          <div class="d-flex align-center">
            <!-- Avatar -->
            <v-avatar color="primary" size="80" class="mr-4">
              <span class="text-h3 text-white">
                {{ profile.username[0].toUpperCase() }}
              </span>
            </v-avatar>

            <!-- User Info -->
            <div class="flex-grow-1">
              <h1 class="text-h4 font-weight-bold">{{ profile.username }}</h1>
              <p v-if="profile.displayName" class="text-h6 text-medium-emphasis mb-2">
                {{ profile.displayName }}
              </p>
              <p v-if="profile.bio" class="text-body-1 mb-3">
                {{ profile.bio }}
              </p>

              <!-- Stats (if visible) -->
              <div v-if="profile.stats" class="d-flex align-center gap-4 flex-wrap">
                <v-chip prepend-icon="mdi-star" variant="text">
                  {{ profile.stats.totalRated }} rated
                </v-chip>
                <v-chip prepend-icon="mdi-bookmark" variant="text">
                  {{ profile.stats.totalWatchlist }} watchlist
                </v-chip>
                <v-chip prepend-icon="mdi-account-group" variant="text">
                  {{ profile.stats.totalFriends }} friends
                </v-chip>
              </div>
            </div>

            <!-- Actions (if not viewing own profile) -->
            <div v-if="!isOwnProfile" class="d-flex flex-column gap-2">
              <v-btn
                v-if="profile.areFriends && profile.privacy.canViewRatings"
                color="primary"
                prepend-icon="mdi-chart-bar"
                @click="goToCompare"
              >
                Compare Ratings
              </v-btn>
              <v-btn
                v-if="profile.privacy.canViewCollection"
                variant="outlined"
                prepend-icon="mdi-folder-open"
                @click="currentTab = 'collection'"
              >
                View Full Library
              </v-btn>
            </div>
          </div>
        </v-card-text>
      </v-card>

      <!-- Showcase Section -->
      <showcase-section
        v-if="profile.privacy.canViewRatings || isOwnProfile"
        :showcase="showcase"
        :is-own="!!isOwnProfile"
        :username="profile.username"
        class="mb-4"
        @edit="showcaseEditorOpen = true"
        @navigate="id => $router.push('/media/' + id)"
      />

      <!-- Showcase Editor (own profile only) -->
      <showcase-editor
        v-if="isOwnProfile"
        v-model="showcaseEditorOpen"
        :current-showcase="showcase"
        :media-list="profile.media || []"
        @saved="showcase = $event"
      />

      <!-- Privacy Message (if limited access) -->
      <v-alert
        v-if="!profile.privacy.canViewStats && !profile.privacy.canViewCollection"
        type="info"
        variant="tonal"
        class="mb-6"
      >
        <div class="d-flex align-center">
          <v-icon start>mdi-lock</v-icon>
          <div>
            <div class="font-weight-bold">This profile is private</div>
            <div class="text-caption">{{ profile.username }} has restricted their profile visibility</div>
          </div>
        </div>
      </v-alert>

      <!-- Tabs -->
      <v-tabs v-model="currentTab" color="primary" class="mb-4">
        <v-tab value="analytics" v-if="profile.privacy.canViewStats">
          <v-icon start>mdi-chart-line</v-icon>
          Analytics
        </v-tab>
        <v-tab value="activity" v-if="profile.privacy.canViewStats">
          <v-icon start>mdi-history</v-icon>
          Activity
        </v-tab>
        <v-tab value="top-rated" v-if="profile.privacy.canViewRatings">
          <v-icon start>mdi-star-circle</v-icon>
          Top Rated
        </v-tab>
        <v-tab value="collection" v-if="profile.privacy.canViewCollection">
          <v-icon start>mdi-folder-open</v-icon>
          Full Library
        </v-tab>
      </v-tabs>

      <!-- Tab Content -->
      <v-window v-model="currentTab">
        <!-- Analytics Tab -->
        <v-window-item value="analytics">
          <user-analytics
            v-if="profile.media"
            :media-list="profile.media"
            :username="profile.username"
          />
        </v-window-item>

        <!-- Activity Tab -->
        <v-window-item value="activity">
          <user-activity-feed
            :user-id="profile.userId"
            :username="profile.username"
          />
        </v-window-item>

        <!-- Top Rated Tab -->
        <v-window-item value="top-rated">
          <top-rated-movies
            v-if="profile.media"
            :media-list="profile.media"
            :username="profile.username"
          />
        </v-window-item>

        <!-- Full Library Tab -->
        <v-window-item value="collection">
          <user-collection
            v-if="profile.media"
            :media-list="profile.media"
            :username="profile.username"
            :can-view-ratings="profile.privacy.canViewRatings"
          />
        </v-window-item>
      </v-window>
    </div>
  </div>
</template>

<script>
import UserAnalytics from '@/components/UserAnalytics.vue';
import UserActivityFeed from '@/components/UserActivityFeed.vue';
import TopRatedMovies from '@/components/TopRatedMovies.vue';
import UserCollection from '@/components/UserCollection.vue';
import ShowcaseSection from '@/components/ShowcaseSection.vue';
import ShowcaseEditor from '@/components/ShowcaseEditor.vue';
import { showcaseAPI } from '@/services/showcase-api';

const API_BASE = process.env.VUE_APP_API_BASE_URL || 'http://localhost:5000';

export default {
  name: 'UserProfileView',

  components: {
    UserAnalytics,
    UserActivityFeed,
    TopRatedMovies,
    UserCollection,
    ShowcaseSection,
    ShowcaseEditor,
  },

  data() {
    return {
      loading: false,
      error: null,
      profile: null,
      currentTab: 'analytics',
      showcase: null,
      showcaseEditorOpen: false,
    };
  },

  computed: {
    username() {
      return this.$route.params.username;
    },
    // Computed locally — don't trust isOwnProfile alone since backend may not set it
    isOwnProfile() {
      const stored = localStorage.getItem('username');
      return !!(this.profile?.isMe || (stored && stored === this.username));
    },
  },

  watch: {
    username() {
      this.loadProfile();
    }
  },

  created() {
    this.loadProfile();
  },

  methods: {
    async loadProfile() {
      this.loading = true;
      this.error = null;

      try {
        const response = await fetch(`${API_BASE}/api/users/${this.username}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (!response.ok) {
          if (response.status === 404) {
            throw new Error('User not found');
          }
          throw new Error('Failed to load profile');
        }

        this.profile = await response.json();

        // Load showcase if viewer has ratings access
        if (this.profile.privacy.canViewRatings || this.isOwnProfile) {
          this.loadShowcase();
        }

        // Set default tab based on what's available
        if (this.profile.privacy.canViewStats) {
          this.currentTab = 'analytics';
        } else if (this.profile.privacy.canViewRatings) {
          this.currentTab = 'top-rated';
        } else if (this.profile.privacy.canViewCollection) {
          this.currentTab = 'collection';
        }
      } catch (err) {
        console.error('Error loading profile:', err);
        this.error = err.message || 'Failed to load profile';
      } finally {
        this.loading = false;
      }
    },

    async loadShowcase() {
      try {
        const result = await showcaseAPI.getByUsername(this.username);
        this.showcase = result.showcase;
      } catch (err) {
        console.warn('Could not load showcase:', err);
      }
    },

    goToCompare() {
      this.$router.push(`/compare/${this.username}`);
    }
  }
};
</script>

<style scoped>
.user-profile-view {
  max-width: 1400px;
  margin: 0 auto;
}

.gap-2 {
  gap: 8px;
}

.gap-4 {
  gap: 16px;
}
</style>
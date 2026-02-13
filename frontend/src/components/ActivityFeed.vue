<template>
  <div class="activity-feed">
    <!-- Feed Header -->
    <div class="feed-header mb-4">
      <h2 class="text-h5 font-weight-bold">Activity Feed</h2>
      
      <!-- Filter Buttons -->
      <v-btn-toggle
        v-model="currentFilter"
        mandatory
        density="compact"
        color="primary"
        class="mt-3"
      >
        <v-btn value="all" size="small">
          <v-icon start size="small">mdi-earth</v-icon>
          All
        </v-btn>
        <v-btn value="me" size="small">
          <v-icon start size="small">mdi-account</v-icon>
          Me
        </v-btn>
        <v-btn value="friends" size="small">
          <v-icon start size="small">mdi-account-group</v-icon>
          Friends
        </v-btn>
      </v-btn-toggle>
    </div>

    <!-- Loading State -->
    <div v-if="loading && activities.length === 0" class="text-center py-12">
      <v-progress-circular indeterminate color="primary" size="64" />
      <p class="text-body-1 mt-4 text-medium-emphasis">Loading activities...</p>
    </div>

    <!-- Error State -->
    <v-alert
      v-else-if="error"
      type="error"
      variant="tonal"
      class="mb-4"
    >
      {{ error }}
      <template v-slot:append>
        <v-btn variant="text" @click="loadActivities">Retry</v-btn>
      </template>
    </v-alert>

    <!-- Empty State -->
    <v-empty-state
      v-else-if="!loading && activities.length === 0"
      icon="mdi-rss"
      :title="emptyStateTitle"
      :text="emptyStateText"
      class="my-8"
    >
      <template v-slot:actions>
        <v-btn
          v-if="currentFilter === 'all' || currentFilter === 'me'"
          color="primary"
          size="large"
          @click="$emit('add-media')"
        >
          <v-icon start>mdi-plus-circle</v-icon>
          Add Your First Movie
        </v-btn>
        <v-btn
          v-else-if="currentFilter === 'friends'"
          color="secondary"
          size="large"
          to="/friends"
        >
          <v-icon start>mdi-account-plus</v-icon>
          Find Friends
        </v-btn>
      </template>
    </v-empty-state>

    <!-- Activity List -->
    <div v-else class="activity-list">
      <activity-card
        v-for="activity in displayedActivities"
        :key="activity.activityId"
        :activity="activity"
      />

      <!-- Show More Button (if more than 10) -->
      <div v-if="!showAll && activities.length > 10" class="text-center mt-6">
        <v-btn
          color="primary"
          variant="outlined"
          size="large"
          @click="showAll = true"
          prepend-icon="mdi-chevron-down"
        >
          Show {{ activities.length - 10 }} More
        </v-btn>
      </div>

      <!-- Show Less Button (if showing all) -->
      <div v-if="showAll && activities.length > 10" class="text-center mt-6">
        <v-btn
          variant="text"
          @click="scrollToTopAndCollapse"
          prepend-icon="mdi-chevron-up"
        >
          Show Less
        </v-btn>
      </div>
    </div>
  </div>
</template>

<script>
import { activityAPI } from '@/services/api-production';
import ActivityCard from '@/components/ActivityCard.vue';

export default {
  name: 'ActivityFeed',

  components: {
    ActivityCard
  },

  emits: ['add-media'],

  data() {
    return {
      activities: [],
      currentFilter: 'all',
      loading: false,
      loadingMore: false,
      error: null,
      limit: 50,       // FIXED: Fetch 50 activities (was 10)
      showAll: false,  // Show only 10 initially
      offset: 0,
      hasMore: true
    };
  },

  computed: {
    emptyStateTitle() {
      switch (this.currentFilter) {
        case 'me':
          return 'No Activity Yet';
        case 'friends':
          return 'No Friend Activity';
        default:
          return 'Activity Feed Empty';
      }
    },

    emptyStateText() {
      switch (this.currentFilter) {
        case 'me':
          return 'Start rating movies and TV shows to see your activity here!';
        case 'friends':
          return 'Add friends to see their activity in your feed.';
        default:
          return 'Your activity feed will show your ratings and friend updates.';
      }
    },

    // FIXED: Display first 10 unless showAll is true
    displayedActivities() {
      return this.showAll ? this.activities : this.activities.slice(0, 10);
    }
  },

  watch: {
    currentFilter() {
      // Reset and reload when filter changes
      this.activities = [];
      this.offset = 0;
      this.hasMore = true;
      this.showAll = false;  // Reset showAll on filter change
      this.loadActivities();
    }
  },

  created() {
    this.loadActivities();
  },

  methods: {
    async loadActivities() {
      this.loading = true;
      this.error = null;

      try {
        const data = await activityAPI.getFeed(this.currentFilter, this.limit, 0);
        this.activities = data;
        this.offset = data.length;
        this.hasMore = data.length >= this.limit;
      } catch (err) {
        console.error('Error loading activities:', err);
        this.error = err.message || 'Failed to load activities';
      } finally {
        this.loading = false;
      }
    },

    async loadMore() {
      if (!this.hasMore || this.loadingMore) return;

      this.loadingMore = true;

      try {
        const data = await activityAPI.getFeed(
          this.currentFilter,
          this.limit,
          this.offset
        );

        this.activities.push(...data);
        this.offset += data.length;
        this.hasMore = data.length >= this.limit;
      } catch (err) {
        console.error('Error loading more activities:', err);
        this.error = err.message || 'Failed to load more activities';
      } finally {
        this.loadingMore = false;
      }
    },

    // NEW: Scroll to top and collapse
    scrollToTopAndCollapse() {
      this.showAll = false;
      // Scroll to top of activity feed
      this.$el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    },

    // Public method to refresh feed (can be called from parent)
    async refresh() {
      this.activities = [];
      this.offset = 0;
      this.hasMore = true;
      this.showAll = false;
      await this.loadActivities();
    }
  }
};
</script>

<style scoped>
.activity-feed {
  width: 100%;
}

.feed-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.activity-list {
  max-width: 100%;
}

/* Mobile: Stack header */
@media (max-width: 600px) {
  .feed-header {
    flex-direction: column;
    align-items: stretch;
  }

  .feed-header h2 {
    text-align: center;
  }

  .feed-header .v-btn-toggle {
    width: 100%;
  }

  .feed-header .v-btn-toggle .v-btn {
    flex: 1;
  }
}
</style>
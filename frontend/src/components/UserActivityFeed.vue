<template>
  <div class="user-activity-feed">
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
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
      v-else-if="activities.length === 0"
      icon="mdi-rss"
      :title="`${username} hasn't logged any activity yet`"
      text="No activities to display"
    />

    <!-- Activity List -->
    <div v-else>
      <activity-card
        v-for="activity in activities"
        :key="activity.activityId"
        :activity="activity"
      />
    </div>
  </div>
</template>

<script>
import { activityAPI } from '@/services/api-production';
import ActivityCard from '@/components/ActivityCard.vue';

export default {
  name: 'UserActivityFeed',

  components: {
    ActivityCard
  },

  props: {
    userId: {
      type: Number,
      required: true
    },
    username: {
      type: String,
      required: true
    }
  },

  data() {
    return {
      activities: [],
      loading: false,
      error: null
    };
  },

  created() {
    this.loadActivities();
  },

  methods: {
    async loadActivities() {
      this.loading = true;
      this.error = null;

      try {
        this.activities = await activityAPI.getUserActivity(this.userId, 50);
      } catch (err) {
        console.error('Error loading user activities:', err);
        this.error = err.message || 'Failed to load activities';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>
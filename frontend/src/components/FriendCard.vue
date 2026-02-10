<template>
  <v-card>
    <v-card-text>
      <div class="d-flex align-center mb-3">
        <!-- Friend Avatar -->
        <v-avatar color="primary" size="48" class="mr-3">
          <span class="text-h6 text-white">
            {{ friend.friendUsername[0].toUpperCase() }}
          </span>
        </v-avatar>
        
        <!-- Friend Info -->
        <div class="flex-grow-1">
          <h3 class="text-h6 mb-1">{{ friend.friendUsername }}</h3>
          <p v-if="friend.friendDisplayName" class="text-body-2 text-medium-emphasis mb-0">
            {{ friend.friendDisplayName }}
          </p>
          <p class="text-caption text-medium-emphasis">
            Friends since {{ formatDate(friend.acceptedAt) }}
          </p>
        </div>
        
        <!-- Actions Menu -->
        <v-menu>
          <template v-slot:activator="{ props }">
            <v-btn icon="mdi-dots-vertical" variant="text" v-bind="props" />
          </template>
          <v-list>
            <v-list-item @click="$emit('remove', friend)">
              <template v-slot:prepend>
                <v-icon>mdi-account-remove</v-icon>
              </template>
              <v-list-item-title>Remove Friend</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </div>
    </v-card-text>
    
    <!-- Action Buttons -->
    <v-card-actions>
      <v-btn
        variant="tonal"
        color="primary"
        prepend-icon="mdi-chart-bar"
        @click="$emit('compare', friend)"
        block
      >
        Compare Ratings
      </v-btn>
    </v-card-actions>
    <v-card-actions class="pt-0">
      <v-btn
        variant="text"
        prepend-icon="mdi-account"
        @click="$emit('profile', friend)"
        block
      >
        View Profile
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'FriendCard',
  
  props: {
    friend: {
      type: Object,
      required: true
    }
  },
  
  emits: ['remove', 'compare', 'profile'],
  
  methods: {
    formatDate(dateString) {
      if (!dateString) return 'recently';
      
      const date = new Date(dateString);
      const now = new Date();
      const diff = now - date;
      
      // Less than 1 day
      if (diff < 86400000) return 'today';
      
      // Less than 1 week
      if (diff < 604800000) {
        const days = Math.floor(diff / 86400000);
        return `${days} ${days === 1 ? 'day' : 'days'} ago`;
      }
      
      // Less than 1 month
      if (diff < 2592000000) {
        const weeks = Math.floor(diff / 604800000);
        return `${weeks} ${weeks === 1 ? 'week' : 'weeks'} ago`;
      }
      
      // Format as date
      return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
    }
  }
};
</script>

<style scoped>
.friend-card {
  height: 100%;
  transition: transform 0.2s ease;
}

.friend-card:hover {
  transform: translateY(-2px);
}

.gap-2 {
  gap: 8px;
}
</style>
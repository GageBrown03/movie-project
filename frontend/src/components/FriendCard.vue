<template>
  <v-card class="friend-card" elevation="2">
    <v-card-text>
      <!-- Friend Avatar & Info -->
      <div class="d-flex align-center mb-3">
        <v-avatar color="primary" size="48" class="mr-3">
          <span class="text-h6 text-white">
            {{ friend.friend_username[0].toUpperCase() }}
          </span>
        </v-avatar>
        
        <div class="flex-grow-1">
          <div class="text-h6">{{ friend.friend_username }}</div>
          <div v-if="friend.friend_display_name" class="text-caption text-medium-emphasis">
            {{ friend.friend_display_name }}
          </div>
          <div class="text-caption text-medium-emphasis">
            Friends since {{ formatDate(friend.accepted_at) }}
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="d-flex gap-2 flex-wrap">
        <v-btn 
          color="primary" 
          variant="tonal"
          size="small"
          prepend-icon="mdi-chart-bar"
          @click="$emit('compare')"
        >
          Compare
        </v-btn>
        
        <v-btn 
          color="secondary" 
          variant="tonal"
          size="small"
          prepend-icon="mdi-account"
          @click="$emit('profile')"
        >
          Profile
        </v-btn>
        
        <v-spacer />
        
        <v-menu>
          <template v-slot:activator="{ props }">
            <v-btn 
              icon="mdi-dots-vertical" 
              size="small"
              variant="text"
              v-bind="props"
            />
          </template>
          <v-list>
            <v-list-item 
              prepend-icon="mdi-account-remove"
              @click="$emit('remove')"
            >
              <v-list-item-title>Remove Friend</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </div>
    </v-card-text>
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
  
  emits: ['compare', 'profile', 'remove'],
  
  methods: {
    formatDate(dateString) {
      if (!dateString) return 'Recently';
      
      const date = new Date(dateString);
      const now = new Date();
      const diffTime = Math.abs(now - date);
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      
      if (diffDays === 0) return 'Today';
      if (diffDays === 1) return 'Yesterday';
      if (diffDays < 7) return `${diffDays} days ago`;
      if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
      if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`;
      
      return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short' 
      });
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
<template>
  <v-card flat border class="friend-card h-100">
    <v-card-text class="pa-2 pa-sm-4">
      <div class="d-flex align-center mb-2 mb-sm-3">
        <v-avatar 
          color="primary" 
          :size="$vuetify.display.xs ? 36 : 48" 
          class="mr-2 mr-sm-3"
        >
          <span :class="$vuetify.display.xs ? 'text-subtitle-2' : 'text-h6'" class="text-white">
            {{ friend.friendUsername[0].toUpperCase() }}
          </span>
        </v-avatar>
        
        <div class="flex-grow-1 overflow-hidden">
          <h3 class="font-weight-bold text-truncate mb-0" :class="$vuetify.display.xs ? 'text-subtitle-2' : 'text-h6'">
            {{ friend.friendUsername }}
          </h3>
          <p v-if="friend.friendDisplayName" class="text-caption text-medium-emphasis text-truncate mb-0">
            {{ friend.friendDisplayName }}
          </p>
          <p class="text-caption text-disabled text-truncate mb-0 d-none d-sm-block">
            Friends since {{ formatDate(friend.acceptedAt) }}
          </p>
        </div>
        
        <v-menu location="bottom end">
          <template v-slot:activator="{ props }">
            <v-btn 
              icon="mdi-dots-vertical" 
              variant="text" 
              v-bind="props" 
              density="comfortable" 
            />
          </template>
          <v-list density="compact">
            <v-list-item @click="$emit('profile', friend)">
              <template v-slot:prepend><v-icon size="small">mdi-account</v-icon></template>
              <v-list-item-title>View Profile</v-list-item-title>
            </v-list-item>
            <v-divider />
            <v-list-item @click="$emit('remove', friend)" base-color="error">
              <template v-slot:prepend><v-icon size="small">mdi-account-remove</v-icon></template>
              <v-list-item-title>Remove Friend</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </div>

      <v-row dense class="mt-1">
        <v-col cols="12">
          <v-btn
            color="primary"
            variant="tonal"
            block
            :size="$vuetify.display.xs ? 'small' : 'default'"
            prepend-icon="mdi-swap-horizontal"
            @click="$emit('compare', friend)"
            class="font-weight-bold"
          >
            Compare
          </v-btn>
        </v-col>
      </v-row>
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
  
  emits: ['remove', 'compare', 'profile'],
  
  methods: {
    formatDate(dateString) {
      if (!dateString) return 'recently';
      
      const date = new Date(dateString);
      const now = new Date();
      const diff = now - date;
      
      if (diff < 86400000) return 'today';
      if (diff < 604800000) {
        const days = Math.floor(diff / 86400000);
        return `${days} ${days === 1 ? 'day' : 'days'} ago`;
      }
      
      return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
      });
    }
  }
};
</script>

<style scoped>
.friend-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.friend-card:hover {
  /* Only apply hover effect on desktop */
  @media (min-width: 960px) {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
  }
}

/* Ensure long names don't break the layout */
.text-truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
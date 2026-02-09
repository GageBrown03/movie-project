<template>
  <v-card class="request-card" elevation="2">
    <v-card-text>
      <!-- User Info -->
      <div class="d-flex align-center mb-3">
        <v-avatar color="primary" size="56" class="mr-3">
          <span class="text-h5 text-white">
            {{ request.other_username[0].toUpperCase() }}
          </span>
        </v-avatar>
        
        <div class="flex-grow-1">
          <div class="text-h6">{{ request.other_username }}</div>
          <div v-if="request.other_display_name" class="text-body-2 text-medium-emphasis">
            {{ request.other_display_name }}
          </div>
          <div class="text-caption text-medium-emphasis">
            {{ formatDate(request.created_at) }}
          </div>
        </div>
      </div>

      <!-- Received Request Actions -->
      <div v-if="type === 'received'" class="d-flex gap-2">
        <v-btn 
          color="success" 
          variant="flat"
          block
          prepend-icon="mdi-check"
          @click="$emit('accept')"
          :loading="loading"
        >
          Accept
        </v-btn>
        <v-btn 
          color="error" 
          variant="outlined"
          block
          prepend-icon="mdi-close"
          @click="$emit('decline')"
          :loading="loading"
        >
          Decline
        </v-btn>
      </div>

      <!-- Sent Request Status -->
      <div v-else-if="type === 'sent'">
        <v-chip 
          color="warning" 
          variant="tonal"
          size="small"
          prepend-icon="mdi-clock-outline"
          class="mb-2"
        >
          Pending
        </v-chip>
        <v-btn 
          color="grey" 
          variant="text"
          size="small"
          block
          prepend-icon="mdi-close"
          @click="$emit('cancel')"
          :loading="loading"
        >
          Cancel Request
        </v-btn>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'FriendRequestCard',
  
  props: {
    request: {
      type: Object,
      required: true
    },
    type: {
      type: String,
      required: true,
      validator: (value) => ['received', 'sent'].includes(value)
    }
  },
  
  emits: ['accept', 'decline', 'cancel'],
  
  data() {
    return {
      loading: false
    };
  },
  
  methods: {
    formatDate(dateString) {
      if (!dateString) return '';
      
      const date = new Date(dateString);
      const now = new Date();
      const diffTime = Math.abs(now - date);
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      
      if (diffDays === 0) return 'Sent today';
      if (diffDays === 1) return 'Sent yesterday';
      if (diffDays < 7) return `Sent ${diffDays} days ago`;
      if (diffDays < 30) return `Sent ${Math.floor(diffDays / 7)} weeks ago`;
      
      return `Sent ${date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric' 
      })}`;
    }
  }
};
</script>

<style scoped>
.request-card {
  height: 100%;
  transition: transform 0.2s ease;
}

.request-card:hover {
  transform: translateY(-2px);
}

.gap-2 {
  gap: 8px;
}
</style>
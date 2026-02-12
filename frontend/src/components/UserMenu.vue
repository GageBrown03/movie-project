<template>
  <v-menu offset-y>
    <template v-slot:activator="{ props }">
      <v-btn icon v-bind="props" class="user-menu-btn">
        <v-avatar color="primary" size="36">
          <span class="text-white font-weight-bold">{{ userInitial }}</span>
        </v-avatar>
      </v-btn>
    </template>
    
    <v-list density="comfortable" class="user-menu-list">
      <!-- User Info Header -->
      <v-list-item class="user-header">
        <template v-slot:prepend>
          <v-avatar color="primary" size="40">
            <span class="text-white font-weight-bold text-h6">{{ userInitial }}</span>
          </v-avatar>
        </template>
        <v-list-item-title class="font-weight-bold">
          {{ username }}
        </v-list-item-title>
        <v-list-item-subtitle v-if="stats.total > 0" class="text-caption">
          📊 {{ stats.total }} {{ stats.total === 1 ? 'item' : 'items' }} rated
        </v-list-item-subtitle>
      </v-list-item>
      
      <v-divider />
      
      <!-- Menu Items -->
      <v-list-item to="/settings/privacy" prepend-icon="mdi-shield-account">
        <v-list-item-title> Settings</v-list-item-title>
      </v-list-item>
      
      
      
      <v-divider />
      
      <v-list-item prepend-icon="mdi-help-circle">
        <v-list-item-title>Help & Support</v-list-item-title>
        <template v-slot:append>
          <v-chip size="x-small" color="grey" variant="text">Soon</v-chip>
        </template>
      </v-list-item>
      
      <v-divider />
      
      <v-list-item @click="$emit('logout')" prepend-icon="mdi-logout">
        <v-list-item-title>Logout</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
import { mediaAPI } from '@/services/api-production';

export default {
  name: 'UserMenu',
  
  emits: ['logout'],
  
  data() {
    return {
      username: '',
      stats: {
        total: 0,
        watched: 0,
        averageRating: 0
      }
    };
  },
  
  computed: {
    userInitial() {
      return this.username ? this.username[0].toUpperCase() : '?';
    }
  },
  
  created() {
    this.loadUserInfo();
    this.loadStats();
  },
  
  methods: {
    loadUserInfo() {
      // Get username from localStorage or JWT
      const storedUsername = localStorage.getItem('username');
      if (storedUsername) {
        this.username = storedUsername;
      } else {
        // Fallback: decode JWT to get username
        const token = localStorage.getItem('token');
        if (token) {
          try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            this.username = payload.sub || payload.username || 'User';
            localStorage.setItem('username', this.username);
          } catch (e) {
            this.username = 'User';
          }
        }
      }
    },
    
    async loadStats() {
      try {
        const mediaList = await mediaAPI.getAll();
        this.stats.total = mediaList.length;
        this.stats.watched = mediaList.filter(m => m.status === 'watched').length;
        
        const ratedMedia = mediaList.filter(m => m.rating);
        this.stats.averageRating = ratedMedia.length > 0
          ? ratedMedia.reduce((sum, m) => sum + m.rating, 0) / ratedMedia.length
          : 0;
      } catch (err) {
        // User might not have media yet - that's OK
        console.log('No media yet:', err);
      }
    }
  }
};
</script>

<style scoped>
.user-menu-btn {
  margin-left: 8px;
}

.user-menu-list {
  min-width: 240px;
}

.user-header {
  background: rgba(var(--v-theme-primary), 0.05);
  padding: 12px 16px;
}
</style>
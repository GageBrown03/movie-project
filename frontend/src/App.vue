<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" app>
      <v-list>
        <v-list-item to="/" prepend-icon="mdi-home">
          <v-list-item-title>Home</v-list-item-title>
        </v-list-item>
        
        <v-divider class="my-2" />
        
        <v-list-item to="/media" prepend-icon="mdi-view-grid">
          <v-list-item-title>Browse Media</v-list-item-title>
        </v-list-item>
        
        <v-list-item to="/analytics" prepend-icon="mdi-chart-line">
          <v-list-item-title>Analytics</v-list-item-title>
        </v-list-item>
        
        <v-divider class="my-2" />
        
        <v-list-item to="/media/new" prepend-icon="mdi-plus">
          <v-list-item-title>Add Media</v-list-item-title>
        </v-list-item>

        <v-list-item to="/friends" prepend-icon="mdi-account-group">
          <v-list-item-title>Friends</v-list-item-title>
          <template v-slot:append v-if="pendingFriendRequests > 0">
            <v-badge :content="pendingFriendRequests" color="error" />
          </template>
        </v-list-item>

        <v-list-item to="/random" prepend-icon="mdi-dice-5" color="primary">
          <v-list-item-title>What to Watch</v-list-item-title>
        </v-list-item>

        <v-list-item to="/discover" prepend-icon="mdi-compass">
          <v-list-item-title>Discover</v-list-item-title>
        </v-list-item>
        
        <v-divider class="my-2" />
        
        <!-- Settings Menu -->
        <v-list-item to="/settings/privacy" prepend-icon="mdi-shield-account">
          <v-list-item-title>Privacy Settings</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-app-bar-title>myMDB</v-app-bar-title>
      
      <v-spacer />
      
      <!-- Theme Toggle -->
      <v-btn icon @click="toggleTheme">
        <v-icon>{{ isDark ? 'mdi-white-balance-sunny' : 'mdi-weather-night' }}</v-icon>
      </v-btn>
      
      <!-- Login/Logout Button -->
      <v-btn v-if="!isLoggedIn" to="/login" variant="text">
        <v-icon start>mdi-login</v-icon>
        Login
      </v-btn>
      <v-btn v-else @click="handleLogout" variant="text">
        <v-icon start>mdi-logout</v-icon>
        Logout
      </v-btn>
    </v-app-bar>
    
    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { authAPI } from '@/services/api-production';
import { useTheme } from 'vuetify';

// Get API base URL (same logic as api-production.js)
const API_BASE = process.env.VUE_APP_API_BASE_URL || 'http://localhost:5000';

export default {
  name: 'App',
  
  data() {
    return {
      drawer: true,
      isLoggedIn: false,
      pendingFriendRequests: 0
    };
  },
  
  setup() {
    const theme = useTheme();
    return { theme };
  },
  
  computed: {
    isDark() {
      return this.theme.global.name.value === 'dark';
    }
  },
  
  created() {
    this.checkAuth();
    this.loadTheme();
    
    // Listen for route changes
    this.$watch(
      () => this.$route.path,
      () => {
        this.checkAuth();
        if (this.isLoggedIn) {
          this.loadPendingRequests();
        }
      }
    );
  },

  mounted() {
    if (this.isLoggedIn) {
      this.loadPendingRequests();
      
      // Refresh every 60 seconds
      this.pendingRequestsInterval = setInterval(() => {
        if (this.isLoggedIn) {
          this.loadPendingRequests();
        }
      }, 60000);
    }
  },

  beforeUnmount() {
    if (this.pendingRequestsInterval) {
      clearInterval(this.pendingRequestsInterval);
    }
  },
  
  methods: {
    checkAuth() {
      const token = localStorage.getItem('token');
      this.isLoggedIn = !!token;
    },
    
    handleLogout() {
      authAPI.logout();
      this.isLoggedIn = false;
      this.$router.push('/login');
    },
    
    loadTheme() {
      const savedTheme = localStorage.getItem('theme') || 'dark';
      this.theme.global.name.value = savedTheme;
    },

    async loadPendingRequests() {
      if (!this.isLoggedIn) {
        this.pendingFriendRequests = 0;
        return;
      }
      
      try {
        const response = await fetch(`${API_BASE}/api/friends/pending`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        // CRITICAL: Check content-type before parsing JSON
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
          // Response is not JSON (probably HTML error page)
          console.warn('Pending requests endpoint returned non-JSON response');
          this.pendingFriendRequests = 0;
          return;
        }
        
        if (response.ok) {
          const requests = await response.json();
          this.pendingFriendRequests = requests.filter(
            r => r.requestType === 'received'
          ).length;
        } else {
          this.pendingFriendRequests = 0;
        }
      } catch (err) {
        // Silently fail - don't spam console with errors
        this.pendingFriendRequests = 0;
      }
    },
    
    toggleTheme() {
      const newTheme = this.isDark ? 'light' : 'dark';
      this.theme.global.name.value = newTheme;
      localStorage.setItem('theme', newTheme);
    }
  }
}
</script>

<style>
.v-application {
  transition: background-color 0.3s ease, color 0.3s ease;
}
</style>

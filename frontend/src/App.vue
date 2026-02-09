<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" app>
      <v-list>
        <v-list-item to="/" prepend-icon="mdi-home">
          <v-list-item-title>Home</v-list-item-title>
        </v-list-item>
        
        <v-divider class="my-2" />
        
        <!--  <v-list-subheader>Media</v-list-subheader>    -->
        
        <v-list-item to="/media" prepend-icon="mdi-view-grid">
          <v-list-item-title>Browse Media</v-list-item-title>
        </v-list-item>
        
        <v-list-item to="/analytics" prepend-icon="mdi-chart-line">
          <v-list-item-title>Analytics</v-list-item-title>
        </v-list-item>
        
        <v-divider class="my-2" />

        
        <!-- <v-list-subheader>Actions</v-list-subheader> -->
        
        <v-list-item to="/media/new" prepend-icon="mdi-plus">
          <v-list-item-title>Add Media</v-list-item-title>
        </v-list-item>

        
        <!-- In your navigation drawer -->
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
      
      <!-- Logout Button (only show if logged in) -->
      <v-btn v-if="isLoggedIn" @click="handleLogout" variant="text">
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

export default {
  name: 'App',
  
  data() {
    return {
      drawer: true,  // Start with drawer open
      isLoggedIn: false,
      pendingFriendRequests: 0 //Track pending friend requests for badge
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
    // Check if user is logged in when app loads
    this.checkAuth();
    
    // Load theme preference from localStorage
    this.loadTheme();
    
    // Listen for route changes to update auth state
    this.$watch(
      () => this.$route.path,
      () => {
        this.checkAuth();
        // Reload friend requests on route change
        if (this.isLoggedIn) {
          this.loadPendingRequests();
        }
      }
    );
  },

  // ADD THIS HOOK TO LOAD PENDING FRIEND REQUESTS WHEN COMPONENT MOUNTS
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
    // Clean up interval
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
      // Load saved theme preference (default to dark)
      const savedTheme = localStorage.getItem('theme') || 'dark';
      this.theme.global.name.value = savedTheme;
    },

    // New method to load pending friend requests and set badge count
    async loadPendingRequests() {
      // Only load if logged in
      if (!this.isLoggedIn) {
        this.pendingFriendRequests = 0;
        return;
      }
      
      try {
        const response = await fetch('/api/friends/pending', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        if (response.ok) {
          const requests = await response.json();
          this.pendingFriendRequests = requests.filter(
            r => r.requestType === 'received'
          ).length;
        } else {
          // If request fails (e.g., 401), clear badge
          this.pendingFriendRequests = 0;
        }
      } catch (err) {
        console.error('Error loading pending requests:', err);
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
/* Smooth transition when switching themes */
.v-application {
  transition: background-color 0.3s ease, color 0.3s ease;
}
</style>
<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" app>
      <v-list>
        <v-list-item to="/" prepend-icon="mdi-home">
          <v-list-item-title>myMDB</v-list-item-title>
        </v-list-item>

        <v-divider class="my-2" />

        <v-list-item to="/media" prepend-icon="mdi-bookshelf">
          <v-list-item-title>Library</v-list-item-title>
        </v-list-item>

        <v-list-item to="/friends" prepend-icon="mdi-account-group">
          <v-list-item-title>Social</v-list-item-title>
          <template v-slot:append v-if="pendingFriendRequests > 0">
            <v-badge :content="pendingFriendRequests" color="error" />
          </template>
        </v-list-item>

        <v-divider class="my-2" />

        <v-list-item to="/analytics" prepend-icon="mdi-chart-line">
          <v-list-item-title>Analytics</v-list-item-title>
        </v-list-item>

        <!-- PHASE 2: Temporary - Will merge to Explore in Phase 4 -->
        <v-list-item to="/random" prepend-icon="mdi-shuffle" base-color="primary">
          <v-list-item-title>Shuffle</v-list-item-title>
        </v-list-item>

        <v-list-item to="/discover" prepend-icon="mdi-compass">
          <v-list-item-title>Discover</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer" />

      <v-app-bar-title class="clickable-title">
        <router-link to="/" class="title-link" aria-label="Go to Home">
          myMDB
        </router-link>
      </v-app-bar-title>

      <v-spacer />

      <!-- PHASE 2: Global Add Media Button -->
      <v-btn
        v-if="isLoggedIn"
        prepend-icon="mdi-plus"
        variant="text"
        @click="showAddDialog = true"
        class="mr-2"
      >
        Add
      </v-btn>

      <!-- Theme Toggle -->
      <v-btn icon @click="toggleTheme" aria-label="Toggle theme">
        <v-icon>{{ isDark ? 'mdi-white-balance-sunny' : 'mdi-weather-night' }}</v-icon>
      </v-btn>

      <!-- Login or UserMenu -->
      <v-btn v-if="!isLoggedIn" to="/login" variant="text">
        <v-icon start>mdi-login</v-icon>
        Login
      </v-btn>
      
      <user-menu v-else @logout="handleLogout" />
    </v-app-bar>
    
    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>

    <!-- PHASE 2: Global Add Media Dialog -->
    <add-media-dialog
      v-model="showAddDialog"
      @media-added="handleMediaAdded"
    />
  </v-app>
</template>

<script>
import { authAPI } from '@/services/api-production';
import { useTheme } from 'vuetify';
import UserMenu from '@/components/UserMenu.vue';
import AddMediaDialog from '@/components/AddMediaDialog.vue';

const API_BASE = process.env.VUE_APP_API_BASE_URL || 'http://localhost:5000';

export default {
  name: 'App',
  
  components: {
    UserMenu,
    AddMediaDialog
  },
  
  data() {
    return {
      drawer: true,
      isLoggedIn: false,
      pendingFriendRequests: 0,
      showAddDialog: false
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
      
      this.pendingRequestsInterval = setInterval(() => {
        if (this.isLoggedIn) {
          this.loadPendingRequests();
        }
      }, 60000);
    }

    // PHASE 2: Listen for keyboard shortcut (Ctrl/Cmd + K)
    window.addEventListener('keydown', this.handleKeyboardShortcut);
  },

  beforeUnmount() {
    if (this.pendingRequestsInterval) {
      clearInterval(this.pendingRequestsInterval);
    }
    window.removeEventListener('keydown', this.handleKeyboardShortcut);
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
        
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
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
        this.pendingFriendRequests = 0;
      }
    },
    
    toggleTheme() {
      const newTheme = this.isDark ? 'light' : 'dark';
      this.theme.global.name.value = newTheme;
      localStorage.setItem('theme', newTheme);
    },

    // PHASE 2: Keyboard shortcut handler
    handleKeyboardShortcut(e) {
      // Ctrl+K or Cmd+K to open add dialog
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        if (this.isLoggedIn) {
          this.showAddDialog = true;
        }
      }
    },

    // PHASE 2: Handle successful media addition
    handleMediaAdded(media) {
      // Optional: Show success snackbar or refresh data
      console.log('Media added:', media);
      // The dialog already navigates to the detail page
    }
  }
}
</script>

<style>
.v-application {
  transition: background-color 0.3s ease, color 0.3s ease;
}

.title-link {
  color: inherit;
  text-decoration: none;
  display: inline-block;
}

.clickable-title {
  cursor: pointer;
}
</style>
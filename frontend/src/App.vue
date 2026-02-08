<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>myMDB</v-toolbar-title>
      <v-spacer></v-spacer>
      
      <!-- Dark mode toggle button (always visible) -->
      <v-btn icon @click="toggleTheme" class="mr-2">
        <v-icon>{{ isDark ? 'mdi-white-balance-sunny' : 'mdi-moon-waning-crescent' }}</v-icon>
      </v-btn>
      
      <!-- Show these buttons only when logged in -->
      <template v-if="isLoggedIn">
        <v-btn to="/">Home</v-btn>
        <v-btn to="/movies">Your Media</v-btn>
        <v-btn @click="handleLogout">
          <v-icon left>mdi-logout</v-icon>
          Logout
        </v-btn>
      </template>
      
      <!-- Show these buttons only when NOT logged in -->
      <template v-else>
        <v-btn to="/login">Login</v-btn>
        <v-btn to="/register">Register</v-btn>
      </template>
    </v-app-bar>
    
    <v-main>
      <v-container>
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
      isLoggedIn: false
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
      }
    );
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
      // Load saved theme preference (default to light)
      const savedTheme = localStorage.getItem('theme') || 'light';
      this.theme.global.name.value = savedTheme;
    },
    
    toggleTheme() {
      // Toggle between light and dark
      const newTheme = this.isDark ? 'light' : 'dark';
      this.theme.global.name.value = newTheme;
      
      // Save preference to localStorage
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
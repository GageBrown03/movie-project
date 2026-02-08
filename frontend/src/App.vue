<template>
  <v-app>
    <v-navigation-drawer app v-model="drawer">
      <v-list>
        <v-list-item to="/" prepend-icon="mdi-home">
          <v-list-item-title>Home</v-list-item-title>
        </v-list-item>
        
        <v-divider class="my-2" />
        
        <v-list-subheader>Your Collection</v-list-subheader>
        
        <v-list-item to="/movies" prepend-icon="mdi-view-grid">
          <v-list-item-title>Browse Media</v-list-item-title>
        </v-list-item>
        
        <v-list-item to="/analytics" prepend-icon="mdi-chart-line">
          <v-list-item-title>Analytics</v-list-item-title>
        </v-list-item>
        
        <v-divider class="my-2" />
        
        <v-list-subheader>Actions</v-list-subheader>
        
        <v-list-item to="/random" prepend-icon="mdi-dice-5" color="primary">
          <v-list-item-title>What to Watch?</v-list-item-title>
        </v-list-item>
        
        <v-list-item to="/movies/new" prepend-icon="mdi-plus">
          <v-list-item-title>Add Media</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-app-bar-title>MyMDB</v-app-bar-title>
    </v-app-bar>
    
    <v-main>
      <router-view />
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
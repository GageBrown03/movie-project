<template>
  <v-container class="privacy-settings-view">
    <!-- Header with Back Button -->
    <v-row class="mb-4 align-center">
      <v-col cols="auto">
        <v-btn
          icon
          variant="text"
          @click="goBack"
        >
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
      </v-col>
      <v-col>
        <h1 class="text-h3 font-weight-bold">Privacy Settings</h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Control who can see your collection and ratings
        </p>
      </v-col>
    </v-row>

    <!-- Loading State -->
    <v-row v-if="loading" justify="center" class="my-12">
      <v-progress-circular indeterminate size="64" color="primary" />
    </v-row>

    <!-- Settings Form -->
    <v-card v-else class="pa-6">
      <v-form>
        <!-- Profile Searchable -->
        <v-row class="mb-6">
          <v-col cols="12">
            <h3 class="text-h6 mb-3">Profile Visibility</h3>
            <v-switch
              v-model="settings.privacyProfileSearchable"
              color="primary"
              label="Allow others to find me in search"
              :disabled="saving"
            />
            <p class="text-caption text-medium-emphasis ml-12">
              When enabled, other users can search for you by username
            </p>
          </v-col>
        </v-row>

        <v-divider class="my-4" />

        <!-- Collection Privacy -->
        <v-row class="mb-6">
          <v-col cols="12">
            <h3 class="text-h6 mb-3">My Collection</h3>
            <p class="text-body-2 text-medium-emphasis mb-3">
              Who can see the movies and TV shows in your collection?
            </p>
            <v-radio-group 
              v-model="settings.privacyCollection"
              :disabled="saving"
            >
              <v-radio value="private" label="Private - Only me" />
              <v-radio value="friends" label="Friends - Only my friends" />
              <v-radio value="public" label="Public - Everyone" />
            </v-radio-group>
          </v-col>
        </v-row>

        <v-divider class="my-4" />

        <!-- Ratings Privacy -->
        <v-row class="mb-6">
          <v-col cols="12">
            <h3 class="text-h6 mb-3">My Ratings</h3>
            <p class="text-body-2 text-medium-emphasis mb-3">
              Who can see your individual ratings and reviews?
            </p>
            <v-radio-group 
              v-model="settings.privacyRatings"
              :disabled="saving"
            >
              <v-radio value="private" label="Private - Only me" />
              <v-radio value="friends" label="Friends - Only my friends" />
              <v-radio value="public" label="Public - Everyone" />
            </v-radio-group>
          </v-col>
        </v-row>

        <v-divider class="my-4" />

        <!-- Stats Privacy -->
        <v-row class="mb-6">
          <v-col cols="12">
            <h3 class="text-h6 mb-3">My Statistics</h3>
            <p class="text-body-2 text-medium-emphasis mb-3">
              Who can see your viewing stats and analytics?
            </p>
            <v-radio-group 
              v-model="settings.privacyStats"
              :disabled="saving"
            >
              <v-radio value="private" label="Private - Only me" />
              <v-radio value="friends" label="Friends - Only my friends" />
              <v-radio value="public" label="Public - Everyone" />
            </v-radio-group>
          </v-col>
        </v-row>

        <v-divider class="my-4" />

        <!-- Email Notifications -->
        <v-row class="mb-6">
          <v-col cols="12">
            <h3 class="text-h6 mb-3">Notifications</h3>
            <v-switch
              v-model="settings.emailNotificationsFriendRequests"
              color="primary"
              label="Email me when I receive friend requests"
              :disabled="saving"
            />
          </v-col>
        </v-row>

        <!-- Action Buttons -->
        <v-row>
          <v-col>
            <v-btn
              color="primary"
              size="large"
              @click="saveSettings"
              :loading="saving"
              :disabled="!hasChanges"
            >
              Save Changes
            </v-btn>
            <v-btn
              variant="text"
              size="large"
              @click="resetSettings"
              :disabled="!hasChanges || saving"
              class="ml-2"
            >
              Reset
            </v-btn>
          </v-col>
        </v-row>
      </v-form>
    </v-card>

    <!-- Snackbar -->
    <v-snackbar v-model="showSnackbar" :color="snackbarColor">
      {{ snackbarMessage }}
    </v-snackbar>
  </v-container>
</template>

<script>
const API_BASE = process.env.VUE_APP_API_BASE_URL || 'http://localhost:5000';

export default {
  name: 'PrivacySettingsView',
  
  data() {
    return {
      loading: false,
      saving: false,
      settings: {
        privacyCollection: 'private',
        privacyRatings: 'private',
        privacyStats: 'private',
        privacyProfileSearchable: false,
        emailNotificationsFriendRequests: true,
      },
      originalSettings: null,
      showSnackbar: false,
      snackbarMessage: '',
      snackbarColor: 'success',
    };
  },
  
  computed: {
    hasChanges() {
      if (!this.originalSettings) return false;
      return JSON.stringify(this.settings) !== JSON.stringify(this.originalSettings);
    }
  },
  
  created() {
    this.loadSettings();
  },
  
  methods: {
    goBack() {
      // Check if there's history to go back to
      if (window.history.length > 1) {
        this.$router.go(-1);
      } else {
        this.$router.push('/friends');
      }
    },
    
    async loadSettings() {
      this.loading = true;
      try {
        const response = await fetch(`${API_BASE}/api/privacy`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        if (response.ok) {
          this.settings = await response.json();
          this.originalSettings = JSON.parse(JSON.stringify(this.settings));
        } else {
          this.showError('Failed to load privacy settings');
        }
      } catch (err) {
        console.error('Error loading privacy settings:', err);
        this.showError('Failed to load privacy settings');
      } finally {
        this.loading = false;
      }
    },
    
    async saveSettings() {
      this.saving = true;
      try {
        const response = await fetch(`${API_BASE}/api/privacy`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.settings)
        });
        
        if (response.ok) {
          this.originalSettings = JSON.parse(JSON.stringify(this.settings));
          this.showSuccess('Privacy settings saved');
        } else {
          this.showError('Failed to save settings');
        }
      } catch (err) {
        console.error('Error saving privacy settings:', err);
        this.showError('Failed to save settings');
      } finally {
        this.saving = false;
      }
    },
    
    resetSettings() {
      this.settings = JSON.parse(JSON.stringify(this.originalSettings));
    },
    
    showSuccess(message) {
      this.snackbarMessage = message;
      this.snackbarColor = 'success';
      this.showSnackbar = true;
    },
    
    showError(message) {
      this.snackbarMessage = message;
      this.snackbarColor = 'error';
      this.showSnackbar = true;
    }
  }
};
</script>

<style scoped>
.privacy-settings-view {
  max-width: 900px;
  margin: 0 auto;
}
</style>
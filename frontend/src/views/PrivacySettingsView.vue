<template>
  <v-container class="account-settings-view">
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
        <h1 class="text-h3 font-weight-bold">Account Settings</h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Manage your profile and privacy preferences
        </p>
      </v-col>
    </v-row>

    <!-- Loading State -->
    <v-row v-if="loading" justify="center" class="my-12">
      <v-progress-circular indeterminate size="64" color="primary" />
    </v-row>

    <!-- Settings Form -->
    <div v-else>
      <!-- Profile Information Card -->
      <v-card class="mb-6 pa-6">
        <h2 class="text-h5 font-weight-bold mb-4">
          <v-icon start color="primary">mdi-account</v-icon>
          Profile Information
        </h2>

        <v-form>
          <!-- Username (Read-only) -->
          <v-text-field
            v-model="currentUser.username"
            label="Username"
            variant="outlined"
            density="comfortable"
            readonly
            disabled
            hint="Username cannot be changed"
            persistent-hint
            class="mb-4"
          />

          <!-- Display Name -->
          <v-text-field
            v-model="settings.displayName"
            label="Display Name"
            variant="outlined"
            density="comfortable"
            :disabled="saving"
            hint="Your name as others see it (optional)"
            persistent-hint
            counter="100"
            maxlength="100"
            class="mb-4"
          />

          <!-- Bio -->
          <v-textarea
            v-model="settings.bio"
            label="Bio"
            variant="outlined"
            density="comfortable"
            :disabled="saving"
            hint="Tell others about yourself and your movie taste (optional)"
            persistent-hint
            counter="500"
            maxlength="500"
            rows="4"
            class="mb-4"
          />
        </v-form>
      </v-card>

      <!-- Privacy Settings Card -->
      <v-card class="pa-6">
        <h2 class="text-h5 font-weight-bold mb-4">
          <v-icon start color="primary">mdi-lock</v-icon>
          Privacy Settings
        </h2>

        <v-form>
          <!-- Profile Searchable -->
          <div class="mb-6">
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
          </div>

          <v-divider class="my-6" />

          <!-- Collection Privacy -->
          <div class="mb-6">
            <h3 class="text-h6 mb-3">My Collection</h3>
            <p class="text-body-2 text-medium-emphasis mb-3">
              Who can see the movies and TV shows in your collection?
            </p>
            <v-radio-group 
              v-model="settings.privacyCollection"
              :disabled="saving"
            >
              <v-radio value="private">
                <template v-slot:label>
                  <div>
                    <div class="font-weight-bold">Private</div>
                    <div class="text-caption text-medium-emphasis">Only you can see your collection</div>
                  </div>
                </template>
              </v-radio>
              <v-radio value="friends">
                <template v-slot:label>
                  <div>
                    <div class="font-weight-bold">Friends Only</div>
                    <div class="text-caption text-medium-emphasis">Only your friends can see your collection</div>
                  </div>
                </template>
              </v-radio>
              <v-radio value="public">
                <template v-slot:label>
                  <div>
                    <div class="font-weight-bold">Public</div>
                    <div class="text-caption text-medium-emphasis">Everyone can see your collection</div>
                  </div>
                </template>
              </v-radio>
            </v-radio-group>
          </div>

          <v-divider class="my-6" />

          <!-- Ratings Privacy -->
          <div class="mb-6">
            <h3 class="text-h6 mb-3">My Ratings</h3>
            <p class="text-body-2 text-medium-emphasis mb-3">
              Who can see your individual ratings and reviews?
            </p>
            <v-radio-group 
              v-model="settings.privacyRatings"
              :disabled="saving"
            >
              <v-radio value="private">
                <template v-slot:label>
                  <div>
                    <div class="font-weight-bold">Private</div>
                    <div class="text-caption text-medium-emphasis">Only you can see your ratings</div>
                  </div>
                </template>
              </v-radio>
              <v-radio value="friends">
                <template v-slot:label>
                  <div>
                    <div class="font-weight-bold">Friends Only</div>
                    <div class="text-caption text-medium-emphasis">Only your friends can see your ratings</div>
                  </div>
                </template>
              </v-radio>
              <v-radio value="public">
                <template v-slot:label>
                  <div>
                    <div class="font-weight-bold">Public</div>
                    <div class="text-caption text-medium-emphasis">Everyone can see your ratings</div>
                  </div>
                </template>
              </v-radio>
            </v-radio-group>
          </div>

          <v-divider class="my-6" />

          <!-- Stats Privacy -->
          <div class="mb-6">
            <h3 class="text-h6 mb-3">My Statistics</h3>
            <p class="text-body-2 text-medium-emphasis mb-3">
              Who can see your viewing stats and analytics?
            </p>
            <v-radio-group 
              v-model="settings.privacyStats"
              :disabled="saving"
            >
              <v-radio value="private">
                <template v-slot:label>
                  <div>
                    <div class="font-weight-bold">Private</div>
                    <div class="text-caption text-medium-emphasis">Only you can see your stats</div>
                  </div>
                </template>
              </v-radio>
              <v-radio value="friends">
                <template v-slot:label>
                  <div>
                    <div class="font-weight-bold">Friends Only</div>
                    <div class="text-caption text-medium-emphasis">Only your friends can see your stats</div>
                  </div>
                </template>
              </v-radio>
              <v-radio value="public">
                <template v-slot:label>
                  <div>
                    <div class="font-weight-bold">Public</div>
                    <div class="text-caption text-medium-emphasis">Everyone can see your stats</div>
                  </div>
                </template>
              </v-radio>
            </v-radio-group>
          </div>
        </v-form>
      </v-card>

      <!-- Action Buttons -->
      <v-row class="mt-6">
        <v-col>
          <v-btn
            color="primary"
            size="large"
            @click="saveSettings"
            :loading="saving"
            :disabled="!hasChanges"
          >
            <v-icon start>mdi-content-save</v-icon>
            Save Changes
          </v-btn>
          <v-btn
            variant="text"
            size="large"
            @click="resetSettings"
            :disabled="!hasChanges || saving"
            class="ml-2"
          >
            <v-icon start>mdi-refresh</v-icon>
            Reset
          </v-btn>
        </v-col>
      </v-row>
    </div>

    <!-- Snackbar -->
    <v-snackbar v-model="showSnackbar" :color="snackbarColor">
      {{ snackbarMessage }}
    </v-snackbar>
  </v-container>
</template>

<script>
const API_BASE = process.env.VUE_APP_API_BASE_URL || 'http://localhost:5000';

export default {
  name: 'AccountSettingsView',
  
  data() {
    return {
      loading: false,
      saving: false,
      currentUser: {
        username: ''
      },
      settings: {
        displayName: '',
        bio: '',
        privacyCollection: 'private',
        privacyRatings: 'private',
        privacyStats: 'private',
        privacyProfileSearchable: false,
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
    this.loadCurrentUser();
    this.loadSettings();
  },
  
  methods: {
    goBack() {
      if (window.history.length > 1) {
        this.$router.go(-1);
      } else {
        this.$router.push('/');
      }
    },

    async loadCurrentUser() {
      try {
        const response = await fetch(`${API_BASE}/auth/me`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        if (response.ok) {
          const user = await response.json();
          this.currentUser = user;
        }
      } catch (err) {
        console.error('Error loading current user:', err);
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
          const data = await response.json();
          this.settings = {
            displayName: data.displayName || '',
            bio: data.bio || '',
            privacyCollection: data.privacyCollection,
            privacyRatings: data.privacyRatings,
            privacyStats: data.privacyStats,
            privacyProfileSearchable: data.privacyProfileSearchable,
          };
          this.originalSettings = JSON.parse(JSON.stringify(this.settings));
        } else {
          this.showError('Failed to load settings');
        }
      } catch (err) {
        console.error('Error loading settings:', err);
        this.showError('Failed to load settings');
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
          this.showSuccess('Settings saved successfully');
          
          // Update localStorage if display name changed
          const user = JSON.parse(localStorage.getItem('user') || '{}');
          user.displayName = this.settings.displayName;
          user.bio = this.settings.bio;
          localStorage.setItem('user', JSON.stringify(user));
          
          // Emit event to update App.vue
          this.$root.$emit('user-updated');
        } else {
          this.showError('Failed to save settings');
        }
      } catch (err) {
        console.error('Error saving settings:', err);
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
.account-settings-view {
  max-width: 900px;
  margin: 0 auto;
}

.v-radio :deep(.v-label) {
  opacity: 1 !important;
}
</style>
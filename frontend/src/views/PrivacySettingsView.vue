<template>
  <div class="privacy-settings-view">
    <!-- Header -->
    <v-row class="mb-6 align-center">
      <v-col>
        <h1 class="text-h3 font-weight-bold">Privacy Settings</h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Control who can see your movie collection and ratings
        </p>
      </v-col>
    </v-row>

    <!-- Loading State -->
    <v-row v-if="loading" justify="center" class="my-12">
      <v-progress-circular indeterminate size="64" color="primary" />
    </v-row>

    <div v-else>
      <!-- Settings Card -->
      <v-card max-width="800">
        <v-card-text class="pa-6">
          <!-- Collection Privacy -->
          <div class="setting-section mb-6">
            <div class="d-flex align-center mb-3">
              <v-icon color="primary" class="mr-3">mdi-movie-open</v-icon>
              <div>
                <h3 class="text-h6">Movie Collection</h3>
                <p class="text-caption text-medium-emphasis">
                  Who can see what movies and TV shows you've added
                </p>
              </div>
            </div>
            
            <v-radio-group v-model="settings.privacyCollection" @change="hasChanges = true">
              <v-radio value="private" color="error">
                <template v-slot:label>
                  <div>
                    <strong>Private</strong>
                    <span class="text-caption text-medium-emphasis d-block">
                      Only you can see your collection
                    </span>
                  </div>
                </template>
              </v-radio>
              
              <v-radio value="friends" color="warning">
                <template v-slot:label>
                  <div>
                    <strong>Friends Only</strong>
                    <span class="text-caption text-medium-emphasis d-block">
                      Only your friends can see your collection
                    </span>
                  </div>
                </template>
              </v-radio>
              
              <v-radio value="public" color="success">
                <template v-slot:label>
                  <div>
                    <strong>Public</strong>
                    <span class="text-caption text-medium-emphasis d-block">
                      Anyone can see your collection
                    </span>
                  </div>
                </template>
              </v-radio>
            </v-radio-group>
          </div>

          <v-divider class="my-6" />

          <!-- Ratings Privacy -->
          <div class="setting-section mb-6">
            <div class="d-flex align-center mb-3">
              <v-icon color="amber" class="mr-3">mdi-star</v-icon>
              <div>
                <h3 class="text-h6">Ratings</h3>
                <p class="text-caption text-medium-emphasis">
                  Who can see your star ratings
                </p>
              </div>
            </div>
            
            <v-radio-group v-model="settings.privacyRatings" @change="hasChanges = true">
              <v-radio value="private" color="error">
                <template v-slot:label>
                  <div>
                    <strong>Private</strong>
                    <span class="text-caption text-medium-emphasis d-block">
                      Only you can see your ratings
                    </span>
                  </div>
                </template>
              </v-radio>
              
              <v-radio value="friends" color="warning">
                <template v-slot:label>
                  <div>
                    <strong>Friends Only</strong>
                    <span class="text-caption text-medium-emphasis d-block">
                      Only friends can see your ratings (enables comparisons)
                    </span>
                  </div>
                </template>
              </v-radio>
              
              <v-radio value="public" color="success">
                <template v-slot:label>
                  <div>
                    <strong>Public</strong>
                    <span class="text-caption text-medium-emphasis d-block">
                      Anyone can see your ratings
                    </span>
                  </div>
                </template>
              </v-radio>
            </v-radio-group>
          </div>

          <v-divider class="my-6" />

          <!-- Stats Privacy -->
          <div class="setting-section mb-6">
            <div class="d-flex align-center mb-3">
              <v-icon color="info" class="mr-3">mdi-chart-bar</v-icon>
              <div>
                <h3 class="text-h6">Statistics</h3>
                <p class="text-caption text-medium-emphasis">
                  Who can see your stats (total watched, favorite genre, etc.)
                </p>
              </div>
            </div>
            
            <v-radio-group v-model="settings.privacyStats" @change="hasChanges = true">
              <v-radio value="private" color="error">
                <template v-slot:label>
                  <div>
                    <strong>Private</strong>
                    <span class="text-caption text-medium-emphasis d-block">
                      Only you can see your stats
                    </span>
                  </div>
                </template>
              </v-radio>
              
              <v-radio value="friends" color="warning">
                <template v-slot:label>
                  <div>
                    <strong>Friends Only</strong>
                    <span class="text-caption text-medium-emphasis d-block">
                      Only friends can see your stats
                    </span>
                  </div>
                </template>
              </v-radio>
              
              <v-radio value="public" color="success">
                <template v-slot:label>
                  <div>
                    <strong>Public</strong>
                    <span class="text-caption text-medium-emphasis d-block">
                      Anyone can see your stats
                    </span>
                  </div>
                </template>
              </v-radio>
            </v-radio-group>
          </div>

          <v-divider class="my-6" />

          <!-- Profile Searchable -->
          <div class="setting-section mb-6">
            <div class="d-flex align-center mb-3">
              <v-icon color="secondary" class="mr-3">mdi-account-search</v-icon>
              <div class="flex-grow-1">
                <h3 class="text-h6">Profile Discoverability</h3>
                <p class="text-caption text-medium-emphasis">
                  Allow others to find you when searching for friends
                </p>
              </div>
              <v-switch
                v-model="settings.privacyProfileSearchable"
                color="success"
                @change="hasChanges = true"
                hide-details
              />
            </div>
            
            <v-alert
              v-if="!settings.privacyProfileSearchable"
              type="warning"
              variant="tonal"
              density="compact"
              class="mt-3"
            >
              Your profile is hidden from search. Others won't be able to find you by username.
            </v-alert>
          </div>

          <v-divider class="my-6" />

          <!-- Email Notifications -->
          <div class="setting-section">
            <div class="d-flex align-center">
              <v-icon color="primary" class="mr-3">mdi-email</v-icon>
              <div class="flex-grow-1">
                <h3 class="text-h6">Email Notifications</h3>
                <p class="text-caption text-medium-emphasis">
                  Receive email when you get friend requests
                </p>
              </div>
              <v-switch
                v-model="settings.emailNotificationsFriendRequests"
                color="success"
                @change="hasChanges = true"
                hide-details
              />
            </div>
          </div>
        </v-card-text>

        <!-- Actions -->
        <v-card-actions class="pa-6 pt-0">
          <v-spacer />
          <v-btn
            variant="text"
            @click="resetSettings"
            :disabled="!hasChanges || saving"
          >
            Reset
          </v-btn>
          <v-btn
            color="primary"
            @click="saveSettings"
            :loading="saving"
            :disabled="!hasChanges"
          >
            Save Changes
          </v-btn>
        </v-card-actions>
      </v-card>

      <!-- Privacy Explanation -->
      <v-card class="mt-6" max-width="800">
        <v-card-text>
          <h3 class="text-h6 mb-3">
            <v-icon color="info" class="mr-2">mdi-information</v-icon>
            Privacy Levels Explained
          </h3>
          
          <v-row>
            <v-col cols="12" md="4">
              <v-chip color="error" variant="tonal" class="mb-2">Private</v-chip>
              <p class="text-caption">
                Only you can see this information. Even friends can't view it.
              </p>
            </v-col>
            
            <v-col cols="12" md="4">
              <v-chip color="warning" variant="tonal" class="mb-2">Friends Only</v-chip>
              <p class="text-caption">
                Only people you've accepted as friends can see this information.
              </p>
            </v-col>
            
            <v-col cols="12" md="4">
              <v-chip color="success" variant="tonal" class="mb-2">Public</v-chip>
              <p class="text-caption">
                Anyone can see this information, even if they're not your friend.
              </p>
            </v-col>
          </v-row>

          <v-alert type="info" variant="tonal" class="mt-4">
            <strong>Note:</strong> Personal notes are always private and never shared with anyone.
          </v-alert>
        </v-card-text>
      </v-card>
    </div>

    <!-- Success Snackbar -->
    <v-snackbar v-model="showSnackbar" :color="snackbarColor">
      {{ snackbarMessage }}
      <template v-slot:actions>
        <v-btn variant="text" @click="showSnackbar = false">Close</v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
export default {
  name: 'PrivacySettingsView',
  
  data() {
    return {
      loading: false,
      saving: false,
      hasChanges: false,
      
      settings: {
        privacyCollection: 'private',
        privacyRatings: 'private',
        privacyStats: 'private',
        privacyProfileSearchable: false,
        emailNotificationsFriendRequests: true,
      },
      
      originalSettings: {},
      
      // Snackbar
      showSnackbar: false,
      snackbarMessage: '',
      snackbarColor: 'success',
    };
  },
  
  created() {
    this.loadSettings();
  },
  
  methods: {
    async loadSettings() {
      this.loading = true;
      try {
        const response = await fetch('/api/privacy', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        if (response.ok) {
          this.settings = await response.json();
          this.originalSettings = { ...this.settings };
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
        const response = await fetch('/api/privacy', {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.settings)
        });
        
        if (response.ok) {
          const updated = await response.json();
          this.settings = {
            privacyCollection: updated.privacyCollection,
            privacyRatings: updated.privacyRatings,
            privacyStats: updated.privacyStats,
            privacyProfileSearchable: updated.privacyProfileSearchable,
            emailNotificationsFriendRequests: updated.emailNotificationsFriendRequests,
          };
          this.originalSettings = { ...this.settings };
          this.hasChanges = false;
          this.showSuccess('Privacy settings saved successfully');
        } else {
          const error = await response.json();
          this.showError(error.error || 'Failed to save settings');
        }
      } catch (err) {
        console.error('Error saving privacy settings:', err);
        this.showError('Failed to save settings');
      } finally {
        this.saving = false;
      }
    },
    
    resetSettings() {
      this.settings = { ...this.originalSettings };
      this.hasChanges = false;
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

.setting-section {
  border-radius: 8px;
  padding: 16px;
  background: rgba(0, 0, 0, 0.02);
}

.v-theme--dark .setting-section {
  background: rgba(255, 255, 255, 0.02);
}
</style>
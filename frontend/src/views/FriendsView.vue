<template>
  <div class="friends-view">
    <!-- Header -->
    <v-row class="mb-6 align-center">
      <v-col>
        <div class="d-flex align-center gap-3">
          <h1 class="text-h3 font-weight-bold">Friends</h1>
          <!-- Privacy Status Chip -->
          <v-chip 
            v-if="profileSearchable" 
            color="success" 
            size="small"
            prepend-icon="mdi-check-circle"
          >
            Profile Public
          </v-chip>
          <v-chip 
            v-else 
            color="warning" 
            size="small"
            prepend-icon="mdi-lock"
          >
            Profile Hidden
          </v-chip>
        </div>
        <p class="text-subtitle-1 text-medium-emphasis">
          Connect with friends to compare ratings and discover new movies
        </p>
      </v-col>
      <v-col cols="auto">
        <v-btn 
          color="primary" 
          prepend-icon="mdi-account-plus"
          @click="showAddFriendDialog = true"
        >
          Add Friend
        </v-btn>
      </v-col>
    </v-row>

    <!-- Quick Actions Row -->
    <v-row class="mb-4">
      <!-- Pending Requests Alert -->
      <v-col cols="12" md="6" v-if="pendingRequests.received.length > 0">
        <v-alert
          type="info"
          variant="tonal"
          prominent
        >
          <v-row align="center" no-gutters>
            <v-col>
              <div class="text-h6">
                {{ pendingRequests.received.length}} pending 
                {{ pendingRequests.received.length === 1 ? 'request' : 'requests' }}
              </div>
            </v-col>
            <v-col cols="auto">
              <v-btn to="/friends/requests" variant="outlined" size="small">
                View Requests
              </v-btn>
            </v-col>
          </v-row>
        </v-alert>
      </v-col>

      <!-- Privacy Warning - ONLY SHOW IF NOT SEARCHABLE -->
      <v-col cols="12" :md="pendingRequests.received.length > 0 ? 6 : 12" v-if="!profileSearchable">
        <v-alert
          type="warning"
          variant="tonal"
        >
          <v-row align="center" no-gutters>
            <v-col>
              <div class="text-subtitle-1 font-weight-bold">Profile Hidden</div>
              <div class="text-caption">Others can't find you in search</div>
            </v-col>
            <v-col cols="auto">
              <v-btn to="/settings/privacy" variant="outlined" size="small">
                Update Settings
              </v-btn>
            </v-col>
          </v-row>
        </v-alert>
      </v-col>
    </v-row>

    <!-- Loading State -->
    <v-row v-if="loading" justify="center" class="my-12">
      <v-progress-circular indeterminate size="64" color="primary" />
    </v-row>

    <!-- Error State -->
    <v-alert v-else-if="error" type="error" variant="tonal" class="mb-6">
      {{ error }}
      <div class="mt-2">
        <v-btn variant="outlined" size="small" @click="loadFriends">Retry</v-btn>
      </div>
    </v-alert>

    <!-- Empty State -->
    <v-card v-else-if="friends.length === 0" class="text-center pa-12">
      <v-icon size="80" color="grey">mdi-account-group-outline</v-icon>
      <h2 class="text-h4 mt-6 mb-4">No Friends Yet</h2>
      <p class="text-body-1 text-medium-emphasis mb-6">
        Add friends to compare ratings and discover new movies together!
      </p>
      
      <v-btn 
        color="primary" 
        size="large"
        @click="showAddFriendDialog = true"
        prepend-icon="mdi-account-plus"
      >
        Add Your First Friend
      </v-btn>
    </v-card>

    <!-- Friends List -->
    <div v-else>
      <v-row>
        <v-col 
          v-for="friend in friends" 
          :key="friend.friendshipId"
          cols="12"
          sm="6"
          md="4"
        >
          <friend-card 
            :friend="friend"
            @remove="confirmRemove(friend)"
            @compare="goToCompare(friend)"
            @profile="goToProfile(friend)"
          />
        </v-col>
      </v-row>
    </div>

    <!-- Add Friend Dialog -->
    <v-dialog v-model="showAddFriendDialog" max-width="500">
      <v-card>
        <v-card-title>Add Friend</v-card-title>
        <v-card-text>
          <v-text-field
            v-model="searchUsername"
            label="Search by username"
            variant="outlined"
            prepend-inner-icon="mdi-account-search"
            @input="debouncedSearch"
            :loading="searching"
            hint="Enter at least 2 characters"
            persistent-hint
          />

          <!-- Search Results -->
          <div v-if="searchResults.length > 0" class="mt-4">
            <v-list>
              <v-list-item
                v-for="user in searchResults"
                :key="user.userId"
              >
                <template v-slot:prepend>
                  <v-avatar color="primary">
                    <span class="text-white">{{ user.username[0].toUpperCase() }}</span>
                  </v-avatar>
                </template>

                <v-list-item-title>{{ user.username }}</v-list-item-title>

                <template v-slot:append>
                  <v-btn
                    color="primary"
                    size="small"
                    @click="sendRequest(user)"
                    :loading="sendingRequest === user.userId"
                  >
                    Add Friend
                  </v-btn>
                </template>
              </v-list-item>
            </v-list>
          </div>

          <!-- No Results -->
          <v-alert
            v-else-if="searchUsername.length >= 2 && !searching"
            type="info"
            variant="tonal"
            class="mt-4"
          >
            No users found matching "{{ searchUsername }}"
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="closeAddDialog">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Remove Dialog -->
    <v-dialog v-model="showRemoveDialog" max-width="400">
      <v-card>
        <v-card-title>Remove Friend?</v-card-title>
        <v-card-text>
          Remove {{ friendToRemove?.friendUsername }}?
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="showRemoveDialog = false">Cancel</v-btn>
          <v-btn color="error" @click="removeFriend">Remove</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar -->
    <v-snackbar v-model="showSnackbar" :color="snackbarColor">
      {{ snackbarMessage }}
    </v-snackbar>
  </div>
</template>

<script>
import FriendCard from '@/components/FriendCard.vue';

// Get API base URL
const API_BASE = process.env.VUE_APP_API_BASE_URL || 'http://localhost:5000';

export default {
  name: 'FriendsView',
  
  components: {
    FriendCard
  },
  
  data() {
    return {
      loading: false,
      error: null,
      friends: [],
      pendingRequests: {
        received: [],
        sent: []
      },
      profileSearchable: true,
      
      showAddFriendDialog: false,
      searchUsername: '',
      searchResults: [],
      searching: false,
      sendingRequest: null,
      searchTimeout: null,
      
      showRemoveDialog: false,
      friendToRemove: null,
      
      showSnackbar: false,
      snackbarMessage: '',
      snackbarColor: 'success',
    };
  },
  
  created() {
    this.loadFriends();
    this.loadPendingRequests();
    this.loadPrivacyStatus();
  },
  
  methods: {
    async loadFriends() {
      this.loading = true;
      this.error = null;
      try {
        const response = await fetch(`${API_BASE}/api/friends`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        if (response.ok) {
          this.friends = await response.json();
        } else {
          this.error = 'Failed to load friends';
        }
      } catch (err) {
        console.error('Error loading friends:', err);
        this.error = err.message || 'Failed to load friends';
      } finally {
        this.loading = false;
      }
    },
    
    async loadPendingRequests() {
      try {
        const response = await fetch(`${API_BASE}/api/friends/pending`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        if (response.ok) {
          const requests = await response.json();
          this.pendingRequests.received = requests.filter(r => r.requestType === 'received');
          this.pendingRequests.sent = requests.filter(r => r.requestType === 'sent');
        }
      } catch (err) {
        console.error('Error loading pending requests:', err);
      }
    },
    
    async loadPrivacyStatus() {
      try {
        const response = await fetch(`${API_BASE}/api/privacy`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        if (response.ok) {
          const settings = await response.json();
          this.profileSearchable = settings.privacyProfileSearchable;
        }
      } catch (err) {
        console.error('Error loading privacy settings:', err);
      }
    },
    
    debouncedSearch() {
      clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(() => {
        this.searchUsers();
      }, 300);
    },
    
    async searchUsers() {
      if (this.searchUsername.length < 2) {
        this.searchResults = [];
        return;
      }
      
      this.searching = true;
      try {
        const response = await fetch(
          `${API_BASE}/api/friends/search?q=${encodeURIComponent(this.searchUsername)}`,
          {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          }
        );
        
        if (response.ok) {
          this.searchResults = await response.json();
        } else {
          console.error('Search failed');
          this.searchResults = [];
        }
      } catch (err) {
        console.error('Error searching users:', err);
        this.searchResults = [];
      } finally {
        this.searching = false;
      }
    },
    
    async sendRequest(user) {
      this.sendingRequest = user.userId;
      try {
        const response = await fetch(`${API_BASE}/api/friends/request`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ username: user.username })
        });
        
        const data = await response.json();
        
        if (response.ok) {
          this.snackbarMessage = 'Friend request sent!';
          this.snackbarColor = 'success';
          this.showSnackbar = true;
          
          user.friendshipStatus = 'pending';
          this.closeAddDialog();
        } else {
          this.snackbarMessage = data.error || 'Failed to send request';
          this.snackbarColor = 'warning';
          this.showSnackbar = true;
        }
      } catch (err) {
        console.error('Error sending request:', err);
        this.snackbarMessage = 'Network error - please try again';
        this.snackbarColor = 'error';
        this.showSnackbar = true;
      } finally {
        this.sendingRequest = null;
      }
    },
    
    confirmRemove(friend) {
      this.friendToRemove = friend;
      this.showRemoveDialog = true;
    },
    
    async removeFriend() {
      try {
        const response = await fetch(
          `${API_BASE}/api/friends/${this.friendToRemove.friendshipId}`,
          {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          }
        );
        
        if (response.ok) {
          this.friends = this.friends.filter(
            f => f.friendshipId !== this.friendToRemove.friendshipId
          );
          this.showRemoveDialog = false;
          this.snackbarMessage = 'Friend removed';
          this.snackbarColor = 'success';
          this.showSnackbar = true;
        }
      } catch (err) {
        console.error('Error removing friend:', err);
      }
    },
    
    closeAddDialog() {
      this.showAddFriendDialog = false;
      this.searchUsername = '';
      this.searchResults = [];
    },

    // NEW: Navigation methods
    goToCompare(friend) {
      this.$router.push(`/compare/${friend.friendUsername}`);
    },

    goToProfile(friend) {
      this.$router.push(`/user/${friend.friendUsername}`);
    }
  }
};
</script>

<style scoped>
.friends-view {
  max-width: 1400px;
  margin: 0 auto;
}
</style>
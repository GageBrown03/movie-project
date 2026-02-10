<template>
  <div class="friends-view">
    <!-- Header -->
    <v-row class="mb-6 align-center">
      <v-col>
        <h1 class="text-h3 font-weight-bold">Friends</h1>
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

    <!-- Settings Link Alert -->
    <v-alert type="info" variant="tonal" class="mb-4">
      <div class="d-flex align-center">
        <div class="flex-grow-1">
          <strong>Make sure your profile is searchable!</strong>
          <div class="text-caption">Others won't be able to find you if your profile is hidden.</div>
        </div>
        <v-btn to="/settings/privacy" variant="outlined" size="small">
          Privacy Settings
        </v-btn>
      </div>
    </v-alert>

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
          
          // Update the user's status in search results
          user.friendshipStatus = 'pending';
          
          this.closeAddDialog();
        } else {
          // Show the actual error message from backend
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
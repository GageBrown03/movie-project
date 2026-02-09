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

      <!-- Privacy Warning -->
      <v-col cols="12" :md="pendingRequests.received.length > 0 ? 6 : 12">
        <v-alert
          type="warning"
          variant="tonal"
          v-if="!profileSearchable"
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

    <!-- Empty State -->
    <v-card v-else-if="friends.length === 0" class="text-center pa-12">
      <v-icon size="80" color="grey">mdi-account-group-outline</v-icon>
      <h2 class="text-h4 mt-6 mb-4">No Friends Yet</h2>
      <p class="text-body-1 text-medium-emphasis mb-6">
        Start building your movie community! Add friends to:
      </p>
      
      <v-row justify="center" class="mb-6">
        <v-col cols="12" sm="4">
          <v-icon color="primary" size="large" class="mb-2">mdi-chart-bar</v-icon>
          <div class="text-subtitle-1 font-weight-bold">Compare Ratings</div>
          <div class="text-caption text-medium-emphasis">
            See how your taste aligns
          </div>
        </v-col>
        <v-col cols="12" sm="4">
          <v-icon color="success" size="large" class="mb-2">mdi-movie-open-star</v-icon>
          <div class="text-subtitle-1 font-weight-bold">Discover Together</div>
          <div class="text-caption text-medium-emphasis">
            Share recommendations
          </div>
        </v-col>
        <v-col cols="12" sm="4">
          <v-icon color="warning" size="large" class="mb-2">mdi-eye</v-icon>
          <div class="text-subtitle-1 font-weight-bold">See Activity</div>
          <div class="text-caption text-medium-emphasis">
            Watch what friends rate
          </div>
        </v-col>
      </v-row>

      <v-btn 
        color="primary" 
        size="large"
        @click="showAddFriendDialog = true"
        prepend-icon="mdi-account-plus"
        class="mb-4"
      >
        Add Your First Friend
      </v-btn>

      <v-divider class="my-6" />

      <p class="text-caption text-medium-emphasis mb-2">
        Make sure your profile is searchable so friends can find you!
      </p>
      <v-btn 
        to="/settings/privacy" 
        variant="text"
        size="small"
        prepend-icon="mdi-cog"
      >
        Check Privacy Settings
      </v-btn>
    </v-card>

    <!-- Friends List -->
    <div v-else>
      <!-- Search/Filter -->
      <v-text-field
        v-model="searchQuery"
        prepend-inner-icon="mdi-magnify"
        label="Search friends"
        variant="outlined"
        density="comfortable"
        clearable
        class="mb-4"
      />

      <!-- Friend Cards -->
      <v-row>
        <v-col 
          v-for="friend in filteredFriends" 
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
          <!-- Username Search -->
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
                class="search-result-item"
              >
                <template v-slot:prepend>
                  <v-avatar color="primary">
                    <span class="text-white">{{ user.username[0].toUpperCase() }}</span>
                  </v-avatar>
                </template>

                <v-list-item-title>{{ user.username }}</v-list-item-title>
                <v-list-item-subtitle v-if="user.displayName">
                  {{ user.displayName }}
                </v-list-item-subtitle>

                <template v-slot:append>
                  <!-- Already Friends -->
                  <v-chip v-if="user.friendshipStatus === 'accepted'" color="success" size="small">
                    Friends
                  </v-chip>

                  <!-- Request Pending -->
                  <v-chip v-else-if="user.friendshipStatus === 'pending'" color="warning" size="small">
                    Pending
                  </v-chip>

                  <!-- Add Friend Button -->
                  <v-btn
                    v-else
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
            <div class="text-caption mt-2">
              Make sure they've enabled profile search in Privacy Settings
            </div>
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="closeAddDialog">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Remove Confirmation Dialog -->
    <v-dialog v-model="showRemoveDialog" max-width="400">
      <v-card>
        <v-card-title>Remove Friend?</v-card-title>
        <v-card-text>
          Are you sure you want to remove <strong>{{ friendToRemove?.friendUsername }}</strong>?
          <br><br>
          You'll no longer see each other's ratings and activity.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="showRemoveDialog = false">Cancel</v-btn>
          <v-btn color="error" @click="removeFriend" :loading="removing">
            Remove
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar -->
    <v-snackbar v-model="showSnackbar" :color="snackbarColor">
      {{ snackbarMessage }}
      <template v-slot:actions>
        <v-btn variant="text" @click="showSnackbar = false">Close</v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import FriendCard from '@/components/FriendCard.vue';
import { friendsAPI, privacyAPI } from '@/services/api-production';

export default {
  name: 'FriendsView',
  
  components: {
    FriendCard
  },
  
  data() {
    return {
      loading: false,
      friends: [],
      pendingRequests: {
        received: [],
        sent: []
      },
      searchQuery: '',
      profileSearchable: true,
      
      // Add friend dialog
      showAddFriendDialog: false,
      searchUsername: '',
      searchResults: [],
      searching: false,
      sendingRequest: null,
      searchTimeout: null,
      
      // Remove friend dialog
      showRemoveDialog: false,
      friendToRemove: null,
      removing: false,
      
      // Snackbar
      showSnackbar: false,
      snackbarMessage: '',
      snackbarColor: 'success',
    };
  },
  
  computed: {
    filteredFriends() {
      if (!this.searchQuery) return this.friends;
      
      const query = this.searchQuery.toLowerCase();
      return this.friends.filter(f => 
        f.friendUsername.toLowerCase().includes(query) ||
        (f.friendDisplayName && f.friendDisplayName.toLowerCase().includes(query))
      );
    }
  },
  
  created() {
    this.loadFriends();
    this.loadPendingRequests();
    this.loadPrivacySettings();
  },
  
  methods: {
    async loadFriends() {
      this.loading = true;
      try {
        this.friends = await friendsAPI.getAll();
      } catch (err) {
        console.error('Error loading friends:', err);
      } finally {
        this.loading = false;
      }
    },
    
    async loadPendingRequests() {
      try {
        const requests = await friendsAPI.getPending();
        this.pendingRequests.received = requests.filter(r => r.requestType === 'received');
        this.pendingRequests.sent = requests.filter(r => r.requestType === 'sent');
      } catch (err) {
        console.error('Error loading pending requests:', err);
      }
    },
    
    async loadPrivacySettings() {
      try {
        const settings = await privacyAPI.getSettings();
        this.profileSearchable = settings.privacyProfileSearchable;
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
        this.searchResults = await friendsAPI.search(this.searchUsername);
      } catch (err) {
        console.error('Error searching users:', err);
        this.showError(err.message || 'Search failed');
      } finally {
        this.searching = false;
      }
    },
    
    async sendRequest(user) {
      this.sendingRequest = user.userId;
      try {
        await friendsAPI.sendRequest(user.username);
        user.friendshipStatus = 'pending';
        await this.loadPendingRequests();
        this.showSuccess('Friend request sent!');
      } catch (err) {
        console.error('Error sending friend request:', err);
        this.showError(err.message || 'Failed to send request');
      } finally {
        this.sendingRequest = null;
      }
    },
    
    confirmRemove(friend) {
      this.friendToRemove = friend;
      this.showRemoveDialog = true;
    },
    
    async removeFriend() {
      this.removing = true;
      try {
        await friendsAPI.remove(this.friendToRemove.friendshipId);
        this.friends = this.friends.filter(
          f => f.friendshipId !== this.friendToRemove.friendshipId
        );
        this.showRemoveDialog = false;
        this.showSuccess('Friend removed');
      } catch (err) {
        console.error('Error removing friend:', err);
        this.showError(err.message || 'Failed to remove friend');
      } finally {
        this.removing = false;
      }
    },
    
    goToCompare(friend) {
      this.$router.push(`/friends/${friend.friendUsername}/compare`);
    },
    
    goToProfile(friend) {
      this.$router.push(`/profile/${friend.friendUsername}`);
    },
    
    closeAddDialog() {
      this.showAddFriendDialog = false;
      this.searchUsername = '';
      this.searchResults = [];
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
.friends-view {
  max-width: 1400px;
  margin: 0 auto;
}

.search-result-item {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}
</style>
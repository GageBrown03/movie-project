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

    <!-- Pending Requests Banner -->
    <v-alert
      v-if="pendingRequests.received.length > 0"
      type="info"
      variant="tonal"
      class="mb-4"
      prominent
    >
      <v-row align="center">
        <v-col>
          <div class="text-h6">
            You have {{ pendingRequests.received.length }} pending friend 
            {{ pendingRequests.received.length === 1 ? 'request' : 'requests' }}
          </div>
        </v-col>
        <v-col cols="auto">
          <v-btn to="/friends/requests" variant="outlined">
            View Requests
          </v-btn>
        </v-col>
      </v-row>
    </v-alert>

    <!-- Loading State -->
    <v-row v-if="loading" justify="center" class="my-12">
      <v-progress-circular indeterminate size="64" color="primary" />
    </v-row>

    <!-- Empty State -->
    <v-empty-state
      v-else-if="friends.length === 0"
      icon="mdi-account-group"
      title="No Friends Yet"
      text="Add friends to compare ratings and see what they're watching!"
    >
      <template v-slot:actions>
        <v-btn 
          color="primary" 
          size="large"
          @click="showAddFriendDialog = true"
          prepend-icon="mdi-account-plus"
        >
          Add Your First Friend
        </v-btn>
      </template>
    </v-empty-state>

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
          :key="friend.friendship_id"
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
                :key="user.user_id"
                class="search-result-item"
              >
                <template v-slot:prepend>
                  <v-avatar color="primary">
                    <span class="text-white">{{ user.username[0].toUpperCase() }}</span>
                  </v-avatar>
                </template>

                <v-list-item-title>{{ user.username }}</v-list-item-title>
                <v-list-item-subtitle v-if="user.display_name">
                  {{ user.display_name }}
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
                    :loading="sendingRequest === user.user_id"
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

    <!-- Remove Confirmation Dialog -->
    <v-dialog v-model="showRemoveDialog" max-width="400">
      <v-card>
        <v-card-title>Remove Friend?</v-card-title>
        <v-card-text>
          Are you sure you want to remove <strong>{{ friendToRemove?.friend_username }}</strong> from your friends?
          <br><br>
          You'll no longer be able to see each other's ratings and activity.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="showRemoveDialog = false">Cancel</v-btn>
          <v-btn color="error" @click="removeFriend" :loading="removing">
            Remove Friend
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import FriendCard from '@/components/FriendCard.vue';

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
    };
  },
  
  computed: {
    filteredFriends() {
      if (!this.searchQuery) return this.friends;
      
      const query = this.searchQuery.toLowerCase();
      return this.friends.filter(f => 
        f.friend_username.toLowerCase().includes(query) ||
        (f.friend_display_name && f.friend_display_name.toLowerCase().includes(query))
      );
    }
  },
  
  created() {
    this.loadFriends();
    this.loadPendingRequests();
  },
  
  methods: {
    async loadFriends() {
      this.loading = true;
      try {
        const response = await fetch('/api/friends', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        if (response.ok) {
          this.friends = await response.json();
        }
      } catch (err) {
        console.error('Error loading friends:', err);
      } finally {
        this.loading = false;
      }
    },
    
    async loadPendingRequests() {
      try {
        const response = await fetch('/api/friends/pending', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        if (response.ok) {
          const requests = await response.json();
          this.pendingRequests.received = requests.filter(r => r.request_type === 'received');
          this.pendingRequests.sent = requests.filter(r => r.request_type === 'sent');
        }
      } catch (err) {
        console.error('Error loading pending requests:', err);
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
          `/api/friends/search?q=${encodeURIComponent(this.searchUsername)}`,
          {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          }
        );
        
        if (response.ok) {
          this.searchResults = await response.json();
        }
      } catch (err) {
        console.error('Error searching users:', err);
      } finally {
        this.searching = false;
      }
    },
    
    async sendRequest(user) {
      this.sendingRequest = user.user_id;
      try {
        const response = await fetch('/api/friends/request', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ username: user.username })
        });
        
        if (response.ok) {
          // Update search results
          user.friendshipStatus = 'pending';
          
          // Reload pending requests
          await this.loadPendingRequests();
        } else {
          const error = await response.json();
          alert(error.error || 'Failed to send friend request');
        }
      } catch (err) {
        console.error('Error sending friend request:', err);
        alert('Failed to send friend request');
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
        const response = await fetch(`/api/friends/${this.friendToRemove.friendship_id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        if (response.ok) {
          // Remove from local list
          this.friends = this.friends.filter(
            f => f.friendship_id !== this.friendToRemove.friendship_id
          );
          this.showRemoveDialog = false;
        } else {
          alert('Failed to remove friend');
        }
      } catch (err) {
        console.error('Error removing friend:', err);
        alert('Failed to remove friend');
      } finally {
        this.removing = false;
      }
    },
    
    goToCompare(friend) {
      this.$router.push(`/friends/${friend.friend_username}/compare`);
    },
    
    goToProfile(friend) {
      this.$router.push(`/profile/${friend.friend_username}`);
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

.search-result-item {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}
</style>
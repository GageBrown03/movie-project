<template>
  <div class="friend-requests-view">
    <!-- Header -->
    <v-row class="mb-6 align-center">
      <v-col>
        <h1 class="text-h3 font-weight-bold">Friend Requests</h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Manage your pending friend requests
        </p>
      </v-col>
      <v-col cols="auto">
        <v-btn 
          variant="text" 
          prepend-icon="mdi-arrow-left"
          to="/friends"
        >
          Back to Friends
        </v-btn>
      </v-col>
    </v-row>

    <!-- Loading State -->
    <v-row v-if="loading" justify="center" class="my-12">
      <v-progress-circular indeterminate size="64" color="primary" />
    </v-row>

    <div v-else>
      <!-- Tabs -->
      <v-tabs v-model="activeTab" class="mb-6">
        <v-tab value="received">
          Received
          <v-badge 
            v-if="receivedRequests.length > 0" 
            :content="receivedRequests.length" 
            color="error"
            inline
            class="ml-2"
          />
        </v-tab>
        <v-tab value="sent">
          Sent
          <v-badge 
            v-if="sentRequests.length > 0" 
            :content="sentRequests.length" 
            color="primary"
            inline
            class="ml-2"
          />
        </v-tab>
      </v-tabs>

      <!-- Received Requests Tab -->
      <v-window v-model="activeTab">
        <v-window-item value="received">
          <!-- Empty State -->
          <v-empty-state
            v-if="receivedRequests.length === 0"
            icon="mdi-account-clock"
            title="No Pending Requests"
            text="You don't have any friend requests at the moment."
          >
            <template v-slot:actions>
              <v-btn color="primary" to="/friends">
                View Friends
              </v-btn>
            </template>
          </v-empty-state>

          <!-- Requests List -->
          <v-row v-else>
            <v-col 
              v-for="request in receivedRequests" 
              :key="request.friendship_id"
              cols="12"
              sm="6"
              md="4"
            >
              <friend-request-card
                :request="request"
                type="received"
                @accept="acceptRequest(request)"
                @decline="declineRequest(request)"
              />
            </v-col>
          </v-row>
        </v-window-item>

        <!-- Sent Requests Tab -->
        <v-window-item value="sent">
          <!-- Empty State -->
          <v-empty-state
            v-if="sentRequests.length === 0"
            icon="mdi-account-arrow-right"
            title="No Sent Requests"
            text="You haven't sent any friend requests."
          >
            <template v-slot:actions>
              <v-btn color="primary" to="/friends">
                Add Friends
              </v-btn>
            </template>
          </v-empty-state>

          <!-- Requests List -->
          <v-row v-else>
            <v-col 
              v-for="request in sentRequests" 
              :key="request.friendship_id"
              cols="12"
              sm="6"
              md="4"
            >
              <friend-request-card
                :request="request"
                type="sent"
                @cancel="cancelRequest(request)"
              />
            </v-col>
          </v-row>
        </v-window-item>
      </v-window>
    </div>

    <!-- Snackbar for notifications -->
    <v-snackbar v-model="showSnackbar" :color="snackbarColor">
      {{ snackbarMessage }}
      <template v-slot:actions>
        <v-btn variant="text" @click="showSnackbar = false">Close</v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import FriendRequestCard from '@/components/FriendRequestCard.vue';

export default {
  name: 'FriendRequestsView',
  
  components: {
    FriendRequestCard
  },
  
  data() {
    return {
      loading: false,
      activeTab: 'received',
      receivedRequests: [],
      sentRequests: [],
      
      // Snackbar
      showSnackbar: false,
      snackbarMessage: '',
      snackbarColor: 'success',
    };
  },
  
  created() {
    this.loadRequests();
  },
  
  methods: {
    async loadRequests() {
      this.loading = true;
      try {
        const response = await fetch('/api/friends/pending', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        if (response.ok) {
          const requests = await response.json();
          this.receivedRequests = requests.filter(r => r.request_type === 'received');
          this.sentRequests = requests.filter(r => r.request_type === 'sent');
        }
      } catch (err) {
        console.error('Error loading requests:', err);
        this.showError('Failed to load friend requests');
      } finally {
        this.loading = false;
      }
    },
    
    async acceptRequest(request) {
      try {
        const response = await fetch(`/api/friends/accept/${request.friendship_id}`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        if (response.ok) {
          // Remove from received requests
          this.receivedRequests = this.receivedRequests.filter(
            r => r.friendship_id !== request.friendship_id
          );
          
          this.showSuccess(`You're now friends with ${request.other_username}!`);
        } else {
          const error = await response.json();
          this.showError(error.error || 'Failed to accept request');
        }
      } catch (err) {
        console.error('Error accepting request:', err);
        this.showError('Failed to accept request');
      }
    },
    
    async declineRequest(request) {
      try {
        const response = await fetch(`/api/friends/decline/${request.friendship_id}`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        if (response.ok) {
          // Remove from received requests
          this.receivedRequests = this.receivedRequests.filter(
            r => r.friendship_id !== request.friendship_id
          );
          
          this.showSuccess('Request declined');
        } else {
          const error = await response.json();
          this.showError(error.error || 'Failed to decline request');
        }
      } catch (err) {
        console.error('Error declining request:', err);
        this.showError('Failed to decline request');
      }
    },
    
    async cancelRequest(request) {
      try {
        const response = await fetch(`/api/friends/${request.friendship_id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        if (response.ok) {
          // Remove from sent requests
          this.sentRequests = this.sentRequests.filter(
            r => r.friendship_id !== request.friendship_id
          );
          
          this.showSuccess('Request cancelled');
        } else {
          const error = await response.json();
          this.showError(error.error || 'Failed to cancel request');
        }
      } catch (err) {
        console.error('Error cancelling request:', err);
        this.showError('Failed to cancel request');
      }
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
.friend-requests-view {
  max-width: 1400px;
  margin: 0 auto;
}
</style>
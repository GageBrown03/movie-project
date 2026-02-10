<template>
  <v-container class="friend-requests-view">
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
        <h1 class="text-h3 font-weight-bold">Friend Requests</h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Manage your incoming and outgoing friend requests
        </p>
      </v-col>
    </v-row>

    <!-- Tabs -->
    <v-tabs v-model="tab" class="mb-4">
      <v-tab value="received">
        Received
        <v-badge 
          v-if="receivedRequests.length > 0" 
          :content="receivedRequests.length"
          color="error"
          class="ml-2"
        />
      </v-tab>
      <v-tab value="sent">
        Sent
        <v-badge 
          v-if="sentRequests.length > 0" 
          :content="sentRequests.length"
          color="primary"
          class="ml-2"
        />
      </v-tab>
    </v-tabs>

    <!-- Loading State -->
    <v-row v-if="loading" justify="center" class="my-12">
      <v-progress-circular indeterminate size="64" color="primary" />
    </v-row>

    <!-- Tab Content -->
    <v-window v-else v-model="tab">
      <!-- Received Requests -->
      <v-window-item value="received">
        <!-- Empty State -->
        <v-card v-if="receivedRequests.length === 0" class="text-center pa-12">
          <v-icon size="80" color="grey">mdi-inbox</v-icon>
          <h2 class="text-h5 mt-6 mb-2">No Pending Requests</h2>
          <p class="text-body-1 text-medium-emphasis">
            You don't have any friend requests right now
          </p>
          <v-btn to="/friends" color="primary" class="mt-4">
            Back to Friends
          </v-btn>
        </v-card>

        <!-- Request Cards -->
        <v-row v-else>
          <v-col 
            v-for="request in receivedRequests" 
            :key="request.friendshipId"
            cols="12"
            md="6"
          >
            <v-card>
              <v-card-text>
                <div class="d-flex align-center">
                  <v-avatar color="primary" size="56" class="mr-4">
                    <span class="text-h5 text-white">
                      {{ request.otherUsername[0].toUpperCase() }}
                    </span>
                  </v-avatar>
                  <div class="flex-grow-1">
                    <h3 class="text-h6">{{ request.otherUsername }}</h3>
                    <p class="text-caption text-medium-emphasis">
                      {{ formatDate(request.createdAt) }}
                    </p>
                  </div>
                </div>
              </v-card-text>
              <v-card-actions>
                <v-btn
                  color="success"
                  variant="flat"
                  @click="acceptRequest(request)"
                  :loading="accepting === request.friendshipId"
                >
                  Accept
                </v-btn>
                <v-btn
                  color="error"
                  variant="text"
                  @click="declineRequest(request)"
                  :loading="declining === request.friendshipId"
                >
                  Decline
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-window-item>

      <!-- Sent Requests -->
      <v-window-item value="sent">
        <!-- Empty State -->
        <v-card v-if="sentRequests.length === 0" class="text-center pa-12">
          <v-icon size="80" color="grey">mdi-send</v-icon>
          <h2 class="text-h5 mt-6 mb-2">No Sent Requests</h2>
          <p class="text-body-1 text-medium-emphasis">
            You haven't sent any friend requests
          </p>
          <v-btn to="/friends" color="primary" class="mt-4">
            Find Friends
          </v-btn>
        </v-card>

        <!-- Request Cards -->
        <v-row v-else>
          <v-col 
            v-for="request in sentRequests" 
            :key="request.friendshipId"
            cols="12"
            md="6"
          >
            <v-card>
              <v-card-text>
                <div class="d-flex align-center">
                  <v-avatar color="grey" size="56" class="mr-4">
                    <span class="text-h5 text-white">
                      {{ request.otherUsername[0].toUpperCase() }}
                    </span>
                  </v-avatar>
                  <div class="flex-grow-1">
                    <h3 class="text-h6">{{ request.otherUsername }}</h3>
                    <p class="text-caption text-medium-emphasis">
                      Sent {{ formatDate(request.createdAt) }}
                    </p>
                    <v-chip size="small" color="warning" class="mt-1">
                      Pending
                    </v-chip>
                  </div>
                </div>
              </v-card-text>
              <v-card-actions>
                <v-btn
                  color="error"
                  variant="text"
                  @click="cancelRequest(request)"
                  :loading="canceling === request.friendshipId"
                >
                  Cancel Request
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-window-item>
    </v-window>

    <!-- Snackbar -->
    <v-snackbar v-model="showSnackbar" :color="snackbarColor">
      {{ snackbarMessage }}
    </v-snackbar>
  </v-container>
</template>

<script>
const API_BASE = process.env.VUE_APP_API_BASE_URL || 'http://localhost:5000';

export default {
  name: 'FriendRequestsView',
  
  data() {
    return {
      loading: false,
      tab: 'received',
      receivedRequests: [],
      sentRequests: [],
      
      accepting: null,
      declining: null,
      canceling: null,
      
      showSnackbar: false,
      snackbarMessage: '',
      snackbarColor: 'success',
    };
  },
  
  created() {
    this.loadRequests();
  },
  
  methods: {
    goBack() {
      this.$router.push('/friends');
    },
    
    async loadRequests() {
      this.loading = true;
      try {
        const response = await fetch(`${API_BASE}/api/friends/pending`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        if (response.ok) {
          const requests = await response.json();
          this.receivedRequests = requests.filter(r => r.requestType === 'received');
          this.sentRequests = requests.filter(r => r.requestType === 'sent');
        }
      } catch (err) {
        console.error('Error loading requests:', err);
        this.showError('Failed to load requests');
      } finally {
        this.loading = false;
      }
    },
    
    async acceptRequest(request) {
      this.accepting = request.friendshipId;
      try {
        const response = await fetch(
          `${API_BASE}/api/friends/accept/${request.friendshipId}`,
          {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          }
        );
        
        if (response.ok) {
          this.receivedRequests = this.receivedRequests.filter(
            r => r.friendshipId !== request.friendshipId
          );
          this.showSuccess(`You're now friends with ${request.otherUsername}!`);
        } else {
          this.showError('Failed to accept request');
        }
      } catch (err) {
        console.error('Error accepting request:', err);
        this.showError('Failed to accept request');
      } finally {
        this.accepting = null;
      }
    },
    
    async declineRequest(request) {
      this.declining = request.friendshipId;
      try {
        const response = await fetch(
          `${API_BASE}/api/friends/decline/${request.friendshipId}`,
          {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          }
        );
        
        if (response.ok) {
          this.receivedRequests = this.receivedRequests.filter(
            r => r.friendshipId !== request.friendshipId
          );
          this.showSuccess('Request declined');
        } else {
          this.showError('Failed to decline request');
        }
      } catch (err) {
        console.error('Error declining request:', err);
        this.showError('Failed to decline request');
      } finally {
        this.declining = null;
      }
    },
    
    async cancelRequest(request) {
      this.canceling = request.friendshipId;
      try {
        const response = await fetch(
          `${API_BASE}/api/friends/${request.friendshipId}`,
          {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          }
        );
        
        if (response.ok) {
          this.sentRequests = this.sentRequests.filter(
            r => r.friendshipId !== request.friendshipId
          );
          this.showSuccess('Request canceled');
        } else {
          this.showError('Failed to cancel request');
        }
      } catch (err) {
        console.error('Error canceling request:', err);
        this.showError('Failed to cancel request');
      } finally {
        this.canceling = null;
      }
    },
    
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      const now = new Date();
      const diff = now - date;
      
      // Less than 1 minute
      if (diff < 60000) return 'Just now';
      
      // Less than 1 hour
      if (diff < 3600000) {
        const mins = Math.floor(diff / 60000);
        return `${mins} ${mins === 1 ? 'minute' : 'minutes'} ago`;
      }
      
      // Less than 1 day
      if (diff < 86400000) {
        const hours = Math.floor(diff / 3600000);
        return `${hours} ${hours === 1 ? 'hour' : 'hours'} ago`;
      }
      
      // Less than 1 week
      if (diff < 604800000) {
        const days = Math.floor(diff / 86400000);
        return `${days} ${days === 1 ? 'day' : 'days'} ago`;
      }
      
      // Format as date
      return date.toLocaleDateString();
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
  max-width: 1200px;
  margin: 0 auto;
}
</style>
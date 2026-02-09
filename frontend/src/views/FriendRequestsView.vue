<template>
  <div class="friend-requests-view">
    <!-- Header -->
    <v-row class="mb-6 align-center">
      <v-col>
        <v-btn
          variant="text"
          prepend-icon="mdi-arrow-left"
          @click="$router.push('/friends')"
        >
          Back to Friends
        </v-btn>
        
        <h1 class="text-h3 font-weight-bold mt-4">Friend Requests</h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Manage your pending friend requests
        </p>
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
            color="warning"
            inline
            class="ml-2"
          />
        </v-tab>
      </v-tabs>

      <!-- Received Requests -->
      <v-window v-model="activeTab">
        <v-window-item value="received">
          <div v-if="receivedRequests.length > 0">
            <friend-request-card
              v-for="request in receivedRequests"
              :key="request.friendshipId"
              :request="request"
              type="received"
              @accept="acceptRequest(request)"
              @decline="declineRequest(request)"
              class="mb-4"
            />
          </div>

          <!-- Empty State -->
          <v-card v-else class="text-center pa-12">
            <v-icon size="64" color="grey">mdi-inbox</v-icon>
            <h3 class="text-h5 mt-4">No Pending Requests</h3>
            <p class="text-body-2 text-medium-emphasis">
              You don't have any friend requests at the moment
            </p>
          </v-card>
        </v-window-item>

        <!-- Sent Requests -->
        <v-window-item value="sent">
          <div v-if="sentRequests.length > 0">
            <friend-request-card
              v-for="request in sentRequests"
              :key="request.friendshipId"
              :request="request"
              type="sent"
              @cancel="cancelRequest(request)"
              class="mb-4"
            />
          </div>

          <!-- Empty State -->
          <v-card v-else class="text-center pa-12">
            <v-icon size="64" color="grey">mdi-send-outline</v-icon>
            <h3 class="text-h5 mt-4">No Pending Requests</h3>
            <p class="text-body-2 text-medium-emphasis">
              You haven't sent any friend requests
            </p>
          </v-card>
        </v-window-item>
      </v-window>
    </div>

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
import FriendRequestCard from '@/components/FriendRequestCard.vue';
import { friendsAPI } from '@/services/api-production';

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
        const requests = await friendsAPI.getPending();
        this.receivedRequests = requests.filter(r => r.requestType === 'received');
        this.sentRequests = requests.filter(r => r.requestType === 'sent');
        
        // Auto-switch to received if there are requests
        if (this.receivedRequests.length > 0) {
          this.activeTab = 'received';
        }
      } catch (err) {
        console.error('Error loading requests:', err);
        this.showError(err.message || 'Failed to load requests');
      } finally {
        this.loading = false;
      }
    },
    
    async acceptRequest(request) {
      try {
        await friendsAPI.acceptRequest(request.friendshipId);
        
        // Remove from list
        this.receivedRequests = this.receivedRequests.filter(
          r => r.friendshipId !== request.friendshipId
        );
        
        this.showSuccess(`You're now friends with ${request.otherUsername}!`);
        
        // Emit event to parent/router if needed
        this.$router.push('/friends');
      } catch (err) {
        console.error('Error accepting request:', err);
        this.showError(err.message || 'Failed to accept request');
      }
    },
    
    async declineRequest(request) {
      try {
        await friendsAPI.declineRequest(request.friendshipId);
        
        // Remove from list
        this.receivedRequests = this.receivedRequests.filter(
          r => r.friendshipId !== request.friendshipId
        );
        
        this.showSuccess('Friend request declined');
      } catch (err) {
        console.error('Error declining request:', err);
        this.showError(err.message || 'Failed to decline request');
      }
    },
    
    async cancelRequest(request) {
      try {
        await friendsAPI.remove(request.friendshipId);
        
        // Remove from list
        this.sentRequests = this.sentRequests.filter(
          r => r.friendshipId !== request.friendshipId
        );
        
        this.showSuccess('Friend request cancelled');
      } catch (err) {
        console.error('Error cancelling request:', err);
        this.showError(err.message || 'Failed to cancel request');
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
  max-width: 800px;
  margin: 0 auto;
}
</style>
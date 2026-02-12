<template>
  <v-card 
    class="activity-card mb-3" 
    :class="{ 'clickable': isClickable }"
    @click="handleCardClick"
    hover
  >
    <v-card-text class="pa-4">
      <div class="d-flex align-start">
        <!-- Activity Icon/Poster -->
        <div class="activity-visual mr-3">
          <!-- Rating/Watchlist: Show poster -->
          <v-avatar
            v-if="activity.media && (activity.activityType === 'rating' || activity.activityType === 'watchlist')"
            size="60"
            rounded
            class="poster-thumb"
          >
            <v-img 
              v-if="activity.media.posterUrl" 
              :src="activity.media.posterUrl" 
              cover
            />
            <v-icon v-else size="40" color="grey">mdi-movie-outline</v-icon>
          </v-avatar>

          <!-- Friend Added: Show icon -->
          <v-avatar
            v-else-if="activity.activityType === 'friend_added'"
            size="60"
            color="secondary"
            class="friend-icon"
          >
            <v-icon size="32" color="white">mdi-account-multiple</v-icon>
          </v-avatar>

          <!-- Milestone: Show trophy -->
          <v-avatar
            v-else-if="activity.activityType === 'milestone'"
            size="60"
            color="amber"
            class="milestone-icon"
          >
            <v-icon size="32" color="white">mdi-trophy</v-icon>
          </v-avatar>
        </div>

        <!-- Activity Content -->
        <div class="activity-content flex-grow-1">
          <!-- User Info - CLICKABLE -->
          <div class="d-flex align-center mb-1">
            <span 
              class="font-weight-bold text-body-1 mr-1 username-link"
              @click.stop="goToUserProfile"
            >
              {{ activity.user.username }}
            </span>
            <span class="text-body-2 text-medium-emphasis">
              {{ activityText }}
            </span>
          </div>

          <!-- Media Title (for rating/watchlist) -->
          <div v-if="activity.media" class="media-title mb-1">
            <span class="text-body-1">{{ activity.media.title }}</span>
            <v-chip 
              v-if="activity.media.releaseYear" 
              size="x-small" 
              variant="text"
              class="ml-1"
            >
              {{ activity.media.releaseYear }}
            </v-chip>
          </div>

          <!-- Rating Stars (for rating activity) -->
          <div v-if="activity.activityType === 'rating' && activity.metadata?.rating" class="mb-1">
            <v-rating
              :model-value="activity.metadata.rating"
              readonly
              size="small"
              density="compact"
              color="amber"
            />
          </div>

          <!-- Friend Name (for friend_added) - CLICKABLE -->
          <div v-if="activity.activityType === 'friend_added' && activity.friend" class="mb-1">
            <v-chip 
              size="small" 
              variant="tonal" 
              color="secondary"
              class="clickable-chip"
              @click.stop="goToFriendProfile"
            >
              <v-icon start size="small">mdi-account</v-icon>
              {{ activity.friend.username }}
            </v-chip>
          </div>

          <!-- Milestone Info -->
          <div v-if="activity.activityType === 'milestone' && activity.metadata" class="mb-1">
            <v-chip size="small" variant="tonal" color="amber">
              <v-icon start size="small">mdi-star</v-icon>
              {{ milestoneText }}
            </v-chip>
          </div>

          <!-- Time Ago -->
          <div class="text-caption text-medium-emphasis">
            <v-icon size="14" class="mr-1">mdi-clock-outline</v-icon>
            {{ timeAgo }}
          </div>
        </div>

        <!-- Activity Type Badge -->
        <div class="activity-badge">
          <v-icon :color="activityColor" size="20">
            {{ activityIcon }}
          </v-icon>
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'ActivityCard',

  props: {
    activity: {
      type: Object,
      required: true
    }
  },

  computed: {
    activityText() {
      switch (this.activity.activityType) {
        case 'rating':
          return 'rated';
        case 'watchlist':
          return 'added to watchlist';
        case 'friend_added':
          return 'is now friends with';
        case 'milestone':
          return 'reached a milestone';
        default:
          return 'did something';
      }
    },

    activityIcon() {
      switch (this.activity.activityType) {
        case 'rating':
          return 'mdi-star';
        case 'watchlist':
          return 'mdi-bookmark';
        case 'friend_added':
          return 'mdi-account-multiple';
        case 'milestone':
          return 'mdi-trophy';
        default:
          return 'mdi-circle';
      }
    },

    activityColor() {
      switch (this.activity.activityType) {
        case 'rating':
          return 'amber';
        case 'watchlist':
          return 'info';
        case 'friend_added':
          return 'secondary';
        case 'milestone':
          return 'amber';
        default:
          return 'grey';
      }
    },

    milestoneText() {
      if (this.activity.metadata?.count) {
        return `${this.activity.metadata.count} movies rated!`;
      }
      return 'Achievement unlocked!';
    },

    timeAgo() {
      if (!this.activity.createdAt) return '';

      const now = new Date();
      const created = new Date(this.activity.createdAt);
      const diffMs = now - created;
      const diffMins = Math.floor(diffMs / 60000);
      const diffHours = Math.floor(diffMs / 3600000);
      const diffDays = Math.floor(diffMs / 86400000);

      if (diffMins < 1) return 'just now';
      if (diffMins < 60) return `${diffMins}m ago`;
      if (diffHours < 24) return `${diffHours}h ago`;
      if (diffDays < 7) return `${diffDays}d ago`;
      if (diffDays < 30) return `${Math.floor(diffDays / 7)}w ago`;
      return created.toLocaleDateString();
    },

    isClickable() {
      return this.activity.media && this.activity.media.mediaId; // Only media activities clickable
    }
  },

  methods: {
    handleCardClick() {
      // Navigate to media detail (only for rating/watchlist activities)
      if (this.activity.media && this.activity.media.mediaId) {
        this.$router.push(`/media/${this.activity.media.mediaId}`);
      }
    },

    goToUserProfile() {
      if (this.activity.user.username) {
        this.$router.push(`/user/${this.activity.user.username}`);
      }
    },

    goToFriendProfile() {
      if (this.activity.friend?.username) {
        this.$router.push(`/user/${this.activity.friend.username}`);
      }
    }
  }
};
</script>

<style scoped>
.activity-card {
  transition: all 0.2s ease;
  border-left: 3px solid transparent;
}

.activity-card.clickable {
  cursor: pointer;
}

.activity-card.clickable:hover {
  border-left-color: rgb(var(--v-theme-primary));
  transform: translateX(4px);
}

.activity-visual {
  flex-shrink: 0;
}

.poster-thumb {
  border: 2px solid rgba(var(--v-border-color), var(--v-border-opacity));
}

.activity-content {
  min-width: 0; /* Allow text truncation */
}

.media-title {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

.activity-badge {
  flex-shrink: 0;
  margin-left: 8px;
}

/* Clickable username */
.username-link {
  cursor: pointer;
  text-decoration: none;
  transition: color 0.2s ease;
}

.username-link:hover {
  color: rgb(var(--v-theme-primary));
  text-decoration: underline;
}

/* Clickable friend chip */
.clickable-chip {
  cursor: pointer;
  transition: transform 0.2s ease;
}

.clickable-chip:hover {
  transform: scale(1.05);
}

/* Mobile optimizations */
@media (max-width: 600px) {
  .activity-card :deep(.v-card-text) {
    padding: 12px !important;
  }

  .activity-visual {
    margin-right: 12px !important;
  }

  .activity-visual .v-avatar {
    width: 48px !important;
    height: 48px !important;
  }

  .friend-icon .v-icon,
  .milestone-icon .v-icon {
    font-size: 24px !important;
  }
}
</style>
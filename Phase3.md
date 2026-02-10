# 🚀 Phase 3: The "User Intent" Architecture
**Sprint Duration:** ~12-15 hours total work  
**Complexity:** Medium-High  
**Impact:** Major UX improvement (50% reduction in nav items)

---

## 🏁 Sprint Objective

Restructure the application navigation to align with **user workflows** (Decide, Manage, Socialize) rather than technical functions. Reduce sidebar clutter by 50% and implement a dynamic Home feed.

**Success Metrics:**
- Navigation items: 8 → 4 (50% reduction)
- Clicks to add media: 2 → 1
- Home page engagement: Static → Dynamic
- User menu: 0 → 1 (settings consolidated)

---

## 📋 Epic 1: Global Action ("Add Media")

**Current Problem:** "Adding" requires leaving the current view.  
**Solution:** Make it an omnipresent action.

### User Story
> As a user, I want to add a movie to my list from anywhere in the app without losing my place.

### Tasks

#### 1.1 Create `AddMediaDialog.vue` Component
```vue
// Reusable modal component
- TMDB search input
- Search results grid
- "Add to Collection" button
- Success/error states
- Emits 'success' event to refresh parent
```

**Acceptance Criteria:**
- [ ] Modal opens from any page
- [ ] Maintains scroll position when closed
- [ ] Shows success snackbar after adding
- [ ] Closes automatically after success
- [ ] ESC key closes dialog

**Files:**
- `frontend/src/components/AddMediaDialog.vue`

---

#### 1.2 Implement Global Trigger

**Desktop Implementation:**
- Add `+ Add` button to global header (right side, between dark mode and user menu)
- Opens AddMediaDialog on click

**Mobile Implementation (Bonus):**
- Floating Action Button (FAB)
- `position: fixed; bottom: 16px; right: 16px`
- z-index above content, below nav drawer

**Acceptance Criteria:**
- [ ] Button visible on all authenticated pages
- [ ] Responsive (shows as FAB on mobile, button on desktop)
- [ ] Keyboard accessible (Tab to focus, Enter to activate)

**Files:**
- `frontend/src/App.vue` (add trigger button)
- `frontend/src/components/AddMediaDialog.vue` (already created)

---

#### 1.3 Cleanup

**Remove:**
- `frontend/src/views/AddMediaView.vue`
- Route: `/media/new` from `router/index.js`
- Sidebar link: "Add Media"

**Acceptance Criteria:**
- [ ] Old route returns 404
- [ ] No broken links in UI
- [ ] Sidebar has one fewer item

---

## 📋 Epic 2: The "Explore" Hub

**Current Problem:** "Discovery" (external) and "What to Watch" (internal) are fragmented.  
**Solution:** Merge them into one intelligent hub.

### User Story
> As an indecisive user, I want one place to go to find something to watch, whether it's from my own list or new suggestions.

### Tasks

#### 2.1 Create `ExploreView.vue` with Tabs

**Tab Structure:**
```
┌────────────────────────────────────┐
│  For You  │  Shuffle  │  Trending  │
├────────────────────────────────────┤
│                                    │
│     [Tab content here]             │
│                                    │
└────────────────────────────────────┘
```

**Acceptance Criteria:**
- [ ] v-tabs component implemented
- [ ] Tab state persists during session (use route query param)
- [ ] Smooth transitions between tabs

**Files:**
- `frontend/src/views/ExploreView.vue`

---

#### 2.2 Tab 1: "For You" (Recommendations)

**Logic Migration:**
- Copy from existing `DiscoverView.vue`
- Show TMDB recommended movies based on genres user likes
- Grid of movie cards with poster, title, rating

**Improvements:**
- Add "Why this?" tooltip (e.g., "Because you liked Inception")
- Filter by genre chips at top

**Acceptance Criteria:**
- [ ] Shows 20 recommendations
- [ ] Loads from TMDB API
- [ ] Infinite scroll or "Load More" button
- [ ] Can add directly to collection

**Backend Required:**
```python
GET /api/recommendations
  → Algorithm: Top genres from user's collection
  → Return: TMDB movies matching those genres
```

---

#### 2.3 Tab 2: "Shuffle" (Random Picker)

**Logic Migration:**
- Copy from existing `RandomPickerView.vue`
- Random movie from user's unwatched collection

**Improvements:**
- Show result INLINE instead of full-screen takeover
- "Shuffle Again" button
- "Mark as Watched" quick action
- "Not Interested" removes from shuffle pool temporarily

**Acceptance Criteria:**
- [ ] Picks random movie from collection
- [ ] Shows poster, title, year, genre
- [ ] Can re-shuffle without leaving tab
- [ ] Can mark watched or skip

**Backend Required:**
```python
GET /api/media/random?filter=unwatched
  → Returns: Random movie from user's collection
```

---

#### 2.4 Tab 3: "Trending" (NEW Feature)

**New Feature:**
- Show what's popular this week (TMDB trending)
- Grid of movie cards
- "Add to Watchlist" quick action

**Acceptance Criteria:**
- [ ] Fetches from TMDB `/trending/all/week`
- [ ] Shows 20 trending items
- [ ] Can add to collection directly
- [ ] Updates weekly (cache for 7 days)

**Backend Required:**
```python
GET /api/trending/week
  → Fetches: TMDB trending endpoint
  → Returns: Top 20 trending movies/shows
  → Cache: 24 hours
```

---

#### 2.5 Cleanup

**Remove:**
- `frontend/src/views/RandomPickerView.vue`
- `frontend/src/views/DiscoverView.vue`
- Routes: `/random`, `/discover`
- Sidebar links: "What to Watch", "Discover"

**Update:**
- Add route: `/explore` → `ExploreView.vue`
- Add sidebar link: "Explore" (icon: `mdi-compass`)

**Acceptance Criteria:**
- [ ] Old routes redirect to `/explore`
- [ ] Sidebar has two fewer items
- [ ] All functionality preserved

---

## 📋 Epic 3: The Activity Feed (New Home)

**Current Problem:** "Home" is a static directory.  
**Solution:** Turn it into a dynamic, engaging dashboard.

### User Story
> As a returning user, I want to see recent activity and relevant updates immediately upon login.

### Tasks

#### 3.1 Backend: Activity Feed System

**Database Schema:**

```python
# New table: activities
class Activity(db.Model):
    __tablename__ = 'activities'
    
    activity_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    activity_type = db.Column(db.String(50))  # 'rating', 'friend_add', 'milestone', 'system'
    target_type = db.Column(db.String(50))    # 'media', 'user', 'achievement'
    target_id = db.Column(db.Integer)
    metadata = db.Column(db.JSON)             # Flexible data storage
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_public = db.Column(db.Boolean, default=True)
```

**Activity Types:**
1. **rating** - User rated a movie
   - `metadata`: `{media_id, title, rating, poster_url}`
2. **friend_add** - User added a friend
   - `metadata`: `{friend_id, friend_username}`
3. **milestone** - User hit a milestone
   - `metadata`: `{milestone_type, count}` (e.g., "50_movies")
4. **collection_add** - User added media
   - `metadata`: `{media_id, title, poster_url}`

**Backend Routes:**

```python
# backend/src/routes/activity.py

@activity.route('/feed', methods=['GET'])
@jwt_required()
def get_activity_feed():
    """
    Get activity feed for current user
    Includes: own activity + friends' activity (respecting privacy)
    """
    current_user_id = int(get_jwt_identity())
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Get user's friend IDs
    friend_ids = get_user_friend_ids(current_user_id)
    
    # Query activities from self and friends
    activities = Activity.query.filter(
        db.or_(
            Activity.user_id == current_user_id,
            db.and_(
                Activity.user_id.in_(friend_ids),
                Activity.is_public == True
            )
        )
    ).order_by(
        Activity.created_at.desc()
    ).paginate(page=page, per_page=per_page)
    
    # Format response
    feed_items = []
    for activity in activities.items:
        user = User.query.get(activity.user_id)
        feed_items.append({
            'activityId': activity.activity_id,
            'type': activity.activity_type,
            'user': {
                'userId': user.user_id,
                'username': user.username
            },
            'metadata': activity.metadata,
            'createdAt': activity.created_at.isoformat(),
            'isOwn': activity.user_id == current_user_id
        })
    
    return jsonify({
        'items': feed_items,
        'page': page,
        'totalPages': activities.pages,
        'hasMore': activities.has_next
    }), 200


@activity.route('/create', methods=['POST'])
@jwt_required()
def create_activity():
    """
    Create a new activity (called internally when user rates, adds friend, etc.)
    """
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    activity = Activity(
        user_id=current_user_id,
        activity_type=data.get('type'),
        target_type=data.get('targetType'),
        target_id=data.get('targetId'),
        metadata=data.get('metadata'),
        is_public=data.get('isPublic', True)
    )
    
    db.session.add(activity)
    db.session.commit()
    
    return jsonify({'message': 'Activity created'}), 201
```

**Update Existing Routes:**

When user rates a movie, also create activity:
```python
# In media_router.py - after saving rating
activity_api.create_activity({
    'type': 'rating',
    'targetType': 'media',
    'targetId': media_id,
    'metadata': {
        'title': media.title,
        'rating': rating_value,
        'poster_url': media.poster_url
    }
})
```

**Acceptance Criteria:**
- [ ] Activity table created
- [ ] Migration runs successfully
- [ ] GET /api/activity/feed returns activities
- [ ] POST /api/activity/create works
- [ ] Activities auto-created on rating

**Files:**
- `backend/src/models.py` (add Activity model)
- `backend/src/routes/activity.py` (new file)
- `backend/app.py` (register blueprint)
- `backend/migrations/` (new migration)

---

#### 3.2 Frontend: `ActivityFeed.vue` Component

**Component Structure:**

```vue
<template>
  <div class="activity-feed">
    <!-- Loading State -->
    <v-progress-circular v-if="loading" />
    
    <!-- Empty State (New User) -->
    <v-card v-else-if="activities.length === 0" class="empty-state">
      <v-icon size="80">mdi-home-heart</v-icon>
      <h2>Welcome to myMDB!</h2>
      <p>Get started:</p>
      <v-list>
        <v-list-item prepend-icon="mdi-plus">Add your first movie</v-list-item>
        <v-list-item prepend-icon="mdi-account-plus">Add a friend</v-list-item>
        <v-list-item prepend-icon="mdi-star">Rate a movie</v-list-item>
      </v-list>
    </v-card>
    
    <!-- Feed Items -->
    <v-timeline v-else>
      <v-timeline-item
        v-for="item in activities"
        :key="item.activityId"
        :dot-color="getActivityColor(item.type)"
      >
        <activity-feed-item :activity="item" />
      </v-timeline-item>
    </v-timeline>
    
    <!-- Load More -->
    <v-btn v-if="hasMore" @click="loadMore">Load More</v-btn>
  </div>
</template>
```

**Feed Item Types:**

```vue
// ActivityFeedItem.vue
<template>
  <v-card>
    <v-card-text>
      <!-- Rating Activity -->
      <div v-if="activity.type === 'rating'" class="d-flex">
        <v-avatar :image="activity.metadata.poster_url" size="48" class="mr-3" />
        <div>
          <strong>{{ activity.user.username }}</strong>
          rated
          <strong>{{ activity.metadata.title }}</strong>
          <v-rating
            :model-value="activity.metadata.rating"
            readonly
            size="small"
            density="compact"
          />
          <div class="text-caption text-medium-emphasis">
            {{ formatTime(activity.createdAt) }}
          </div>
        </div>
      </div>
      
      <!-- Friend Add Activity -->
      <div v-else-if="activity.type === 'friend_add'">
        <strong>{{ activity.user.username }}</strong>
        and
        <strong>{{ activity.metadata.friend_username }}</strong>
        are now friends
      </div>
      
      <!-- Milestone Activity -->
      <div v-else-if="activity.type === 'milestone'">
        🎉 <strong>{{ activity.user.username }}</strong>
        reached {{ activity.metadata.count }} movies!
      </div>
    </v-card-text>
  </v-card>
</template>
```

**Acceptance Criteria:**
- [ ] Shows timeline of activities
- [ ] Different styles for different activity types
- [ ] Relative timestamps ("2 hours ago")
- [ ] Infinite scroll or "Load More"
- [ ] Click movie poster → Go to detail page
- [ ] Click username → Go to profile

**Files:**
- `frontend/src/components/ActivityFeed.vue`
- `frontend/src/components/ActivityFeedItem.vue`

---

#### 3.3 Update `HomeView.vue`

**Before:**
```vue
// Static dashboard with links
<template>
  <div>
    <h1>Welcome!</h1>
    <v-row>
      <v-col><Link to="/media">Browse</Link></v-col>
      <v-col><Link to="/friends">Friends</Link></v-col>
    </v-row>
    <StatsCards />
  </div>
</template>
```

**After:**
```vue
// Dynamic activity feed
<template>
  <div class="home-view">
    <v-row>
      <!-- Main Feed (2/3 width) -->
      <v-col cols="12" md="8">
        <h1 class="text-h4 mb-4">What's Happening</h1>
        <activity-feed />
      </v-col>
      
      <!-- Sidebar (1/3 width) -->
      <v-col cols="12" md="4">
        <!-- Quick Stats Card -->
        <v-card class="mb-4">
          <v-card-title>Your Stats</v-card-title>
          <v-card-text>
            <v-list dense>
              <v-list-item>
                <template v-slot:prepend>
                  <v-icon>mdi-movie</v-icon>
                </template>
                <v-list-item-title>{{ stats.totalMovies }} Movies</v-list-item-title>
              </v-list-item>
              <v-list-item>
                <template v-slot:prepend>
                  <v-icon>mdi-account-group</v-icon>
                </template>
                <v-list-item-title>{{ stats.friendCount }} Friends</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
        
        <!-- Trending This Week -->
        <v-card>
          <v-card-title>Trending This Week</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item
                v-for="movie in trending.slice(0, 5)"
                :key="movie.id"
                :to="`/media/${movie.id}`"
              >
                <template v-slot:prepend>
                  <v-avatar :image="movie.posterUrl" />
                </template>
                <v-list-item-title>{{ movie.title }}</v-list-item-title>
                <v-list-item-subtitle>⭐ {{ movie.rating }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>
            <v-btn to="/explore?tab=trending" block variant="text" size="small">
              See All
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>
```

**Acceptance Criteria:**
- [ ] Activity feed is main content
- [ ] Quick stats in sidebar
- [ ] Trending preview in sidebar
- [ ] Responsive (sidebar below on mobile)
- [ ] Loads fast (< 1 second)

**Files:**
- `frontend/src/views/HomeView.vue`

---

#### 3.4 Milestone Detection (Bonus)

**Auto-create milestone activities:**

```python
# backend/src/routes/media_router.py

def check_and_create_milestones(user_id):
    """Check if user hit any milestones"""
    media_count = Media.query.filter_by(user_id=user_id).count()
    
    milestones = [10, 25, 50, 100, 250, 500, 1000]
    
    if media_count in milestones:
        # Create milestone activity
        Activity(
            user_id=user_id,
            activity_type='milestone',
            metadata={'milestone_type': f'{media_count}_movies', 'count': media_count}
        )
        db.session.commit()
```

**Acceptance Criteria:**
- [ ] Milestones auto-detected on media add
- [ ] Celebration animation in feed
- [ ] One-time only (don't create duplicate)

---

## 📋 Epic 4: Navigation & Settings Cleanup

**Current Problem:** Settings clutter the main usage area.  
**Solution:** Move them to a utility menu.

### User Story
> As a user, I want a clean sidebar focused on my primary daily tasks.

### Tasks

#### 4.1 Create User Dropdown Menu

**Component Structure:**

```vue
<!-- UserMenu.vue -->
<template>
  <v-menu offset-y>
    <template v-slot:activator="{ props }">
      <v-btn icon v-bind="props">
        <v-avatar color="primary" size="32">
          <span class="text-white">{{ userInitial }}</span>
        </v-avatar>
      </v-btn>
    </template>
    
    <v-list>
      <!-- User Info Header -->
      <v-list-item>
        <v-list-item-title class="font-weight-bold">
          {{ username }}
        </v-list-item-title>
        <v-list-item-subtitle>
          📊 {{ stats.totalMovies }} movies rated
        </v-list-item-subtitle>
      </v-list-item>
      
      <v-divider />
      
      <!-- Menu Items -->
      <v-list-item to="/profile" prepend-icon="mdi-account">
        <v-list-item-title>My Profile</v-list-item-title>
      </v-list-item>
      
      <v-list-item to="/settings/privacy" prepend-icon="mdi-shield-account">
        <v-list-item-title>Privacy Settings</v-list-item-title>
      </v-list-item>
      
      <v-list-item to="/settings/account" prepend-icon="mdi-cog">
        <v-list-item-title>Account Settings</v-list-item-title>
      </v-list-item>
      
      <v-divider />
      
      <v-list-item prepend-icon="mdi-help-circle">
        <v-list-item-title>Help & Support</v-list-item-title>
      </v-list-item>
      
      <v-list-item @click="logout" prepend-icon="mdi-logout">
        <v-list-item-title>Logout</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>
```

**Acceptance Criteria:**
- [ ] Shows user avatar with initial
- [ ] Quick stats in header ("47 movies rated")
- [ ] All settings accessible
- [ ] Logout button
- [ ] Keyboard accessible (Tab, Enter)
- [ ] Closes on outside click

**Files:**
- `frontend/src/components/UserMenu.vue`
- `frontend/src/App.vue` (add to header)

---

#### 4.2 Update Global Header

**Before:**
```vue
<v-app-bar>
  <v-app-bar-title>myMDB</v-app-bar-title>
  <v-spacer />
  <v-btn @click="toggleTheme">Theme</v-btn>
  <v-btn @click="logout">Logout</v-btn>
</v-app-bar>
```

**After:**
```vue
<v-app-bar>
  <v-app-bar-title>myMDB</v-app-bar-title>
  <v-spacer />
  
  <!-- Add Media Button -->
  <v-btn prepend-icon="mdi-plus" @click="showAddDialog = true">
    Add
  </v-btn>
  
  <!-- Theme Toggle -->
  <v-btn icon @click="toggleTheme">
    <v-icon>mdi-theme-light-dark</v-icon>
  </v-btn>
  
  <!-- User Menu -->
  <user-menu />
</v-app-bar>
```

**Acceptance Criteria:**
- [ ] Add button visible
- [ ] Theme toggle present
- [ ] User menu on right
- [ ] Responsive (collapses on mobile)

---

#### 4.3 Sidebar Refactor

**Old Structure (8 items):**
1. Home
2. Browse Media
3. Analytics
4. Add Media ← Remove
5. Friends
6. What to Watch ← Merge
7. Discover ← Merge
8. Privacy Settings ← Move

**New Structure (4-5 items):**
1. 🏠 **Home** (Activity Feed)
2. 📚 **Library** (Browse Media)
3. 🧭 **Explore** (Merged: What to Watch + Discover)
4. 👥 **Social** (Friends)
5. 📊 **Analytics**

**Implementation:**

```vue
<v-navigation-drawer>
  <v-list>
    <v-list-item to="/" prepend-icon="mdi-home">
      <v-list-item-title>Home</v-list-item-title>
    </v-list-item>
    
    <v-divider />
    
    <v-list-item to="/library" prepend-icon="mdi-bookshelf">
      <v-list-item-title>Library</v-list-item-title>
    </v-list-item>
    
    <v-list-item to="/explore" prepend-icon="mdi-compass">
      <v-list-item-title>Explore</v-list-item-title>
    </v-list-item>
    
    <v-list-item to="/social" prepend-icon="mdi-account-group">
      <v-list-item-title>Social</v-list-item-title>
      <template v-slot:append v-if="pendingRequests > 0">
        <v-badge :content="pendingRequests" color="error" />
      </template>
    </v-list-item>
    
    <v-divider />
    
    <v-list-item to="/analytics" prepend-icon="mdi-chart-line">
      <v-list-item-title>Analytics</v-list-item-title>
    </v-list-item>
  </v-list>
</v-navigation-drawer>
```

**Alternative Naming:**
- "Library" → "Collections" (sounds more curated)
- "Social" → "Friends" (simpler)
- "Explore" → "Discover" OR "Decide"

**Acceptance Criteria:**
- [ ] 4-5 items total (down from 8)
- [ ] Clear iconography
- [ ] Pending requests badge on Social
- [ ] Active state highlighting
- [ ] Keyboard navigable

---

#### 4.4 Breadcrumbs System (Additional Suggestion)

**Purpose:** Help users understand where they are in deep pages.

**Implementation:**

```vue
<!-- Breadcrumbs.vue -->
<template>
  <v-breadcrumbs :items="breadcrumbs" divider="›">
    <template v-slot:item="{ item }">
      <v-breadcrumbs-item
        :to="item.to"
        :disabled="item.disabled"
      >
        {{ item.title }}
      </v-breadcrumbs-item>
    </template>
  </v-breadcrumbs>
</template>

<script>
export default {
  computed: {
    breadcrumbs() {
      const route = this.$route;
      const crumbs = [];
      
      // Build breadcrumbs from route meta
      if (route.matched) {
        route.matched.forEach(match => {
          if (match.meta.breadcrumb) {
            crumbs.push({
              title: match.meta.breadcrumb,
              to: match.path,
              disabled: match.path === route.path
            });
          }
        });
      }
      
      return crumbs;
    }
  }
}
</script>
```

**Usage in Router:**

```javascript
{
  path: '/social/:username/compare',
  component: CompareRatingsView,
  meta: {
    breadcrumb: 'Compare Ratings',
    parent: '/social'
  }
}
```

**Shows:**
```
Social › @username › Compare Ratings
```

**Acceptance Criteria:**
- [ ] Shows on all nested routes
- [ ] Links are clickable (except current page)
- [ ] Updates on route change
- [ ] Responsive (collapses on mobile)

**Files:**
- `frontend/src/components/Breadcrumbs.vue`
- `frontend/src/App.vue` (add below header)

---

#### 4.5 Route Updates

**Route Mapping Changes:**

```javascript
// Old routes (redirect)
{ path: '/media', redirect: '/library' },
{ path: '/friends', redirect: '/social' },
{ path: '/random', redirect: '/explore?tab=shuffle' },
{ path: '/discover', redirect: '/explore?tab=for-you' },

// New routes
{ path: '/library', component: LibraryView },
{ path: '/explore', component: ExploreView },
{ path: '/social', component: SocialView },
{ path: '/social/:username', component: UserProfileView },
{ path: '/social/:username/compare', component: CompareRatingsView },
```

**Acceptance Criteria:**
- [ ] Old URLs redirect to new structure
- [ ] Bookmarks don't break
- [ ] SEO-friendly paths
- [ ] All routes authenticated (meta.requiresAuth)

---

## 🎯 Recommended Execution Order

### Phase 1: Foundation (3-4 hours)
**Easy wins to clear the path:**

1. ✅ **User Menu** (Epic 4.1, 4.2)
   - Create UserMenu component
   - Add to header
   - Move Privacy Settings link

2. ✅ **Cleanup Old Routes** (Epic 4.5)
   - Add redirects
   - Update sidebar

**Deliverables:** Cleaner navigation, settings consolidated

---

### Phase 2: Global Actions (2-3 hours)
**Add media from anywhere:**

3. ✅ **Add Media Modal** (Epic 1.1, 1.2)
   - Create AddMediaDialog component
   - Add trigger to header
   - Test from multiple pages

4. ✅ **Remove Add Media Page** (Epic 1.3)
   - Delete old view
   - Update routes

**Deliverables:** Add media is now omnipresent

---

### Phase 3: Backend (2-3 hours)
**Build the data layer:**

5. ✅ **Activity System** (Epic 3.1)
   - Create Activity model
   - Run migration
   - Create activity routes
   - Update rating route to create activities

6. ✅ **Trending API** (Epic 2.4)
   - Add trending endpoint
   - Cache TMDB data

**Deliverables:** Backend ready for feed

---

### Phase 4: Explore Hub (3-4 hours)
**The big merge:**

7. ✅ **Create Explore View** (Epic 2.1-2.4)
   - Build ExploreView with tabs
   - Migrate "For You" logic
   - Migrate "Shuffle" logic
   - Add "Trending" tab

8. ✅ **Remove Old Views** (Epic 2.5)
   - Delete RandomPicker, Discover
   - Update routes

**Deliverables:** Explore hub complete

---

### Phase 5: Activity Feed (2-3 hours)
**The finale:**

9. ✅ **Activity Feed Component** (Epic 3.2)
   - Create ActivityFeed component
   - Create ActivityFeedItem component
   - Test with mock data

10. ✅ **Update Home** (Epic 3.3)
    - Replace static home with feed
    - Add sidebar with stats
    - Add trending preview

**Deliverables:** Dynamic home page

---

### Phase 6: Polish (1-2 hours)
**Final touches:**

11. ✅ **Breadcrumbs** (Epic 4.4)
    - Add Breadcrumbs component
    - Update route meta
    - Test on deep pages

12. ✅ **Testing & Refinement**
    - Test all routes
    - Fix responsive issues
    - Polish animations

**Deliverables:** Production-ready

---

## 📊 Success Metrics

After Phase 3 completion, measure:

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Nav items | 8 | 4 | ✅ 50% reduction |
| Clicks to add media | 2 | 1 | ✅ 50% faster |
| Settings in sidebar | 1 | 0 | ✅ Decluttered |
| Home engagement | Static | Dynamic | ✅ Activity-driven |
| Discovery paths | 2 separate | 1 unified | ✅ Less confusion |

---

## 🎨 Visual Mockup

**New Navigation:**
```
┌──────────────────────────────────────────────┐
│ myMDB        [+ Add] [🌙] [👤]              │ ← Header
├──────────────────────────────────────────────┤
│ ┌─────────┐  ┌───────────────────────────┐  │
│ │ 🏠 Home │  │ What's Happening          │  │
│ │ 📚 Lib  │  ├───────────────────────────┤  │
│ │ 🧭 Exp  │  │ [Activity Feed Timeline]  │  │
│ │ 👥 Soc  │  │ • Friend rated Dune 5★    │  │
│ │ 📊 Ana  │  │ • You hit 50 movies! 🎉   │  │
│ └─────────┘  │ • Trending: Oppenheimer   │  │
│              └───────────────────────────┘  │
└──────────────────────────────────────────────┘
```

---

## 🚀 Ready to Start?

**Next Immediate Steps:**

1. **Start with Phase 1** (User Menu)
   - Low risk, high visibility
   - Gets settings out of sidebar
   - ~1 hour work

2. **Then Phase 2** (Add Media Modal)
   - Clear UX win
   - Users will notice immediately
   - ~2 hours work

3. **Backend work** (Activity system)
   - Foundation for feed
   - Can work on while frontend progresses
   - ~2-3 hours

**Want me to start building Phase 1 (User Menu)?** I can create:
- UserMenu.vue component
- Updated App.vue header
- Route redirects

Let me know and we'll knock this out! 🎯
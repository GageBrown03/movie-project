import { createRouter, createWebHistory } from 'vue-router'
import ViewContainer from '../views/ViewContainer.vue';
import HomeView from '../views/HomeView.vue'
import AllMediaView from '../views/AllMediaView.vue';
import CreateMediaView from '../views/CreateMediaView.vue';
import SingleMediaView from '../views/SingleMediaView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import AnalyticsView from '../views/AnalyticsView.vue';
import RandomPickerView from '../views/RandomPickerView.vue';
import DiscoverView from '../views/DiscoverView.vue'; 
import FriendsView from '../views/FriendsView.vue';
import FriendRequestsView from '../views/FriendRequestsView.vue';
import PrivacySettingsView from '../views/PrivacySettingsView.vue'; 
import CompareRatingsView from '../views/CompareRatingsView.vue'; 

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: { requiresGuest: true }
  },
  // Analytics and Random Picker - At root level, protected by auth
  {
    path: '/analytics',
    name: 'analytics',
    component: AnalyticsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/random',
    name: 'random-picker',
    component: RandomPickerView,
    meta: { requiresAuth: true }
  },
  // Media routes
  {
    path: '/media',
    component: ViewContainer,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        component: AllMediaView,
        name: 'all-media',
      },
      {
        path: 'new',
        component: CreateMediaView,
        name: 'create-media',
      },
      {
        path: ':mediaId',
        component: SingleMediaView,
        name: 'single-media',
      },
    ],
  },
  // Friend system routes
  {
    path: '/friends',
    name: 'friends',
    component: FriendsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/friends/requests',
    name: 'friend-requests',
    component: FriendRequestsView,
    meta: { requiresAuth: true }
  },
  // Legacy /movies routes - redirect to /media
  {
    path: '/movies',
    redirect: '/media'
  },
  {
    path: '/movies/new',
    redirect: '/media/new'
  },
  {
    path: '/movies/:mediaId',
    redirect: to => `/media/${to.params.mediaId}`
  },
  // Add route for DiscoverView
  {
    path: '/discover',
    name: 'discover',
    component: DiscoverView,
    meta: { requiresAuth: true }
  },
  {// Add Routing for privacy settings
     path: '/settings/privacy',
     component: PrivacySettingsView,
     meta: { requiresAuth: true }
   },
   {
     path: '/friends/:username/compare',
     component: CompareRatingsView,
     meta: { requiresAuth: true }
   }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

// Navigation guard to protect routes
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  const isLoggedIn = !!token;
  
  // If route requires auth and user is not logged in
  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/login');
  }
  // If route is for guests only (login/register) and user IS logged in
  else if (to.meta.requiresGuest && isLoggedIn) {
    next('/media');
  }
  // Otherwise, proceed normally
  else {
    next();
  }
});

export default router;
import { createRouter, createWebHistory } from 'vue-router'
import ViewContainer from '../views/ViewContainer.vue';
import HomeView from '../views/HomeView.vue'
import AllMoviesView from '../views/AllMoviesView.vue';
import CreateMovieView from '../views/CreateMovieView.vue';
import SingleMovieView from '../views/SingleMovieView.vue';
import EditMovieView from '../views/EditMovieView.vue';
import LoginView from '../views/LoginView.vue';  // NEW
import RegisterView from '../views/RegisterView.vue';  // NEW

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/login',  // NEW
    name: 'login',
    component: LoginView,
    meta: { requiresGuest: true }  // Only accessible when NOT logged in
  },
  {
    path: '/register',  // NEW
    name: 'register',
    component: RegisterView,
    meta: { requiresGuest: true }  // Only accessible when NOT logged in
  },
  {
    path: '/movies',
    component: ViewContainer,
    meta: { requiresAuth: true },  // NEW: Requires authentication
    children: [
      {
        path: '',
        component: AllMoviesView,
        name: 'all-movies',
      },
      {
        path: 'new',
        component: CreateMovieView,
        name: 'create-movie',
      },
      {
        path: ':movieId',
        component: ViewContainer,
        children: [
          {
            path: '',
            component: SingleMovieView,
          },
          {
            path: 'edit',
            component: EditMovieView,
          },
        ],
      },
    ],
  },
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
    next('/movies');
  }
  // Otherwise, proceed normally
  else {
    next();
  }
});

export default router;
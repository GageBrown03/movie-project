import { createRouter, createWebHistory } from 'vue-router'
import ViewContainer from '../views/ViewContainer.vue';
import HomeView from '../views/HomeView.vue'
import AllmoviesView from '../views/AllmoviesView.vue';
import CreatemovieView from '../views/CreatemovieView.vue';
import SinglemovieView from '../views/SinglemovieView.vue';
import EditmovieView from '../views/EditmovieView.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/movies',
    component: ViewContainer,
    children: [
      {
        path: '',
        component: AllmoviesView,
        name: 'all-movies',
      },
      {
        path: 'new',
        component: CreatemovieView,
        name: 'create-movie',
      },
      {
        path: ':movieId',
        component: ViewContainer,
        children: [
          {
            path: '',
            component: SinglemovieView,
          },
          {
            path: 'edit',
            component: EditmovieView,
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

export default router;
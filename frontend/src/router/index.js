import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DeteksiView from '../views/DeteksiView.vue'
import TentangView from '../views/TentangView.vue'
import RiwayatView from '../views/RiwayatView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/deteksi',
      name: 'deteksi',
      component: DeteksiView,
    },
    {
      path: '/tentang',
      name: 'tentang',
      component: TentangView,
    },
    {
      path: '/riwayat',
      name: 'riwayat',
      component: RiwayatView,
    },
  ],
})

export default router

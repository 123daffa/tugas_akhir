import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DeteksiView from '../views/DeteksiView.vue'
import RiwayatView from '../views/RiwayatView.vue'
import RiwayatDetailView from '../views/RiwayatDetailView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ForgotPasswordView from '../views/ForgotPasswordView.vue'
import ProfileView from '../views/ProfileView.vue'
import { useAuth } from '../composables/useAuth'



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {requiresAuth: true}
    },
    {
      path: '/deteksi',
      name: 'deteksi',
      component: DeteksiView,
      meta: {requiresAuth: true}
    },
    {
      path: '/riwayat',
      name: 'riwayat',
      component: RiwayatView,
      meta: {requiresAuth: true}
    },
    {
      path: '/riwayat/:id',
      name: 'riwayat_detail',
      component: RiwayatDetailView,
      meta: {requiresAuth: true}
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      // meta: { hideLayout: true }
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: { hideLayout: true}
    },
    {
      path: '/lupa_password',
      name: 'lupa_password',
      component: ForgotPasswordView,
      meta: { hideLayout: true}
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
    }
  ],
})


// ===== INI BAGIAN PENJAGANYA (route guard) =====
// SEBELUM halaman tujuan benar-benar dirender.
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    next('/login')
  } else if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next('/')
  } else {
    next()
  }
})
export default router

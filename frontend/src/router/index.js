import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DeteksiView from '../views/DeteksiView.vue'
import RiwayatView from '../views/RiwayatView.vue'
import RiwayatDetailView from '../views/RiwayatDetailView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ForgotPasswordView from '../views/ForgotPasswordView.vue'
import ProfileView from '../views/ProfileView.vue'
import AdminLayout from '../components/admin/AdminLayout.vue'
import AdminDashboardView from '../views/AdminDashboardView.vue'
import AdminUsersView from '../views/AdminUsersView.vue'
import AdminHistoryView from '../views/AdminHistoryView.vue'
import { useAuthStore } from '../stores/auth'



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
      meta: {requiresAuth: true, hideLayout: true}
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { hideLayout: true }
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
    },
     {
      path: '/admin',
      component: AdminLayout,
      meta: { requiresAuth: true, requiresAdmin: true, hideLayout: true },
      children: [
        {
          path: '',
          name: 'admin_dashboard',
          component: AdminDashboardView,
        },
        {
          path: 'users',
          name: 'admin_users',
          component: AdminUsersView,
        },
        {
          path: 'history',
          name: 'admin_history',
          component: AdminHistoryView,
          meta: { hideLayout: true}
        },
      ],
    },
  ],
})


router.beforeEach(async (to) => {
  const authStore = useAuthStore()

  if (!authStore.isInitialized) {
    await authStore.initialize()
  }

  // Belum login
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    return '/login'
  }

  // Halaman khusus admin
  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    return '/'
  }

  // Sudah login lalu membuka login/register
  if (
    (to.path === '/login' || to.path === '/register') &&
    authStore.isLoggedIn
  ) {
    return authStore.isAdmin ? '/admin' : '/'
  }

  // Admin tidak boleh masuk ke halaman user
  if (
    authStore.isAdmin &&
    ['/', '/deteksi', '/riwayat', '/profile'].includes(to.path)
  ) {
    return '/admin'
  }

  return true
})

export default router

<script setup>
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { LayoutDashboard, Users, History, LogOut, ShieldCheck } from 'lucide-vue-next'
import { showSuccess, showConfirm} from '../utils/alert'

const router = useRouter()
const authStore = useAuthStore()

async function handleLogout() {
  const confirmed = await showConfirm(
    'Kamu akan keluar dari akun ini.',
    'Keluar dari Akun?',
    'Iya, Keluar'
  )
  if (!confirmed) return

  authStore.logout()
  showSuccess('Berhasil keluar dari akun.')
  router.push('/login')
}
</script>

<template>
  <aside class="sidebar">
    <div class="brand">
      <div class="brand-icon"><ShieldCheck :size="20" /></div>
      <div class="brand-text">
        <h1>FactCheck.ID</h1>
        <span>Admin Panel</span>
      </div>
    </div>

    <nav class="nav">
      <RouterLink to="/admin" class="nav-link" exact-active-class="nav-link--active">
        <LayoutDashboard :size="18" />
        <span>Dashboard</span>
      </RouterLink>
      <RouterLink to="/admin/users" class="nav-link" exact-active-class="nav-link--active">
        <Users :size="18" />
        <span>Kelola User</span>
      </RouterLink>
      <RouterLink to="/admin/history" class="nav-link" exact-active-class="nav-link--active">
        <History :size="18" />
        <span>Kelola Riwayat</span>
      </RouterLink>
    </nav>

    <div class="sidebar-footer">
      <div class="admin-info" v-if="authStore.user">
        <div class="avatar">{{ authStore.user.fullName?.charAt(0) || 'A' }}</div>
        <div class="admin-text">
          <strong>{{ authStore.user.fullName }}</strong>
          <span>{{ authStore.user.email }}</span>
        </div>
      </div>

      <button class="footer-link footer-link--danger" @click="handleLogout">
        <LogOut :size="16" />
        <span>Log Out</span>
      </button>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: 260px;
  height: 100vh;
  background: #111827;
  color: #e5e7eb;
  display: flex;
  flex-direction: column;
  z-index: 100;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 24px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.brand-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: #20d48a;
  color: #111827;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.brand-text h1 {
  font-size: 16px;
  font-weight: 700;
  color: #ffffff;
  line-height: 1.2;
}

.brand-text span {
  font-size: 12px;
  color: #9ca3af;
}

.nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 16px 12px;
  flex: 1;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: 8px;
  color: #d1d5db;
  font-size: 14px;
  font-weight: 500;
  transition: background 0.15s ease, color 0.15s ease;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.06);
  color: #ffffff;
}

.nav-link--active {
  background: #20d48a;
  color: #0b1220;
  font-weight: 600;
}

.sidebar-footer {
  padding: 16px 12px 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.admin-info {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px 16px;
}

.avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: #20d48a;
  color: #0b1220;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.admin-text {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.admin-text strong {
  font-size: 13px;
  color: #ffffff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.admin-text span {
  font-size: 12px;
  color: #9ca3af;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.footer-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 10px;
  border-radius: 8px;
  color: #d1d5db;
  font-size: 13px;
  font-weight: 500;
  background: none;
  border: none;
  cursor: pointer;
  font-family: inherit;
  width: 100%;
  text-align: left;
}

.footer-link:hover {
  background: rgba(255, 255, 255, 0.06);
  color: #ffffff;
}

.footer-link--danger:hover {
  color: #ff4d4d;
}
</style>
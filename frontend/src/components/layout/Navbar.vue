<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter} from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { House, ShieldAlert, GalleryVerticalEnd, UserPen, LogOut } from 'lucide-vue-next';
import { showSuccess, showConfirm } from '../../utils/alert'

const menuOpen = ref(false)

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
    <header class="header">
        <RouterLink to="/" class="text">
          <h1>FactCheck.ID</h1>
        </RouterLink>

        <!-- Navbar (kanan) -->
        <nav class="navbar" :class="{ open: menuOpen }">
          <RouterLink to="/" > 
            <House :size="16" style="vertical-align: middle; margin-bottom: 2px;" /> Home
          </RouterLink>
          <RouterLink to="/deteksi">
            <ShieldAlert :size="16" style="vertical-align: middle; margin-bottom: 2px; margin-right: 3px;" />Deteksi
          </RouterLink>
          <RouterLink to="/riwayat">
            <GalleryVerticalEnd :size="16" style="vertical-align: middle; margin-bottom: 2px; margin-right: 3px;" />Riwayat
          </RouterLink>
          <RouterLink to="/profile">
            <UserPen :size="16" style="vertical-align: middle; margin-bottom: 2px; margin-right: 3px;" />Profile
          </RouterLink>
          <button class="btn-mulai" @click="handleLogout">
            <LogOut :size="16" style="vertical-align: middle; margin-bottom: 2px; margin-right: 3px;" />Log Out
          </button>
        </nav>
    </header>

  
</template>


<style scoped>
/* ── Header ─────────────────────────────── */
.header {
  position       : sticky;
  top            : 0;
  z-index        : 100;
  background     : #ffffff;
  border-bottom  : 1px solid #e5e7eb;
  margin         : 0 auto;
  padding        : 0 1.5rem;
  height         : 64px;
  display        : flex;
  align-items    : center;
  justify-content: space-between;
  width: 90%;
  border-radius: 50px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* ── Navbar (kiri) ─────────────────────────── */

.text h1 {
  font-size  : 1.5rem;
  font-weight: 700;
  margin-left: 1rem; 
  color: black; 

}

/* ── Navbar (kanan) ──────────────────────── */
.navbar {
  display    : flex;
  align-items: center;
  gap        : 0.25rem;
  margin-right: 6rem;
}

.navbar a {
  text-decoration: none;
  color          : black;
  font-size      : 0.95rem;
  font-weight    : 500;
  padding        : 0.5rem 0.85rem;
  border-radius  : 6px;
  transition     : color 0.2s, background 0.2s;
  white-space    : nowrap;
}

.navbar a:hover {
  color     : #ffffff;
  background: #111827;
}

/* Link aktif */
.navbar a.router-link-exact-active {
  color          : #1B2B4B;
  background     : transparent;
  text-underline-offset: 4px;
}

.navbar a.router-link-exact-active:hover {
  background: transparent;
}

/* Tombol Mulai Deteksi */
.btn-mulai {
  background  : #111827 !important;
  color       : #ffffff !important;
  padding     : 0.5rem 1.1rem !important;
  border-radius: 20px !important;
  font-weight : 600 !important;
  margin-left: 2rem;
  margin-right: 20px;
  transition  : background 0.2s, transform 0.1s !important;
  border: none;
  cursor: pointer;
  font-family: inherit;
}

.btn-mulai:hover {
  background: #374151 !important;
  transform : translateY(-1px);
}

.btn-mulai.router-link-exact-active {
  background: #374151 !important;
  color     : #ffffff !important;
}
</style>
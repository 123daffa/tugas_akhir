<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'
import { MoveLeft } from 'lucide-vue-next';
import { showSuccess, showConfirm, showError } from '../utils/alert'

const router = useRouter()
const authStore = useAuthStore()

// Data user diambil LANGSUNG dari Pinia store -- sudah otomatis ke-fetch
// saat login/refresh lewat authStore.initialize() (GET /api/user/me),
// jadi tidak perlu fetch ulang di sini.
const user = computed(() => authStore.user || { fullName: '', email: '', joinedAt: '-' })

// Statistik pemakaian -- kartu pertama (Total Deteksi) di-highlight beda dari 4 kategori lainnya
const stats = ref([
  { label: 'Total Deteksi', value: 0, highlight: true },
  { label: 'Fakta', value: 0 },
  { label: 'False', value: 0 },
  { label: 'Misleading', value: 0 },
  { label: 'Fabricated', value: 0 }
])

async function loadStats() {
  try {
    const { data } = await api.get('/api/history', { params: { per_page: 1000, page: 1 } })
    const items = data.items || []
    const counts = { 'Fakta': 0, 'False Content': 0, 'Misleading Content': 0, 'Fabricated Content': 0 }
    items.forEach((item) => {
      if (counts[item.category] !== undefined) counts[item.category] += 1
    })
    stats.value = [
      { label: 'Total Deteksi', value: data.totalItems ?? items.length, highlight: true },
      { label: 'Fakta', value: counts['Fakta'] },
      { label: 'False', value: counts['False Content'] },
      { label: 'Misleading', value: counts['Misleading Content'] },
      { label: 'Fabricated', value: counts['Fabricated Content'] }
    ]
  } catch (err) {
    console.error('Gagal ambil statistik riwayat:', err)
  }
}

onMounted(() => {
  loadStats()
})

const initials = computed(() => user.value.fullName.trim()[0]?.toUpperCase() || '?')

// ===== Edit Nama & Email =====
const isEditingProfile = ref(false)
const profileForm = ref({ fullName: '', email: '' })
const isSavingProfile = ref(false)
const profileMessage = ref('')

const isProfileFormValid = computed(() => {
  return (
    profileForm.value.fullName.trim().length > 0 &&
    profileForm.value.email.trim().length > 0 &&
    profileForm.value.email.trim().endsWith('@gmail.com')
  )
})


function startEditingProfile() {
  profileForm.value = { fullName: user.value.fullName, email: user.value.email }
  isEditingProfile.value = true
  profileMessage.value = ''
}

function cancelEditingProfile() {
  isEditingProfile.value = false
}

async function saveProfile() {
  isSavingProfile.value = true
  profileMessage.value = ''
  try {
    const {data} = await api.put ('api/user/me', { 
      fullName: profileForm.value.fullName,
      email: profileForm.value.email
    })
    authStore.setUser(data) // update data user di store, langsung ke-reflect di Navbar dll
    isEditingProfile.value = false
    profileMessage.value = 'Profil berhasil diperbarui.'
    showSuccess('Profil berhasil diperbarui.')
  } catch (err) {
    profileMessage.value = err.response?.data?.message || 'Gagal menyimpan perubahan. Silakan coba lagi.'
    showError(message, 'Gagal Memperbarui Profil')
  } finally {
    isSavingProfile.value = false
  }
}

// ===== Ubah Password (terpisah dari edit profil, karena flownya beda:
// butuh verifikasi password lama, bukan cuma update field biasa) =====
const isChangingPassword = ref(false)
const passwordForm = ref({ currentPassword: '', newPassword: '', confirmPassword: '' })
const isSavingPassword = ref(false)
const passwordMessage = ref('')
const passwordError = ref('')

const passwordMismatch = computed(() => {
  return (
    passwordForm.value.confirmPassword.length > 0 &&
    passwordForm.value.newPassword !== passwordForm.value.confirmPassword
  )
})

const newPasswordTooShort = computed(() => {
  return passwordForm.value.newPassword.length > 0 && passwordForm.value.newPassword.length < 8
})

const isPasswordFormValid = computed(() => {
  return (
    passwordForm.value.currentPassword.length > 0 &&
    passwordForm.value.newPassword.length >= 8 &&
    passwordForm.value.newPassword === passwordForm.value.confirmPassword
  )
})

function startChangingPassword() {
  passwordForm.value = { currentPassword: '', newPassword: '', confirmPassword: '' }
  isChangingPassword.value = true
  passwordMessage.value = ''
  passwordError.value = ''
}

function cancelChangingPassword() {
  isChangingPassword.value = false
}

async function savePassword() {
  if (!isPasswordFormValid.value) return
  isSavingPassword.value = true
  passwordError.value = ''
  try {
    await api.put('api/user/me/password', {
      currentPassword: passwordForm.value.currentPassword,
      newPassword: passwordForm.value.newPassword
    })
    isChangingPassword.value = false
    passwordMessage.value = 'Password berhasil diubah.'
    showSuccess('Password berhasil diubah.')
  } catch (err) {
    // Contoh: kalau backend bilang password lama salah
    passwordError.value = err.response?.data?.message ||'Password lama tidak sesuai.'
    passwordMessage.value = message || 'Gagal mengubah password. Silakan coba lagi.'
    showError(message, 'Gagal Mengubah Password')
  } finally {
    isSavingPassword.value = false
  }
}

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
  <div class="profile-page">
    <RouterLink to="/" class="back-link"> <MoveLeft :size="16" style="vertical-align: middle; margin-bottom: 2px; margin-right: 3px;" />Kembali ke Halaman Utama</RouterLink>

    <h1 class="page-title">Pengaturan Akun</h1>

    <!-- ===== Header profil ===== -->
    <div class="profile-header">
      <div class="avatar">{{ initials }}</div>
      <div class="profile-header-text">
        <h2>{{ user.fullName }}</h2>
        <p>{{ user.email }}</p>
        <span class="joined-badge">Bergabung sejak {{ user.joinedAt }}</span>
      </div>
    </div>

    <!-- ===== Statistik: kartu pertama highlight, 4 sisanya kategori ===== -->
    <div class="stats-grid">
      <div
        v-for="stat in stats"
        :key="stat.label"
        class="stat-card"
        :class="{ 'stat-card--highlight': stat.highlight }"
      >
        <div class="stat-value">{{ stat.value }}</div>
        <div class="stat-label">{{ stat.label }}</div>
      </div>
    </div>

    <!-- ===== Informasi Akun ===== -->
    <div class="info-card">
      <div class="info-card-header">
        <h3>Informasi Akun</h3>
        <button v-if="!isEditingProfile" class="btn-edit" @click="startEditingProfile">✎ Edit Profil</button>
      </div>

      <!-- Baris Nama & Email: mode tampil -->
      <div v-if="!isEditingProfile" class="info-list">
        <div class="info-row">
          <span class="info-label">Nama Lengkap</span>
          <span class="info-value">{{ user.fullName }}</span>
        </div>
        <div class="info-row">
          <span class="info-label">Email</span>
          <span class="info-value">{{ user.email }}</span>
        </div>
      </div>

      <!-- Baris Nama & Email: mode edit -->
      <form v-else class="edit-form" @submit.prevent="saveProfile">
        <div class="form-field">
          <label for="fullName">Nama Lengkap</label>
          <input 
          id="fullName" 
          v-model="profileForm.fullName" 
          type="text" 
          :class="{ 'input-error': !profileForm.fullName.trim() }"
          />
          <p v-if="!profileForm.fullName.trim()" class="field-error">Nama lengkap tidak boleh kosong.</p>
        </div>
        <div class="form-field">
          <label for="email">Email</label>
          <input 
          id="email" 
          v-model="profileForm.email" 
          type="email" 
          :class="{ 'input-error': !profileForm.email.trim() }"
          />
           <p v-if="!profileForm.email.trim()" class="field-error">Email tidak boleh kosong.</p>
           <p v-else-if="emailInvalidDomain" class="field-error">Email harus menggunakan domain @gmail.com.</p>
        </div>
        <div class="edit-actions">
          <button type="button" class="btn-cancel" @click="cancelEditingProfile">Batal</button>
          <button type="submit" class="btn-save" :disabled="!isProfileFormValid || isSavingProfile">
            {{ isSavingProfile ? 'Menyimpan...' : 'Simpan' }}
          </button>
        </div>
      </form>

      <p v-if="profileMessage" class="save-message">{{ profileMessage }}</p>

      <!-- Baris Password: terpisah, punya flow expand sendiri -->
      <div class="password-row">
        <div v-if="!isChangingPassword" class="info-row info-row--password">
          <span class="info-label">Password</span>
          <span class="info-value-group">
            <span class="password-dots">••••••••</span>
            <button class="btn-link" @click="startChangingPassword">Ubah</button>
          </span>
        </div>

        <!-- Form ubah password, muncul cuma pas "Ubah" diklik -->
        <form v-else class="edit-form" @submit.prevent="savePassword">
          <div class="form-field">
            <label for="currentPassword">Password Saat Ini</label>
            <input id="currentPassword" v-model="passwordForm.currentPassword" type="password" autocomplete="current-password" />
          </div>
          <div class="form-field">
            <label for="newPassword">Password Baru</label>
            <input id="newPassword" v-model="passwordForm.newPassword" type="password" placeholder="Minimal 8 karakter" autocomplete="new-password" />
            <p v-if="newPasswordTooShort" class="field-error">Password minimal 8 karakter.</p>
          </div>
          <div class="form-field">
            <label for="confirmPassword">Konfirmasi Password Baru</label>
            <input id="confirmPassword" v-model="passwordForm.confirmPassword" type="password" autocomplete="new-password" />
            <p v-if="passwordMismatch" class="field-error">Password baru tidak cocok.</p>
          </div>

          <p v-if="passwordError" class="field-error">{{ passwordError }}</p>

          <div class="edit-actions">
            <button type="button" class="btn-cancel" @click="cancelChangingPassword">Batal</button>
            <button type="submit" class="btn-save" :disabled="!isPasswordFormValid || isSavingPassword">
              {{ isSavingPassword ? 'Menyimpan...' : 'Simpan Password' }}
            </button>
          </div>
        </form>

        <p v-if="passwordMessage" class="save-message">{{ passwordMessage }}</p>
      </div>
    </div>

    <!-- ===== Tombol logout ===== -->
    <div class="logout-wrapper">
      <button class="btn-logout" @click="handleLogout">⏻ Keluar dari Akun</button>
    </div>
  </div>
</template>

<style scoped>
.profile-page {
  width: 100%;
  max-width: 640px;
  margin: 0 auto;
  margin-top: 30px;
  padding: 20px;
}

.back-link {
  display: inline-block;
  font-size: 13px;
  font-weight: 700;
  color: #0f6b52 ;
  text-decoration: none;
  margin-bottom: 16px;
}

.back-link:hover {
  text-decoration: underline;
}

.page-title {
  font-size: 40px;
  font-weight: 700;
  color: var(--color-navy);
  margin: 0 0 20px;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 16px;
  background-color: #EFF4FF;
  border: 1px solid #EFF4FF;
  border-radius: 20px;
  padding: 20px;
  margin-bottom: 20px;
}

.avatar {
  width: 94px;
  height: 94px;
  border-radius: 50%;
  background: var;
  background-color: #0f6b52;
  color: white;
  font-size: 24px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.profile-header-text h2 {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-navy);
  margin: 0 0 2px;
}

.profile-header-text p {
  font-size: 15px;
  color: var(--color-text-muted);
  margin: 0 0 8px;
}

.joined-badge {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-muted);
  background: var(--color-surface);
  border-radius: 999px; 
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;
  margin-bottom: 20px;

}

@media (max-width: 640px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.stat-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  padding: 14px 8px;
  text-align: center;
  border-radius: 10px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.stat-value {
  font-size: 20px;
  font-weight: 800;
  color: #0f6b52;
}

.stat-label {
  font-size: 12px;
  color: black;
  margin-top: 2px;
}

/* Kartu "Total Deteksi" -- di-highlight beda dari 4 kartu kategori lainnya */
.stat-card--highlight {
  background: #0f6b52;
  border-color: #0f6b52;
}

.stat-card--highlight .stat-value {
  color: #fff;
}

.stat-card--highlight .stat-label {
  color: rgba(255, 255, 255, 0.8);
}

.info-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 20px;
  padding: 22px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.info-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.info-card-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: black;
}

.btn-edit {
  border: none;
  background: #0f6b52;
  color: white;
  font-size: 12px;
  font-weight: 600;
  padding: 7px 16px;
  border-radius: 999px;
}

.btn-edit:hover {
  background: white;
  color: black;
}

.info-list {
  display: flex;
  flex-direction: column;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  padding: 12px 0;
  border-bottom: 1px solid var(--color-border);
}

.password-row .info-row {
  border-bottom: none;
}

.info-label {
  color: var(--color-text-muted);
}

.info-value {
  font-weight: 600;
  color: var(--color-text);
}

.info-value-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.password-dots {
  font-weight: 600;
  letter-spacing: 2px;
  color: var(--color-text);
}

.btn-link {
  border: none;
  background: transparent;
  color: var(--color-green);
  font-size: 13px;
  font-weight: 600;
  padding: 0;
}

.btn-link:hover {
  text-decoration: underline;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding-top: 8px;
}

.form-field label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: var(--color-navy);
  margin-bottom: 6px;
}

.form-field input {
  width: 100%;
  border: 1px solid var(--color-border);
  border-radius: 10px;
  padding: 10px 12px;
  font-size: 13px;
  font-family: inherit;
}

.form-field input:focus {
  outline: none;
  border-color: var(--color-green);
}

.field-error {
  font-size: 11px;
  color: red;
  margin: 6px 0 0;
}

.edit-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 6px;
}

.btn-cancel {
  border: 1px solid var(--color-border);
  background: transparent;
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 600;
  padding: 8px 18px;
  border-radius: 999px;
}

.btn-cancel:hover {
  background-color: #0f6b52;
  color: white;
}
.btn-save {
  border: none;
  background: white;
  color: black;
  font-size: 13px;
  font-weight: 600;
  padding: 8px 18px;
  border-radius: 999px;
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-save:hover {
  background-color: #0f6b52;
  color: white;
}

.save-message {
  font-size: 12px;
  color: var(--color-green);
  margin: 12px 0 0;
}

.logout-wrapper {
  display: flex;
  justify-content: center;
}

.btn-logout {
  border: 1px solid var(--color-red);
  background: var(--color-red-bg);
  color: var(--color-red);
  font-size: 13px;
  font-weight: 600;
  padding: 10px 24px;
  border-radius: 999px;
}

.btn-logout:hover {
  background: #0f6b52;
  color: white;
}
</style>
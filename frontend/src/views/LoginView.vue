<script setup>
import { ref, computed } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { Eye,EyeOff } from 'lucide-vue-next';
import { showSuccess, showError } from '../utils/alert'

const router = useRouter()
const authStore = useAuthStore()
const form = ref({
  email: '',
  password: ''
})

const showPassword = ref(false)
const isSubmitting = ref(false)
const errorMessage = ref('')

const isFormValid = computed(() => form.value.email.trim().endsWith('@gmail.com') && form.value.password.length > 0)
const passwordTooShort = computed(() => form.value.password.length > 0 && form.value.password.length <= 8)

const emailInvalidDomain = computed(() => {
  const email = form.value.email.trim()
  return email.length > 0 && !email.endsWith('@gmail.com')
})

async function handleLogin() {
  if (!isFormValid.value) return
  errorMessage.value = ''
  isSubmitting.value = true
   try {
    await authStore.login(form.value.email, form.value.password)
    showSuccess('Login berhasil, mengalihkan ke halaman utama...')
   if (authStore.isAdmin) {
      router.replace('/admin')
    } else {
      router.replace('/')
    }

  } catch (err) {
    errorMessage.value =
      err.response?.data?.message ||'Tidak dapat terhubung ke server. Coba lagi nanti.'
      showError(errorMessage.value, 'Login Gagal')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-wrapper">
      <div class="auth-brand">
        <h1>FactCheck.ID</h1>
        <p>Akses teknologi AI untuk deteksi kebenaran informasi.</p>
      </div>

      <div class="auth-card">
        <h2 class="auth-card-title">Masuk</h2>

        <form class="auth-form" @submit.prevent="handleLogin">
          <div class="form-field">
            <label for="email">Email</label>
            <div class="input-wrapper">
              <input
                id="email"
                v-model="form.email"
                type="email"
                placeholder="nama@email.com"
                autocomplete="email"
              />
            </div>
            <p v-if="emailInvalidDomain" class="field-hint">Email harus menggunakan domain @gmail.com.</p>
          </div>

          <div class="form-field">
            <label for="password">Password</label>
            <div class="input-wrapper">
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="••••••••"
                autocomplete="current-password"
              />
              <button type="button" class="toggle-visibility" @click="showPassword = !showPassword">
                <EyeOff v-if="!showPassword" :size="18" />
                <Eye v-else :size="18" />
              </button>
            </div>
             <p v-if="passwordTooShort" class="field-hint">Password minimal 8 karakter</p>
          </div>

          <div class="form-options">
            <RouterLink to="/lupa_password" class="forgot-link">Lupa Password?</RouterLink>
          </div>

          <button type="submit" class="btn-submit" :disabled="!isFormValid || isSubmitting">
            {{ isSubmitting ? 'Memproses...' : 'Masuk' }}
          </button>
        </form>

        <p class="auth-footer-link">
          Belum punya akun? <RouterLink to="/register">Daftar</RouterLink>
        </p>
      </div>

      <p class="auth-copyright">© 2026 FactCheck.ID. Teknologi AI untuk Kebenaran Informasi.</p>
    </div>
  </div>
</template>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  background: linear-gradient(160deg, #eaf1ff 0%, #f7f9fd 60%);
}

.auth-wrapper {
  width: 100%;
  max-width: 380px;
  text-align: center;
}

.auth-brand {
  margin-bottom: 24px;
}

.auth-brand h1 {
  font-size: 50px;
  font-weight: 700;
  color: #006C49;
  margin: 0 0 8px;
}

.auth-brand p {
  font-size: 16px;
  color: #666;
  margin: 0;
  white-space: nowrap;
}

.auth-card {
  background: #ffffff ;
  border: 1px solid #e6eaf5;
  border-radius: 20px;
  padding: 28px;
  box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.06);
  text-align: left;
}

.auth-card-title {
  font-size: 20px;
  font-weight: 600;
  color: black;
  margin: 0 0 20px;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-field label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #222;
  margin-bottom: 5px;
}

.input-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  border: 1px solid #dfe3ee;
  border-radius: 999px;
  padding: 11px 16px;
  background: #fff;
  transition: border-color 0.15s ease;
}

.input-wrapper:focus-within {
  border-color: #20d48a;
}

.input-wrapper input {
  border: none;
  outline: none;
  font-size: 13px;
  font-family: inherit;
  width: 100%;
  background: transparent;
}

.toggle-visibility {
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 13px;
  opacity: 0.6;
  flex-shrink: 0;
}

.form-options {
  text-align: right;
  font-size: 12px;
}

.checkbox-row {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #555;
  cursor: pointer;
}

.checkbox-row input {
  appearance: none;
  -webkit-appearance: none;
  width: 18px;
  height: 18px;
  border: 1.5px solid #ccc;
  border-radius: 50%;
  cursor: pointer;
  flex-shrink: 0;
  position: relative;
  transition: background 0.15s ease, border-color 0.15s ease;
}
 
.checkbox-row input:checked {
  background: #20d48a;
  border-color: #20d48a;
}
 
.checkbox-row input:checked::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 11px;
  line-height: 1;
}

.forgot-link {
  color: #20d48a;
  font-weight: 600;
  text-decoration: none;
}

.forgot-link:hover {
  text-decoration: underline;
}

.field-hint {
  font-size: 12px;
  color: #ff4d4d;
  margin: 0;
  text-align: center;
}

.btn-submit {
  background: #0f6b52;
  color: #fff;
  border: none;
  padding: 13px;
  border-radius: 999px;
  font-size: 14px;
  font-weight: 600;
  margin-top: 4px;
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-submit:not(:disabled):hover {
  background: #0c5943;
}

.auth-footer-link {
  font-size: 13px;
  color: #555;
  text-align: center;
  margin: 20px 0 0;
}

.auth-footer-link a {
  color: #20d48a;
  font-weight: 600;
  text-decoration: none;
}

.auth-footer-link a:hover {
  text-decoration: underline;
}

.auth-copyright {
  font-size: 11px;
  color: #888;
  margin-top: 24px;
}
</style>
<script setup>
import { ref, computed } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { ShieldUser, Eye, EyeOff, Lock, Mail, UserPen } from 'lucide-vue-next';

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  fullName: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const agreeTerms = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const isSubmitting = ref(false)
const errorMessage = ref('')

// Validasi sederhana: tombol daftar cuma aktif kalau semua field keisi,
// password & konfirmasi cocok, dan syarat & ketentuan udah dicentang
const isFormValid = computed(() => {
  return (
    form.value.fullName.trim() &&
    form.value.email.trim() &&
    form.value.password.length >= 8 &&
    form.value.password === form.value.confirmPassword &&
    agreeTerms.value
  )
})

const passwordMismatch = computed(() => {
  return form.value.confirmPassword.length > 0 && form.value.password !== form.value.confirmPassword
})

async function handleRegister() {
  if (!isFormValid.value) return
  errorMessage.value = ''
  isSubmitting.value = true
  try {
    await authStore.register(form.value.fullName, form.value.email, form.value.password)
    router.push('/login')
  } catch (err) {
    errorMessage.value = err.response?.data?.message || 'Pendaftaran gagal. Silakan coba lagi.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-icon"><ShieldUser/></div>

      <h1 class="auth-title">Daftar FactCheck.ID</h1>
      <p class="auth-subtitle">Bergabunglah untuk memulai verifikasi informasi dengan teknologi AI.</p>

      <form class="auth-form" @submit.prevent="handleRegister">
        <div class="form-field">
          <label for="fullName">Nama Lengkap</label>
          <div class="input-wrapper">
            <span class="input-icon"><UserPen :size="18" /></span>
            <input
              id="fullName"
              v-model="form.fullName"
              type="text"
              placeholder="Masukkan nama lengkap Anda"
              autocomplete="name"
            />
          </div>
        </div>

        <div class="form-field">
          <label for="email">Email</label>
          <div class="input-wrapper">
            <span class="input-icon"><Mail :size="18" /></span>
            <input
              id="email"
              v-model="form.email"
              type="email"
              placeholder="nama@email.com"
              autocomplete="email"
            />
          </div>
        </div>

        <div class="form-field">
          <label for="password">Kata Sandi</label>
          <div class="input-wrapper">
            <span class="input-icon"><Lock :size="18" /></span>
            <input
              id="password"
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="Minimal 8 karakter"
              autocomplete="new-password"
            />
            <button type="button" class="toggle-visibility" @click="showPassword = !showPassword">
                <EyeOff v-if="!showPassword" :size="18" />
                <Eye v-else :size="18" />
            </button>
          </div>
        </div>

        <div class="form-field">
          <label for="confirmPassword">Konfirmasi Kata Sandi</label>
          <div class="input-wrapper" :class="{ 'input-wrapper--error': passwordMismatch }">
            <span class="input-icon"><Lock :size="18" /></span>
            <input
              id="confirmPassword"
              v-model="form.confirmPassword"
              :type="showConfirmPassword ? 'text' : 'password'"
              placeholder="Ulangi kata sandi"
              autocomplete="new-password"
            />
            <button type="button" class="toggle-visibility" @click="showConfirmPassword = !showConfirmPassword">
                <EyeOff v-if="!showConfirmPassword" :size="18" />
                <Eye v-else :size="18" />
            </button>
          </div>
          <p v-if="passwordMismatch" class="field-error">Kata sandi tidak cocok.</p>
        </div>

        <label class="checkbox-row">
          <input v-model="agreeTerms" type="checkbox" />
          <span>
            Saya menyetujui <a href="#">Syarat &amp; Ketentuan</a> serta
            <a href="#">Kebijakan Privasi</a>.
          </span>
        </label>

        <p v-if="errorMessage" class="form-error">{{ errorMessage }}</p>

        <button type="submit" class="btn-submit" :disabled="!isFormValid || isSubmitting">
          {{ isSubmitting ? 'Memproses...' : 'Daftar Sekarang' }}
        </button>
      </form>

      <p class="auth-footer-link">
        Sudah punya akun? <RouterLink to="/login">Login</RouterLink>
      </p>
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

.auth-card {
  width: 100%;
  max-width: 380px;
  background: #ffffff;
  border: 1px solid #e6eaf5;
  border-radius: 20px;
  padding: 32px 28px;
  box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.06);
  text-align: center;
}

.auth-icon {
  width: 48px;
  height: 48px;
  margin: 0 auto 16px;
  background: rgba(32, 212, 138, 0.12);
  color: #20d48a;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.auth-title {
  font-size: 20px;
  font-weight: 700;
  color: #0f6b52;
  margin: 0 0 6px;
}

.auth-subtitle {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  margin: 0 0 24px;
}

.auth-form {
  text-align: left;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-field label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #222;
  margin-bottom: 6px;
}

.input-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  border: 1px solid #dfe3ee;
  border-radius: 10px;
  padding: 10px 12px;
  background: #fff;
  transition: border-color 0.15s ease;
}

.input-wrapper:focus-within {
  border-color: #20d48a;
}

.input-wrapper--error {
  border-color: #ff4d4d;
}

.input-icon {
  font-size: 13px;
  opacity: 0.6;
  flex-shrink: 0;
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

.field-error {
  font-size: 11px;
  color: #ff4d4d;
  margin: 6px 0 0;
}

.checkbox-row {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 12px;
  color: #555;
  line-height: 1.5;
  cursor: pointer;
}

.checkbox-row input {
  appearance: none;
  -webkit-appearance: none;
  width: 18px;
  height: 18px;
  margin-top: 2px;
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

.checkbox-row a {
  color: #20d48a;
  font-weight: 600;
  text-decoration: none;
}

.checkbox-row a:hover {
  text-decoration: underline;
}

.form-error {
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
</style>
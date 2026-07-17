<script setup>
import { ref, computed } from 'vue'
import { RouterLink } from 'vue-router'

const form = ref({
  email: '',
  password: ''
})

const rememberMe = ref(false)
const showPassword = ref(false)
const isSubmitting = ref(false)
const errorMessage = ref('')

const isFormValid = computed(() => form.value.email.trim() && form.value.password.length > 0)

async function handleLogin() {
  if (!isFormValid.value) return
  errorMessage.value = ''
  isSubmitting.value = true
  try {
    // TODO: sambungkan ke endpoint backend, misal:
    // await api.post('/auth/login', form.value)
    console.log('Login payload:', form.value)
  } catch (err) {
    errorMessage.value = 'Email atau kata sandi salah.'
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
                {{ showPassword ? '🙈' : '👁' }}
              </button>
            </div>
          </div>

          <div class="form-options">
            <label class="checkbox-row">
              <input v-model="rememberMe" type="checkbox" />
              <span>Ingat saya</span>
            </label>
            <a href="#" class="forgot-link">Lupa Password?</a>
          </div>

          <p v-if="errorMessage" class="form-error">{{ errorMessage }}</p>

          <button type="submit" class="btn-submit" :disabled="!isFormValid || isSubmitting">
            {{ isSubmitting ? 'Memproses...' : 'Masuk' }}
          </button>
        </form>

        <p class="auth-footer-link">
          Belum punya akun? <RouterLink to="/register">Daftar</RouterLink>
        </p>
      </div>

      <p class="auth-copyright">© 2024 FactCheck.ID. Teknologi AI untuk Kebenaran Informasi.</p>
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
  background: linear-gradient(160deg, #eafaf3 0%, #f3f8ff 60%);
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
  font-size: 26px;
  font-weight: 700;
  color: #0f6b52;
  margin: 0 0 8px;
}

.auth-brand p {
  font-size: 13px;
  color: #666;
  margin: 0;
}

.auth-card {
  background: #ffffff;
  border: 1px solid #e6eaf5;
  border-radius: 20px;
  padding: 28px;
  box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.06);
  text-align: left;
}

.auth-card-title {
  font-size: 16px;
  font-weight: 700;
  color: #111;
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
  margin-bottom: 6px;
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
  display: flex;
  align-items: center;
  justify-content: space-between;
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
  accent-color: #20d48a;
}

.forgot-link {
  color: #20d48a;
  font-weight: 600;
  text-decoration: none;
}

.forgot-link:hover {
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
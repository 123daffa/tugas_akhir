<script setup>
import { ref, computed } from 'vue'
import { RouterLink } from 'vue-router'

const email = ref('')
const isSubmitting = ref(false)
const isSubmitted = ref(false) // true setelah email berhasil dikirim -- ganti tampilan jadi pesan konfirmasi
const errorMessage = ref('')

const isFormValid = computed(() => email.value.trim().length > 0)

async function handleSubmit() {
  if (!isFormValid.value) return
  errorMessage.value = ''
  isSubmitting.value = true
  try {
    // TODO: sambungkan ke endpoint backend, misal:
    // await api.post('/auth/forgot-password', { email: email.value })
    console.log('Kirim link reset ke:', email.value)

    // Tampilkan pesan konfirmasi, JANGAN kasih tau apakah email-nya
    // terdaftar atau tidak -- ini demi keamanan (mencegah orang lain
    // "menebak" email mana saja yang punya akun di sistem kita)
    isSubmitted.value = true
  } catch (err) {
    errorMessage.value = 'Terjadi kesalahan. Silakan coba lagi.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-icon">✉</div>

      <template v-if="!isSubmitted">
        <h1 class="auth-title">Lupa Kata Sandi</h1>
        <p class="auth-subtitle">Masukkan email yang terdaftar, kami akan kirimkan link untuk reset kata sandi Anda.</p>

        <form class="auth-form" @submit.prevent="handleSubmit">
          <div class="form-field">
            <label for="email">Email</label>
            <div class="input-wrapper">
              <input
                id="email"
                v-model="email"
                type="email"
                placeholder="nama@email.com"
                autocomplete="email"
              />
            </div>
          </div>

          <p v-if="errorMessage" class="form-error">{{ errorMessage }}</p>

          <button type="submit" class="btn-submit" :disabled="!isFormValid || isSubmitting">
            {{ isSubmitting ? 'Mengirim...' : 'Kirim Link Reset' }}
          </button>
        </form>
      </template>

      <!-- Tampilan setelah berhasil submit -->
      <template v-else>
        <h1 class="auth-title">Periksa Email Anda</h1>
        <p class="auth-subtitle">
          Kalau email <strong>{{ email }}</strong> terdaftar di sistem kami, link untuk reset kata sandi
          sudah kami kirimkan. Silakan cek folder inbox atau spam.
        </p>
      </template>

      <p class="auth-footer-link">
        Ingat kata sandi Anda? <RouterLink to="/login">Kembali ke Login</RouterLink>
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
  font-size: 19px;
  font-weight: 700;
  color: #0f6b52;
  margin: 0 0 6px;
}

.auth-subtitle {
  font-size: 12px;
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

.input-wrapper input {
  border: none;
  outline: none;
  font-size: 13px;
  font-family: inherit;
  width: 100%;
  background: transparent;
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
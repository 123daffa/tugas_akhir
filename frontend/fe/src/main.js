import './assets/main.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth.js'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(router)

// PENTING: tunggu initialize() selesai SEBELUM mount, supaya navbar/footer/guard
// tidak sempat render dengan state "belum login" yang salah
const authStore = useAuthStore()
authStore.initialize().then(() => {
  app.mount('#app')
})
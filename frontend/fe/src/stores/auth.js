import { defineStore } from 'pinia'
import api from '../services/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    // PENTING: baca localStorage di sini, saat state pertama kali dibuat —
    // bukan lewat action terpisah yang jalan belakangan (asynchronous/telat)
    token: localStorage.getItem('token') || null,
    user: null,
    isInitialized: false   // penanda: sudah selesai cek validitas token atau belum
  }),

  getters: {
    isLoggedIn: (state) => !!state.token && !!state.user,
    isAdmin: (state) => state.user?.role === 'admin'
  },

  actions: {
    async login(email, password) {
      const { data } = await api.post('/auth/login', { email, password })
      this.token = data.token
      this.user = data.user
      localStorage.setItem('token', data.token)
    },

    async register(fullName, email, password) {
      const { data } = await api.post('/auth/register', { fullName, email, password })
      this.token = data.token
      this.user = data.user
      localStorage.setItem('token', data.token)
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
    },

    // Dipanggil SEKALI saat app pertama kali dimuat (lihat main.js).
    // Kalau ada token di localStorage, verifikasi ke backend + ambil data user-nya
    // (karena user TIDAK ikut tersimpan di localStorage, cuma token).
    async initialize() {
      if (this.token) {
        try {
          const { data } = await api.get('/user/me')
          this.user = data
        } catch (error) {
          // token invalid/expired → bersihkan
          this.logout()
        }
      }
      this.isInitialized = true
    }
  }
})
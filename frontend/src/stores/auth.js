import { defineStore } from 'pinia'
import api from '../services/api'

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
      const { data } = await api.post('api/auth/login', { email, password })
      this.token = data.token
      this.user = data.user
      localStorage.setItem('token', data.token)
    },

    async register(fullName, email, password) {
      await api.post('api/auth/register', { fullName, email, password })
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
    },

    setUser(user) {
      this.user = user
    },

    // Dipanggil SEKALI saat app pertama kali dimuat (lihat main.js).
    // Kalau ada token di localStorage, verifikasi ke backend + ambil data user-nya
    // (karena user TIDAK ikut tersimpan di localStorage, cuma token).
    async initialize() {
      if (this.token) {
        try {
          const { data } = await api.get('api/user/me')
          this.user = data
        } catch (error) {
          // token invalid/expired → bersihkan
          this.logout()
        }
      }
      this.isInitialized = true
      // console.log('[DEBUG] initialize() selesai, isLoggedIn:', this.isLoggedIn)
    }
  }
})
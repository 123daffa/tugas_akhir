import { ref } from 'vue'

// Reactive state ini dideklarasikan DI LUAR fungsi useAuth(), bukan di dalamnya.
// Ini penting: kalau di dalam, tiap komponen yang panggil useAuth() bakal dapat
// state-nya sendiri-sendiri (gak nyambung satu sama lain). Ditaruh di luar,
// semua komponen "berbagi" 1 state yang sama -- ini pola dasar state management
// tanpa perlu install Pinia/Vuex untuk kasus sesederhana ini.

// Saat pertama kali file ini di-load, cek localStorage: kalau ada token
// tersimpan dari sesi sebelumnya, anggap user masih login (persist antar refresh halaman).
const isAuthenticated = ref(!!localStorage.getItem('factcheck_token'))

function login(token, remember = false) {
  if (remember) {
    localStorage.setItem('factcheck_token', token)    // permanen, tetap login walau browser ditutup
  } else {
    sessionStorage.setItem('factcheck_token', token)  // hilang begitu tab/browser ditutup
  }
  isAuthenticated.value = true
}

function logout() {
  localStorage.removeItem('factcheck_token')
  isAuthenticated.value = false
}

export function useAuth() {
  return { isAuthenticated, login, logout }
}
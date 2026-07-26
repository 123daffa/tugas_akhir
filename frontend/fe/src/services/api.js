import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000',
  timeout: 60000,
})

apiClient.interceptors.request.use((config) => { // api.js perlu ada interceptor yang otomatis nempelin token
  const token = localStorage.getItem('factcheck_token') || sessionStorage.getItem('factcheck_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export default apiClient
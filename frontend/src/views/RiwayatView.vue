<script setup>
import { ref, computed } from 'vue'
import FilterTabs from '../components/riwayat/FilterTabs.vue'
import HistoryCard from '../components/riwayat/HistoryCard.vue'
import PaginationBar from '../components/riwayat/PaginationBar.vue'
import apiClient from '../services/api'

const searchQuery = ref('')
const activeFilter = ref('Semua')
const currentPage = ref(1)
const totalPages = ref(1)

const items = ref([])
const isLoading = ref(false)
const errorMessage = ref('')

let searchDebounceTimer = null

async function fetchHistory() {
  isLoading.value = true
  errorMessage.value = ''
  try {
    const { data } = await apiClient.get('/api/history', {
      params: {
        category: activeFilter.value === 'Semua' ? undefined : activeFilter.value,
        q: searchQuery.value || undefined,
        page: currentPage.value,
        per_page: 8
      }
    })
    items.value = data.items
    totalPages.value = data.totalPages || 1
  } catch (err) {
    errorMessage.value = err.response?.data?.message || 'Gagal memuat riwayat. Coba lagi nanti.'
    items.value = []
  } finally {
    isLoading.value = false
  }
}

// Ganti filter kategori -> balik ke halaman 1, fetch ulang
watch(activeFilter, () => {
  currentPage.value = 1
  fetchHistory()
})

// Ganti halaman pagination -> fetch ulang
watch(currentPage, fetchHistory)

// Ketikan di search box di-debounce 400ms -- gak nembak API tiap 1 huruf diketik
watch(searchQuery, () => {
  clearTimeout(searchDebounceTimer)
  searchDebounceTimer = setTimeout(() => {
    currentPage.value = 1
    fetchHistory()
  }, 400)
})

onMounted(fetchHistory)
</script>

<template>
  <div class="riwayat-page">
    <header class="page-header">
      <div class="header-text">
        <h1>Riwayat Deteksi</h1>
        <p>Pantau jejak penelusuran fakta dan verifikasi informasi Anda.</p>
      </div>

      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Cari riwayat (judul, kata kunci)..."
        />
      </div>
    </header>

    <FilterTabs v-model="activeFilter" />

    <p v-if="errorMessage" class="error-banner">⚠ {{ errorMessage }}</p>

    <div v-if="isLoading" class="loading-state">
      <p>Memuat riwayat...</p>
    </div>

    <div v-else-if="items.length" class="history-grid">
      <HistoryCard
        v-for="item in items"
        :key="item.id"
        :id="item.id"
        :image="item.image"
        :category="item.category"
        :date="item.date"
        :type="item.type"
        :title="item.title"
        :verified="item.verified"
      />
    </div>

    <div v-else class="empty-state">
      <p>Tidak ada riwayat yang cocok dengan pencarian atau filter ini.</p>
    </div>

    <PaginationBar v-if="totalPages > 1" v-model:current-page="currentPage" :total-pages="totalPages" />
  </div>
</template>

<style scoped>
.riwayat-page {
  width: 100%;
}

.page-header {
  display: flex;
  align-items: flex-start;
  /* justify-content: space-between; */
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 24px;
}

.header-text h1 {
  font-size: 50px;
  font-weight: 700;
  color: black;
  margin-top: 30px;
  margin-left: 120px;
}

.header-text p {
  font-size: 15px;
  color: black;
  margin-left: 120px;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 8px;
  background: white;
  border: 1px solid var(--color-border);
  border-radius: 50px;       
  padding: 10px 16px;
  max-width: 320px;    
  width: 100%;
  margin-left: auto;
  margin-right: 90px;
  margin-top: 60px;
}

.search-icon {
  font-size: 13px;
  opacity: 0.6;
}

.search-box input {
  border: none;
  outline: none;
  font-size: 13px;
  font-family: inherit;
  width: 100%;               
}

.history-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
  margin-top: 24px;
  margin-left: 120px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--color-text-muted);
  font-size: 14px;
}

.error-banner {
  background: #fdecec;
  color: #dc2626;
  border: 1px solid #dc2626;
  border-radius: 10px;
  padding: 12px 16px;
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 16px;
}

.loading-state {
  text-align: center;
  padding: 60px 20px;
  color: #888;
  font-size: 14px;
}
</style>
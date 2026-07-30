<script setup>
import { ref, watch, onMounted } from 'vue'
import FilterTabs from '../components/riwayat/FilterTabs.vue'
import HistoryCard from '../components/riwayat/HistoryCard.vue'
import PaginationBar from '../components/riwayat/PaginationBar.vue'
import api from '../services/api'
import { ScanSearch } from 'lucide-vue-next';


const searchQuery = ref('')
const activeFilter = ref('Semua')
const currentPage = ref(1)

const items = ref([])
const totalPages = ref(1)
const isLoading = ref(false)

async function loadHistory() {
  isLoading.value = true
  try {
    const { data } = await api.get('/api/history', {
      params: {
        page: currentPage.value,
        category: activeFilter.value,
        q: searchQuery.value,
        per_page: 8
      }
    })
    items.value = data.items
    totalPages.value = data.totalPages || 1
  } catch (err) {
    console.error('Gagal ambil riwayat:', err)
    items.value = []
  } finally {
    isLoading.value = false
  }
}

onMounted(loadHistory)

watch(currentPage, loadHistory)

watch(activeFilter, () => {
  currentPage.value = 1
  loadHistory()
})

let searchTimeout = null
watch(searchQuery, () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    currentPage.value = 1
    loadHistory()
  }, 400)
})
// </script>

<template>
  <div class="riwayat-page">
    <header class="page-header">
      <div class="header-text">
        <h1>Riwayat Deteksi</h1>
        <p>Pantau jejak penelusuran fakta dan verifikasi informasi Anda.</p>
      </div>

      <div class="search-box">
        <span class="search-icon"><ScanSearch :size="16" style="vertical-align: middle; margin-bottom: 2px;" /></span>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Cari riwayat (judul, kata kunci)..."
        />
      </div>
    </header>

    <FilterTabs v-model="activeFilter" />

    <div v-if="items.length" class="history-grid">
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

    <!-- Kondisi kosong: ditampilkan kalau filter/pencarian gak menemukan hasil apapun -->
    <div v-else class="empty-state">
      <p>Tidak ada riwayat yang cocok dengan pencarian atau filter ini.</p>
    </div>

    <PaginationBar v-model:current-page="currentPage" :total-pages="totalPages" />
  </div>
</template>

<style scoped>
.riwayat-page {
  width: 100%;
}

.page-header {
  display: flex;
  align-items: flex-start;
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

.search-box input {
  border: none;
  outline: none;
  font-size: 13px;
  font-family: inherit;
  width: 100%;               
}

.history-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(10px, 1fr));
  gap: 20px;
  margin-top: 24px;
  margin-left: 120px;
  margin-right: 120px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--color-text-muted);
  font-size: 14px;
}
</style>
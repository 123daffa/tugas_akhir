<script setup>
import { ref, computed } from 'vue'
import FilterTabs from '../components/riwayat/FilterTabs.vue'
import HistoryCard from '../components/riwayat/HistoryCard.vue'
import PaginationBar from '../components/riwayat/PaginationBar.vue'
import { historyItems } from '../stores/Mockhistory.js'

const searchQuery = ref('')
const activeFilter = ref('Semua')
const currentPage = ref(1)

// Data dummy -- nanti diganti dengan hasil fetch dari backend Flask,
// misalnya GET /api/history?page=1&category=Fakta&q=...

// Filter berdasarkan kategori aktif + pencarian judul, dihitung ulang otomatis
// tiap kali searchQuery atau activeFilter berubah (computed = reaktif)
const filteredItems = computed(() => {
  return historyItems.filter((item) => {
    const matchCategory = activeFilter.value === 'Semua' || item.category === activeFilter.value
    const matchSearch = item.title.toLowerCase().includes(searchQuery.value.toLowerCase())
    return matchCategory && matchSearch
  })
})

// Dummy total halaman -- nanti diganti nilai dari response backend (misal data.totalPages)
const totalPages = ref(5)
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

    <div v-if="filteredItems.length" class="history-grid">
      <HistoryCard
        v-for="item in filteredItems"
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
</style>
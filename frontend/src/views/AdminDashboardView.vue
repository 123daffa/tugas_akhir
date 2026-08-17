<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'
import { Users, FileSearch, ShieldAlert } from 'lucide-vue-next'
import BarChart from '../components/admin/BarChart.vue'

const isLoading = ref(true)
const error = ref('')
const stats = ref({
  totalUsers: 0,
  totalDetections: 0,
  categoryBreakdown: {},
  modeBreakdown: {}
})

// Warna kategori, senada dengan ResultCard.vue, HistoryCard.vue, dan
// FilterTabs.vue -- diurutkan dari low harm (hijau/teal) ke high harm
// (merah tua/abu), mengacu pada "7 Types of Mis- and Disinformation"
// (First Draft, Claire Wardle 2019).
const CATEGORY_COLORS = {
  'Fakta': '#20d48a',
  'Satire atau Parodi': '#4dd0c4',
  'False Connection': '#ffe066',
  'Misleading Content': '#ffcc00',
  'False Context': '#ff9933',
  'Imposter Content': '#ff704d',
  'Manipulated Content': '#ff4d4d',
  'Fabricated Content': '#808080'
}

// Kategori yang dihitung sebagai "terindikasi hoaks" -- semua kategori
// selain "Fakta". "Satire atau Parodi" tetap dihitung karena meski tidak
// berniat menyakiti, tetap berpotensi menyesatkan pembaca (lihat definisi
// di build_prompt_klasifikasi.py).
const KATEGORI_HOAKS = [
  'Satire atau Parodi',
  'False Connection',
  'Misleading Content',
  'False Context',
  'Imposter Content',
  'Manipulated Content',
  'Fabricated Content'
]

const MODE_LABELS = { text: 'Teks', image: 'Gambar', video: 'Video' }
const MODE_COLORS = { text: '#111827', image: '#20d48a', video: '#3b82f6' }

const categoryChartData = computed(() =>
  Object.entries(stats.value.categoryBreakdown || {}).map(([label, value]) => ({
    label,
    value,
    color: CATEGORY_COLORS[label] || '#111827'
  }))
)

const modeChartData = computed(() =>
  Object.entries(stats.value.modeBreakdown || {}).map(([mode, value]) => ({
    label: MODE_LABELS[mode] || mode,
    value,
    color: MODE_COLORS[mode] || '#111827'
  }))
)

const hoaxCount = computed(() => {
  const b = stats.value.categoryBreakdown || {}
  return KATEGORI_HOAKS.reduce((total, kategori) => total + (b[kategori] || 0), 0)
})

async function loadStats() {
  isLoading.value = true
  error.value = ''
  try {
    const { data } = await api.get('/api/admin/stats')
    stats.value = data
  } catch (err) {
    console.error('Gagal ambil statistik:', err)
    error.value = 'Gagal memuat statistik. Coba muat ulang halaman.'
  } finally {
    isLoading.value = false
  }
}

onMounted(loadStats)
</script>

<template>
  <div class="dashboard">
    <header class="page-header">
      <h1>Dashboard</h1>
      <p>Ringkasan aktivitas deteksi hoaks di seluruh platform.</p>
    </header>

    <p v-if="error" class="error-banner">{{ error }}</p>

    <section class="stat-cards">
      <div class="stat-card">
        <div class="stat-icon stat-icon--blue"><Users :size="20" /></div>
        <div class="stat-text">
          <span class="stat-label">Total User</span>
          <span class="stat-value">{{ isLoading ? '—' : stats.totalUsers }}</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon stat-icon--dark"><FileSearch :size="20" /></div>
        <div class="stat-text">
          <span class="stat-label">Total Berita Dideteksi</span>
          <span class="stat-value">{{ isLoading ? '—' : stats.totalDetections }}</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon stat-icon--red"><ShieldAlert :size="20" /></div>
        <div class="stat-text">
          <span class="stat-label">Terindikasi Hoaks</span>
          <span class="stat-value">{{ isLoading ? '—' : hoaxCount }}</span>
        </div>
      </div>
    </section>

    <section class="charts-grid">
      <div class="chart-card">
        <h2>Distribusi Kategori Deteksi</h2>
        <BarChart v-if="!isLoading" :data="categoryChartData" />
      </div>

      <div class="chart-card">
        <h2>Distribusi Berdasarkan Type</h2>
        <BarChart v-if="!isLoading" :data="modeChartData" />
      </div>
    </section>
  </div>
</template>

<style scoped>
.dashboard {
  max-width: 1100px;
}

.page-header {
  margin-bottom: 28px;
}

.page-header h1 {
  font-size: 32px;
  font-weight: 700;
  color: #111827;
}

.page-header p {
  font-size: 14px;
  color: #6b7280;
  margin-top: 4px;
}

.error-banner {
  background: #fee2e2;
  color: #b91c1c;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 13px;
  margin-bottom: 20px;
}

.stat-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 28px;
}

.stat-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 14px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
}

.stat-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: #ffffff;
}

.stat-icon--blue {
  background: #3b82f6;
}

.stat-icon--dark {
  background: #111827;
}

.stat-icon--red {
  background: #ff4d4d;
}

.stat-text {
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 13px;
  color: #6b7280;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}

.chart-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 24px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
}

.chart-card h2 {
  font-size: 15px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 20px;
}
</style>
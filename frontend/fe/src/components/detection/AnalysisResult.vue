<script setup>
// Kartu "Hasil Analisis": menampilkan label klasifikasi, kesimpulan dari LLM,
// dan sumber rujukan yang ditemukan oleh Tavily search
defineProps({
  label: { type: String, default: '' },    // fakta | disinformasi | misleading | fabricated
  conclusion: { type: String, required: true },
  articles: {
    type: Array,
    default: () => []
  },
  jumlah_artikel: { type: Number, default: 0 },      // ← tambah
  kredibilitas_score: { type: Number, default: 0 }   // ← tambah (opsional)
})

// Mapping label -> warna badge, biar gampang extend kalau ada kategori baru
const labelStyleMap = {
  'Fakta': { bg: '#20d48a', color: 'white', icon: '✓' },
  'False Content': { bg: '#ff4d4d', color: 'white', icon: '⚠' },
  'Misleading Content': { bg: '#ffcc00', color: 'white', icon: '⏱' },
  'Fabricated Content': { bg: '#808080', color: 'white', icon: '✂' }
}
</script>

<template>
  <div class="result-card">
    <div class="result-header">
      <h3>Hasil Analisis</h3>
      <span
        class="badge"
        :style="{
          background: labelStyleMap[label]?.bg,
          color: labelStyleMap[label]?.color
        }">
        {{ labelStyleMap[label]?.icon}} {{ label }}
      </span>
    </div>

    <div class="section">
      <div class="section-title">
        <span class="dot">✨</span> Kesimpulan Groq AI
      </div>
      <p class="conclusion-text">{{ conclusion }}</p>
    </div>

    <!-- section jumlah artikel -->
    <div class="section">
      <div class="section-title">📊 Statistik Pencarian</div>
      <div class="stats-grid">
        <div class="stat-item">
          <span class="stat-label">Jumlah Artikel</span>
          <span class="stat-value">{{ jumlah_artikel }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Rata Rata Kredibilitas Score</span>
          <span class="stat-value">{{ (kredibilitas_score * 100).toFixed(1) }}%</span>
        </div>
      </div>
    </div>

    <div class="section">
      <div class="section-title">Sumber Rujukan Terpercaya</div>

      <div v-if="articles.length === 0">
        <p class="no-source">Tidak ada artikel ditemukan</p>
      </div>

      <div v-else class="article-list">
        <a
          v-for="(article, index) in articles"
          :key="index"
          :href="article.url"
          target="_blank"
          rel="noopener noreferrer"
          class="source-chip"
        >
          <span class="source-icon">🔗</span>
          <span class="source-title">{{ article.title }}</span>
          <span class="source-score">{{ (article.score * 100).toFixed(0) }}%</span>
        </a>
      </div>

    </div>
  </div>
</template>

<style scoped>
.result-card {
  background: white;
  border-radius: 40px;
  padding: 20px;
  box-shadow: var(--shadow-card);
  margin-left: 110px;
}

.result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.result-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
}

.badge {
  font-size: 16px;
  font-weight: 600;
  padding: 5px 12px;
  border-radius: 999px;
  white-space: nowrap;
}

.section {
  margin-bottom: 16px;
}

.section:last-child {
  margin-bottom: 0;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-navy);
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 8px;
}

.conclusion-text {
  font-size: 16px;
  line-height: 1.6;
  color: var(--color-text-muted);
  margin: 0;
}

.stats-grid {
  display: flex;
  gap: 12px;
}

.stat-item {
  flex: 1;
  background: #F8F9FF;
  border-radius: 16px;
  padding: 12px 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-label {
  font-size: 12px;
  color: var(--color-text-muted);
}

.stat-value {
  font-size: 18px;
  font-weight: 700;
  color: #006C49;
}

/* Style baru untuk list artikel */
.article-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.source-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #E5EEFF;
  color: black;
  font-size: 14px;
  font-weight: 500;
  padding: 10px 14px;
  border-radius: 20px;
  text-decoration: none;
  transition: background 0.2s;
}

.source-chip:hover {
  background: #d0e0ff;  /* sedikit lebih gelap saat hover */
}

.source-icon {
  font-size: 12px;
  flex-shrink: 0;
}

.source-title {
  flex: 1;           /* ambil sisa ruang */
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.source-score {
  font-size: 12px;
  font-weight: 700;
  color: #006C49;
  flex-shrink: 0;
}

.no-source {
  color: var(--color-text-muted);
  font-size: 14px;
}
</style>
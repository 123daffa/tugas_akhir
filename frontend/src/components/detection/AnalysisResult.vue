<script setup>
import { computed } from 'vue'
// Kartu "Hasil Analisis": menampilkan label klasifikasi, kesimpulan dari LLM,
// dan sumber rujukan yang ditemukan oleh Tavily search
const props = defineProps({
  label: { type: String, default: '' },    // fakta | false | misleading | fabricated
  penjelasan: { type: String, required: true },
  articles: {
    type: Array,
    default: () => []
  },
  jumlah_artikel: { type: Number, default: 0 },      // ← tambah
  kredibilitas_score: { type: Number, default: 0 },
  confidence: { type: Number, default: 0 },              // ← tambah
  stance_breakdown: {                                     // ← tambah
    type: Object,
    default: () => ({ MENDUKUNG: 0, MEMBANTAH: 0, TIDAK_RELEVAN: 0 })
  },
  alasan_per_artikel: {
    type: Array,
    default: () => []
  },
  // ← baru: hasil analisis gambar
  image_relevance_score: { type: Number, default: null },
  penjelasan_gambar: { type: String, default: '' },
  artikel_gambar_paling_relevan: { type: String, default: null },
  detail_gambar_per_artikel: {
    type: Array,
    default: () => []
  }
})

// Mapping label -> warna badge, biar gampang extend kalau ada kategori baru
const labelStyleMap = {
  'Fakta': { bg: '#20d48a', color: 'white', icon: '✓' },
  'False Content': { bg: '#ff4d4d', color: 'white', icon: '⚠' },
  'Misleading Content': { bg: '#ffcc00', color: 'white', icon: '⏱' },
  'Fabricated Content': { bg: '#808080', color: 'white', icon: '✂' }
}

// Warna bar confidence ikut label klasifikasi
const confidenceBarGradient = computed(() => {
  const gradientMap = {
    'Fakta': 'linear-gradient(90deg, #20d48a, #006C49)',
    'False Content': 'linear-gradient(90deg, #ff8080, #cc0000)',
    'Misleading Content': 'linear-gradient(90deg, #ffdd55, #cc9900)',
    'Fabricated Content': 'linear-gradient(90deg, #a0a0a0, #505050)'
  }
  return gradientMap[props.label] || 'linear-gradient(90deg, #20d48a, #006C49)'
})

// Warna bar image relevance: hijau kalau lolos threshold visual, merah kalau nggak.
// (Threshold visual ini cuma dipakai buat warna, angka aslinya tetap ditentukan backend)
const imageBarGradient = computed(() => {
  if (props.image_relevance_score === null) return 'linear-gradient(90deg, #20d48a, #006C49)'
  return props.image_relevance_score >= 50
    ? 'linear-gradient(90deg, #20d48a, #006C49)'
    : 'linear-gradient(90deg, #ff8080, #cc0000)'
})
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
      <p class="conclusion-text">{{ penjelasan }}</p>
    </div>

    <!-- section confidence -->
    <div class="section">
      <div class="section-title">🎯 Tingkat Keyakinan</div>
      <div class="confidence-bar-track">
        <div class="confidence-bar-fill" :style="{ width: confidence + '%', background: confidenceBarGradient }"></div>
      </div>
      <span class="confidence-label">{{ confidence.toFixed(1) }}%</span>
    </div>

    <!-- section relevansi gambar (cuma muncul kalau ada cek gambar) -->
    <div class="section" v-if="image_relevance_score !== null">
      <div class="section-title">🖼️ Relevansi Gambar</div>
      <div class="confidence-bar-track">
        <div class="confidence-bar-fill" :style="{ width: image_relevance_score + '%', background: imageBarGradient }"></div>
      </div>
      <span class="confidence-label">{{ image_relevance_score.toFixed(1) }}%</span>
      <p class="conclusion-text" v-if="penjelasan_gambar">{{ penjelasan_gambar }}</p>
      <p class="conclusion-text" v-if="artikel_gambar_paling_relevan" style="font-size: 13px; font-style: italic;">
        Dibandingkan dengan gambar dari: {{ artikel_gambar_paling_relevan }}
      </p>
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
          <span class="stat-label">Top 5 Rata Rata Kredibilitas Score</span>
          <span class="stat-value">{{ (kredibilitas_score * 100).toFixed(1) }}%</span>
        </div>
      </div>
    </div>

    <!-- section stance breakdown -->
    <div class="section">
      <div class="section-title">🗳️ Rincian Sikap Artikel</div>
      <div class="stance-grid">
        <div class="stance-item stance-support">
          <span class="stance-label">Mendukung</span>
          <span class="stance-value">{{ stance_breakdown.MENDUKUNG.toFixed(2) }}</span>
        </div>
        <div class="stance-item stance-against">
          <span class="stance-label">Membantah</span>
          <span class="stance-value">{{ stance_breakdown.MEMBANTAH.toFixed(2) }}</span>
        </div>
        <div class="stance-item stance-neutral">
          <span class="stance-label">Tidak Relevan</span>
          <span class="stance-value">{{ stance_breakdown.TIDAK_RELEVAN.toFixed(2) }}</span>
        </div>
      </div>
    </div>

      <!-- section alasan per artikel -->
  <div class="section" v-if="alasan_per_artikel.length > 0">
    <div class="section-title">📝 Analisis Per Artikel</div>
    <div class="stance-detail-list">
      <div
        v-for="(item, index) in alasan_per_artikel"
        :key="index"
        class="stance-detail-item"
        :class="{
          'stance-detail-support': item.stance === 'MENDUKUNG',
          'stance-detail-against': item.stance === 'MEMBANTAH',
          'stance-detail-neutral': item.stance === 'TIDAK_RELEVAN'
        }"
      >
        <div class="stance-detail-header">
          <span class="stance-detail-title">{{ item.judul }}</span>
          <span class="stance-detail-badge">{{ item.stance }}</span>
        </div>
        <p class="stance-detail-reason">{{ item.alasan }}</p>
      </div>
    </div>
  </div>

    <!-- section detail gambar per artikel -->
    <div class="section" v-if="detail_gambar_per_artikel.length > 0">
      <div class="section-title">🖼️ Analisis Gambar Per Artikel</div>
      <div class="stance-detail-list">
        <div
          v-for="(item, index) in detail_gambar_per_artikel"
          :key="index"
          class="stance-detail-item"
          :class="item.relevance_score >= 50 ? 'stance-detail-support' : 'stance-detail-against'"
        >
          <div class="stance-detail-header">
            <span class="stance-detail-title">{{ item.judul }}</span>
            <span class="stance-detail-badge">{{ item.relevance_score.toFixed(0) }}%</span>
          </div>
          <p class="stance-detail-reason">{{ item.penjelasan }}</p>
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

.confidence-bar-track {
  width: 100%;
  height: 10px;
  background: #F0F0F5;
  border-radius: 999px;
  overflow: hidden;
}

.confidence-bar-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.3s ease;
}

.confidence-label {
  display: inline-block;
  margin-top: 4px;
  font-size: 14px;
  font-weight: 700;
  color: #006C49;
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

.stance-grid {
  display: flex;
  gap: 8px;
}

.stance-item {
  flex: 1;
  border-radius: 16px;
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  text-align: center;
}

.stance-support {
  background: #E5FFF3;
}

.stance-against {
  background: #FFE5E5;
}

.stance-neutral {
  background: #F0F0F0;
}

.stance-label {
  font-size: 12px;
  color: var(--color-text-muted);
}

.stance-value {
  font-size: 16px;
  font-weight: 700;
}

.stance-detail-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.stance-detail-item {
  border-radius: 16px;
  padding: 12px 14px;
  border-left: 4px solid;
}

.stance-detail-support {
  background: #F0FFF7;
  border-left-color: #20d48a;
}

.stance-detail-against {
  background: #FFF0F0;
  border-left-color: #ff4d4d;
}

.stance-detail-neutral {
  background: #F5F5F5;
  border-left-color: #a0a0a0;
}

.stance-detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 6px;
}

.stance-detail-title {
  font-size: 14px;
  font-weight: 600;
  flex: 1;
}

.stance-detail-badge {
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 999px;
  background: rgba(0,0,0,0.08);
  white-space: nowrap;
  flex-shrink: 0;
}

.stance-detail-reason {
  font-size: 13px;
  line-height: 1.5;
  color: var(--color-text-muted);
  margin: 0;
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
  background: #d0e0ff;
}

.source-icon {
  font-size: 12px;
  flex-shrink: 0;
}

.source-title {
  flex: 1;
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
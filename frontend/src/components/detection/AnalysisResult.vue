<script setup>
import { computed } from 'vue'
import { Lightbulb,Feather,ChartColumnIncreasing,GalleryVerticalEnd,Image,FileText } from 'lucide-vue-next';
// Kartu "Hasil Analisis": menampilkan label klasifikasi, kesimpulan dari LLM,
// dan sumber rujukan yang ditemukan oleh Tavily search
const props = defineProps({
  label: { type: String, default: '' },    // salah satu dari kategoriUrutan di bawah
  conclusion: { type: String, required: true },
  articles: {
    type: Array,
    default: () => []
  },
  jumlah_artikel: { type: Number, default: 0 },      
  score_tavily: { type: Number, default: 0 },
  confidence: { type: Number, default: 0 },              
  stance_breakdown: {                                     
    type: Object,
    default: () => ({
      'Fakta': 0,
      'Satire atau Parodi': 0,
      'False Connection': 0,
      'Misleading Content': 0,
      'False Context': 0,
      'Imposter Content': 0,
      'Manipulated Content': 0,
      'Fabricated Content': 0
    })
  },
  alasan_per_artikel: {
    type: Array,
    default: () => []
  },
  // ← baru: hasil analisis gambar
  image_relevance_score: { type: Number, default: null },
  conclusion_gambar: { type: String, default: '' },
  artikel_gambar_paling_relevan: { type: String, default: null },
  detail_gambar_per_artikel: {
    type: Array,
    default: () => []
  }
})

// Mapping label -> warna badge, diurutkan dari low harm (hijau/teal) ke
// high harm (merah tua/abu), mengikuti spektrum "7 Types of Mis- and
// Disinformation" (First Draft, Claire Wardle 2019).
const labelStyleMap = {
  'Fakta': { bg: '#20d48a', color: 'white', icon: '✓' },
  'Satire atau Parodi': { bg: '#4dd0c4', color: 'white', icon: '😄' },
  'False Connection': { bg: '#ffe066', color: '#333', icon: '🔗' },
  'Misleading Content': { bg: '#ffcc00', color: 'white', icon: '⏱' },
  'False Context': { bg: '#ff9933', color: 'white', icon: '🗺' },
  'Imposter Content': { bg: '#ff704d', color: 'white', icon: '🎭' },
  'Manipulated Content': { bg: '#ff4d4d', color: 'white', icon: '✂' },
  'Fabricated Content': { bg: '#808080', color: 'white', icon: '⚠' }
}

const stanceCardStyleMap = {
  'Fakta': { bg: '#E5FFF3', border: '#20d48a' },
  'Satire atau Parodi': { bg: '#E5FBF9', border: '#4dd0c4' },
  'False Connection': { bg: '#FFF9E5', border: '#ffe066' },
  'Misleading Content': { bg: '#FFF8E1', border: '#ffcc00' },
  'False Context': { bg: '#FFF1E0', border: '#ff9933' },
  'Imposter Content': { bg: '#FFE9E2', border: '#ff704d' },
  'Manipulated Content': { bg: '#FFE5E5', border: '#ff4d4d' },
  'Fabricated Content': { bg: '#F0F0F0', border: '#808080' }
}

// Warna bar confidence ikut label klasifikasi
const confidenceBarGradient = computed(() => {
  const gradientMap = {
    'Fakta': 'linear-gradient(90deg, #20d48a, #006C49)',
    'Satire atau Parodi': 'linear-gradient(90deg, #7de0d6, #2c9c92)',
    'False Connection': 'linear-gradient(90deg, #ffe066, #cc9900)',
    'Misleading Content': 'linear-gradient(90deg, #ffdd55, #cc9900)',
    'False Context': 'linear-gradient(90deg, #ffb366, #cc6600)',
    'Imposter Content': 'linear-gradient(90deg, #ff9980, #cc3300)',
    'Manipulated Content': 'linear-gradient(90deg, #ff8080, #cc0000)',
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

// Urutan tampilan tetap konsisten (bukan urutan acak dari Object.keys),
// mengikuti spektrum low->high harm First Draft, "Fakta" ditaruh paling awal.
const kategoriUrutan = [
  'Fakta',
  'Satire atau Parodi',
  'False Connection',
  'Misleading Content',
  'False Context',
  'Imposter Content',
  'Manipulated Content',
  'Fabricated Content'
]
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
        <span class="dot">
          <Feather :size="20" style="vertical-align: middle; margin-bottom: 2px;" />
        </span> Kesimpulan Klasifikasi
      </div>
      <p class="conclusion-text">{{ conclusion }}</p>
    </div>

    <!-- section confidence -->
    <div class="section">
      <div class="section-title">
        <Lightbulb :size="20" style="vertical-align: middle; margin-bottom: 2px;" /> Tingkat Keyakinan</div>
      <div class="confidence-bar-track">
        <div class="confidence-bar-fill" :style="{ width: confidence + '%', background: confidenceBarGradient }"></div>
      </div>
      <span class="confidence-label">{{ confidence.toFixed(1) }}%</span>
    </div>

    <!-- section relevansi gambar (cuma muncul kalau ada cek gambar) -->
    <div class="section" v-if="image_relevance_score !== null">
      <div class="section-title">
        <Image :size="20" style="vertical-align: middle; margin-bottom: 2px;" /> Relevansi Gambar</div>
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
      <div class="section-title">
        <ChartColumnIncreasing :size="20" style="vertical-align: middle; margin-bottom: 2px;" /> Statistik Pencarian</div>
      <div class="stats-grid">
        <div class="stat-item">
          <span class="stat-label">Jumlah Artikel</span>
          <span class="stat-value">{{ jumlah_artikel }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Top 5 Rata Rata Score</span>
          <span class="stat-value">{{ (score_tavily * 100).toFixed(1) }}%</span>
        </div>
      </div>
    </div>

     <!-- section stance breakdown -- sekarang 4 kategori (majority vote), bukan 3 sikap -->
    <div class="section">
      <div class="section-title">
        <GalleryVerticalEnd :size="20" style="vertical-align: middle; margin-bottom: 2px;" /> Rincian Vote Per Kategori</div>
      <div class="stance-grid-4">
        <div
          v-for="kategori in kategoriUrutan"
          :key="kategori"
          class="stance-item-4"
          :style="{ background: stanceCardStyleMap[kategori].bg }"
        >
          <span class="stance-label">{{ kategori }}</span>
          <span class="stance-value">{{ stance_breakdown[kategori] || 0 }}</span>
        </div>
      </div>
    </div>

   <!-- section alasan per artikel -->
    <div class="section" v-if="alasan_per_artikel.length > 0">
      <div class="section-title">
        <FileText :size="20" style="vertical-align: middle; margin-bottom: 2px;" /> Analisis Per Artikel</div>
      <div class="stance-detail-list">
        <div
          v-for="(item, index) in alasan_per_artikel"
          :key="index"
          class="stance-detail-item"
          :style="{
            background: stanceCardStyleMap[item.stance]?.bg || '#F5F5F5',
            borderLeftColor: stanceCardStyleMap[item.stance]?.border || '#a0a0a0'
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

/* Grid 4 kategori (menggantikan stance-grid 3 kolom lama) */
.stance-grid-4 {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

@media (max-width: 480px) {
  .stance-grid-4 {
    grid-template-columns: 1fr;
  }
}

.stance-item-4 {
  border-radius: 16px;
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  text-align: center;
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
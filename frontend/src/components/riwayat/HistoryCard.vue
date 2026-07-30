<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import defaultThumbnail from '../../assets/default-thumbnail-home.jpeg'

const props = defineProps({
  id: { type: [String, Number], required: true },
  image: { type: String, default: '' },
  category: { type: String, required: true },  // 'Fakta' | 'False Content' | 'Misleading Content' | 'Fabricated Content'
  date: { type: String, required: true },
  type: { type: String, required: true },        // 'Teks' | 'Gambar' | 'Video'
  title: { type: String, required: true },
  verified: { type: Boolean, default: true }
})

// Mapping kategori -> warna badge & icon, senada dengan AnalysisResult.vue
// biar konsisten di seluruh aplikasi (badge yang sama warnanya di halaman manapun)
const categoryStyleMap = {
  'Fakta': { bg: '#20d48a', color: 'white', icon: '✓' },
  'False Content': { bg: '#ff4d4d', color: 'white', icon: '⚠' },
  'Misleading Content': { bg: '#ffcc00', color: 'white', icon: '⏱' },
  'Fabricated Content': { bg: '#808080', color: 'white', icon: '✂' }
}

// Icon kecil di samping tanggal, sesuai jenis konten yang dianalisis
const typeIconMap = {
  Teks: '📝',
  Gambar: '🖼',
  Video: '🎬'
}

const displayImage = computed(() => props.image || defaultThumbnail)
</script>

<template>
  <div class="history-card">
    <div class="thumbnail">
      <img :src="displayImage" :alt="title" class="thumbnail-img" />
      
      <span
        class="category-badge"
        :style="{
          background: categoryStyleMap[category]?.bg,
          color: categoryStyleMap[category]?.color
        }"
      >
        {{ categoryStyleMap[category]?.icon }} {{ category }}
      </span>
    </div>

    <div class="card-body">
      <div class="meta-row">
        <span class="meta-item">📅 {{ date }}</span>
        <span class="meta-item">{{ typeIconMap[type] }} {{ type }}</span>
      </div>

      <h3 class="card-title">{{ title }}</h3>

      <div class="card-footer">
        <span class="status-dot" :class="{ 'status-dot--verified': verified }"></span>
        <RouterLink :to="`/riwayat/${id}`" class="detail-link">Lihat Detail →</RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.history-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-card);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.history-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.thumbnail {
  position: relative;
  aspect-ratio: 16 / 10;
  background: var(--color-navy-light);
}

.thumbnail-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.thumbnail-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: var(--color-text-muted);
  opacity: 0.5;
}

.category-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 999px;
}

.card-body {
  padding: 16px;
}

.meta-row {
  display: flex;
  gap: 12px;
  font-size: 11px;
  color: var(--color-text-muted);
  margin-bottom: 8px;
}

.card-title {
  font-size: 14px;
  font-weight: 700;
  color: var(--color-navy);
  margin: 0 0 14px;
  line-height: 1.4;
  /* Batasi judul jadi maksimal 2 baris, sisanya "..." -- sesuai desain */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-border);
}

.status-dot--verified {
  background: var(--color-green);
}

.detail-link {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-green);
}

.detail-link:hover {
  text-decoration: underline;
}
</style>
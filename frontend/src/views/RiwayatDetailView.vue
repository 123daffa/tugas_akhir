<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import AnalysisResult from '../components/detection/AnalysisResult.vue'
import ConfidenceScore from '../components/detection/ConfidenceScore.vue'
import api from '../services/api'
import { MoveLeft } from 'lucide-vue-next';

const route = useRoute()

const item = ref(null)
const isLoading = ref(true)
const notFound = ref(false)

async function loadDetail() {
  isLoading.value = true
  notFound.value = false
  try {
    const { data } = await api.get(`/api/history/${route.params.id}`)
    item.value = data
  } catch (err) {
    notFound.value = true
  } finally {
    isLoading.value = false
  }
}

onMounted(loadDetail)

const typeIconMap = {
  Teks: '📝',
  Gambar: '🖼',
  Video: '🎬'
}
</script>

<template>
  <div class="detail-page">
    <RouterLink to="/riwayat" class="back-link"><MoveLeft :size="16" style="vertical-align: middle; margin-bottom: 2px; margin-right: 3px;" />Kembali ke Riwayat</RouterLink>

    <div v-if="isLoading" class="not-found">
      <p>Memuat riwayat...</p>
    </div>

    <div v-if="item">
      <div class="detail-meta">
        <span class="meta-item">📅 {{ item.date }}</span>
        <span class="meta-item">{{ typeIconMap[item.type] }} {{ item.type }}</span>
      </div>

      <h1 class="detail-title">{{ item.title }}</h1>

      <div v-if="item.image" class="detail-thumbnail">
        <img :src="item.image" :alt="item.title" />
      </div>

      <div class="content-grid">
        <div class="left-col">
          <AnalysisResult
            :label="item.category"
            :conclusion="item.conclusion"
            :articles="item.articles || []"
            :jumlah_artikel="item.jumlah_artikel ?? (item.articles || []).length"
            :kredibilitas_score="item.accuracy / 100"
            :confidence="item.confidence || 0"
            :stance_breakdown="item.stance_breakdown"
            :alasan_per_artikel="item.alasan_per_artikel || []"
            :image_relevance_score="item.image_relevance_score ?? null"
            :penjelasan_gambar="item.penjelasan_gambar || ''"
            :artikel_gambar_paling_relevan="item.artikel_gambar_paling_relevan"
            :detail_gambar_per_artikel="item.detail_gambar_per_artikel || []"
          />
        </div>
        <div class="right-col" v-if="item.mode === 'video' && item.video_relevance_score != null">
          <ConfidenceScore
            :video_relevance_score="item.video_relevance_score"
            :penjelasan_video="item.penjelasan_video || ''"
            :artikel_video_paling_relevan="item.artikel_video_paling_relevan"
            :jumlah_frame="item.jumlah_frame"
            :detail_video_per_artikel="item.detail_video_per_artikel || []"
          />
        </div>
      </div>
    </div>

    <div v-else class="not-found">
      <p>Riwayat dengan ID ini tidak ditemukan.</p>
      <RouterLink to="/riwayat" class="btn-back"> <MoveLeft :size="16" style="vertical-align: middle; margin-bottom: 2px; margin-right: 3px;" />Kembali ke Riwayat</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.detail-page {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
}

.back-link {
  display: inline-block;
  font-size: 15px;
  font-weight: 600;
  color: var(--color-green);
  margin-bottom: 20px;
  margin-top: 40px;
}

.back-link:hover {
  text-decoration: underline;
  color: #0f6b52;
}

.detail-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: var(--color-text-muted);
  margin-bottom: 8px;
}

.detail-title {
  font-size: 22px;
  font-weight: 800;
  color: var(--color-navy);
  margin: 0 0 20px;
  line-height: 1.4;
}

.detail-thumbnail {
  aspect-ratio: 16 / 9;
  border-radius: var(--radius-lg);
  overflow: hidden;
  margin-bottom: 20px;
  background: var(--color-navy-light);
}

.detail-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  align-items: start;
}

@media (max-width: 720px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

.not-found {
  text-align: center;
  padding: 80px 20px;
  color: var(--color-text-muted);
}

.not-found p {
  margin-bottom: 16px;
}

.btn-back {
  display: inline-block;
  background: var(--color-green);
  color: #fff;
  padding: 10px 24px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 600;
}
</style>
<script setup>
import { ref, watch, onMounted } from 'vue';

const props = defineProps({
  video_relevance_score: { type: Number, required: true },
  penjelasan_video: { type: String, default: '' },
  artikel_video_paling_relevan: { type: String, default: null },
  jumlah_frame: { type: Number, default: null },
  detail_video_per_artikel: {
    type: Array,
    default: () => []
  }
})

const displayedScore = ref(0)

function animateCountUp(target) {
  const duration = 1200
  const startTime = performance.now()
  const startValue = displayedScore.value

  function tick(now) {
    const elapsed = now - startTime
    const progress = Math.min(elapsed / duration, 1)
    const eased = 1 - Math.pow(1 - progress, 3)

    displayedScore.value = Math.round(startValue + (target - startValue) * eased)

    if (progress < 1) {
      requestAnimationFrame(tick)
    } else {
      displayedScore.value = target
    }
  }

  requestAnimationFrame(tick)
}

onMounted(() => {
  animateCountUp(Math.round(props.video_relevance_score))
})

watch(() => props.video_relevance_score, (newValue) => {
  animateCountUp(Math.round(newValue))
})
</script>

<template>
  <div class="confidence-card">
    <h3 class="title">🎬 Relevansi Video</h3>
    <div class="score">
      <div class="score-circle">
        <span class="score-number">{{ displayedScore }}%</span>
        <span class="score-label">Kemiripan</span>
      </div>
    </div>

    <p v-if="penjelasan_video" class="conclusion-text">{{ penjelasan_video }}</p>

    <div v-if="artikel_video_paling_relevan" class="translated-caption">
      <p class="translated-label">Dibandingkan dengan gambar dari</p>
      <p class="translated-text">{{ artikel_video_paling_relevan }}</p>
    </div>

    <p v-if="jumlah_frame !== null" class="frame-note">
      Dianalisis dari {{ jumlah_frame }} frame video.
    </p>

    <!-- breakdown per artikel, dipindah ke sini dari AnalysisResult.vue -->
    <div v-if="detail_video_per_artikel.length > 0" class="detail-section">
      <p class="detail-title">Analisis Video Per Artikel</p>
      <div class="stance-detail-list">
        <div
          v-for="(item, index) in detail_video_per_artikel"
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
  </div>
</template>

<style scoped>
.confidence-card {
  width: 100%;
  background: white;
  border-radius: 40px;
  padding: 20px;
  box-shadow: var(--shadow-card);
  text-align: center;
}

.title {
  margin: 0 0 16px;
  font-size: 20px;
  font-weight: 700;
  text-align: center;
}

.score {
  display: flex;
  justify-content: center;
  padding: 12px 0 24px;
}

.score-circle {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: rgba(253, 251, 251, 0.9);
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
}

.score-number {
  font-size: 50px;
  font-weight: 800;
  color: #006C49;
  line-height: 1;
}

.score-label {
  font-size: 15px;
  color: black;
  margin-top: 4px;
}

.conclusion-text {
  font-size: 14px;
  line-height: 1.5;
  color: var(--color-text-muted);
  text-align: left;
  margin: 0 0 16px;
}

.translated-caption {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid var(--color-border);
  text-align: left;
}

.translated-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-muted);
  margin: 0 0 6px;
  text-transform: uppercase;
  letter-spacing: 0.4px;
}

.translated-text {
  font-size: 14px;
  color: black;
  font-style: italic;
  margin: 0;
  line-height: 1.5;
}

.frame-note {
  font-size: 12px;
  color: var(--color-text-muted);
  opacity: 0.7;
  margin-top: 12px;
  text-align: left;
}

/* Breakdown per artikel -- style disalin dari AnalysisResult.vue supaya konsisten */
.detail-section {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid var(--color-border);
  text-align: left;
}

.detail-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-navy);
  margin: 0 0 10px;
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
  min-width: 0;
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
</style>
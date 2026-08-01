<script setup>
import { ref } from 'vue'
import DetectionTabs from '../components/detection/DetectionTabs.vue'
import TextDetectionForm from '../components/detection/TextDetectionForm.vue'
import ImageDetectionForm from '../components/detection/ImageDetectionForm.vue'
import VideoDetectionForm from '../components/detection/VideoDetectionForm.vue'
import AnalysisResult from '../components/detection/AnalysisResult.vue'
import ConfidenceScore from '../components/detection/ConfidenceScore.vue'
import { checkText, checkImage, checkVideo } from '../services/hoaxDetectionService'

const activeTab = ref('teks')
const result = ref(null)
const errorMessage = ref('')
const isLoading = ref(false)

function mapResult(data, type) {
  const metrics = [
    {
      label: 'Kredibilitas Sumber',
      value: Math.round(data.kredibilitas_score * 100),
      color: data.kredibilitas_score >= 0.7 ? 'green' : data.kredibilitas_score >= 0.4 ? 'orange' : 'red'
    }
  ]

  return {
    label: data.klasifikasi,
    conclusion: data.penjelasan || data.penjelasan_teks || '',
    articles: data.articles || [],
    jumlah_artikel: data.jumlah_artikel || 0,
    kredibilitas_score: data.kredibilitas_score || 0,
    metrics,
    confidence: data.confidence || 0,
    stance_breakdown: data.stance_breakdown || {
      'Fakta': 0, 'False Content': 0, 'Misleading Content': 0, 'Fabricated Content': 0
    },
    alasan_per_artikel: data.alasan_per_artikel || [],
    // field gambar
    image_relevance_score: data.image_relevance_score ?? null,
    penjelasan_gambar: data.penjelasan_gambar || '',
    artikel_gambar_paling_relevan: data.artikel_gambar_paling_relevan || null,
    detail_gambar_per_artikel: data.detail_gambar_per_artikel || [],
    // field video
    jumlah_frame: data.jumlah_frame ?? null,
    video_relevance_score: data.video_relevance_score ?? null,
    penjelasan_video: data.penjelasan_video || '',
    artikel_video_paling_relevan: data.artikel_video_paling_relevan || null,
    detail_video_per_artikel: data.detail_video_per_artikel || [],
    // Simpan raw data kalau butuh debug
    raw: data
  }
}

async function handleTextSubmit(text) {
  errorMessage.value = ''
  isLoading.value = true
  result.value = null

  try {
    const response = await checkText(text)
    if (response.success) {
      result.value = mapResult(response.data, 'text')
    } else {
      errorMessage.value = response.error
    }
  } catch (err) {
    errorMessage.value = 'Terjadi kesalahan, coba lagi'
    console.error(err)
  } finally {
    isLoading.value = false
  }
}

async function handleImageSubmit({ text, image }) {
  errorMessage.value = ''
  isLoading.value = true
  result.value = null

  try {
    const response = await checkImage(image, text)
    if (response.success) {
      result.value = mapResult(response.data, 'image')
    } else {
      errorMessage.value = response.error
    }
  } catch (err) {
    errorMessage.value = 'Terjadi kesalahan, coba lagi'
    console.error(err)
  } finally {
    isLoading.value = false
  }
}

async function handleVideoSubmit({ text, video }) {
  errorMessage.value = ''
  isLoading.value = true
  result.value = null

  try {
    const response = await checkVideo(video, text)
    if (response.success) {
      result.value = mapResult(response.data, 'video')
    } else {
      errorMessage.value = response.error
    }
  } catch (err) {
    errorMessage.value = 'Terjadi kesalahan, coba lagi'
    console.error(err)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="detection-page">
    <DetectionTabs v-model="activeTab" />

    <div class="content-grid">
      <div class="left-col">
        <TextDetectionForm
          v-if="activeTab === 'teks'"
          :is-loading="isLoading"
          @submit="handleTextSubmit"
        />
        <ImageDetectionForm
          v-else-if="activeTab === 'gambar'"
          :is-loading="isLoading"
          @submit="handleImageSubmit"
        />
        <VideoDetectionForm
          v-else
          :is-loading="isLoading"
          @submit="handleVideoSubmit"
        />

        <AnalysisResult
          v-if="result"
          :label="result.label"
          :penjelasan="result.conclusion"
          :articles="result.articles"
          :jumlah_artikel="result.jumlah_artikel"
          :kredibilitas_score="result.kredibilitas_score"
          :confidence="result.confidence"
          :stance_breakdown="result.stance_breakdown"
          :alasan_per_artikel="result.alasan_per_artikel"
          :image_relevance_score="result.image_relevance_score"
          :penjelasan_gambar="result.penjelasan_gambar"
          :artikel_gambar_paling_relevan="result.artikel_gambar_paling_relevan"
          :detail_gambar_per_artikel="result.detail_gambar_per_artikel"
        />
      </div>

      <!-- Kolom kanan: khusus hasil video -->
      <div class="right-col" v-if="result && result.video_relevance_score !== null">
        <ConfidenceScore
          :video_relevance_score="result.video_relevance_score"
          :penjelasan_video="result.penjelasan_video"
          :artikel_video_paling_relevan="result.artikel_video_paling_relevan"
          :jumlah_frame="result.jumlah_frame"
          :detail_video_per_artikel="result.detail_video_per_artikel" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.detection-page {
  width: 100%;
}

.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  align-items: start;
}

@media (max-width: 860px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}
</style>
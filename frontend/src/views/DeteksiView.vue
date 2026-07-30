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

// Fungsi untuk mapping response backend ke format yang dipakai komponen
function mapResult(data, type) {
  const labelMap = {
  'FAKTA': 'Fakta',
  'MISLEADING': 'Misleading Content',
  'FABRICATED': 'Fabricated Content',
  'FALSE': 'False Content'
}

  const metrics = [
    {
      label: 'Kredibilitas Sumber',
      value: Math.round(data.kredibilitas_score * 100),
      color: data.kredibilitas_score >= 0.7 ? 'green' : data.kredibilitas_score >= 0.4 ? 'orange' : 'red'
    }
  ]

  return {
    label: labelMap[data.klasifikasi] || data.klasifikasi,
    conclusion: data.penjelasan,
    articles: data.articles || [],
    jumlah_artikel: data.jumlah_artikel || 0,        
    kredibilitas_score: data.kredibilitas_score || 0,      
    metrics,
    confidence: data.confidence || 0,                          // ← tambah
    stance_breakdown: data.stance_breakdown || {               // ← tambah
      MENDUKUNG: 0, MEMBANTAH: 0, TIDAK_RELEVAN: 0
    },
    metrics,
    similarity_score: data.similarity_score,
    caption_translated: data.caption_translated,
    alasan_per_artikel: data.alasan_per_artikel || [], 
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
      <!-- Kolom kiri: form input + hasil analisis -->
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
          :conclusion="result.conclusion"
          :articles="result.articles"
          :jumlah_artikel="result.jumlah_artikel"
          :kredibilitas_score="result.kredibilitas_score"
          :confidence="result.confidence"
          :stance_breakdown="result.stance_breakdown"
          :alasan_per_artikel="result.alasan_per_artikel"
          :image_relevance_score="hasil.image_relevance_score"
          :penjelasan_gambar="hasil.penjelasan_gambar"
          :artikel_gambar_paling_relevan="hasil.artikel_gambar_paling_relevan"
          :detail_gambar_per_artikel="hasil.detail_gambar_per_artikel"
        />
      </div>

      <!-- Kolom kanan: kartu tingkat keyakinan AI, hanya tampil kalau sudah ada hasil -->
        <div class="right-col" 
        v-if="result && result.raw.similarity_score !== undefined">
          <ConfidenceScore 
          :similarity_score="result.raw.similarity_score"
          :caption_translated="result.raw.caption_translated || ''" />
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
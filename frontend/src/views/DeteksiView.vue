<script setup>
import { ref } from 'vue'
import DetectionTabs from '../components/detection/DetectionTabs.vue'
import TextDetectionForm from '../components/detection/TextDetectionForm.vue'
import ImageDetectionForm from '../components/detection/ImageDetectionForm.vue'
import VideoDetectionForm from '../components/detection/VideoDetectionForm.vue'
import AnalysisResult from '../components/detection/AnalysisResult.vue'
import ConfidenceScore from '../components/detection/ConfidenceScore.vue'

// ← GANTI import yang di-comment dengan ini
import { checkText, checkImage, checkVideo } from '../services/hoaxDetectionService'

const activeTab = ref('teks')
const result = ref(null)
const errorMessage = ref('')
const isLoading = ref(false)

// Fungsi untuk mapping response backend ke format yang dipakai komponen
function mapResult(data, type) {
  // Backend mengembalikan klasifikasi: FAKTA/MISLEADING/FABRICATED/FALSE/TIDAK PASTI
  // Frontend pakai: label, accuracy, conclusion, source, metrics
  
  const labelMap = {
  'FAKTA': 'Fakta',
  'MISLEADING': 'Misleading Content',
  'FABRICATED': 'Fabricated Content',
  'FALSE': 'False Content'
}

  // // Konversi kredibilitas_score (0.0-1.0) ke persentase (0-100)
  // const accuracy = Math.round(data.kredibilitas_score * 100)

  // Metrics untuk ConfidenceScore component
  const metrics = [
    {
      label: 'Kredibilitas Sumber',
      value: Math.round(data.kredibilitas_score * 100),
      color: data.kredibilitas_score >= 0.7 ? 'green' : data.kredibilitas_score >= 0.4 ? 'orange' : 'red'
    }
  ]

  // Tambah similarity score kalau ada (image/video pipeline)
  if (data.similarity_score !== undefined) {
    metrics.push({
      label: 'Konsistensi Visual-Teks',
      value: Math.round(data.similarity_score * 100),
      color: data.similarity_score >= 0.7 ? 'green' : data.similarity_score >= 0.5 ? 'orange' : 'red'
    })
  }

  return {
    label: labelMap[data.klasifikasi] || data.klasifikasi,
    // accuracy: data.rata_rata_score,
    conclusion: data.penjelasan,
    articles: data.articles || [],
    jumlah_artikel: data.jumlah_artikel || 0,        
    kredibilitas_score: data.kredibilitas_score || 0,      
    metrics,
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
        />
      </div>

      <!-- Kolom kanan: kartu tingkat keyakinan AI, hanya tampil kalau sudah ada hasil -->
        <!-- <div class="right-col" v-if="result">
          <ConfidenceScore :accuracy="result.accuracy" :metrics="result.metrics" />
        </div> -->
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
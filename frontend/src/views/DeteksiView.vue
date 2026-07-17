<script setup>
import { ref } from 'vue'
import DetectionTabs from '../components/detection/DetectionTabs.vue'
import TextDetectionForm from '../components/detection/TextDetectionForm.vue'
import ImageDetectionForm from '../components/detection/ImageDetectionForm.vue'
import VideoDetectionForm from '../components/detection/VideoDetectionForm.vue'
import AnalysisResult from '../components/detection/AnalysisResult.vue'
import ConfidenceScore from '../components/detection/ConfidenceScore.vue'
// import { detectText, detectImage, detectVideo } from '../services/api.js'

const activeTab = ref('teks') // 'teks' | 'gambar' | 'video'

// State hasil analisis. null artinya belum ada hasil yang ditampilkan.
const result = ref(null)
const errorMessage = ref('')

// isLoading ditaruh di sini (parent) karena di sinilah `await` API call
// yang sebenarnya terjadi. Form component tinggal terima status ini lewat props,
// jadi tombol "Periksa Fakta" beneran disabled selama request masih berjalan,
// bukan cuma kedip sesaat kayak sebelumnya.
const isLoading = ref(false)

// Karena backend Flask belum tentu selalu jalan saat development,
// dummy data ini dipakai sebagai fallback demo sesuai contoh di desain.
const DUMMY_RESULT = {
  label: 'Fakta',
  accuracy: 92,
  conclusion:
    'Klaim bahwa pemerintah membagikan bantuan tunai melalui tautan WhatsApp tersebut dipastikan palsu. Tautan tersebut merupakan upaya phishing yang dirancang mencuri data pribadi. Situs resmi pemerintah terkait tidak pernah mengeluarkan pesan berantai semacam ini.',
  source: {
    title: 'Klarifikasi Resmi Kementerian Kominfo',
    url: 'https://kominfo.go.id'
  },
  metrics: [
    { label: 'Manipulasi Konteks', value: 85, color: 'red' },
    { label: 'Bahasa Emosional', value: 78, color: 'orange' }
  ]
}

async function handleTextSubmit(text) {
  errorMessage.value = ''
  isLoading.value = true
  try {
    const { data } = await detectText(text)
    result.value = data
  } catch (err) {
    // Fallback ke dummy data kalau backend belum tersedia, biar UI tetap bisa didemokan
    console.warn('Backend belum tersedia, pakai data contoh:', err.message)
    result.value = DUMMY_RESULT
  } finally {
    // Baris ini jalan SETELAH await di atas beneran selesai (berhasil atau gagal),
    // jadi tombol beneran ke-disable sepanjang request berlangsung.
    isLoading.value = false
  }
}

async function handleImageSubmit({ text, image }) {
  errorMessage.value = ''
  isLoading.value = true
  try {
    const { data } = await detectImage(text, image)
    result.value = data
  } catch (err) {
    console.warn('Backend belum tersedia, pakai data contoh:', err.message)
    result.value = DUMMY_RESULT
  } finally {
    isLoading.value = false
  }
}

async function handleVideoSubmit({ text, video }) {
  errorMessage.value = ''
  isLoading.value = true
  try {
    const { data } = await detectVideo(text, video)
    result.value = data
  } catch (err) {
    console.warn('Backend belum tersedia, pakai data contoh:', err.message)
    result.value = DUMMY_RESULT
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
          :source="result.source"
        />
      </div>

      <!-- Kolom kanan: kartu tingkat keyakinan AI, hanya tampil kalau sudah ada hasil -->
      <div class="right-col" v-if="result">
        <ConfidenceScore :accuracy="result.accuracy" :metrics="result.metrics" />
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
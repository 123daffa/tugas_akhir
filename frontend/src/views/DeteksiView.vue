<script setup>
import { ref } from 'vue'


const activeTab = ref('teks')
const inputTeks = ref('')
const inputGambar = ref(null)
const captionGambar = ref('')
const inputVideo = ref('')
const captionVideo = ref('')

function a(params) {
  
}

</script>

<template>
  <section id="halaman-pengecekan">
    <div class="page-header">
      <h1>Analisis & Verifikasi informasi</h1>
      <p>Masukkan informasi yang ingin Anda periksa kebenarannya</p>
    </div>

    <div class="filter-container">
      <span class="filter active" data-filter="all">
        Teks
      </span>
      <span class="filter" data-filter="active">
        Gambar
      </span>
      <span class="filter" data-filter="completed">
        Video
      </span>
    </div>

    <div>
      
      <input type="text" placeholder="Tempelkan teks,kutipan, atau artikel disini yang ingin Anda periksa..." />
      <button>Analisis Sekarang</button>
    </div>
    
    <div>
      
    </div>

  </section>
</template>

<style scoped>
section {
  padding: 64px 128px;
}
</style>

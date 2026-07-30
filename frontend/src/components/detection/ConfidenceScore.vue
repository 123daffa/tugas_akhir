<script setup>
import {ref, watch, onMounted} from 'vue';

 const props = defineProps({
  label: { type: String, default: '' },
  similarity_score: { type: Number, required: true },        // contoh: 92
  caption_translated: {type: String, required: true}
})

// Angka yang BENERAN ditampilkan di layar -- mulai dari 0, nanti di-animasikan
// naik pelan-pelan sampai menyentuh nilai `accuracy` yang asli.
const displayedAccuracy = ref(0)
 
function animateCountUp(target) {
  const duration = 1200 // total durasi animasi dalam milidetik (1.2 detik)
  const startTime = performance.now()
  const startValue = displayedAccuracy.value
 
  function tick(now) {
    const elapsed = now - startTime
    const progress = Math.min(elapsed / duration, 1) // 0 -> 1, gak boleh lebih dari 1
 
    // Easing "ease-out": animasi cepat di awal, melambat di akhir -- kerasa lebih natural
    // daripada kecepatan konstan (linear). Rumus umum: 1 - (1-progress)^3
    const eased = 1 - Math.pow(1 - progress, 3)
 
    displayedAccuracy.value = Math.round(startValue + (target - startValue) * eased)
 
    if (progress < 1) {
      requestAnimationFrame(tick) // lanjut ke frame berikutnya kalau belum selesai
    } else {
      displayedAccuracy.value = target // pastikan berhenti PERSIS di angka final, gak kelebihan/kekurangan
    }
  }
 
  requestAnimationFrame(tick)
}
 
// Animasi jalan pas komponen pertama kali muncul di layar...
onMounted(() => {
  animateCountUp(Math.round(props.similarity_score * 100))
})
 
// ...DAN setiap kali prop accuracy berubah (misal user analisis klaim baru,
// hasil baru masuk, animasinya jalan ulang dari angka lama ke angka baru)
watch(() => props.similarity_score, (newValue) => {
  animateCountUp(Math.round(newValue * 100))
})
</script>

<template>
  <div class="confidence-card">
    <h3 class="title">Similarity Score</h3>
        <!-- Wrapper ini yang nge-center-in lingkaran secara horizontal di dalam card -->
    <div class="score">
      <div class="score-circle">
        <span class="score-number">{{ displayedAccuracy }}%</span>
        <span class="score-label">Similarity</span>
      </div>
    </div>

     <div v-if="caption_translated" class="translated-caption">
      <p class="translated-label">Caption (diterjemahkan)</p>
      <p class="translated-text">"{{ caption_translated }}"</p>
    </div>

  </div>
</template>

<style scoped>
.confidence-card {
  width: 90%;
  padding-left: 50px;
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
  justify-content: center;  /* center-in lingkaran secara horizontal di card */
  padding: 12px 0 24px;
}
 
.score-circle {
  display: flex;
  flex-direction: column;
  align-items: center;      /* center horizontal (cross-axis, karena column) */
  justify-content: center;  /* center vertikal (main-axis) -- ganti padding-top manual */
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: rgba(253, 251, 251, 0.9); /* biru pucat, alpha 0.9 = ketajaman 90% */
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

.metric-list {
  list-style: none;
  margin: 0;
  padding: 16px 0 0;
  /* border-top: 1px solid var(--color-border); */
  text-align: left;
}

.metric-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 13px;
  padding: 6px 0;
}

.metric-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--color-text-muted);
}

.metric-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}

.metric-dot--red {
  background: var(--color-red);
}

.metric-dot--orange {
  background: #f59e0b;
}

.metric-value {
  font-weight: 600;
}
</style>
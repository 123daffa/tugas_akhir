<script setup>
defineProps({
  accuracy: { type: Number, required: true },        // contoh: 92
  metrics: {
    type: Array,
    default: () => [
      // { label: 'Manipulasi Konteks', value: 85, color: 'red' },
      // { label: 'Bahasa Emosional', value: 78, color: 'orange' }
    ]
  }
})
</script>

<template>
  <div class="confidence-card">
    <h3 class="title">Similarity Score</h3>

        <!-- Wrapper ini yang nge-center-in lingkaran secara horizontal di dalam card -->
    <div class="score">
      <div class="score-circle">
        <span class="score-number">{{ accuracy }}%</span>
        <span class="score-label">Akurasi</span>
      </div>
    </div>

    <ul class="metric-list">
      <li v-for="metric in metrics" :key="metric.label" class="metric-item">
        <span class="metric-label">
          <span class="metric-dot" :class="`metric-dot--${metric.color}`"></span>
          {{ metric.label }}
        </span>
        <span class="metric-value">{{ metric.value }}%</span>
      </li>
    </ul>
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
  font-size: 14px;
  font-weight: 700;
  text-align: left;
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
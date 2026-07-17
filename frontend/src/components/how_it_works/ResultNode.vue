<script setup>
defineProps({
  label: { type: String, required: true },
  description: { type: String, required: true },
  tone: { type: String, required: true } // 'green' | 'orange' | 'red' | 'pink'
})
</script>

<template>
  <div class="result-node" :class="`result-node--${tone}`">
    <div class="result-label">{{ label }}</div>
    <div class="result-desc">{{ description }}</div>
  </div>
</template>

<style scoped>
.result-node {
  border-radius: var(--radius-md);
  padding: 14px 16px;
  border: 1.5px solid;
  min-width: 220px;
}

.result-label {
  font-weight: 700;
  font-size: 13px;
  margin-bottom: 4px;
}

.result-desc {
  font-size: 11px;
  line-height: 1.5;
  opacity: 0.85;
}

.result-node--green {
  background: var(--color-green-bg);
  border-color: var(--color-green);
  color: var(--color-green);
}

.result-node--orange {
  background: #fff7e6;
  border-color: #f59e0b;
  color: #b45309;
}

.result-node--red {
  background: var(--color-red-bg);
  border-color: var(--color-red);
  color: var(--color-red);
}

.result-node--pink {
  background: #fdf2f8;
  border-color: #db2777;
  color: #db2777;
}
</style>
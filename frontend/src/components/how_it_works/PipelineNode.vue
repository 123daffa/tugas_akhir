<script setup>
// Satu kotak tahap dalam pipeline. `variant` nentuin warna aksen
// biar bisa dibedain: proses biasa (default), output/hasil (output), atau final (final)
defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  variant: { type: String, default: 'default' } // 'default' | 'output' | 'final'
})
</script>

<template>
  <div class="node" :class="`node--${variant}`">
    <div class="node-title">{{ title }}</div>
    <div v-if="subtitle" class="node-subtitle">{{ subtitle }}</div>
  </div>
</template>

<style scoped>
.node {
  background: var(--color-surface);
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 14px 16px;
  min-width: 150px;
  text-align: center;
  font-size: 13px;
  font-weight: 700;
  color: var(--color-navy);
  box-shadow: var(--shadow-card);
}

.node-subtitle {
  font-size: 11px;
  font-weight: 400;
  color: var(--color-text-muted);
  margin-top: 4px;
  line-height: 1.4;
}

/* Output sampingan seperti "Similarity Score" -- aksen biru */
.node--output {
  border-color: var(--color-blue);
  background: var(--color-blue-bg);
  color: var(--color-blue);
}

/* Node terakhir sebelum hasil klasifikasi -- aksen hijau */
.node--final {
  border-color: var(--color-green);
  background: var(--color-green-bg);
  color: var(--color-green);
}
</style>
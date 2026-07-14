<script setup>
// Kartu "Hasil Analisis": menampilkan label klasifikasi, kesimpulan dari LLM,
// dan sumber rujukan yang ditemukan oleh Tavily search
defineProps({
  label: { type: String, default: 'Disinformasi' },    // fakta | disinformasi | misleading | fabricated
  conclusion: { type: String, required: true },
  source: {
    type: Object,
    default: () => ({ title: '', url: '#' })
  }
})

// Mapping label -> warna badge, biar gampang extend kalau ada kategori baru
const labelStyleMap = {
  Fakta: { bg: 'var(--color-green-bg)', color: 'var(--color-green)', icon: '✓' },
  Disinformasi: { bg: 'var(--color-red-bg)', color: 'var(--color-red)', icon: '⚠' },
  Misleading: { bg: '#fff7e6', color: '#d97706', icon: '⚠' },
  Fabrikasi: { bg: 'var(--color-red-bg)', color: 'var(--color-red)', icon: '⚠' }
}
</script>

<template>
  <div class="result-card">
    <div class="result-header">
      <h3>Hasil Analisis</h3>
      <span
        class="badge"
        :style="{
          background: labelStyleMap[label]?.bg || 'var(--color-red-bg)',
          color: labelStyleMap[label]?.color || 'var(--color-red)'
        }"
      >
        {{ labelStyleMap[label]?.icon || '⚠' }} {{ label }}
      </span>
    </div>

    <div class="section">
      <div class="section-title">
        <span class="dot">✨</span> Kesimpulan Groq AI
      </div>
      <p class="conclusion-text">{{ conclusion }}</p>
    </div>

    <div class="section">
      <div class="section-title">Sumber Rujukan Terpercaya</div>
      <a :href="source.url" target="_blank" class="source-chip">
        <span class="source-icon">🔗</span>
        {{ source.title || 'Belum ada sumber ditemukan' }}
      </a>
    </div>
  </div>
</template>

<style scoped>
.result-card {
  background: white;
  border-radius: 40px;
  padding: 20px;
  box-shadow: var(--shadow-card);
  margin-left: 110px;
}

.result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.result-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
}

.badge {
  font-size: 12px;
  font-weight: 600;
  padding: 5px 12px;
  border-radius: 999px;
  white-space: nowrap;
}

.section {
  margin-bottom: 16px;
}

.section:last-child {
  margin-bottom: 0;
}

.section-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-navy);
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 8px;
}

.conclusion-text {
  font-size: 13px;
  line-height: 1.6;
  color: var(--color-text-muted);
  margin: 0;
}

.source-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--color-blue-bg);
  color: var(--color-blue);
  font-size: 12px;
  font-weight: 600;
  padding: 8px 14px;
  border-radius: var(--radius-md);
}

.source-icon {
  font-size: 12px;
}
</style>
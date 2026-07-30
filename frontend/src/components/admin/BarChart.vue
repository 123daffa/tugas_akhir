<script setup>
import { computed } from 'vue'

const props = defineProps({
  data: {
    // [{ label: 'Fakta', value: 12, color: '#20d48a' }, ...]
    type: Array,
    required: true
  },
  height: { type: Number, default: 220 }
})

const maxValue = computed(() => {
  const max = Math.max(...props.data.map((d) => d.value), 0)
  return max === 0 ? 1 : max
})
</script>

<template>
  <div class="bar-chart" :style="{ height: height + 'px' }">
    <div v-if="!data.length || maxValue === 1 && data.every(d => d.value === 0)" class="empty">
      Belum ada data untuk ditampilkan.
    </div>
    <div v-else class="bars">
      <div class="bar-col" v-for="item in data" :key="item.label">
        <div class="bar-value">{{ item.value }}</div>
        <div class="bar-track">
          <div
            class="bar-fill"
            :style="{
              height: (item.value / maxValue) * 100 + '%',
              background: item.color || '#111827'
            }"
          />
        </div>
        <div class="bar-label">{{ item.label }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.bar-chart {
  width: 100%;
  display: flex;
  align-items: stretch;
}

.empty {
  margin: auto;
  color: #9ca3af;
  font-size: 13px;
}

.bars {
  display: flex;
  align-items: flex-end;
  gap: 20px;
  width: 100%;
  padding: 0 8px;
}

.bar-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  min-width: 0;
}

.bar-value {
  font-size: 13px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 6px;
}

.bar-track {
  flex: 1;
  width: 100%;
  max-width: 56px;
  background: #f1f5f9;
  border-radius: 8px 8px 0 0;
  display: flex;
  align-items: flex-end;
  overflow: hidden;
}

.bar-fill {
  width: 100%;
  border-radius: 8px 8px 0 0;
  transition: height 0.5s ease;
  min-height: 2px;
}

.bar-label {
  margin-top: 10px;
  font-size: 12px;
  color: #6b7280;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}
</style>
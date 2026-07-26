<script setup>
// Komponen tab murni presentational, parent yang pegang state activeTab-nya
defineProps({
  modelValue: { type: String, required: true } // 'teks' | 'gambar' | 'video'
})
const emit = defineEmits(['update:modelValue'])

const tabs = [
  { key: 'teks', label: 'Teks' },
  { key: 'gambar', label: 'Gambar' },
  { key: 'video', label: 'Video' }
]
</script>

<template>
  <div class="tabs">
    <button
      v-for="tab in tabs"
      :key="tab.key"
      class="tab"
      :class="{ 'tab--active': modelValue === tab.key }"
      @click="emit('update:modelValue', tab.key)"
    >
      {{ tab.label }}
    </button>
  </div>
</template>

<style scoped>
.tabs {
  display: inline-flex;
  padding: 4px;
  border-radius: 999px;
  gap: 4px;
  margin-bottom: 16px;
  margin-top: 50px;
  margin-left: 110px;
}

.tab {
  border: none;
  padding: 8px 22px;
  border-radius: 999px;
  font-size: 14px;
  font-weight: 500;
  background: #E5EEFF;
  transition: background 0.15s ease, color 0.15s ease;
}

.tab--active {
  background: #1DBB82;
  color: black;
  box-shadow: 0 1px 4px rgba(30, 39, 73, 0.12);
}
</style>
<script setup>
defineProps({
  modelValue: { type: String, required: true }
})
const emit = defineEmits(['update:modelValue'])

const filters = ['Semua', 'Fakta', 'False Content', 'Misleading Content', 'Fabricated Content']
</script>

<template>
  <div class="filter-tabs">
    <button
      v-for="filter in filters"
      :key="filter"
      class="filter-pill"
      :class="{ 'filter-pill--active': modelValue === filter }"
      @click="emit('update:modelValue', filter)"
    >
      {{ filter }}
    </button>
  </div>
</template>

<style scoped>
.filter-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-left: 120px;
}

.filter-pill {
  border: 1px solid var(--color-border);
  background: white;
  color: black;
  padding: 8px 18px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 500;
  transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease;
}

.filter-pill:hover {
  border-color: green;
}

.filter-pill--active {
  background: #006C49;
  border-color: #006C49;
  color: white;
}
</style>
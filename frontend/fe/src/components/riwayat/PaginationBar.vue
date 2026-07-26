<script setup>
const props = defineProps({
  currentPage: { type: Number, required: true },
  totalPages: { type: Number, required: true }
})
const emit = defineEmits(['update:currentPage'])

function goTo(page) {
  if (page < 1 || page > props.totalPages) return
  emit('update:currentPage', page)
}
</script>

<template>
  <div class="pagination">
    <button class="page-btn page-btn--arrow" :disabled="currentPage === 1" @click="goTo(currentPage - 1)">
      ‹
    </button>

    <button
      v-for="page in totalPages"
      :key="page"
      class="page-btn"
      :class="{ 'page-btn--active': page === currentPage }"
      @click="goTo(page)"
    >
      {{ page }}
    </button>

    <button class="page-btn page-btn--arrow" :disabled="currentPage === totalPages" @click="goTo(currentPage + 1)">
      ›
    </button>
  </div>
</template>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: 32px;
}

.page-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
}

.page-btn:hover:not(:disabled) {
  border-color: var(--color-green);
}

.page-btn--active {
  background: #006C49;
  border-color: #006C49;
  color: #fff;
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-btn--arrow {
  font-size: 16px;
}
</style>
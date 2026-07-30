<script setup>
import { ref } from 'vue'
import AdminModal from './AdminModal.vue'

defineProps({
  title: { type: String, default: 'Konfirmasi' },
  message: { type: String, required: true },
  confirmLabel: { type: String, default: 'Hapus' }
})
const emit = defineEmits(['close', 'confirm'])

const isSubmitting = ref(false)

async function handleConfirm() {
  isSubmitting.value = true
  try {
    await emit('confirm')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <AdminModal :title="title" @close="emit('close')">
    <p class="message">{{ message }}</p>
    <div class="form-actions">
      <button type="button" class="btn-secondary" @click="emit('close')">Batal</button>
      <button type="button" class="btn-danger" :disabled="isSubmitting" @click="handleConfirm">
        {{ isSubmitting ? 'Memproses...' : confirmLabel }}
      </button>
    </div>
  </AdminModal>
</template>

<style scoped>
.message {
  font-size: 14px;
  color: #374151;
  line-height: 1.6;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 24px;
}

.btn-danger,
.btn-secondary {
  padding: 9px 18px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  font-family: inherit;
}

.btn-danger {
  background: #ff4d4d;
  color: #ffffff;
}

.btn-danger:hover {
  background: #e53e3e;
}

.btn-danger:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: #f3f4f6;
  color: #111827;
}

.btn-secondary:hover {
  background: #e5e7eb;
}
</style>
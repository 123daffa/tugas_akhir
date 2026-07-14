<script setup>
import { ref } from 'vue'

defineProps({
  isLoading: { type: Boolean, default: false }
})

const emit = defineEmits(['submit'])
const claimText = ref('')

function handleSubmit() {
  if (!claimText.value.trim()) return
  // Cukup emit data ke parent. Parent yang atur kapan loading mulai & selesai.
  emit('submit', claimText.value)

}
</script>

<template>
  <div class="form-card">
    <textarea
      v-model="claimText"
      class="claim-input"
      rows="6"
      placeholder="Masukkan teks berita atau klaim di sini untuk dianalisis..."
    ></textarea>

    <div class="counter">{{ claimText.length }} / 5000 karakter</div>
    <button class="btn-check" :disabled="!claimText.trim() || isLoading" @click="handleSubmit">
      🔍 {{ isLoading ? 'Memeriksa...' : 'Periksa Fakta' }}
    </button>
  </div>
</template>

<style scoped>
.form-card {
  background: white;
  margin-left: 110px;
  border-radius: 50px;
  padding: 20px;
  margin-bottom: 20px;
}

.claim-input {
  width: 100%;
  border: none;
  padding: 14px;
  font-family: inherit;
  font-size: 15px;
  resize: vertical;
}

.claim-input:focus {
  outline: none;
  border: 1px solid var(--color-green);
}

.counter {
  font-size: 11px;
  color: var(--color-text-muted);
  text-align: left;
  margin: 6px 2px 14px;
}

.btn-check {
  display: block;
  margin-left: auto;
  width: auto;
  text-align: center;
  background: #006C49;
  color: white;
  border: none;
  padding: 15px;
  border-radius: 18px;
  font-size: 14px;
  font-weight: 500;
}

.btn-check:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-check:not(:disabled):hover {
  opacity: 0.92;
}
</style>
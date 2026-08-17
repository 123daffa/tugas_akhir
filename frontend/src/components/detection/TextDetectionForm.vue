<script setup>
import { ref, computed } from 'vue'
import { ScanSearch } from 'lucide-vue-next';

defineProps({
  isLoading: { type: Boolean, default: false }
})

const emit = defineEmits(['submit'])
const claimText = ref('')

const wordCount = computed(() => {
  return claimText.value.trim().split(/\s+/).filter(Boolean).length
})

const MIN_WORDS = 8
const MAX_CHARS = 400   // batas nyata dari Tavily, satuan KARAKTER bukan kata

const isTooShort = computed(() => wordCount.value < MIN_WORDS)
const isTooLong = computed(() => claimText.value.length > MAX_CHARS)
const isTextValid = computed(() => !isTooShort.value && !isTooLong.value)
const showWordCountError = computed(() => claimText.value.trim().length > 0 && !isTextValid.value)

const errorMessage = computed(() => {
  if (isTooLong.value) {
    return `Maksimal ${MAX_CHARS} karakter diperbolehkan (saat ini ${claimText.value.length} karakter). Silakan persingkat teksnya.`
  }
  if (isTooShort.value) {
    return `Minimal ${MIN_WORDS} kalimat (saat ini baru ${wordCount.value} kalimat).`
  }
  return ''
})

function handleSubmit() {
  if (!claimText.value.trim()) return
  emit('submit', claimText.value)
}
</script>

<template>
  <div class="form-card">
    <textarea
      v-model="claimText"
      class="claim-input"
      :class="{ 'claim-input--error': showWordCountError }"
      rows="6"
      placeholder="Masukkan teks berita atau klaim di sini untuk dianalisis..."
    ></textarea>

    <p v-if="showWordCountError" class="field-error">
      {{ errorMessage }}
    </p>

    <div class="form-footer">
      <span class="counter" :class="{ 'counter--error': isTooLong }">
        {{ claimText.length }} / {{ MAX_CHARS }} karakter · {{ wordCount }} kalimat
      </span>
      <button class="btn-check" :disabled="!isTextValid || isLoading" @click="handleSubmit">
        <ScanSearch :size="16" style="vertical-align: middle; margin-bottom: 2px; margin-right: 3px;" /> {{ isLoading ? 'Memeriksa...' : 'Periksa Fakta' }}
      </button>
    </div>
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

.claim-input--error {
  outline: 1.5px solid var(--color-red);
}

.field-error {
  font-size: 12px;
  color: var(--color-red);
  margin: 6px 0 0;
}

.form-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 10px;
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
<script setup>
import { ref, computed } from 'vue'


defineProps({
  isLoading: { type: Boolean, default: false }
})

const emit = defineEmits(['submit'])
const claimText = ref('')

// Hitung jumlah kata: pecah teks berdasarkan spasi/whitespace,
// buang elemen kosong hasil pecahan (misal spasi ganda menghasilkan '').
const wordCount = computed(() => {
  return claimText.value.trim().split(/\s+/).filter(Boolean).length
})
 
const MIN_WORDS = 10
const isTextValid = computed(() => wordCount.value >= MIN_WORDS)
 
// Pesan error cuma ditampilin kalau user UDAH mulai ngetik (bukan pas form kosong-kosong aja),
// biar gak langsung nge-judge user kosongan padahal belum sempat ngetik apa-apa
const showWordCountError = computed(() => claimText.value.trim().length > 0 && !isTextValid.value)

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
      :class="{ 'claim-input--error': showWordCountError }"
      rows="6"
      placeholder="Masukkan teks berita atau klaim di sini untuk dianalisis..."
    ></textarea>

    <p v-if="showWordCountError" class="field-error">
      Minimal {{ MIN_WORDS }} kata diperlukan (saat ini baru {{ wordCount }} kata).
    </p>

    <!-- Dibungkus flex-row: counter nempel kiri, tombol nempel kanan -->
    <div class="form-footer">
      <span class="counter">{{ claimText.length }} / 5000 karakter · {{ wordCount }} kata</span>
      <button class="btn-check" :disabled="!isTextValid || isLoading" @click="handleSubmit">
        🔍 {{ isLoading ? 'Memeriksa...' : 'Periksa Fakta' }}
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
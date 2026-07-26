<script setup>
import { ref,computed } from 'vue'
import FileUploadBox from './FileUploadBox.vue'

// isLoading datang dari parent, karena parent yang beneran ngejalanin await API call
defineProps({
  isLoading: { type: Boolean, default: false }
})

const emit = defineEmits(['submit'])
const claimText = ref('')
const videoFile = ref(null)

const wordCount = computed(() => {
  return claimText.value.trim().split(/\s+/).filter(Boolean).length
})
 
const MIN_WORDS = 10
const isTextValid = computed(() => wordCount.value >= MIN_WORDS)
const showWordCountError = computed(() => claimText.value.trim().length > 0 && !isTextValid.value)
 
// Form valid kalau: teks udah cukup kata DAN gambar udah dipilih
const isFormValid = computed(() => isTextValid.value && !!videoFile.value)

function onFileSelected(file) {
  videoFile.value = file
}

function handleSubmit() {
  if (!claimText.value.trim() || !videoFile.value) return
  emit('submit', { text: claimText.value, video: videoFile.value })
}
</script>

<template>
  <div class="form-card">
    <div class="form-grid">
      <div class="field">
        <label class="field-label">📝 Masukkan teks berita atau klaim</label>
        <textarea
          v-model="claimText"
          class="claim-input"
          :class="{ 'claim-input--error': showWordCountError }"
          rows="6"
          placeholder="Ketik atau tempel klaim di sini..."
        ></textarea>
        <p v-if="showWordCountError" class="field-error">
          Minimal {{ MIN_WORDS }} kata diperlukan (saat ini baru {{ wordCount }} kata).
        </p>
      </div>
      <div class="field">
        <label class="field-label">🎬 Unggah Video</label>
        <FileUploadBox
          class="file-upload-box"
          label="Unggah Video"
          hint="Seret & lepas video ke sini atau klik untuk memilih file (MP4, MOV, maks. 50MB)"
          accept="video/*"
          @file-selected="onFileSelected"
        />
      </div>
    </div>

    <button
      class="btn-check"
      :disabled="!isFormValid || isLoading"
      @click="handleSubmit"
    >
      🔍 {{ isLoading ? 'Memeriksa...' : 'Periksa Fakta' }}
    </button>
  </div>
</template>

<style scoped>
.form-card {
  background: white;
  border-radius: 50px;
  padding: 20px;
  box-shadow: var(--shadow-card);
  margin-bottom: 20px;
  margin-left: 110px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 16px;
}

@media (max-width: 720px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}

.field-label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: black;
  margin-bottom: 8px;
}

.claim-input {
  width: 100%;
  height: calc(100% - 24px);
  border: 1px solid var(--color-border);
  border-radius: 30px;
  background: #F8F9FF;
  padding: 14px;
  font-family: inherit;
  font-size: 16px;
  resize: vertical;
  min-height: 110px;
}

.file-upload-box {
  background: #F8F9FF;
  border-radius: 30px;
}

.claim-input:focus {
  outline: none;
  border-color: var(--color-blue);
  background: #fff;
}

.claim-input--error {
  outline: 1.5px solid var(--color-red);
}
 
.field-error {
  font-size: 12px;
  color: var(--color-red);
  margin: 6px 0 0;
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
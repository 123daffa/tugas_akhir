<script setup>
import { ref } from 'vue'
import FileUploadBox from './FileUploadBox.vue'

// isLoading datang dari parent, karena parent yang beneran ngejalanin await API call
defineProps({
  isLoading: { type: Boolean, default: false }
})

const emit = defineEmits(['submit'])
const claimText = ref('')
const videoFile = ref(null)

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
          rows="6"
          placeholder="Ketik atau tempel klaim di sini..."
        ></textarea>
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
      :disabled="!claimText.trim() || !videoFile || isLoading"
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
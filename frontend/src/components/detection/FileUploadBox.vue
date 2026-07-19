<script setup>
import { ref } from 'vue'

const props = defineProps({
  label: { type: String, required: true },       // contoh: "Unggah Gambar Pendukung"
  hint: { type: String, required: true },         // contoh: "Seret & lepas gambar di sini (JPG, PNG, maks 5MB)"
  accept: { type: String, default: '*' }
})
const emit = defineEmits(['file-selected'])

const fileName = ref('')
const isDragging = ref(false)
const fileInput = ref(null)

function handleFiles(files) {
  if (!files || !files.length) return
  const file = files[0]
  fileName.value = file.name
  emit('file-selected', file)
}

function onDrop(e) {
  isDragging.value = false
  handleFiles(e.dataTransfer.files)
}

function onInputChange(e) {
  handleFiles(e.target.files)
}

function openPicker() {
  fileInput.value?.click()
}
</script>

<template>
  <div
    class="upload-box"
    :class="{ 'upload-box--dragging': isDragging, 'upload-box--filled': fileName }"
    @dragover.prevent="isDragging = true"
    @dragleave.prevent="isDragging = false"
    @drop.prevent="onDrop"
    @click="openPicker"
  >
    <input
      ref="fileInput"
      type="file"
      :accept="accept"
      class="hidden-input"
      @change="onInputChange"
    />
    <div class="upload-icon"><img src="../../assets/upload.svg" alt="upload"></div>
    <div class="upload-label">{{ fileName || label }}</div>
    <div class="upload-hint">{{ fileName ? 'Klik untuk ganti file' : hint }}</div>
  </div>
</template>

<style scoped>
.upload-box {
  border: 1.5px dashed var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-navy-light);
  padding: 40px 16px;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.15s ease, background 0.15s ease;
}

.upload-box:hover,
.upload-box--dragging {
  border-color: var(--color-blue);
  background: var(--color-blue-bg);
}

.upload-box--filled {
  border-style: solid;
  border-color: var(--color-green);
}

.hidden-input {
  display: none;
}

.upload-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  margin: 0 auto 10px;
  border-radius: 50%;
  background: rgba(32, 212, 138, 0.12);
}

.upload-icon img {
  width: 30px;
  height: 30px;
  opacity: 1;
}

.upload-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text);
  word-break: break-all;
}

.upload-hint {
  font-size: 11px;
  color: var(--color-text-muted);
  margin-top: 4px;
}
</style>
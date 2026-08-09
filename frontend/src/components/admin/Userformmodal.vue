<script setup>
import { ref, watch } from 'vue'
import AdminModal from './AdminModal.vue'

const props = defineProps({
  mode: { type: String, required: true },
  initialData: { type: Object, default: () => ({}) },
  isSaving: { type: Boolean, default: false }   // <-- baru, dikontrol parent
})
const emit = defineEmits(['close', 'submit'])

const fullName = ref('')
const email = ref('')
const password = ref('')
const role = ref('user')
const error = ref('')

watch(
  () => props.initialData,
  (data) => {
    fullName.value = data?.fullName || ''
    email.value = data?.email || ''
    role.value = data?.role || 'user'
    password.value = ''
  },
  { immediate: true }
)

function handleSubmit() {
  error.value = ''

  if (!fullName.value.trim() || !email.value.trim()) {
    error.value = 'Nama dan email wajib diisi.'
    return
  }
  if (!email.value.trim().endsWith('@gmail.com')) {
    error.value = 'Email harus berakhiran @gmail.com'
    return
  }
  if (props.mode === 'create' && password.value.length < 8) {
    error.value = 'Password minimal 8 karakter.'
    return
  }

  const payload = {
    fullName: fullName.value.trim(),
    email: email.value.trim(),
    role: role.value
  }
  if (props.mode === 'create') {
    payload.password = password.value
  }

  emit('submit', payload)   // cukup tembak, tidak perlu await/try/finally lagi
}
</script>

<template>
  <AdminModal :title="mode === 'create' ? 'Tambah User' : 'Edit User'" @close="emit('close')">
    <form class="user-form" @submit.prevent="handleSubmit">
      <label class="field">
        <span>Nama Lengkap</span>
        <input v-model="fullName" type="text" placeholder="Nama lengkap" />
      </label>

      <label class="field">
        <span>Email</span>
        <input v-model="email" type="email" placeholder="nama@email.com" />
      </label>

      <label class="field" v-if="mode === 'create'">
        <span>Password</span>
        <input v-model="password" type="password" placeholder="Minimal 8 karakter" />
      </label>

      <label class="field">
        <span>Role</span>
        <select v-model="role">
          <option value="user">User</option>
          <option value="admin">Admin</option>
        </select>
      </label>

      <p v-if="error" class="error-text">{{ error }}</p>

      <div class="form-actions">
        <button type="button" class="btn-secondary" @click="emit('close')">Batal</button>
        <button type="submit" class="btn-primary" :disabled="isSaving">
          {{ isSaving ? 'Menyimpan...' : mode === 'create' ? 'Tambah' : 'Simpan' }}
        </button>
      </div>
    </form>
  </AdminModal>
</template>

<style scoped>
.user-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
}

.field input,
.field select {
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 10px 12px;
  font-size: 14px;
  font-family: inherit;
  font-weight: 400;
  color: #111827;
}

.field input:focus,
.field select:focus {
  outline: none;
  border-color: #111827;
}

.error-text {
  color: #ff4d4d;
  font-size: 13px;
  font-weight: 500;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 8px;
}

.btn-primary,
.btn-secondary {
  padding: 9px 18px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  font-family: inherit;
}

.btn-primary {
  background: #111827;
  color: #ffffff;
}

.btn-primary:hover {
  background: #374151;
}

.btn-primary:disabled {
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
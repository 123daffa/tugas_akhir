<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'
import { Plus, Pencil, Trash2 } from 'lucide-vue-next'
import Userformmodal from '../components/admin/Userformmodal.vue'
import ConfirmDialog from '../components/admin/ConfirmDialog.vue'

const users = ref([])
const isLoading = ref(true)
const error = ref('')

const showFormModal = ref(false)
const formMode = ref('create') // 'create' | 'edit'
const selectedUser = ref(null)

const showConfirmDialog = ref(false)
const userToDelete = ref(null)

async function loadUsers() {
  isLoading.value = true
  error.value = ''
  try {
    const { data } = await api.get('/api/admin/users')
    users.value = data.items
  } catch (err) {
    console.error('Gagal ambil daftar user:', err)
    error.value = 'Gagal memuat daftar user. Coba muat ulang halaman.'
  } finally {
    isLoading.value = false
  }
}

function openCreateModal() {
  formMode.value = 'create'
  selectedUser.value = null
  showFormModal.value = true
}

function openEditModal(user) {
  formMode.value = 'edit'
  selectedUser.value = user
  showFormModal.value = true
}

async function handleFormSubmit(payload) {
  try {
    if (formMode.value === 'create') {
      await api.post('/api/admin/users', payload)
    } else {
      await api.put(`/api/admin/users/${selectedUser.value.id}`, payload)
    }
    showFormModal.value = false
    await loadUsers()
  } catch (err) {
    console.error('Gagal menyimpan user:', err)
  }
}

function openDeleteConfirm(user) {
  userToDelete.value = user
  showConfirmDialog.value = true
}

async function handleDeleteConfirm() {
  try {
    await api.delete(`/api/admin/users/${userToDelete.value.id}`)
    showConfirmDialog.value = false
    userToDelete.value = null
    await loadUsers()
  } catch (err) {
    console.error('Gagal menghapus user:', err)
  }
}

onMounted(loadUsers)
</script>

<template>
  <div class="users-page">
    <header class="page-header">
      <div>
        <h1>Kelola User</h1>
        <p>Kelola akun pengguna yang terdaftar di platform.</p>
      </div>
      <button class="btn-primary" @click="openCreateModal">
        <Plus :size="16" />
        <span>Tambah User</span>
      </button>
    </header>

    <p v-if="error" class="error-banner">{{ error }}</p>

    <section class="table-card">
      <p v-if="isLoading" class="empty-state">Memuat data...</p>
      <p v-else-if="!users.length" class="empty-state">Belum ada user terdaftar.</p>
      <table v-else class="users-table">
        <thead>
          <tr>
            <th>Nama</th>
            <th>Email</th>
            <th>Role</th>
            <th class="col-actions">Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.fullName }}</td>
            <td>{{ user.email }}</td>
            <td>
              <span class="role-badge" :class="`role-badge--${user.role}`">{{ user.role }}</span>
            </td>
            <td class="col-actions">
              <button class="icon-btn" title="Edit" @click="openEditModal(user)">
                <Pencil :size="16" />
              </button>
              <button class="icon-btn icon-btn--danger" title="Hapus" @click="openDeleteConfirm(user)">
                <Trash2 :size="16" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>

    <Userformmodal
      v-if="showFormModal"
      :mode="formMode"
      :initial-data="selectedUser || {}"
      @close="showFormModal = false"
      @submit="handleFormSubmit"
    />

    <ConfirmDialog
      v-if="showConfirmDialog"
      title="Hapus User"
      :message="`Yakin ingin menghapus user '${userToDelete?.fullName}'? Tindakan ini tidak bisa dibatalkan.`"
      confirm-label="Hapus"
      @close="showConfirmDialog = false"
      @confirm="handleDeleteConfirm"
    />
  </div>
</template>

<style scoped>
.users-page {
  max-width: 1100px;
}

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 28px;
}

.page-header h1 {
  font-size: 32px;
  font-weight: 700;
  color: #111827;
}

.page-header p {
  font-size: 14px;
  color: #6b7280;
  margin-top: 4px;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #111827;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  padding: 10px 18px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
  white-space: nowrap;
}

.btn-primary:hover {
  background: #374151;
}

.error-banner {
  background: #fee2e2;
  color: #b91c1c;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 13px;
  margin-bottom: 20px;
}

.table-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 8px 24px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
}

.empty-state {
  padding: 32px 0;
  text-align: center;
  color: #6b7280;
  font-size: 14px;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
}

.users-table th {
  text-align: left;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #6b7280;
  padding: 16px 8px;
  border-bottom: 1px solid #e5e7eb;
}

.users-table td {
  padding: 14px 8px;
  border-bottom: 1px solid #f3f4f6;
  font-size: 14px;
  color: #111827;
}

.users-table tr:last-child td {
  border-bottom: none;
}

.col-actions {
  text-align: right;
  white-space: nowrap;
}

.role-badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  text-transform: capitalize;
  background: #f3f4f6;
  color: #374151;
}

.role-badge--admin {
  background: #dcfce7;
  color: #15803d;
}

.icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px;
  border-radius: 6px;
  color: #6b7280;
  display: inline-flex;
}

.icon-btn:hover {
  background: #f3f4f6;
  color: #111827;
}

.icon-btn--danger:hover {
  background: #fee2e2;
  color: #dc2626;
}
</style>
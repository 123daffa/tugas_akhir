<script setup>
import { ref, onMounted, watch } from 'vue'
import { RouterLink } from 'vue-router'
import api from '../services/api'
import { Trash2, Eye } from 'lucide-vue-next'
import ConfirmDialog from '../components/admin/ConfirmDialog.vue'
import Pagination from '../components/riwayat/PaginationBar.vue'
import { showSuccess } from '../utils/alert'

const CATEGORY_CLASS = {
  'Fakta': 'badge--fakta',
  'False Content': 'badge--false',
  'Misleading Content': 'badge--misleading',
  'Fabricated Content': 'badge--fabricated'
}

const history = ref([])
const isLoading = ref(true)
const error = ref('')

const currentPage = ref(1)
const totalPages = ref(1)
const totalItems = ref(0)

const showConfirmDialog = ref(false)
const itemToDelete = ref(null)

async function loadHistory(page = 1) {
  isLoading.value = true
  error.value = ''

  try {
    const { data } = await api.get('/api/admin/content', {
      params: {
        page
      }
    })

    history.value = data.items
    currentPage.value = data.currentPage
    totalPages.value = data.totalPages
    totalItems.value = data.totalItems

  } catch (err) {
    console.error('Gagal ambil riwayat deteksi:', err)
    error.value = 'Gagal memuat riwayat deteksi. Coba muat ulang halaman.'
  } finally {
    isLoading.value = false
  }
}

watch(currentPage, (page, oldPage) => {
  if (page !== oldPage) {
    loadHistory(page)
  }
})

function openDeleteConfirm(item) {
  itemToDelete.value = item
  showConfirmDialog.value = true
}

async function handleDeleteConfirm() {
  try {
    await api.delete(`/api/admin/content/${itemToDelete.value.id}`)
    showConfirmDialog.value = false
    itemToDelete.value = null
    await loadHistory(currentPage.value)
    showSuccess('Riwayat Berhasil Dihapus.')
  } catch (err) {
    console.error('Gagal menghapus riwayat:', err)
  }
}

onMounted(() => {
  loadHistory(1)
})
</script>

<template>
  <div class="history-page">
    <header class="page-header">
      <div>
        <h1>Kelola Riwayat</h1>
        <p>Pantau dan kelola seluruh riwayat deteksi dari semua pengguna.</p>
      </div>

      <div class="summary">
        Total Data : <strong>{{ totalItems }}</strong>
      </div>
    </header>

    <p v-if="error" class="error-banner">
      {{ error }}
    </p>

    <section class="table-card">

      <p
        v-if="isLoading"
        class="empty-state"
      >
        Memuat data...
      </p>

      <p
        v-else-if="history.length === 0"
        class="empty-state"
      >
        Belum ada riwayat deteksi.
      </p>

      <table
        v-else
        class="history-table"
      >
        <thead>
          <tr>
            <th>User</th>
            <th>Jenis</th>
            <th>Kategori</th>
            <th>Tanggal</th>
            <th class="col-actions">Aksi</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="item in history"
            :key="item.id"
          >
            <td>{{ item.ownerName }}</td>

            <td>{{ item.type }}</td>

            <td>
              <span
                class="badge"
                :class="CATEGORY_CLASS[item.category] || ''"
              >
                {{ item.category }}
              </span>
            </td>

            <td>{{ item.date }}</td>

            <td class="col-actions">

              <RouterLink
                class="icon-btn"
                :to="`/riwayat/${item.id}`"
                title="Lihat Detail"
              >
                <Eye :size="16"/>
              </RouterLink>

              <button
                class="icon-btn icon-btn--danger"
                title="Hapus"
                @click="openDeleteConfirm(item)"
              >
                <Trash2 :size="16"/>
              </button>

            </td>
          </tr>
        </tbody>
      </table>

      <Pagination
        v-if="totalPages > 1"
        v-model:currentPage="currentPage"
        :totalPages="totalPages"
      />

    </section>

    <ConfirmDialog
      v-if="showConfirmDialog"
      title="Hapus Riwayat"
      message="Yakin ingin menghapus riwayat deteksi ini? Tindakan ini tidak dapat dibatalkan."
      confirm-label="Hapus"
      @close="showConfirmDialog = false"
      @confirm="handleDeleteConfirm"
    />

  </div>
</template>

<style scoped>
.history-page {
  max-width: 1100px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 28px;
}

.page-header h1 {
  font-size: 32px;
  font-weight: 700;
  color: #111827;
}

.page-header p {
  margin-top: 4px;
  font-size: 14px;
  color: #6b7280;
}

.summary {
  font-size: 14px;
  color: #6b7280;
}

.error-banner {
  background: #fee2e2;
  color: #b91c1c;
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.table-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 8px 24px 24px;
  box-shadow: 0 1px 2px rgba(0,0,0,.03);
}

.empty-state {
  padding: 40px 0;
  text-align: center;
  color: #6b7280;
}

.history-table {
  width: 100%;
  border-collapse: collapse;
}

.history-table th {
  text-align: left;
  padding: 16px 8px;
  font-size: 12px;
  text-transform: uppercase;
  color: #6b7280;
  border-bottom: 1px solid #e5e7eb;
}

.history-table td {
  padding: 14px 8px;
  border-bottom: 1px solid #f3f4f6;
  font-size: 14px;
}

.history-table tr:last-child td {
  border-bottom: none;
}

.col-actions {
  text-align: right;
  white-space: nowrap;
}

.badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
}

.badge--fakta {
  background: #dcfce7;
  color: #15803d;
}

.badge--false {
  background: #fee2e2;
  color: #b91c1c;
}

.badge--misleading {
  background: #fef9c3;
  color: #a16207;
}

.badge--fabricated {
  background: #e5e7eb;
  color: #374151;
}

.icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  display: inline-flex;
  padding: 6px;
  border-radius: 6px;
  color: #6b7280;
  text-decoration: none;
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
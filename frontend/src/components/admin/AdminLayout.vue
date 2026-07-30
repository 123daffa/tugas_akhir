<script setup>
import AdminSidebar from '../admin/AdminSidebar.vue'
</script>

<template>
  <div class="admin-shell">
    <AdminSidebar />
    <main class="admin-content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.admin-shell {
  min-height: 100vh;
  background: #f8fafc;
}

.admin-content {
  margin-left: 260px;
  padding: 32px 40px 60px;
  min-height: 100vh;
}

@media (max-width: 900px) {
  .admin-content {
    margin-left: 0;
    padding: 20px;
  }
}
</style>
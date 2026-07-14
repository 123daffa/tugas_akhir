<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Navbar from './components/layout/Navbar.vue'
import Footer from './components/layout/Footer.vue'
</script>

<template>
  <div id="app">
    <!-- Header -->
    <Navbar />

    <!-- Konten halaman -->
    <main class="main">
      <RouterView />
    </main>

  </div>

  <!-- Footer -->
  <Footer />
</template>


<style scoped>
/* ── Main ────────────────────────────────── */
.main {
  min-height: calc(100vh - 64px);
  background-color: #F8FAFC;
}
</style>
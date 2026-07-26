<script setup>
import { useRoute} from 'vue-router'
import Navbar from './components/layout/Navbar.vue'
import Footer from './components/layout/Footer.vue'

const route = useRoute()
</script>

<template>
  <div id="app">
    <!-- Header -->
    <Navbar v-if="!route.meta.hideLayout"/>

    <!-- Konten halaman -->
     <!-- Halaman full-page (login/register): render langsung tanpa wrapper apapun -->
    <router-view v-if="route.meta.hideLayout" />

    <main v-else class="main">
      <RouterView />
    </main>

  </div>

  <!-- Footer -->
  <Footer v-if="!route.meta.hideLayout"/>
</template>


<style scoped>
/* ── Main ────────────────────────────────── */
.main {
  min-height: calc(100vh - 64px);
  background-color: #F8FAFC;
}
</style>
<script setup>
import { useRoute } from 'vue-router'
import Navbar from './components/layout/Navbar.vue'
import Footer from './components/layout/Footer.vue'

const route = useRoute()
</script>

<template>

  <div class="app-shell">
    <Navbar v-if="!route.meta.hideLayout" />
    <router-view v-if="route.meta.hideLayout" />
    <main v-else class="app-main">
      <router-view />
    </main>
 
    <Footer v-if="!route.meta.hideLayout" />
  </div>
</template>


<style scoped>
/* ── Main ────────────────────────────────── */
.main {
  min-height: calc(100vh - 64px);
  background-color: #F8FAFC;
}
</style>
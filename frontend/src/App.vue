<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div id="app">

    <header class="header">
        <RouterLink to="/" class="text">
          <h1>FactCheck.ID</h1>
        </RouterLink>

        <!-- Navbar (kanan) -->
        <nav class="navbar" :class="{ open: menuOpen }">
          <RouterLink to="/">Home</RouterLink>
          <RouterLink to="/deteksi">Deteksi</RouterLink>
          <RouterLink to="/riwayat">Riwayat</RouterLink>
          <RouterLink to="/tentang">Tentang</RouterLink>
          <RouterLink to="/deteksi" class="btn-mulai">
            Mulai Deteksi
          </RouterLink>
        </nav>
    </header>

    <!-- Konten halaman -->
    <main class="main">
      <RouterView />
    </main>

  </div>

  <footer class="footer">
  <div class="footer-inner">
    <div class="footer-brand">
      <h1>FactCheck.ID</h1>
      <p>Platform verifikasi berita geopolitik terpercaya yang dibangun di atas pilar transparansi dan kecerdasan buatan.</p>
    </div>

    <div class="footer-col">
      <h3>Teknologi</h3>
      <ul>
        <li><a href="#">Groq AI</a></li>
        <li><a href="#">Tavily Search</a></li>
        <li><a href="#">OpenCV Vision</a></li>
      </ul>
    </div>

    <div class="footer-col">
      <h3>Perusahaan</h3>
      <ul>
        <li><RouterLink to="/tentang">Misi Kami</RouterLink></li>
        <li><a href="#">Panduan Verifikasi</a></li>
        <li><a href="#">Kebijakan Privasi</a></li>
      </ul>
    </div>
  </div>

  <div class="footer-bottom">
    <p>© 2024 FactCheck.ID. Geopolitical Truth Powered by AI.</p>
  </div>
</footer>
</template>


<style scoped>
/* ── Header ─────────────────────────────── */
.header {
  position       : sticky;
  top            : 0;
  z-index        : 100;
  background     : #ffffff;
  border-bottom  : 1px solid #e5e7eb;
  margin         : 0 auto;
  padding        : 0 1.5rem;
  height         : 64px;
  display        : flex;
  align-items    : center;
  justify-content: space-between;
  width: 90%;
  border-radius: 50px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* ── Navbar (kiri) ─────────────────────────── */

.text h1 {
  font-size  : 1.5rem;
  font-weight: 700;
  margin-left: 6.5rem; 
  color: black; 

}

/* ── Navbar (kanan) ──────────────────────── */
.navbar {
  display    : flex;
  align-items: center;
  gap        : 0.25rem;
  margin-right: 6rem;
}

.navbar a {
  text-decoration: none;
  color          : black;
  font-size      : 0.95rem;
  font-weight    : 500;
  padding        : 0.5rem 0.85rem;
  border-radius  : 6px;
  transition     : color 0.2s, background 0.2s;
  white-space    : nowrap;
}

.navbar a:hover {
  color     : #ffffff;
  background: #111827;
}

/* Link aktif */
.navbar a.router-link-exact-active {
  color          : #1B2B4B;
  background     : transparent;
  text-decoration: underline;
  text-underline-offset: 4px;
}

.navbar a.router-link-exact-active:hover {
  background: transparent;
}

/* Tombol Mulai Deteksi */
.btn-mulai {
  background  : #111827 !important;
  color       : #ffffff !important;
  padding     : 0.5rem 1.1rem !important;
  border-radius: 20px !important;
  font-weight : 600 !important;
  margin-left: 2rem;
  margin-right: 20px;
  transition  : background 0.2s, transform 0.1s !important;
}

.btn-mulai:hover {
  background: #374151 !important;
  transform : translateY(-1px);
}

.btn-mulai.router-link-exact-active {
  background: #374151 !important;
  color     : #ffffff !important;
}

/* ── Main ────────────────────────────────── */
.main {
  min-height: calc(100vh - 64px);
  background-color: #F8FAFC;
}

/* ── Footer ─────────────────────────────── */
.footer {
  background  : #f9fafb;
  border-top  : 1px solid #e5e7eb;
  margin-top  : auto;
}

.footer-inner {
  max-width      : 1100px;
  margin         : 0 auto;
  padding        : 2.5rem 1.5rem;
  display        : grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap            : 2rem;
}

.footer-brand h2 {
  font-size  : 1.1rem;
  font-weight: 700;
  color      : #111827;
  margin     : 0 0 0.75rem;
}

.footer-brand p {
  font-size  : 0.875rem;
  color      : #6b7280;
  line-height: 1.6;
  margin     : 0;
  max-width  : 260px;
}

.footer-col h3 {
  font-size  : 0.875rem;
  font-weight: 600;
  color      : #111827;
  margin     : 0 0 0.75rem;
}

.footer-col ul {
  list-style: none;
  padding   : 0;
  margin    : 0;
  display   : flex;
  flex-direction: column;
  gap       : 0.5rem;
}

.footer-col ul li a {
  font-size      : 0.875rem;
  color          : #6b7280;
  text-decoration: none;
  transition     : color 0.2s;
}

.footer-col ul li a:hover {
  color: #111827;
}

.footer-bottom {
  border-top: 1px solid #e5e7eb;
  padding   : 1rem 1.5rem;
  text-align: center;
}

.footer-bottom p {
  font-size: 0.8rem;
  color    : #9ca3af;
  margin   : 0;
}
</style>
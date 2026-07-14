<script setup>
const links = ['Kebijakan Privasi', 'Syarat & Ketentuan', 'Kontak', 'Bantuan']
</script>

<template>
  <footer class="footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <div class="footer-title">FactCheck.ID</div>
        <div class="footer-sub">© 2024 FactCheck.ID. Teknologi AI untuk Kebenaran Informasi.</div>
      </div>
      <nav class="footer-links">
        <a v-for="link in links" :key="link" href="#">{{ link }}</a>
      </nav>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  border-top: 1px solid var(--color-border);
  background: var(--color-surface);
}

.footer-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
}

.footer-brand {
  margin-right: 200px;
}

.footer-title {
  font-weight: 700;
  color: var(--color-navy);
  font-size: 15px;
}

.footer-sub {
  font-size: 12px;
  color: var(--color-text-muted);
  margin-top: 2px;
}

.footer-links {
  display: flex;
  gap: 20px;
  font-size: 13px;
  color: var(--color-text-muted);
}

.footer-links a:hover {
  color: var(--color-navy);
}
</style>
<script setup>
</script>

<template>
  <footer class="footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <div class="footer-title">FactCheck.ID</div>
        <div class="footer-sub">© 2026 FactCheck.ID. Teknologi AI untuk Kebenaran Informasi.</div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  border-top: 1px solid var(--color-border);
  background: var(--color-surface);
  padding: 0px 128px;
}

.footer-inner {
  max-width: 1200px;
  padding: 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
}

.footer-brand {
  gap: 200px;
}

.footer-title {
  font-weight: 700;
  color: black;
  font-size: 15px;
  margin-right: 100px;
}

.footer-sub {
  font-size: 12px;
  color: black;
  margin-top: 2px;
}
</style>
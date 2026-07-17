<script setup>
defineProps({
  direction: { type: String, default: 'horizontal' } // 'horizontal' | 'vertical'
})
</script>

<template>
  <div class="arrow" :class="`arrow--${direction}`">
    <span class="arrow-line"></span>
    <span class="arrow-head">{{ direction === 'horizontal' ? '›' : '⌄' }}</span>
  </div>
</template>

<style scoped>
.arrow {
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-muted);
  flex-shrink: 0;
}

.arrow--horizontal {
  flex-direction: row;
  min-width: 32px;
}

.arrow--horizontal .arrow-line {
  width: 100%;
  height: 1.5px;
  background: var(--color-border);
}

.arrow--horizontal .arrow-head {
  font-size: 20px;
  line-height: 1;
  margin-left: -4px;
}

.arrow--vertical {
  flex-direction: column;
  min-height: 28px;
}

.arrow--vertical .arrow-line {
  width: 1.5px;
  height: 100%;
  background: var(--color-border);
}

.arrow--vertical .arrow-head {
  font-size: 16px;
  line-height: 1;
  margin-top: -6px;
}
</style>
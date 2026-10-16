<template>
  <div class="language-badge">
    <span class="globe-icon">🌐</span>
    <span class="locale-text">EN</span>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  document.documentElement.lang = 'en'
})
</script>

<style scoped>
.language-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #f1f5f9;
  color: #334155;
  border: 1px solid #cbd5e1;
  border-radius: 4px;
  padding: 4px 10px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  user-select: none;
}

.globe-icon {
  font-size: 0.85rem;
}

.locale-text {
  color: #0284c7;
}
</style>

<script setup>
import AppNav from './AppNav.vue'

defineProps({
  page: { type: String, default: '' },
  mainClass: { type: String, default: '' },
})
</script>

<template>
  <AppNav :page="page" />
  <main class="app-main" :class="mainClass">
    <slot />
  </main>
</template>

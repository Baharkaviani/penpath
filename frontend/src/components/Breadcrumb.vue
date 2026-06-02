<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  items: { type: Array, default: () => [] },
})
</script>

<template>
  <nav v-if="items.length" class="breadcrumb" aria-label="Breadcrumb">
    <template v-for="(item, i) in items" :key="i">
      <RouterLink v-if="item.to && i < items.length - 1" :to="item.to">{{ item.label }}</RouterLink>
      <span v-else-if="i < items.length - 1">{{ item.label }}</span>
      <span v-else aria-current="page">{{ item.label }}</span>
      <span v-if="i < items.length - 1" class="breadcrumb__sep">/</span>
    </template>
  </nav>
</template>

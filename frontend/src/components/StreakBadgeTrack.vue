<script setup>
const props = defineProps({
  streakPosition: { type: Number, default: 0 },
})

const badges = [
  { src: '/badges/week1.webp', alt: 'Seed', title: 'The Seed of Beginning — Week 1' },
  { src: '/badges/week2.webp', alt: 'Flame', title: 'The Flame of Focus — Week 2' },
  { src: '/badges/week3.webp', alt: 'Garden', title: 'The Garden of Growth — Week 3' },
  { src: '/badges/week4.webp', alt: 'Gem', title: 'The Gem of Balance — Week 4' },
]

function badgeClass(i) {
  const pos = i + 1
  if (pos < props.streakPosition) return 'streak-badge is-earned'
  if (pos === props.streakPosition) return 'streak-badge is-current'
  return 'streak-badge is-locked'
}
</script>

<template>
  <div class="streak-badge-track" aria-label="Badge cycle: four crystals and crown">
    <div v-for="(b, i) in badges" :key="b.alt" :class="badgeClass(i)" :title="b.title">
      <img :src="b.src" :alt="b.alt" />
    </div>
    <span class="streak-badge-track__arrow" aria-hidden="true">→</span>
    <div
      class="streak-badge"
      :class="streakPosition > 4 ? 'is-earned' : streakPosition === 4 ? 'is-current' : 'is-locked'"
      title="The Crown of Consistency"
    >
      <img src="/badges/crown.webp" alt="Crown" />
    </div>
  </div>
</template>

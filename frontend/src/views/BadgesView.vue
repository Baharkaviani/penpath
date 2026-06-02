<script setup>
import { computed, onMounted, ref } from 'vue'
import AppNav from '../components/AppNav.vue'
import Breadcrumb from '../components/Breadcrumb.vue'
import StreakBadgeTrack from '../components/StreakBadgeTrack.vue'
import api from '../api/client'

const data = ref(null)

onMounted(async () => {
  const res = await api.get('/badges/')
  data.value = res.data
})

const progress = computed(() => data.value?.progress || { streak_position: 0, tier: 1, crowns_earned: 0 })
const earned = computed(() => data.value?.earned || [])

const collection = [
  { type: 'seed', src: '/badges/week1.webp', name: 'Seed of Beginning' },
  { type: 'flame', src: '/badges/week2.webp', name: 'Flame of Focus' },
  { type: 'garden', src: '/badges/week3.webp', name: 'Garden of Growth' },
  { type: 'gem', src: '/badges/week4.webp', name: 'Gem of Balance' },
  { type: 'crown', src: '/badges/crown.webp', name: 'Crown of Consistency' },
  { type: 'phoenix', src: '/badges/phoenix.png', name: 'Phoenix of Return' },
]

function hasBadge(type) {
  return earned.value.some((b) => b.badge_type === type)
}
</script>

<template>
  <AppNav page="badges" />
  <main class="app-main">
    <Breadcrumb :items="[{ label: 'Dashboard', to: '/dashboard' }, { label: 'Badges', to: '/badges' }]" />
    <header class="page-header">
      <h1>Badges</h1>
      <p>Win ≥80% Weekly Score to advance the crystal streak. Four wins earn a Crown; loss then win awards Phoenix.</p>
    </header>

    <div class="badges-hero">
      <div class="card">
        <h2 class="section-title">Current cycle · Tier {{ progress.tier }}</h2>
        <StreakBadgeTrack :streak-position="progress.streak_position" />
        <p class="tier-label">Streak position {{ progress.streak_position }} / 4 · {{ progress.crowns_earned }} crown(s) total</p>
      </div>
      <div class="card card--mist">
        <h2 class="section-title">Rules</h2>
        <table class="rules-table">
          <thead><tr><th>Event</th><th>Effect</th></tr></thead>
          <tbody>
            <tr><td>Weekly Score ≥ 80%</td><td>Win — advance streak (Week 1→4)</td></tr>
            <tr><td>4 consecutive wins</td><td>Crown awarded; cycle restarts at next tier</td></tr>
            <tr><td>Score &lt; 80%</td><td>Streak resets to zero</td></tr>
            <tr><td>Loss → immediate win</td><td>Phoenix (permanent); streak restarts at Week 1</td></tr>
          </tbody>
        </table>
      </div>
    </div>

    <h2 class="dashboard-section-title">Permanent collection</h2>
    <div class="badge-row">
      <div v-for="b in collection" :key="b.type" class="badge-chip">
        <img class="badge-img badge-img--lg" :class="{ 'is-locked': !hasBadge(b.type) }" :src="b.src" :alt="b.name" />
        <span>{{ b.name }}</span>
      </div>
    </div>
  </main>
</template>

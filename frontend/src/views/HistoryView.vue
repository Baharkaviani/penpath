<script setup>
import { onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import PageLayout from '../components/PageLayout.vue'
import Breadcrumb from '../components/Breadcrumb.vue'
import { useWeekStore } from '../stores/week'

const weekStore = useWeekStore()

onMounted(() => weekStore.fetchHistory())
</script>

<template>
  <PageLayout page="history">
    <Breadcrumb :items="[{ label: 'Dashboard', to: '/dashboard' }, { label: 'History', to: '/history' }]" />
    <header class="page-header">
      <h1>Week history</h1>
      <p>Click a row to open that week’s archived flowboard.</p>
    </header>
    <div class="card" style="padding: 0; overflow: hidden">
      <table class="data-table">
        <thead>
          <tr>
            <th>Week</th>
            <th>Core</th>
            <th>Side</th>
            <th>Score</th>
            <th>Result</th>
            <th>FLAME</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="w in weekStore.history"
            :key="w.id"
            class="history-row"
            tabindex="0"
            @click="$router.push(`/flowboard/${w.id}`)"
            @keydown.enter="$router.push(`/flowboard/${w.id}`)"
          >
            <td>
              <strong>{{ w.weekShort }}</strong>
              <div class="history-row__sub">{{ w.label }}</div>
            </td>
            <td>{{ w.core }}%</td>
            <td>{{ w.side }}%</td>
            <td><strong>{{ w.score }}%</strong></td>
            <td>
              <span class="win-pill" :class="w.win ? 'win-pill--win' : 'win-pill--loss'">{{ w.win ? 'Win' : 'Loss' }}</span>
            </td>
            <td>{{ w.flame }}</td>
            <td class="history-row__action">
              <RouterLink class="btn btn--secondary btn--sm" :to="`/flowboard/${w.id}`" @click.stop>View flowboard</RouterLink>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </PageLayout>
</template>

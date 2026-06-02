<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import AppNav from '../components/AppNav.vue'
import Breadcrumb from '../components/Breadcrumb.vue'
import FlowboardSheet from '../components/FlowboardSheet.vue'
import { normalizeWeek } from '../utils/flowboard'
import { useWeekStore } from '../stores/week'

const route = useRoute()
const weekStore = useWeekStore()
const week = ref(null)
const loading = ref(true)
const error = ref('')
const saving = ref(false)
let saveTimer = null

function print() {
  globalThis.print()
}

const weekId = computed(() => route.params.weekId)
const readOnly = computed(
  () => Boolean(weekId.value) || (week.value && week.value.isCurrent === false)
)

async function load() {
  loading.value = true
  error.value = ''
  try {
    if (weekId.value) {
      week.value = normalizeWeek(await weekStore.fetchWeek(weekId.value))
    } else {
      week.value = normalizeWeek(await weekStore.fetchCurrent())
    }
  } catch (e) {
    week.value = null
    const status = e.response?.status
    if (status === 404) {
      error.value = 'No current week found. Run: docker compose exec backend python manage.py seed_demo'
    } else {
      error.value = e.response?.data?.detail || 'Could not load flowboard.'
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  document.body.classList.add('flowboard-page')
  load()
})
onUnmounted(() => {
  document.body.classList.remove('flowboard-page')
})

watch(() => route.params.weekId, load)

function onUpdate(payload) {
  if (readOnly.value) return
  clearTimeout(saveTimer)
  saveTimer = setTimeout(async () => {
    saving.value = true
    try {
      week.value = normalizeWeek(await weekStore.saveCurrent(payload))
    } catch (e) {
      error.value = e.response?.data?.detail || 'Failed to save.'
    } finally {
      saving.value = false
    }
  }, 400)
}

const crumbs = computed(() => {
  const items = [
    { label: 'Dashboard', to: '/dashboard' },
    { label: 'History', to: '/history' },
  ]
  if (weekId.value && week.value) {
    items.push({ label: week.value.weekShort, to: `/flowboard/${weekId.value}` })
  } else {
    items.push({ label: 'This week', to: '/flowboard' })
  }
  return items
})
</script>

<template>
  <div class="flowboard-page">
    <AppNav page="flowboard" />
    <div class="flowboard-toolbar">
      <div>
        <h1 style="font-size: 1.25rem; margin: 0">
          {{ readOnly ? `Past week · ${week?.label}` : 'This week’s flowboard' }}
        </h1>
        <p style="margin: 0.35rem 0 0; color: var(--ink-muted); font-size: 0.875rem">
          {{ readOnly ? 'Read-only archive.' : 'Fill tasks, tap circles, rate FLAME at week’s end.' }}
          <span v-if="saving"> · Saving…</span>
        </p>
      </div>
      <div class="banner__actions">
        <template v-if="readOnly">
          <RouterLink class="btn btn--secondary" to="/history">← All weeks</RouterLink>
          <RouterLink class="btn btn--primary" to="/flowboard">Edit current week</RouterLink>
        </template>
        <template v-else>
          <button type="button" class="btn btn--ghost" @click="print">Print</button>
          <RouterLink class="btn btn--secondary" to="/scan">Scan paper</RouterLink>
          <RouterLink class="btn btn--primary" to="/dashboard">Dashboard</RouterLink>
        </template>
      </div>
    </div>

    <div v-if="readOnly && week" class="banner banner--archive" style="max-width: 1100px; margin: 0 auto 1rem">
      <div>
        <strong>Archived week</strong> · {{ week.label }}
        <span class="win-pill" :class="week.win ? 'win-pill--win' : 'win-pill--loss'" style="margin-left: 0.5rem">
          {{ week.win ? 'Win' : 'Loss' }}
        </span>
        <span style="margin-left: 0.5rem; color: var(--ink-muted)">Score {{ week.score }}% · FLAME {{ week.flame }}</span>
      </div>
    </div>

    <main class="app-main flowboard-main">
      <Breadcrumb :items="crumbs" />

      <p v-if="loading" style="color: var(--ink-muted)">Loading flowboard…</p>
      <div v-else-if="error" class="card" style="max-width: 1100px; margin: 0 auto">
        <p style="color: var(--danger); margin: 0 0 1rem">{{ error }}</p>
        <button type="button" class="btn btn--primary" @click="load">Retry</button>
      </div>
      <FlowboardSheet v-else-if="week" :week="week" :read-only="readOnly" @update="onUpdate" />
    </main>
  </div>
</template>

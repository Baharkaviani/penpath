<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import PageLayout from '../components/PageLayout.vue'
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
  document.body.classList.add('is-flowboard')
  load()
})
onUnmounted(() => {
  document.body.classList.remove('is-flowboard')
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

const pageTitle = computed(() =>
  readOnly.value && week.value ? week.value.label : 'This week’s flowboard'
)

const pageDescription = computed(() => {
  if (readOnly.value) {
    return 'Read-only archive. Edit the current week or pick another from History.'
  }
  return 'Fill tasks, tap circles as you progress, rate FLAME at week’s end, then check your Dashboard score.'
})
</script>

<template>
  <PageLayout page="flowboard">
    <Breadcrumb :items="crumbs" />

    <header class="page-header">
      <h1>{{ pageTitle }}</h1>
      <p>
        {{ pageDescription }}
        <span v-if="saving && !readOnly"> · Saving…</span>
      </p>
    </header>

    <div class="page-actions">
      <template v-if="readOnly">
        <RouterLink class="btn btn--secondary" to="/history">← All weeks</RouterLink>
        <RouterLink class="btn btn--primary" to="/flowboard">Edit current week</RouterLink>
      </template>
      <template v-else>
        <button type="button" class="btn btn--secondary" @click="print">Print</button>
        <RouterLink class="btn btn--secondary" to="/scan">Scan paper</RouterLink>
        <RouterLink class="btn btn--primary" to="/dashboard">Dashboard</RouterLink>
      </template>
    </div>

    <div v-if="readOnly && week" class="banner banner--archive">
      <div>
        <strong>Archived week</strong>
        <span class="win-pill" :class="week.win ? 'win-pill--win' : 'win-pill--loss'" style="margin-left: 0.5rem">
          {{ week.win ? 'Win' : 'Loss' }}
        </span>
        <span style="margin-left: 0.5rem; color: var(--ink-muted)">Score {{ week.score }}% · FLAME {{ week.flame }}</span>
      </div>
    </div>

    <p v-if="loading" style="color: var(--ink-muted)">Loading flowboard…</p>
    <div v-else-if="error" class="card">
      <p style="color: var(--danger); margin: 0 0 1rem">{{ error }}</p>
      <button type="button" class="btn btn--primary" @click="load">Retry</button>
    </div>
    <FlowboardSheet v-else-if="week" :week="week" :read-only="readOnly" @update="onUpdate" />
  </PageLayout>
</template>

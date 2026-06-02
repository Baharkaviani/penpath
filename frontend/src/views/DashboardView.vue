<script setup>
import { computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import AppNav from '../components/AppNav.vue'
import Breadcrumb from '../components/Breadcrumb.vue'
import StreakBadgeTrack from '../components/StreakBadgeTrack.vue'
import { useDashboardStore } from '../stores/dashboard'
import { scoreClass } from '../utils/scoring'

const dash = useDashboardStore()

onMounted(() => dash.fetch())

const stats = computed(() => dash.data?.stats || {})
const flame = computed(() => dash.data?.flame || [])
const chartBars = computed(() => dash.data?.chartBars || [])
const current = computed(() => dash.data?.currentWeek)
const maxHeight = computed(() => Math.max(...chartBars.value.map((b) => b.height), 1))
</script>

<template>
  <AppNav page="dashboard" />
  <main class="app-main">
    <Breadcrumb :items="[{ label: 'Dashboard', to: '/dashboard' }]" />
    <header class="page-header">
      <h1>Your numbers this week</h1>
      <p>Weekly Score = <strong>0.7 × Core Rate + 0.3 × Side Rate</strong>. Core and side rates come from filled tracker circles on your flowboard.</p>
    </header>

    <div class="stat-grid">
      <div class="stat-card">
        <span class="stat-card__icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.25" fill="currentColor" stroke="none"/></svg>
        </span>
        <div class="stat-card__value" :class="scoreClass(stats.weeklyScore)">{{ stats.weeklyScore }}%</div>
        <div class="stat-card__label">Weekly Score</div>
        <div class="stat-card__hint">Win · needs ≥ 80%</div>
      </div>
      <div class="stat-card">
        <span class="stat-card__icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><path d="M12 3l2.2 6.8H21l-5.5 4.2 2.1 6.5L12 16.2 6.4 20.5l2.1-6.5L3 9.8h6.8L12 3z"/></svg>
        </span>
        <div class="stat-card__value">{{ stats.coreRate }}%</div>
        <div class="stat-card__label">Core Rate</div>
        <div class="stat-card__hint">Main goals · circle trackers</div>
      </div>
      <div class="stat-card">
        <span class="stat-card__icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><path d="M8 6h12M8 12h9M8 18h11"/><circle cx="4" cy="6" r="1.25" fill="currentColor" stroke="none"/><circle cx="4" cy="12" r="1.25" fill="currentColor" stroke="none"/><circle cx="4" cy="18" r="1.25" fill="currentColor" stroke="none"/></svg>
        </span>
        <div class="stat-card__value">{{ stats.sideRate }}%</div>
        <div class="stat-card__label">Side Rate</div>
        <div class="stat-card__hint">Side quests · circle trackers</div>
      </div>
      <div class="stat-card">
        <span class="stat-card__icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round">
            <line x1="4" y1="20" x2="4" y2="12"/><line x1="7.5" y1="20" x2="7.5" y2="8"/><line x1="11" y1="20" x2="11" y2="5"/>
            <line x1="14.5" y1="20" x2="14.5" y2="10"/><line x1="18" y1="20" x2="18" y2="7"/><line x1="21.5" y1="20" x2="21.5" y2="14"/>
          </svg>
        </span>
        <div class="stat-card__value">{{ stats.avgFlame }}</div>
        <div class="stat-card__label">FLAME average</div>
        <div class="stat-card__hint">6 ratings · scale 1–5</div>
      </div>
    </div>

    <div class="dashboard-grid">
      <div class="card">
        <h2 class="section-title">Score trend · click a week</h2>
        <div class="chart-placeholder" aria-label="Score trend chart">
          <RouterLink
            v-for="b in chartBars"
            :key="b.weekId"
            class="chart-bar"
            :class="{ 'is-win': b.win }"
            :to="`/flowboard/${b.weekId}`"
            :style="{ height: `${(b.height / maxHeight) * 100}%` }"
            :title="`View ${b.label} flowboard`"
          >
            <span class="chart-bar__label">{{ b.label }}</span>
          </RouterLink>
        </div>
        <p style="font-size: 0.8125rem; color: var(--ink-muted); margin: 2rem 0 0">
          Dark bars = wins (≥ 80%). Select a bar to open that week’s archived flowboard.
        </p>
      </div>
      <div class="card card--mist">
        <h2 class="section-title">FLAME + Fulfillment (this week)</h2>
        <ul class="flame-list">
          <li v-for="f in flame" :key="f.name">
            <span class="flame-letter">{{ f.letter }}</span>
            <span>{{ f.name }}</span>
            <div class="flame-bar"><span :style="{ width: `${f.score * 20}%` }" /></div>
            <span class="flame-score">{{ f.score }}</span>
          </li>
        </ul>
        <RouterLink class="btn btn--ghost" to="/flowboard" style="margin-top: 1rem; width: 100%">Update ratings on flowboard</RouterLink>
      </div>
    </div>

    <div class="dashboard-grid" style="margin-top: 1.5rem">
      <div class="card">
        <h2 class="section-title">Badge streak · week {{ stats.streakWeek }} of 4</h2>
        <StreakBadgeTrack :streak-position="stats.streakWeek" />
        <p style="font-size: 0.875rem; color: var(--ink-muted); margin: 1rem 0 0">
          Tier {{ stats.tier }} · {{ stats.crownsEarned }} crown(s) earned
        </p>
        <RouterLink class="btn btn--secondary" to="/badges" style="margin-top: 1rem">How badges work →</RouterLink>
      </div>
      <div class="card">
        <h2 class="section-title">All-time stats</h2>
        <ul class="flame-list">
          <li><span class="flame-letter">W</span><span>Weeks tracked</span><span /><span class="flame-score">{{ stats.weeksTracked }}</span></li>
          <li><span class="flame-letter">%</span><span>Win rate</span><span /><span class="flame-score">{{ stats.winRate }}%</span></li>
          <li><span class="flame-letter">♛</span><span>Crowns</span><span /><span class="flame-score">{{ stats.crownsEarned }}</span></li>
          <li><span class="flame-letter">🔥</span><span>Phoenix badges</span><span /><span class="flame-score">{{ stats.phoenixCount }}</span></li>
        </ul>
      </div>
    </div>

    <section class="dashboard-section">
      <h2 class="dashboard-section-title">Quick actions</h2>
      <div class="quick-actions dashboard-footer-actions">
        <RouterLink class="action-card" to="/flowboard">
          <span class="action-card__label">Primary</span>
          <h3>This week’s flowboard</h3>
          <p>Plan, track circles, FLAME review.</p>
          <span class="action-card__cta">Open flowboard →</span>
        </RouterLink>
        <RouterLink class="action-card" to="/scan">
          <span class="action-card__label">On paper</span>
          <h3>Scan printed sheet</h3>
          <p>Upload photo → OCR review → save.</p>
          <span class="action-card__cta">Start scan →</span>
        </RouterLink>
        <RouterLink class="action-card" to="/history">
          <span class="action-card__label">Archive</span>
          <h3>Week history</h3>
          <p>Every past week as read-only flowboard.</p>
          <span class="action-card__cta">Browse history →</span>
        </RouterLink>
        <RouterLink class="action-card" to="/badges">
          <span class="action-card__label">Progress</span>
          <h3>Badge collection</h3>
          <p>Crystals, crowns, Phoenix rules.</p>
          <span class="action-card__cta">View badges →</span>
        </RouterLink>
      </div>
    </section>

    <section v-if="current" class="dashboard-section">
      <h2 class="dashboard-section-title">Current week</h2>
      <div class="this-week-banner">
        <div class="this-week-banner__meta">
          <strong>{{ current.label }}</strong> · Focus: {{ current.focus || '—' }}
        </div>
        <div>
          <RouterLink class="btn btn--secondary" to="/flowboard">Edit flowboard</RouterLink>
          <RouterLink class="btn btn--primary" to="/history" style="margin-left: 0.5rem">History</RouterLink>
        </div>
      </div>
    </section>
  </main>
</template>

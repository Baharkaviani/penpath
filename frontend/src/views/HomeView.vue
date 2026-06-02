<script setup>
import { RouterLink } from 'vue-router'
import AppNav from '../components/AppNav.vue'
</script>

<template>
  <AppNav page="home" />
  <section class="hub-hero">
    <h1>Plan on paper.<br />Track digitally.</h1>
    <p class="tagline">A weekly flowboard for your goals, plus a dashboard for scores, FLAME review, and badges.</p>
    <RouterLink class="btn btn--primary" to="/dashboard">Go to dashboard</RouterLink>
  </section>

  <div class="hub-layout">
    <div class="hub-grid hub-grid--primary">
      <RouterLink class="hub-card" to="/dashboard">
        <div class="hub-card__icon">📊</div>
        <h3>Dashboard</h3>
        <p>Quick actions and this week’s stats.</p>
      </RouterLink>
      <RouterLink class="hub-card" to="/flowboard">
        <div class="hub-card__icon">📋</div>
        <h3>Flowboard</h3>
        <p>Plan and track this week (or open a past week from History).</p>
      </RouterLink>
      <RouterLink class="hub-card" to="/badges">
        <div class="hub-card__icon">💎</div>
        <h3>Badges</h3>
        <p>Win streaks, crystals, crowns, and Phoenix recovery.</p>
      </RouterLink>
    </div>
    <div class="hub-grid hub-grid--secondary">
      <RouterLink class="hub-card" to="/scan">
        <div class="hub-card__icon">📷</div>
        <h3>Scan</h3>
        <p>Upload a photo of your printed sheet.</p>
      </RouterLink>
      <RouterLink class="hub-card" to="/history">
        <div class="hub-card__icon">📅</div>
        <h3>History</h3>
        <p>Click any week to view its full archived flowboard.</p>
      </RouterLink>
    </div>
  </div>

  <section class="hub-guide">
    <div class="callout callout--guide">
      <h2>How Penpath works</h2>
      <p>
        Plan your week on a <strong>flowboard</strong> — on paper or in the app. Track progress by filling in circles,
        close the week with a FLAME review, then see your <strong>Weekly Score</strong> and badges on the dashboard.
      </p>
      <ol class="workflow-steps">
        <li class="workflow-step">
          <div class="workflow-step__num">Step 1</div>
          <strong>Plan</strong>
          <span>Set focus, prize, core tasks, and side quests.</span>
          <RouterLink to="/flowboard">Open flowboard →</RouterLink>
        </li>
        <li class="workflow-step">
          <div class="workflow-step__num">Step 2</div>
          <strong>Track</strong>
          <span>Fill tracker circles as you progress during the week.</span>
          <RouterLink to="/flowboard">Track on flowboard →</RouterLink>
        </li>
        <li class="workflow-step">
          <div class="workflow-step__num">Step 3</div>
          <strong>Review</strong>
          <span>Rate FLAME + Fulfillment (1–5) and write reflection lines.</span>
          <RouterLink to="/dashboard">See dashboard →</RouterLink>
        </li>
        <li class="workflow-step">
          <div class="workflow-step__num">Step 4</div>
          <strong>Score</strong>
          <span>Weekly Score = 0.7×Core + 0.3×Side. Win at ≥80%.</span>
          <RouterLink to="/badges">Badge rules →</RouterLink>
        </li>
      </ol>
      <div class="guide-extras">
        <p><strong>Scan</strong> — photograph your printed sheet; OCR fills a draft for review.</p>
        <p><strong>History</strong> — every past week opens as a read-only flowboard archive.</p>
      </div>
    </div>
  </section>
</template>

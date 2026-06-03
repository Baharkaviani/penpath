<script setup>
import { RouterLink } from 'vue-router'
import AppNav from '../components/AppNav.vue'
import HowItWorksSection from '../components/HowItWorksSection.vue'
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

  <HowItWorksSection />
</template>

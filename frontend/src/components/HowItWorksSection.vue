<script setup>
import { RouterLink } from 'vue-router'

const weekBadges = [
  { src: '/badges/week1.webp', alt: 'Seed of Beginning' },
  { src: '/badges/week2.webp', alt: 'Flame of Focus' },
  { src: '/badges/week3.webp', alt: 'Garden of Growth' },
  { src: '/badges/week4.webp', alt: 'Gem of Balance' },
]
</script>

<template>
  <section class="how-it-works" aria-labelledby="how-it-works-title">
    <header class="how-it-works__header">
      <h2 id="how-it-works-title">How Penpath works</h2>
      <p>Two paths in, one dashboard out — paper, digital, or both.</p>
    </header>

    <div class="how-zigzag">
      <!-- Block 1: Paper -->
      <article class="how-zigzag__row">
        <div class="how-zigzag__visual" aria-hidden="true">
          <div class="hiw-scene hiw-scene--desk">
            <div class="hiw-desk-surface" />
            <div class="hiw-sheet hiw-sheet--back" />
            <div class="hiw-sheet hiw-sheet--front">
              <div class="hiw-sheet__header" />
              <div v-for="n in 5" :key="n" class="hiw-sheet__row">
                <span class="hiw-sheet__dot" />
                <span class="hiw-sheet__line" />
              </div>
            </div>
            <div class="hiw-pen" />
            <div class="hiw-mug">
              <div class="hiw-mug__liquid" />
            </div>
          </div>
        </div>
        <div class="how-zigzag__content">
          <p class="how-zigzag__eyebrow">🖨️ Prefer Paper? Print Your Planner.</p>
          <p class="how-zigzag__text">
            Love the feeling of pen on paper? Generate and print custom, minimalist planner sheets designed to keep
            you focused and distraction-free.
          </p>
          <RouterLink class="btn btn--primary" to="/flowboard">Download Templates ➔</RouterLink>
        </div>
      </article>

      <!-- Block 2: Digital -->
      <article class="how-zigzag__row how-zigzag__row--flip">
        <div class="how-zigzag__visual" aria-hidden="true">
          <div class="hiw-scene hiw-scene--app">
            <div class="hiw-mock-panel hiw-mock-window">
              <div class="hiw-mock-window__chrome">
                <span /><span /><span />
              </div>
              <div class="hiw-mock-window__title">Flowboard · This week</div>
              <div class="hiw-mock-table">
                <div class="hiw-mock-table__head">
                  <span>Task</span>
                  <span>M</span><span>T</span><span>W</span><span>T</span><span>F</span>
                </div>
                <div v-for="n in 4" :key="n" class="hiw-mock-table__row">
                  <span class="hiw-mock-table__task" />
                  <span v-for="d in 5" :key="d" class="hiw-mock-table__cell" :class="{ 'is-filled': d <= n }" />
                </div>
              </div>
              <div class="hiw-mock-flame">
                <span v-for="n in 5" :key="n" class="hiw-mock-flame__dot" :class="{ 'is-on': n <= 4 }" />
              </div>
            </div>
          </div>
        </div>
        <div class="how-zigzag__content">
          <p class="how-zigzag__eyebrow">💻 Stay Digital? Use the Flowboard.</p>
          <p class="how-zigzag__text">
            More of a screen person? Our interactive digital Flowboard lets you drag, drop, and organize your core
            tasks and side quests seamlessly in your browser.
          </p>
          <RouterLink class="btn btn--primary" to="/flowboard">Open Flowboard ➔</RouterLink>
        </div>
      </article>

      <!-- Block 3: Scan -->
      <article class="how-zigzag__row">
        <div class="how-zigzag__visual" aria-hidden="true">
          <div class="hiw-scene hiw-scene--scan">
            <div class="hiw-scan-paper">
              <div v-for="n in 4" :key="n" class="hiw-scan-paper__line" />
            </div>
            <div class="hiw-phone">
              <div class="hiw-phone__screen">
                <div class="hiw-scan-box hiw-scan-box--1" />
                <div class="hiw-scan-box hiw-scan-box--2" />
                <div class="hiw-scan-box hiw-scan-box--3" />
                <div class="hiw-scan-line hiw-scan-line--1" />
                <div class="hiw-scan-line hiw-scan-line--2" />
              </div>
            </div>
            <div class="hiw-sync-beam" />
            <div class="hiw-sync-laptop">
              <div class="hiw-sync-laptop__screen">
                <div class="hiw-sync-bar" />
                <div class="hiw-sync-bar hiw-sync-bar--short" />
              </div>
            </div>
          </div>
        </div>
        <div class="how-zigzag__content">
          <p class="how-zigzag__eyebrow">📸 Scan to Sync in Seconds</p>
          <p class="how-zigzag__text">
            Don't lose your history. If you chose the paper route, simply snap a quick photo of your sheet at the end
            of the week. Our built-in OCR automatically reads your handwriting and fills out your digital dashboard.
          </p>
          <RouterLink class="btn btn--primary" to="/scan">Scan Your Flowboard ➔</RouterLink>
        </div>
      </article>

      <!-- Block 4: Reward -->
      <article class="how-zigzag__row how-zigzag__row--flip">
        <div class="how-zigzag__visual" aria-hidden="true">
          <div class="hiw-scene hiw-scene--dashboard">
            <div class="hiw-dash-stack">
              <div class="hiw-dash-card">
                <div class="hiw-dash-card__header">
                  <div class="hiw-dash-card__label">Weekly Score trend</div>
                  <div class="hiw-dash-score">91%</div>
                </div>
                <div class="hiw-dash-chart">
                  <div v-for="(h, i) in [42, 58, 72, 68, 88, 91]" :key="i" class="hiw-dash-chart__bar" :style="{ height: `${h}%` }" />
                </div>
              </div>
              <div class="hiw-dash-badges">
                <div v-for="b in weekBadges" :key="b.alt" class="hiw-dash-badge">
                  <img :src="b.src" :alt="b.alt" />
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="how-zigzag__content">
          <p class="how-zigzag__eyebrow">🏆 Review, Score, Level Up</p>
          <p class="how-zigzag__text">
            Close out your week with a structured FLAME review. The app calculates your Weekly Score based on your
            completed core tasks and side quests, unlocking unique badges as you stay consistent.
          </p>
          <RouterLink class="btn btn--primary" to="/badges">Learn about Badge Rules ➔</RouterLink>
        </div>
      </article>
    </div>
  </section>
</template>

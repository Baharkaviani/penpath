<script setup>
import { RouterLink } from 'vue-router'

const hiwSteps = [
  {
    image: '/how-it-works/prefer-paper.png',
    flip: false,
    eyebrow: '🖨️ Prefer Paper? Print Your Planner.',
    text: 'Love the feeling of pen on paper? Generate and print custom, minimalist planner sheets designed to keep you focused and distraction-free.',
    to: '/flowboard',
    cta: 'Download Templates ➔',
  },
  {
    image: '/how-it-works/stay-digital.png',
    flip: true,
    eyebrow: '💻 Stay Digital? Use the Flowboard.',
    text: 'More of a screen person? Our interactive digital Flowboard lets you drag, drop, and organize your core tasks and side quests seamlessly in your browser.',
    to: '/flowboard',
    cta: 'Open Flowboard ➔',
  },
  {
    image: '/how-it-works/scan-to-sync.png',
    flip: false,
    eyebrow: '📸 Scan to Sync in Seconds',
    text: "Don't lose your history. If you chose the paper route, simply snap a quick photo of your sheet at the end of the week. Our built-in OCR automatically reads your handwriting and fills out your digital dashboard.",
    to: '/scan',
    cta: 'Scan Your Flowboard ➔',
  },
  {
    image: '/how-it-works/review.png',
    flip: true,
    eyebrow: '🏆 Review, Score, Level Up',
    text: 'Close out your week with a structured FLAME review. The app calculates your Weekly Score based on your completed core tasks and side quests, unlocking unique badges as you stay consistent.',
    to: '/badges',
    cta: 'Learn about Badge Rules ➔',
  },
]
</script>

<template>
  <section class="how-it-works" aria-labelledby="how-it-works-title">
    <header class="how-it-works__header">
      <h2 id="how-it-works-title">How Penpath works</h2>
      <p>Two paths in, one dashboard out — paper, digital, or both.</p>
    </header>

    <div class="how-zigzag">
      <article
        v-for="step in hiwSteps"
        :key="step.image"
        class="how-zigzag__row"
        :class="{ 'how-zigzag__row--flip': step.flip }"
      >
        <div class="how-zigzag__visual" aria-hidden="true">
          <div class="hiw-scene hiw-scene--photo">
            <img :src="step.image" alt="" class="hiw-scene__img" />
          </div>
        </div>
        <div class="how-zigzag__content">
          <p class="how-zigzag__eyebrow">{{ step.eyebrow }}</p>
          <p class="how-zigzag__text">{{ step.text }}</p>
          <RouterLink class="btn btn--primary" :to="step.to">{{ step.cta }}</RouterLink>
        </div>
      </article>
    </div>
  </section>
</template>

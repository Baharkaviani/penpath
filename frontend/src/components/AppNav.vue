<script setup>
import { ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useTheme } from '../composables/useTheme'
import { useAuthStore } from '../stores/auth'

defineProps({ page: { type: String, default: '' } })

const route = useRoute()
const auth = useAuthStore()
const navOpen = ref(false)
const { theme, setTheme } = useTheme()

const links = [
  { to: '/', page: 'home', label: 'Home' },
  { to: '/dashboard', page: 'dashboard', label: 'Dashboard' },
  { to: '/flowboard', page: 'flowboard', label: 'Flowboard' },
  { to: '/badges', page: 'badges', label: 'Badges' },
  { to: '/scan', page: 'scan', label: 'Scan' },
  { to: '/history', page: 'history', label: 'History' },
]

function isActive(link) {
  if (link.page === 'flowboard' && route.name?.startsWith('flowboard')) return true
  return route.path === link.to || route.meta?.page === link.page
}
</script>

<template>
  <nav class="app-nav" :class="{ 'is-open': navOpen }">
    <RouterLink class="app-nav__brand" to="/" @click="navOpen = false">
      <span class="app-nav__mark" aria-hidden="true">
        <svg viewBox="0 0 24 24" stroke-width="2"><path d="M4 19V5M8 19V9M12 19V3M16 19V11M20 19V7"/></svg>
      </span>
      Penpath
    </RouterLink>
    <div class="app-nav__links">
      <RouterLink
        v-for="link in links"
        :key="link.to"
        :to="link.to"
        :class="{ 'is-active': isActive(link) }"
        @click="navOpen = false"
      >
        {{ link.label }}
      </RouterLink>
    </div>
    <div class="app-nav__actions">
      <label class="theme-toggle">
        <select :value="theme" @change="setTheme($event.target.value)" aria-label="Theme">
          <option value="light">Light</option>
          <option value="dark">Dark</option>
          <option value="system">System</option>
        </select>
      </label>
      <button v-if="auth.user" type="button" class="btn btn--ghost btn--sm" @click="auth.logout()">Log out</button>
      <RouterLink v-else class="btn btn--ghost btn--sm" to="/login">Log in</RouterLink>
      <button type="button" class="btn btn--ghost btn--sm" style="display: none" @click="navOpen = !navOpen" aria-label="Menu">☰</button>
    </div>
  </nav>
</template>

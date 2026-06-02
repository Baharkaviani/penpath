<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import PageLayout from '../components/PageLayout.vue'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()
const username = ref('demo')
const password = ref('demo')
const error = ref('')
const mode = ref('login')

async function submit() {
  error.value = ''
  try {
    if (mode.value === 'login') {
      await auth.login(username.value, password.value)
    } else {
      await auth.register(username.value, password.value)
    }
    router.push(route.query.redirect || '/dashboard')
  } catch (e) {
    const status = e.response?.status
    const detail = e.response?.data?.detail
    if (status === 403) {
      error.value = 'CSRF blocked — restart frontend and use demo/demo. Avoid VITE_API_BASE_URL=http://localhost:8000 unless needed.'
    } else if (!e.response) {
      error.value = 'Cannot reach API. Is backend running on port 8000?'
    } else {
      error.value = detail || `Login failed (${status}). Try demo / demo after seed_demo.`
    }
  }
}
</script>

<template>
  <PageLayout main-class="app-main--login">
    <div class="card login-panel">
      <h1 style="font-family: var(--font-display); margin-top: 0">Sign in</h1>
      <p style="color: var(--ink-muted); font-size: 0.875rem">Demo account: <code>demo</code> / <code>demo</code> (after seed_demo)</p>
      <form @submit.prevent="submit">
        <input v-model="username" type="text" placeholder="Username" autocomplete="username" required />
        <input v-model="password" type="password" placeholder="Password" autocomplete="current-password" required />
        <p v-if="error" style="color: var(--danger); font-size: 0.875rem">{{ error }}</p>
        <button type="submit" class="btn btn--primary" style="width: 100%">
          {{ mode === 'login' ? 'Log in' : 'Register' }}
        </button>
      </form>
      <button type="button" class="btn btn--ghost" style="margin-top: 0.75rem; width: 100%" @click="mode = mode === 'login' ? 'register' : 'login'">
        {{ mode === 'login' ? 'Create account' : 'Use existing account' }}
      </button>
    </div>
  </PageLayout>
</template>

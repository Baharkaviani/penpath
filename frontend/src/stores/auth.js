import { defineStore } from 'pinia'
import { ref } from 'vue'
import api, { setCsrfToken } from '../api/client'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const ready = ref(false)

  async function fetchMe() {
    try {
      const { data } = await api.get('/me/')
      user.value = data
    } catch {
      user.value = null
    } finally {
      ready.value = true
    }
  }

  async function ensureCsrf() {
    const { data } = await api.get('/auth/csrf/')
    if (data?.csrfToken) setCsrfToken(data.csrfToken)
  }

  async function login(username, password) {
    await ensureCsrf()
    const { data } = await api.post('/auth/login/', { username, password })
    user.value = data
    return data
  }

  async function register(username, password) {
    await ensureCsrf()
    const { data } = await api.post('/auth/register/', { username, password })
    user.value = data
    return data
  }

  async function logout() {
    await ensureCsrf()
    await api.post('/auth/logout/')
    user.value = null
  }

  return { user, ready, fetchMe, ensureCsrf, login, register, logout }
})

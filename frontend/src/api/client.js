import axios from 'axios'

/** Fallback when document.cookie cannot read csrftoken (rare with proxy). */
let csrfToken = null

export function setCsrfToken(token) {
  csrfToken = token
}

function readCsrfFromCookie() {
  const match = document.cookie
    .split('; ')
    .find((row) => row.startsWith('csrftoken='))
  return match ? decodeURIComponent(match.split('=').slice(1).join('=')) : null
}

/** Prefer the cookie — it updates when the session changes (e.g. after login). */
export function getCsrfToken() {
  const fromCookie = readCsrfFromCookie()
  if (fromCookie) {
    csrfToken = fromCookie
    return fromCookie
  }
  return csrfToken
}

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  withCredentials: true,
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use((config) => {
  if (config.data instanceof FormData) {
    delete config.headers['Content-Type']
  }
  const token = getCsrfToken()
  if (token) config.headers['X-CSRFToken'] = token
  return config
})

export async function refreshCsrfToken() {
  const { data } = await api.get('/auth/csrf/')
  if (data?.csrfToken) {
    setCsrfToken(data.csrfToken)
    return data.csrfToken
  }
  return getCsrfToken()
}

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const { config, response } = error
    const isCsrf =
      response?.status === 403 &&
      typeof response?.data === 'object' &&
      String(response?.data?.detail || '').toLowerCase().includes('csrf')

    if (isCsrf && config && !config._csrfRetry) {
      config._csrfRetry = true
      await refreshCsrfToken()
      return api.request(config)
    }
    return Promise.reject(error)
  }
)

export default api

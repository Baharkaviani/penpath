import axios from 'axios'

/** CSRF token from /auth/csrf/ (needed when API is on a different port than the UI). */
let csrfToken = null

export function setCsrfToken(token) {
  csrfToken = token
}

const api = axios.create({
  // Use Vite proxy in Docker dev (/api → backend). Override only if you configure CORS + cookies.
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  withCredentials: true,
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use((config) => {
  const fromCookie = document.cookie
    .split('; ')
    .find((row) => row.startsWith('csrftoken='))
    ?.split('=')[1]
  const token = csrfToken || fromCookie
  if (token) config.headers['X-CSRFToken'] = token
  return config
})

export default api

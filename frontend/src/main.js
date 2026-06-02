import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import api, { setCsrfToken } from './api/client'
import './styles/penpath.css'

api.get('/auth/csrf/').then((res) => {
  if (res.data?.csrfToken) setCsrfToken(res.data.csrfToken)
}).catch(() => {})

createApp(App).use(createPinia()).use(router).mount('#app')

import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/', name: 'home', component: () => import('../views/HomeView.vue'), meta: { page: 'home' } },
  { path: '/login', name: 'login', component: () => import('../views/LoginView.vue'), meta: { guest: true } },
  { path: '/dashboard', name: 'dashboard', component: () => import('../views/DashboardView.vue'), meta: { page: 'dashboard', auth: true } },
  { path: '/flowboard', name: 'flowboard', component: () => import('../views/FlowboardView.vue'), meta: { page: 'flowboard', auth: true } },
  { path: '/flowboard/:weekId', name: 'flowboard-archive', component: () => import('../views/FlowboardView.vue'), meta: { page: 'flowboard', auth: true } },
  { path: '/badges', name: 'badges', component: () => import('../views/BadgesView.vue'), meta: { page: 'badges', auth: true } },
  { path: '/scan', name: 'scan', component: () => import('../views/ScanView.vue'), meta: { page: 'scan', auth: true } },
  { path: '/history', name: 'history', component: () => import('../views/HistoryView.vue'), meta: { page: 'history', auth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()
  if (!auth.ready) await auth.fetchMe()
  if (to.meta.auth && !auth.user) return { name: 'login', query: { redirect: to.fullPath } }
  if (to.meta.guest && auth.user) return { name: 'dashboard' }
})

export default router

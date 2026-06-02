import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api/client'

export const useDashboardStore = defineStore('dashboard', () => {
  const data = ref(null)

  async function fetch() {
    const res = await api.get('/dashboard/')
    data.value = res.data
    return res.data
  }

  return { data, fetch }
})

import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api/client'

export const useWeekStore = defineStore('week', () => {
  const currentWeek = ref(null)
  const history = ref([])

  async function fetchCurrent() {
    const { data } = await api.get('/weeks/current/')
    currentWeek.value = data
    return data
  }

  async function fetchWeek(weekId) {
    const { data } = await api.get(`/weeks/${weekId}/flowboard/`)
    return data
  }

  async function saveCurrent(payload) {
    const { data } = await api.patch('/weeks/current/', payload)
    currentWeek.value = data
    return data
  }

  async function fetchHistory() {
    const { data } = await api.get('/history/')
    history.value = data
    return data
  }

  return { currentWeek, history, fetchCurrent, fetchWeek, saveCurrent, fetchHistory }
})

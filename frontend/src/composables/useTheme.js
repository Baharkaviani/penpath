import { onMounted, ref, watch } from 'vue'

const STORAGE_KEY = 'penpath-theme'
const theme = ref('system')

function systemPrefersDark() {
  return window.matchMedia('(prefers-color-scheme: dark)').matches
}

function resolvedTheme() {
  if (theme.value === 'system') return systemPrefersDark() ? 'dark' : 'light'
  return theme.value
}

function applyTheme() {
  document.documentElement.setAttribute('data-theme', resolvedTheme())
}

export function useTheme() {
  onMounted(() => {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved === 'light' || saved === 'dark' || saved === 'system') {
      theme.value = saved
    }
    applyTheme()
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
      if (theme.value === 'system') applyTheme()
    })
  })

  watch(theme, (val) => {
    localStorage.setItem(STORAGE_KEY, val)
    applyTheme()
  })

  function setTheme(val) {
    theme.value = val
  }

  return { theme, setTheme }
}

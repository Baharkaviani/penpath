<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import PageLayout from '../components/PageLayout.vue'
import Breadcrumb from '../components/Breadcrumb.vue'
import api from '../api/client'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const status = ref('')
const scanId = ref(null)
const busy = ref(false)

async function onFile(e) {
  const input = e.target
  const file = input.files?.[0]
  if (!file) return

  busy.value = true
  status.value = 'Uploading…'
  try {
    await auth.ensureCsrf()
    const form = new FormData()
    form.append('image', file)
    const { data } = await api.post('/scans/', form)
    scanId.value = data.id
    status.value = 'Processing…'
    await pollScan()
  } catch (err) {
    status.value = err.response?.data?.detail || 'Upload failed. Check that you are logged in and the backend is running.'
    busy.value = false
  } finally {
    input.value = ''
  }
}

async function pollScan() {
  const check = async () => {
    try {
      const { data } = await api.get(`/scans/${scanId.value}/`)
      if (data.status === 'review') {
        status.value = 'Applying draft to your flowboard…'
        await auth.ensureCsrf()
        await api.post(`/scans/${scanId.value}/confirm/`)
        router.push('/flowboard')
        return
      }
      if (data.status === 'failed') {
        status.value = 'Scan failed. Try another photo.'
        busy.value = false
        return
      }
      setTimeout(check, 800)
    } catch {
      status.value = 'Could not check scan status.'
      busy.value = false
    }
  }
  check()
}
</script>

<template>
  <PageLayout page="scan">
    <Breadcrumb :items="[{ label: 'Dashboard', to: '/dashboard' }, { label: 'Scan', to: '/scan' }]" />
    <header class="page-header">
      <h1>Scan your flowboard</h1>
      <p>Upload a photo of your printed weekly sheet. OCR extracts a draft for you to review on the flowboard.</p>
    </header>

    <label class="scan-zone" :class="{ 'scan-zone--busy': busy }">
      <input
        type="file"
        accept="image/*"
        capture="environment"
        class="scan-zone__input"
        :disabled="busy"
        @change="onFile"
      />
      <div class="scan-zone__body">
        <div class="scan-zone__icon" aria-hidden="true">📷</div>
        <p class="scan-zone__title"><strong>Tap to upload</strong> or drop an image</p>
        <p class="scan-zone__hint">{{ status || 'JPEG or PNG · good lighting recommended' }}</p>
      </div>
    </label>

    <div class="scan-steps">
      <div class="scan-step">
        <div class="scan-step__num">1</div>
        <strong>Upload</strong>
        <p>Photo of completed flowboard</p>
      </div>
      <div class="scan-step">
        <div class="scan-step__num">2</div>
        <strong>Review</strong>
        <p>OCR draft (stub uses sample data)</p>
      </div>
      <div class="scan-step">
        <div class="scan-step__num">3</div>
        <strong>Save</strong>
        <p>Confirm on flowboard</p>
      </div>
    </div>
  </PageLayout>
</template>

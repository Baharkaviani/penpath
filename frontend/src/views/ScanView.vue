<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import PageLayout from '../components/PageLayout.vue'
import Breadcrumb from '../components/Breadcrumb.vue'
import api from '../api/client'

const router = useRouter()
const status = ref('')
const scanId = ref(null)
const polling = ref(false)

async function onFile(e) {
  const file = e.target.files?.[0]
  if (!file) return
  status.value = 'Uploading…'
  const form = new FormData()
  form.append('image', file)
  const { data } = await api.post('/scans/', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  scanId.value = data.id
  status.value = 'Processing…'
  pollScan()
}

async function pollScan() {
  polling.value = true
  const check = async () => {
    const { data } = await api.get(`/scans/${scanId.value}/`)
    if (data.status === 'review') {
      status.value = 'Ready for review — applying draft to current week…'
      await api.post(`/scans/${scanId.value}/confirm/`)
      polling.value = false
      router.push('/flowboard')
      return
    }
    if (data.status === 'failed') {
      status.value = 'Scan failed.'
      polling.value = false
      return
    }
    setTimeout(check, 800)
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

    <label class="scan-zone">
      <input type="file" accept="image/*" capture="environment" hidden @change="onFile" />
      <div class="scan-zone__icon">📷</div>
      <p><strong>Tap to upload</strong> or drop an image</p>
      <p style="font-size: 0.8125rem; color: var(--ink-muted)">{{ status || 'JPEG or PNG · good lighting recommended' }}</p>
    </label>

    <div class="scan-steps">
      <div class="scan-step">
        <div class="scan-step__num">1</div>
        <strong>Upload</strong>
        <p style="font-size: 0.8125rem; color: var(--ink-muted); margin: 0">Photo of completed flowboard</p>
      </div>
      <div class="scan-step">
        <div class="scan-step__num">2</div>
        <strong>Review</strong>
        <p style="font-size: 0.8125rem; color: var(--ink-muted); margin: 0">OCR draft (stub uses sample data)</p>
      </div>
      <div class="scan-step">
        <div class="scan-step__num">3</div>
        <strong>Save</strong>
        <p style="font-size: 0.8125rem; color: var(--ink-muted); margin: 0">Confirm on flowboard</p>
      </div>
    </div>
  </PageLayout>
</template>

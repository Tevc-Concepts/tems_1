<template>
  <div class="min-h-screen bg-background pb-20">
    <div class="p-4">
      <h1 class="text-2xl font-bold text-gray-800 mb-4">Report Incident</h1>
      <IncidentReportForm @submit="handleSubmit" />
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useIncidentStore } from '@/stores/incident'
import IncidentReportForm from '@/components/Incident/IncidentReportForm.vue'
import { useToast } from '@/composables/useToast'

const router = useRouter()
const incidentStore = useIncidentStore()
const { showToast } = useToast()

const handleSubmit = async (data) => {
  try {
    await incidentStore.reportIncident(data)
    showToast('Incident reported successfully', 'success')
    router.push('/driver')
  } catch (error) {
    showToast('Failed to report incident', 'error')
  }
}
</script>

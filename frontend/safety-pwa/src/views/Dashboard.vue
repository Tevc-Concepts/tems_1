<template>
  <AppLayout>
    <template #header>
      <h1 class="text-2xl font-bold text-gray-900">Safety Dashboard</h1>
    </template>

    <!-- KPI Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <Card>
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600">Open Incidents</p>
            <p class="text-3xl font-bold text-primary-600">{{ incidentStore.openIncidents.length }}</p>
          </div>
          <AlertTriangle class="w-12 h-12 text-primary-400" />
        </div>
      </Card>

      <Card>
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600">Critical Incidents</p>
            <p class="text-3xl font-bold text-error">{{ incidentStore.criticalCount }}</p>
          </div>
          <AlertCircle class="w-12 h-12 text-error" />
        </div>
      </Card>

      <Card>
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600">Compliance Rate</p>
            <p class="text-3xl font-bold text-success">{{ complianceStore.complianceRate }}%</p>
          </div>
          <Shield class="w-12 h-12 text-success" />
        </div>
      </Card>

      <Card>
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600">Pending Audits</p>
            <p class="text-3xl font-bold text-warning">{{ auditStore.pendingAudits.length }}</p>
          </div>
          <ClipboardCheck class="w-12 h-12 text-warning" />
        </div>
      </Card>
    </div>

    <!-- Quick Actions -->
    <div class="mb-8">
      <h2 class="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Button variant="primary" @click="router.push('/incidents')" class="py-6">
          <Plus class="w-5 h-5 mr-2" />
          Report Incident
        </Button>
        <Button variant="secondary" @click="router.push('/audits')" class="py-6">
          <ClipboardCheck class="w-5 h-5 mr-2" />
          Schedule Audit
        </Button>
        <Button variant="secondary" @click="router.push('/compliance')" class="py-6">
          <Shield class="w-5 h-5 mr-2" />
          Check Compliance
        </Button>
      </div>
    </div>

    <!-- Critical Incidents -->
    <div class="mb-8">
      <Card>
        <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <AlertTriangle class="w-5 h-5 text-primary-600 mr-2" />
          Critical Incidents
        </h3>
        <div v-if="incidentStore.loading" class="text-center py-8">
          <Loading />
        </div>
        <div v-else-if="criticalIncidents.length === 0" class="text-center py-8 text-gray-500">
          No critical incidents
        </div>
        <div v-else class="space-y-4">
          <div
            v-for="incident in criticalIncidents"
            :key="incident.name"
            class="flex items-center justify-between p-4 border border-red-200 bg-red-50 rounded-lg hover:bg-red-100"
          >
            <div>
              <h4 class="font-medium text-gray-900">{{ incident.title }}</h4>
              <p class="text-sm text-gray-600">{{ incident.location }} • {{ incident.reported_by }}</p>
            </div>
            <Badge variant="error">
              {{ incident.status }}
            </Badge>
          </div>
        </div>
      </Card>
    </div>

    <!-- Expiring Compliance Items -->
    <div>
      <h2 class="text-xl font-semibold text-gray-900 mb-4">Expiring Compliance</h2>
      <Card>
        <div v-if="complianceStore.loading" class="text-center py-8">
          <Loading />
        </div>
        <div v-else-if="expiringItems.length === 0" class="text-center py-8 text-gray-500">
          No items expiring soon
        </div>
        <div v-else class="space-y-4">
          <div
            v-for="item in expiringItems"
            :key="item.name"
            class="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50"
          >
            <div>
              <h4 class="font-medium text-gray-900">{{ item.title }}</h4>
              <p class="text-sm text-gray-600">Expires: {{ formatDate(item.expiry_date) }}</p>
            </div>
            <Badge variant="warning">
              Expiring Soon
            </Badge>
          </div>
        </div>
      </Card>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { AppLayout, Card, Button, Badge, Loading, formatDate } from '@shared'
import { AlertTriangle, AlertCircle, Shield, ClipboardCheck, Plus } from 'lucide-vue-next'
import { useIncidentStore } from '../stores/incidents'
import { useAuditStore } from '../stores/audits'
import { useComplianceStore } from '../stores/compliance'

const router = useRouter()
const incidentStore = useIncidentStore()
const auditStore = useAuditStore()
const complianceStore = useComplianceStore()

const criticalIncidents = computed(() => 
  incidentStore.criticalIncidents.slice(0, 5)
)

const expiringItems = computed(() => 
  complianceStore.expiringItems.slice(0, 5)
)

onMounted(async () => {
  await Promise.all([
    incidentStore.fetchCriticalIncidents(),
    incidentStore.fetchIncidents({ limit: 10 }),
    auditStore.fetchUpcomingAudits(),
    complianceStore.fetchExpiringItems(30),
    complianceStore.fetchComplianceItems()
  ])
})
</script>

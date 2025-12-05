<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Page Header -->
    <div class="bg-white border-b border-gray-200 px-4 py-6">
      <div class="max-w-7xl mx-auto">
        <h1 class="text-2xl font-bold text-gray-900">Operations Dashboard</h1>
        <p class="text-sm text-gray-600 mt-1">Fleet Tracking & Dispatch Management</p>
      </div>
    </div>

    <!-- Content -->
    <div class="max-w-7xl mx-auto px-4 py-6 space-y-8">
      <!-- KPI Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <Card>
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600">Active Vehicles</p>
            <p class="text-3xl font-bold text-primary-600">{{ fleetStore.activeCount }}</p>
          </div>
          <Truck class="w-12 h-12 text-primary-400" />
        </div>
      </Card>

      <Card>
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600">Pending Dispatches</p>
            <p class="text-3xl font-bold text-warning">{{ dispatchStore.pendingCount }}</p>
          </div>
          <Package class="w-12 h-12 text-warning" />
        </div>
      </Card>

      <Card>
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600">Active Routes</p>
            <p class="text-3xl font-bold text-success">{{ routeStore.activeCount }}</p>
          </div>
          <MapPin class="w-12 h-12 text-success" />
        </div>
      </Card>

      <Card>
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600">Available Vehicles</p>
            <p class="text-3xl font-bold text-info">{{ fleetStore.availableCount }}</p>
          </div>
          <CheckCircle class="w-12 h-12 text-info" />
        </div>
      </Card>
    </div>

    <!-- Quick Actions -->
    <div class="mb-8">
      <h2 class="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Button variant="primary" @click="router.push('/dispatch')" class="py-6">
          <Plus class="w-5 h-5 mr-2" />
          New Dispatch
        </Button>
        <Button variant="secondary" @click="router.push('/fleet')" class="py-6">
          <MapPin class="w-5 h-5 mr-2" />
          Track Fleet
        </Button>
        <Button variant="secondary" @click="router.push('/routes')" class="py-6">
          <Route class="w-5 h-5 mr-2" />
          Manage Routes
        </Button>
      </div>
    </div>

    <!-- Active Vehicles Map -->
    <div class="mb-8">
      <Card>
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Active Vehicles</h3>
        <div class="bg-gray-100 h-96 rounded-lg flex items-center justify-center">
          <p class="text-gray-500">Map View (Leaflet integration)</p>
        </div>
      </Card>
    </div>

    <!-- Recent Dispatches -->
    <div>
      <h2 class="text-xl font-semibold text-gray-900 mb-4">Recent Dispatches</h2>
      <Card>
        <div v-if="dispatchStore.loading" class="text-center py-8">
          <Loading />
        </div>
        <div v-else-if="recentDispatches.length === 0" class="text-center py-8 text-gray-500">
          No recent dispatches
        </div>
        <div v-else class="space-y-4">
          <div
            v-for="dispatch in recentDispatches"
            :key="dispatch.name"
            class="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50"
          >
            <div>
              <h4 class="font-medium text-gray-900">{{ dispatch.route_name }}</h4>
              <p class="text-sm text-gray-600">Driver: {{ dispatch.driver_name || 'Unassigned' }}</p>
            </div>
            <Badge :variant="getStatusVariant(dispatch.status)">
              {{ dispatch.status }}
            </Badge>
          </div>
        </div>
      </Card>
    </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Card, Button, Badge, Loading } from '@shared'
import { Truck, Package, MapPin, CheckCircle, Plus, Route } from 'lucide-vue-next'
import { useFleetStore } from '../stores/fleet'
import { useDispatchStore } from '../stores/dispatch'
import { useRouteStore } from '../stores/routes'

const router = useRouter()
const fleetStore = useFleetStore()
const dispatchStore = useDispatchStore()
const routeStore = useRouteStore()

const recentDispatches = computed(() => 
  dispatchStore.dispatches.slice(0, 5)
)

function getStatusVariant(status) {
  const variants = {
    pending: 'warning',
    assigned: 'info',
    in_progress: 'primary',
    completed: 'success',
    cancelled: 'error'
  }
  return variants[status] || 'secondary'
}

const loading = ref(true)
const fetchError = ref(null)

onMounted(async () => {
  try {
    await Promise.all([
      fleetStore.fetchActiveVehicles().catch(e => console.warn('Fleet fetch error:', e)),
      dispatchStore.fetchPendingDispatches().catch(e => console.warn('Dispatch fetch error:', e)),
      dispatchStore.fetchDispatches({ limit: 5 }).catch(e => console.warn('Dispatches fetch error:', e)),
      routeStore.fetchActiveRoutes().catch(e => console.warn('Routes fetch error:', e))
    ])
  } catch (err) {
    fetchError.value = err.message
    console.error('Dashboard data fetch error:', err)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Page Header -->
    <div class="bg-white border-b border-gray-200 px-4 py-6">
      <div class="max-w-7xl mx-auto">
        <h1 class="text-2xl font-bold text-gray-900">Driver Dashboard</h1>
        <p class="text-sm text-gray-600 mt-1">Welcome back, {{ authStore.userName || 'Driver' }}! • {{ currentDate }}</p>
      </div>
    </div>

    <!-- Content -->
    <div class="max-w-7xl mx-auto px-4 py-6 space-y-8">
      <!-- KPI Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">Trips Today</p>
              <p class="text-3xl font-bold text-blue-600">{{ dashboardData?.journey_plans?.length || 0 }}</p>
            </div>
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <Truck class="w-6 h-6 text-blue-600" />
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">Active Trips</p>
              <p class="text-3xl font-bold text-green-600">{{ activeTripsCount }}</p>
            </div>
            <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <Route class="w-6 h-6 text-green-600" />
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">Pending Tasks</p>
              <p class="text-3xl font-bold text-amber-600">{{ dashboardData?.pending_checks?.length || 0 }}</p>
            </div>
            <div class="w-12 h-12 bg-amber-100 rounded-lg flex items-center justify-center">
              <Clipboard class="w-6 h-6 text-amber-600" />
            </div>
          </div>
        </div>
      </div>

      <!-- Driver Qualification Status -->
      <div v-if="dashboardData?.qualification" class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Driver License Status</h3>
          <CreditCard class="w-6 h-6 text-gray-400" />
        </div>
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600">License Number</p>
            <p class="font-medium text-gray-900">{{ dashboardData.qualification.license_no }}</p>
          </div>
          <div class="text-right">
            <p class="text-sm text-gray-600">Expires</p>
            <p class="font-medium" :class="qualificationExpiringSoon ? 'text-amber-600' : 'text-gray-900'">
              {{ formatDate(dashboardData.qualification.expiry_date) }}
            </p>
          </div>
        </div>
        <div v-if="qualificationExpiringSoon" class="mt-4 p-3 bg-amber-50 border border-amber-200 rounded-lg flex items-start space-x-2">
          <AlertCircle class="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
          <p class="text-sm text-amber-700">
            Your license is expiring soon. Please renew it to continue driving.
          </p>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button @click="router.push('/trips')" class="p-4 border-2 border-gray-200 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors">
            <Route class="w-8 h-8 text-blue-600 mx-auto mb-2" />
            <p class="text-sm font-medium text-gray-900">My Trips</p>
          </button>
          <button @click="router.push('/inspection')" class="p-4 border-2 border-gray-200 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors">
            <Clipboard class="w-8 h-8 text-blue-600 mx-auto mb-2" />
            <p class="text-sm font-medium text-gray-900">Inspection</p>
          </button>
          <button @click="router.push('/incident')" class="p-4 border-2 border-gray-200 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors">
            <AlertTriangle class="w-8 h-8 text-blue-600 mx-auto mb-2" />
            <p class="text-sm font-medium text-gray-900">Report Incident</p>
          </button>
        </div>
      </div>

      <!-- Active/Upcoming Trips -->
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Today's Trips</h3>
          <router-link to="/trips" class="text-sm text-blue-600 font-medium flex items-center space-x-1 hover:text-blue-700">
            <span>View All</span>
            <ChevronRight class="w-4 h-4" />
        </router-link>
      </div>

        <div v-if="tripStore.loading" class="flex justify-center py-8">
          <LoadingSpinner message="Loading trips..." />
        </div>
        
        <div v-else-if="upcomingTrips.length > 0" class="space-y-4">
          <TripCard
            v-for="trip in upcomingTrips"
            :key="trip.name"
            :trip="trip"
            @start="handleStartTrip"
            @view="handleViewTrip"
          />
        </div>
        
        <EmptyState
          v-else
          :icon="MapPin"
          title="No trips scheduled"
          message="You don't have any trips scheduled for today. Check back later or contact dispatch."
        />
      </div>

      <!-- Pending Actions -->

      <!-- Pending Actions -->
      <div v-if="hasPendingActions" class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Pending Actions</h3>
        
        <div class="space-y-3">
          <!-- Pending Spot Checks -->
          <div v-if="dashboardData?.pending_checks?.length > 0" class="flex items-center justify-between p-4 bg-amber-50 border border-amber-200 rounded-lg">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-amber-100 rounded-lg flex items-center justify-center">
                <ClipboardCheck class="w-5 h-5 text-amber-600" />
              </div>
              <div>
                <p class="font-medium text-gray-900">Vehicle Inspection</p>
                <p class="text-sm text-gray-600">
                  {{ dashboardData.pending_checks.length }} pending check(s)
                </p>
              </div>
            </div>
            <router-link to="/inspection" class="px-4 py-2 bg-amber-600 text-white rounded-lg hover:bg-amber-700 text-sm font-medium">
              Inspect Now
            </router-link>
          </div>

          <!-- Recent Incidents -->
          <div v-if="dashboardData?.recent_incidents?.length > 0" class="flex items-center justify-between p-4 bg-red-50 border border-red-200 rounded-lg">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
                <AlertTriangle class="w-5 h-5 text-red-600" />
              </div>
              <div>
                <p class="font-medium text-gray-900">Recent Incidents</p>
                <p class="text-sm text-gray-600">
                  {{ dashboardData.recent_incidents.length }} incident(s) this week
                </p>
              </div>
            </div>
            <button @click="showIncidents = true" class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 text-sm font-medium">
              View
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { format, differenceInDays } from 'date-fns'
import { 
  User, MapPin, ChevronRight, CreditCard, 
  AlertCircle, ClipboardCheck, AlertTriangle, Fuel,
  Truck, Route, Clipboard
} from 'lucide-vue-next'
import { useAuth as useAuthStore } from '@shared'
import { useTripStore } from '@/stores/trip'
import TripCard from '@/components/trip/TripCard.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const router = useRouter()
const authStore = useAuthStore()
const tripStore = useTripStore()

const dashboardData = ref(null)
const showIncidents = ref(false)

const currentDate = computed(() => format(new Date(), 'EEEE, MMMM d, yyyy'))

const upcomingTrips = computed(() => {
  if (!dashboardData.value) return []
  
  const journeys = dashboardData.value.journey_plans || []
  const operations = dashboardData.value.operation_plans || []
  
  return [...journeys, ...operations]
    .sort((a, b) => new Date(a.start_time) - new Date(b.start_time))
    .slice(0, 3)
})

const activeTripsCount = computed(() => {
  if (!dashboardData.value) return 0
  const operations = dashboardData.value.operation_plans || []
  return operations.filter(op => op.status === 'Active').length
})

const qualificationExpiringSoon = computed(() => {
  if (!dashboardData.value?.qualification?.expiry_date) return false
  const daysUntilExpiry = differenceInDays(
    new Date(dashboardData.value.qualification.expiry_date),
    new Date()
  )
  return daysUntilExpiry <= 30 && daysUntilExpiry >= 0
})

const hasPendingActions = computed(() => {
  return (dashboardData.value?.pending_checks?.length > 0) || 
         (dashboardData.value?.recent_incidents?.length > 0)
})

function formatDate(date) {
  return format(new Date(date), 'MMM d, yyyy')
}

async function handleStartTrip(trip) {
  router.push(`/driver/trips/${trip.name}?action=start`)
}

function handleViewTrip(trip) {
  router.push(`/driver/trips/${trip.name}`)
}

onMounted(async () => {
  try {
    // Ensure auth is loaded first
    if (!authStore.isAuthenticated) {
      await authStore.fetchUserInfo()
    }
    dashboardData.value = await tripStore.fetchDashboard()
  } catch (error) {
    console.error('Failed to load dashboard:', error)
  }
})
</script>
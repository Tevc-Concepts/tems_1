<template>
  <div class="space-y-6">
    <!-- Welcome Card -->
    <div class="card p-6 bg-gradient-to-br from-charcoal-600 via-charcoal-500 to-charcoal-600 border-2 border-primary-500/30 shadow-neon">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-2xl font-bold mb-1 text-primary-500">
            Welcome back, {{ authStore.driverName }}!
          </h2>
          <p class="text-charcoal-300">{{ currentDate }}</p>
        </div>
        <div class="w-16 h-16 bg-primary-500/20 rounded-2xl flex items-center justify-center backdrop-blur-sm border-2 border-primary-500/50">
          <User class="w-8 h-8 text-primary-500" />
        </div>
      </div>
      
      <!-- Quick Stats -->
      <div class="grid grid-cols-3 gap-4 mt-6">
        <div class="bg-primary-500/10 backdrop-blur-sm rounded-lg p-3 text-center border border-primary-500/30">
          <p class="text-2xl font-bold text-primary-500">{{ dashboardData?.journey_plans?.length || 0 }}</p>
          <p class="text-xs text-charcoal-300">Trips Today</p>
        </div>
        <div class="bg-primary-500/10 backdrop-blur-sm rounded-lg p-3 text-center border border-primary-500/30">
          <p class="text-2xl font-bold text-primary-500">{{ activeTripsCount }}</p>
          <p class="text-xs text-charcoal-300">Active</p>
        </div>
        <div class="bg-primary-500/10 backdrop-blur-sm rounded-lg p-3 text-center border border-primary-500/30">
          <p class="text-2xl font-bold text-primary-500">{{ dashboardData?.pending_checks?.length || 0 }}</p>
          <p class="text-xs text-charcoal-300">Pending</p>
        </div>
      </div>
    </div>

    <!-- Driver Qualification Status -->
    <div 
      v-if="dashboardData?.qualification"
      class="card p-4"
      :class="qualificationExpiringSoon ? 'border-l-4 border-amber-500' : ''"
    >
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="w-12 h-12 bg-primary-50 rounded-xl flex items-center justify-center">
            <CreditCard class="w-6 h-6 text-primary-600" />
          </div>
          <div>
            <h3 class="font-semibold text-gray-900">Driver License</h3>
            <p class="text-sm text-gray-600">{{ dashboardData.qualification.license_no }}</p>
          </div>
        </div>
        <div class="text-right">
          <p class="text-xs text-gray-500">Expires</p>
          <p 
            class="text-sm font-semibold"
            :class="qualificationExpiringSoon ? 'text-amber-600' : 'text-gray-900'"
          >
            {{ formatDate(dashboardData.qualification.expiry_date) }}
          </p>
        </div>
      </div>
      <div 
        v-if="qualificationExpiringSoon"
        class="mt-3 p-3 bg-amber-50 rounded-lg flex items-start space-x-2"
      >
        <AlertCircle class="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
        <p class="text-sm text-amber-700">
          Your license is expiring soon. Please renew it to continue driving.
        </p>
      </div>
    </div>

    <!-- Active/Upcoming Trips -->
    <div class="space-y-4">
      <div class="flex items-center justify-between">
        <h3 class="section-title mb-0">Today's Trips</h3>
        <router-link 
          to="/driver/trips"
          class="text-sm text-primary-600 font-medium flex items-center space-x-1 hover:text-primary-700"
        >
          <span>View All</span>
          <ChevronRight class="w-4 h-4" />
        </router-link>
      </div>

      <LoadingSpinner v-if="tripStore.loading" message="Loading trips..." />
      
      <template v-else-if="upcomingTrips.length > 0">
        <TripCard
          v-for="trip in upcomingTrips"
          :key="trip.name"
          :trip="trip"
          @start="handleStartTrip"
          @view="handleViewTrip"
        />
      </template>
      
      <EmptyState
        v-else
        :icon="MapPin"
        title="No trips scheduled"
        message="You don't have any trips scheduled for today. Check back later or contact dispatch."
      />
    </div>

    <!-- Pending Actions -->
    <div 
      v-if="hasPendingActions"
      class="card p-4"
    >
      <h3 class="section-title">Pending Actions</h3>
      
      <div class="space-y-3">
        <!-- Pending Spot Checks -->
        <div 
          v-if="dashboardData?.pending_checks?.length > 0"
          class="flex items-center justify-between p-3 bg-amber-50 rounded-lg"
        >
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
          <router-link to="/driver/inspection" class="btn-secondary text-sm py-2">
            Inspect Now
          </router-link>
        </div>

        <!-- Recent Incidents -->
        <div 
          v-if="dashboardData?.recent_incidents?.length > 0"
          class="flex items-center justify-between p-3 bg-red-50 rounded-lg"
        >
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
          <button class="btn-secondary text-sm py-2" @click="showIncidents = true">
            View
          </button>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="grid grid-cols-2 gap-4">
      <button
        @click="$router.push('/driver/fuel')"
        class="card p-4 hover:shadow-lg transition-shadow active:scale-95 duration-200"
      >
        <div class="flex flex-col items-center space-y-2 text-center">
          <div class="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center">
            <Fuel class="w-6 h-6 text-blue-600" />
          </div>
          <p class="font-semibold text-gray-900">Log Fuel</p>
        </div>
      </button>

      <button
        @click="$router.push('/driver/incident')"
        class="card p-4 hover:shadow-lg transition-shadow active:scale-95 duration-200"
      >
        <div class="flex flex-col items-center space-y-2 text-center">
          <div class="w-12 h-12 bg-red-50 rounded-xl flex items-center justify-center">
            <AlertTriangle class="w-6 h-6 text-red-600" />
          </div>
          <p class="font-semibold text-gray-900">Report Incident</p>
        </div>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { format, differenceInDays } from 'date-fns'
import { 
  User, MapPin, ChevronRight, CreditCard, 
  AlertCircle, ClipboardCheck, AlertTriangle, Fuel 
} from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'
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
    dashboardData.value = await tripStore.fetchDashboard()
  } catch (error) {
    console.error('Failed to load dashboard:', error)
  }
})
</script>
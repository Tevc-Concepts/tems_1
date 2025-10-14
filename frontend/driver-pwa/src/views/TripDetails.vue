<template>
  <AppLayout>
    <div class="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <!-- Header with Back Button -->
      <div class="sticky top-0 z-10 bg-white border-b border-gray-200 shadow-sm">
        <div class="flex items-center px-4 py-3">
          <button 
            @click="router.back()" 
            class="mr-3 p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <ChevronLeft class="w-6 h-6 text-gray-700" />
          </button>
          <div class="flex-1">
            <h1 class="text-lg font-semibold text-gray-900">Trip Details</h1>
            <p class="text-sm text-gray-500">{{ trip?.name }}</p>
          </div>
          <button 
            @click="refreshTrip" 
            :disabled="loading"
            class="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <RefreshCw 
              class="w-5 h-5 text-gray-600" 
              :class="{ 'animate-spin': loading }"
            />
          </button>
        </div>
      </div>

      <div v-if="loading && !trip" class="p-8 flex justify-center">
        <LoadingSpinner />
      </div>

      <div v-else-if="error" class="p-4">
        <div class="bg-red-50 border border-red-200 rounded-lg p-4">
          <p class="text-red-800">{{ error }}</p>
          <button 
            @click="fetchTripDetails" 
            class="mt-2 text-red-600 font-medium"
          >
            Try Again
          </button>
        </div>
      </div>

      <div v-else-if="trip" class="pb-24">
        <!-- Status Banner -->
        <div 
          class="mx-4 mt-4 p-4 rounded-xl shadow-soft"
          :class="statusBannerClass"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-white/20 rounded-lg">
                <MapPin class="w-6 h-6 text-white" />
              </div>
              <div>
                <p class="text-white text-sm font-medium">Trip Status</p>
                <StatusBadge :status="trip.status" size="lg" />
              </div>
            </div>
            <button 
              v-if="canStartTrip"
              @click="startTrip"
              class="px-4 py-2 bg-white text-green-600 rounded-lg font-medium shadow-md hover:shadow-lg transition-all"
            >
              Start Trip
            </button>
            <button 
              v-else-if="canCompleteTrip"
              @click="completeTrip"
              class="px-4 py-2 bg-white text-blue-600 rounded-lg font-medium shadow-md hover:shadow-lg transition-all"
            >
              Complete Trip
            </button>
          </div>
        </div>

        <!-- Route Information -->
        <div class="mx-4 mt-4 bg-white rounded-xl shadow-card p-5">
          <h2 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <Route class="w-5 h-5 mr-2 text-primary-600" />
            Route Information
          </h2>
          
          <div class="space-y-4">
            <!-- Origin -->
            <div class="flex items-start space-x-3">
              <div class="p-2 bg-green-100 rounded-lg">
                <MapPin class="w-5 h-5 text-green-600" />
              </div>
              <div class="flex-1">
                <p class="text-xs text-gray-500 uppercase tracking-wide">Origin</p>
                <p class="text-sm font-medium text-gray-900">{{ route?.start_location }}</p>
                <p v-if="trip.start_time" class="text-xs text-gray-600 mt-1">
                  {{ formatDateTime(trip.start_time) }}
                </p>
              </div>
            </div>

            <!-- Destination -->
            <div class="flex items-start space-x-3">
              <div class="p-2 bg-red-100 rounded-lg">
                <MapPin class="w-5 h-5 text-red-600" />
              </div>
              <div class="flex-1">
                <p class="text-xs text-gray-500 uppercase tracking-wide">Destination</p>
                <p class="text-sm font-medium text-gray-900">{{ route?.end_location }}</p>
                <p v-if="trip.end_time" class="text-xs text-gray-600 mt-1">
                  {{ formatDateTime(trip.end_time) }}
                </p>
              </div>
            </div>

            <!-- Waypoints -->
            <div v-if="waypoints?.length" class="pt-3 border-t border-gray-100">
              <button 
                @click="showWaypoints = !showWaypoints"
                class="flex items-center justify-between w-full text-left"
              >
                <span class="text-sm font-medium text-gray-700">
                  Waypoints ({{ waypoints.length }})
                </span>
                <ChevronRight 
                  class="w-5 h-5 text-gray-400 transition-transform"
                  :class="{ 'rotate-90': showWaypoints }"
                />
              </button>
              
              <div v-show="showWaypoints" class="mt-3 space-y-2">
                <div 
                  v-for="(waypoint, index) in waypoints" 
                  :key="index"
                  class="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg"
                >
                  <div class="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                    <span class="text-xs font-semibold text-primary-700">{{ index + 1 }}</span>
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-gray-900 truncate">{{ waypoint.stop_name }}</p>
                    <p class="text-xs text-gray-500">{{ waypoint.stop_type }}</p>
                  </div>
                  <StatusBadge 
                    :status="waypoint.completed ? 'Completed' : 'Pending'" 
                    size="sm"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Vehicle & Driver Info -->
        <div class="mx-4 mt-4 bg-white rounded-xl shadow-card p-5">
          <h2 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <Truck class="w-5 h-5 mr-2 text-primary-600" />
            Vehicle & Assignment
          </h2>

          <div class="space-y-4">
            <!-- Vehicle -->
            <div class="flex items-center space-x-3">
              <div class="p-3 bg-blue-50 rounded-lg">
                <Truck class="w-6 h-6 text-blue-600" />
              </div>
              <div class="flex-1">
                <p class="text-xs text-gray-500 uppercase tracking-wide">Vehicle</p>
                <p class="text-sm font-semibold text-gray-900">{{ vehicle?.license_plate || trip.vehicle }}</p>
                <p class="text-xs text-gray-600">{{ vehicle?.make }} {{ vehicle?.model }}</p>
              </div>
            </div>

            <!-- Driver -->
            <div class="flex items-center space-x-3">
              <div class="p-3 bg-purple-50 rounded-lg">
                <User class="w-6 h-6 text-purple-600" />
              </div>
              <div class="flex-1">
                <p class="text-xs text-gray-500 uppercase tracking-wide">Driver</p>
                <p class="text-sm font-semibold text-gray-900">{{ driverName }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Trip Timeline -->
        <TripTimeline :trip-id="tripId" :events="tripEvents" class="mx-4 mt-4" />

        <!-- Quick Actions -->
        <div class="mx-4 mt-4 grid grid-cols-2 gap-3">
          <button 
            @click="navigateToInspection"
            class="p-4 bg-white rounded-xl shadow-card hover:shadow-lg transition-shadow"
          >
            <div class="flex flex-col items-center space-y-2">
              <div class="p-3 bg-orange-100 rounded-full">
                <ClipboardCheck class="w-6 h-6 text-orange-600" />
              </div>
              <span class="text-sm font-medium text-gray-700">Vehicle Check</span>
            </div>
          </button>

          <button 
            @click="navigateToFuelLog"
            class="p-4 bg-white rounded-xl shadow-card hover:shadow-lg transition-shadow"
          >
            <div class="flex flex-col items-center space-y-2">
              <div class="p-3 bg-green-100 rounded-full">
                <Fuel class="w-6 h-6 text-green-600" />
              </div>
              <span class="text-sm font-medium text-gray-700">Log Fuel</span>
            </div>
          </button>

          <button 
            @click="reportIncident"
            class="p-4 bg-white rounded-xl shadow-card hover:shadow-lg transition-shadow"
          >
            <div class="flex flex-col items-center space-y-2">
              <div class="p-3 bg-red-100 rounded-full">
                <AlertTriangle class="w-6 h-6 text-red-600" />
              </div>
              <span class="text-sm font-medium text-gray-700">Report Issue</span>
            </div>
          </button>

          <button 
            @click="openNavigation"
            class="p-4 bg-white rounded-xl shadow-card hover:shadow-lg transition-shadow"
          >
            <div class="flex flex-col items-center space-y-2">
              <div class="p-3 bg-blue-100 rounded-full">
                <Navigation class="w-6 h-6 text-blue-600" />
              </div>
              <span class="text-sm font-medium text-gray-700">Navigate</span>
            </div>
          </button>
        </div>

        <!-- Notes Section -->
        <div v-if="trip.notes" class="mx-4 mt-4 mb-4 bg-white rounded-xl shadow-card p-5">
          <h3 class="text-sm font-semibold text-gray-900 mb-2 flex items-center">
            <FileText class="w-4 h-4 mr-2 text-gray-600" />
            Notes
          </h3>
          <p class="text-sm text-gray-600 whitespace-pre-wrap">{{ trip.notes }}</p>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { 
  ChevronLeft, RefreshCw, MapPin, Route, Truck, User, 
  ChevronRight, ClipboardCheck, Fuel, AlertTriangle, 
  Navigation, FileText 
} from 'lucide-vue-next'
import AppLayout from '@/components/layout/AppLayout.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import StatusBadge from '@/components/common/StatusBadge.vue'
import TripTimeline from '@/components/trip/TripTimeline.vue'
import { useTripStore } from '@/stores/trip'
import { useVehicleStore } from '@/stores/vehicle'
import { useNotifications } from '@shared'
import { formatDateTime } from '@/utils/helpers'

const router = useRouter()
const route = useRoute()
const tripStore = useTripStore()
const vehicleStore = useVehicleStore()
const { showSuccess, showError } = useNotification()

const tripId = ref(route.params.id)
const trip = ref(null)
const routeData = ref(null)
const vehicle = ref(null)
const waypoints = ref([])
const tripEvents = ref([])
const loading = ref(false)
const error = ref(null)
const showWaypoints = ref(false)

const statusBannerClass = computed(() => {
  const status = trip.value?.status?.toLowerCase()
  switch (status) {
    case 'active':
    case 'in progress':
      return 'bg-gradient-to-r from-green-500 to-green-600'
    case 'completed':
      return 'bg-gradient-to-r from-blue-500 to-blue-600'
    case 'assigned':
      return 'bg-gradient-to-r from-yellow-500 to-yellow-600'
    default:
      return 'bg-gradient-to-r from-gray-500 to-gray-600'
  }
})

const canStartTrip = computed(() => {
  return trip.value?.status === 'Assigned'
})

const canCompleteTrip = computed(() => {
  return trip.value?.status === 'Active' || trip.value?.status === 'In Progress'
})

const driverName = computed(() => {
  return trip.value?.driver || 'Not Assigned'
})

const fetchTripDetails = async () => {
  loading.value = true
  error.value = null
  
  try {
    // Fetch trip details from Journey Plan
    const tripData = await tripStore.fetchTripById(tripId.value)
    trip.value = tripData
    
    // Fetch route details if available
    if (tripData.route) {
      routeData.value = await tripStore.fetchRouteDetails(tripData.route)
      waypoints.value = routeData.value?.waypoints || []
    }
    
    // Fetch vehicle details
    if (tripData.vehicle) {
      vehicle.value = await vehicleStore.fetchVehicleById(tripData.vehicle)
    }
    
    // Fetch trip events/timeline
    tripEvents.value = await tripStore.fetchTripEvents(tripId.value)
    
  } catch (err) {
    error.value = err.message || 'Failed to load trip details'
    showError('Failed to load trip details')
  } finally {
    loading.value = false
  }
}

const refreshTrip = async () => {
  await fetchTripDetails()
  showSuccess('Trip details refreshed')
}

const startTrip = async () => {
  try {
    loading.value = true
    await tripStore.startTrip(tripId.value)
    await fetchTripDetails()
    showSuccess('Trip started successfully')
  } catch (err) {
    showError(err.message || 'Failed to start trip')
  } finally {
    loading.value = false
  }
}

const completeTrip = async () => {
  try {
    loading.value = true
    await tripStore.completeTrip(tripId.value)
    await fetchTripDetails()
    showSuccess('Trip completed successfully')
    router.push('/trips')
  } catch (err) {
    showError(err.message || 'Failed to complete trip')
  } finally {
    loading.value = false
  }
}

const navigateToInspection = () => {
  router.push(`/inspection?vehicle=${trip.value.vehicle}&trip=${tripId.value}`)
}

const navigateToFuelLog = () => {
  router.push(`/fuel?vehicle=${trip.value.vehicle}&trip=${tripId.value}`)
}

const reportIncident = () => {
  router.push(`/incident?trip=${tripId.value}&vehicle=${trip.value.vehicle}`)
}

const openNavigation = () => {
  if (routeData.value?.start_location && routeData.value?.end_location) {
    const url = `https://www.google.com/maps/dir/?api=1&origin=${routeData.value.start_location}&destination=${routeData.value.end_location}`
    window.open(url, '_blank')
  } else {
    showError('Navigation data not available')
  }
}

onMounted(() => {
  fetchTripDetails()
})
</script>
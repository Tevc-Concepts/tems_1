<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold text-gray-900">My Trips</h1>
      <button 
        @click="refreshTrips"
        class="p-2 rounded-lg hover:bg-gray-100 transition-colors"
        :disabled="tripStore.loading"
      >
        <RefreshCw :class="['w-5 h-5 text-gray-600', tripStore.loading && 'animate-spin']" />
      </button>
    </div>

    <!-- Filter Tabs -->
    <div class="card p-2 flex space-x-2">
      <button
        v-for="filter in filters"
        :key="filter.value"
        @click="activeFilter = filter.value"
        class="flex-1 py-2 px-4 rounded-lg font-medium text-sm transition-all"
        :class="activeFilter === filter.value 
          ? 'bg-primary-500 text-white shadow-sm' 
          : 'text-gray-600 hover:bg-gray-50'"
      >
        {{ filter.label }}
      </button>
    </div>

    <!-- Trip List -->
    <LoadingSpinner v-if="tripStore.loading" message="Loading trips..." />
    
    <template v-else-if="filteredTrips.length > 0">
      <div class="space-y-4">
        <TripCard
          v-for="trip in filteredTrips"
          :key="trip.name"
          :trip="trip"
          :show-actions="true"
          @start="handleStartTrip"
          @complete="handleCompleteTrip"
          @view="handleViewTrip"
        />
      </div>
    </template>
    
    <EmptyState
      v-else
      :icon="MapPin"
      title="No trips found"
      :message="emptyStateMessage"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { RefreshCw, MapPin } from 'lucide-vue-next'
import { useTripStore } from '@/stores/trip'
import TripCard from '@/components/trip/TripCard.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const router = useRouter()
const tripStore = useTripStore()

const activeFilter = ref('upcoming')

const filters = [
  { label: 'Upcoming', value: 'upcoming' },
  { label: 'Active', value: 'active' },
  { label: 'Completed', value: 'completed' }
]

const filteredTrips = computed(() => {
  const now = new Date()
  
  switch (activeFilter.value) {
    case 'upcoming':
      return tripStore.trips.filter(t => 
        new Date(t.start_time) > now && t.status !== 'Completed'
      )
    case 'active':
      return tripStore.trips.filter(t => t.status === 'Active')
    case 'completed':
      return tripStore.trips.filter(t => t.status === 'Completed')
    default:
      return tripStore.trips
  }
})

const emptyStateMessage = computed(() => {
  switch (activeFilter.value) {
    case 'upcoming':
      return 'You have no upcoming trips scheduled.'
    case 'active':
      return 'You have no active trips at the moment.'
    case 'completed':
      return 'You have no completed trips yet.'
    default:
      return 'No trips found.'
  }
})

async function refreshTrips() {
  await tripStore.fetchDashboard()
}

function handleStartTrip(trip) {
  router.push(`/driver/trips/${trip.name}?action=start`)
}

function handleCompleteTrip(trip) {
  router.push(`/driver/trips/${trip.name}?action=complete`)
}

function handleViewTrip(trip) {
  router.push(`/driver/trips/${trip.name}`)
}

onMounted(async () => {
  await refreshTrips()
})
</script>
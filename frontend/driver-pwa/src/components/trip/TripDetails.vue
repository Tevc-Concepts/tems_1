<template>
  <div class="bg-white rounded-xl shadow-card p-4">
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-lg font-bold text-gray-800">Trip Details</h2>
      <StatusBadge :status="trip.status" />
    </div>

    <div class="space-y-3">
      <!-- Route -->
      <div class="flex items-start">
        <MapPin class="w-5 h-5 text-primary-600 mr-3 mt-0.5" />
        <div class="flex-1">
          <div class="text-sm text-gray-600">Route</div>
          <div class="font-medium">{{ trip.route || 'N/A' }}</div>
        </div>
      </div>

      <!-- Vehicle -->
      <div class="flex items-start">
        <Truck class="w-5 h-5 text-primary-600 mr-3 mt-0.5" />
        <div class="flex-1">
          <div class="text-sm text-gray-600">Vehicle</div>
          <div class="font-medium">{{ trip.vehicle || 'N/A' }}</div>
        </div>
      </div>

      <!-- Schedule -->
      <div class="flex items-start">
        <Clock class="w-5 h-5 text-primary-600 mr-3 mt-0.5" />
        <div class="flex-1">
          <div class="text-sm text-gray-600">Schedule</div>
          <div class="font-medium">
            {{ formatTime(trip.start_time) }} - {{ formatTime(trip.end_time) }}
          </div>
        </div>
      </div>

      <!-- Distance -->
      <div class="flex items-start" v-if="trip.distance">
        <Navigation class="w-5 h-5 text-primary-600 mr-3 mt-0.5" />
        <div class="flex-1">
          <div class="text-sm text-gray-600">Distance</div>
          <div class="font-medium">{{ trip.distance }} km</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { MapPin, Truck, Clock, Navigation } from 'lucide-vue-next'
import StatusBadge from '@/components/common/StatusBadge.vue'
import { format, parseISO } from 'date-fns'

defineProps({
  trip: {
    type: Object,
    required: true,
  },
})

const formatTime = (dateString) => {
  if (!dateString) return 'N/A'
  try {
    return format(parseISO(dateString), 'HH:mm')
  } catch (error) {
    return 'Invalid'
  }
}
</script>

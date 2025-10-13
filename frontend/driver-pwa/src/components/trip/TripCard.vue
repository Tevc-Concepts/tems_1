<template>
  <div
    class="card hover:shadow-md transition-all active:scale-98 cursor-pointer"
    @click="$emit('view', trip)"
  >
    <div class="p-4">
      <!-- Header -->
      <div class="flex items-start justify-between mb-3">
        <div class="flex-1">
          <div class="flex items-center space-x-2 mb-1">
            <component :is="tripIcon" class="w-5 h-5 text-primary-600" />
            <h3 class="font-semibold text-gray-900">{{ tripTitle }}</h3>
          </div>
          <p class="text-sm text-gray-600">{{ trip.route || trip.title }}</p>
        </div>
        <StatusBadge :status="trip.status" />
      </div>

      <!-- Route Info -->
      <div class="space-y-2 mb-4">
        <div class="flex items-center space-x-2 text-sm">
          <MapPin class="w-4 h-4 text-gray-400" />
          <span class="text-gray-700">{{ trip.start_location || 'Start Location' }}</span>
        </div>
        <div class="flex items-center space-x-2 text-sm">
          <Navigation class="w-4 h-4 text-gray-400" />
          <span class="text-gray-700">{{ trip.end_location || 'End Location' }}</span>
        </div>
      </div>

      <!-- Time & Vehicle Info -->
      <div class="grid grid-cols-2 gap-3 mb-4">
        <div class="flex items-center space-x-2">
          <Clock class="w-4 h-4 text-gray-400" />
          <div class="text-sm">
            <p class="text-gray-500">Departure</p>
            <p class="font-medium text-gray-900">{{ formatTime(trip.start_time) }}</p>
          </div>
        </div>
        <div v-if="trip.vehicle" class="flex items-center space-x-2">
          <Truck class="w-4 h-4 text-gray-400" />
          <div class="text-sm">
            <p class="text-gray-500">Vehicle</p>
            <p class="font-medium text-gray-900">{{ trip.vehicle }}</p>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center space-x-2 pt-3 border-t">
        <button
          v-if="canStart"
          @click.stop="$emit('start', trip)"
          class="flex-1 btn-primary text-sm py-2"
        >
          <Play class="w-4 h-4 mr-1" />
          Start Trip
        </button>
        <button
          v-else-if="canComplete"
          @click.stop="$emit('complete', trip)"
          class="flex-1 btn-primary text-sm py-2"
        >
          <CheckCircle class="w-4 h-4 mr-1" />
          Complete
        </button>
        <button
          v-else
          @click.stop="$emit('view', trip)"
          class="flex-1 btn-secondary text-sm py-2"
        >
          View Details
        </button>
        
        <button
          @click.stop="$emit('navigate', trip)"
          class="btn-secondary p-2"
        >
          <Navigation2 class="w-5 h-5" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { format, parseISO } from 'date-fns'
import { 
  MapPin, Navigation, Clock, Truck, Play, CheckCircle, 
  Navigation2, Package, Users 
} from 'lucide-vue-next'
import StatusBadge from '../common/StatusBadge.vue'

const props = defineProps({
  trip: {
    type: Object,
    required: true
  }
})

defineEmits(['view', 'start', 'complete', 'navigate'])

const tripIcon = computed(() => {
  if (props.trip.type === 'operation' || props.trip.operation_mode === 'Cargo') {
    return Package
  } else if (props.trip.operation_mode === 'Passenger') {
    return Users
  }
  return Navigation
})

const tripTitle = computed(() => {
  return props.trip.name || props.trip.title || 'Trip'
})

const canStart = computed(() => {
  return ['Draft', 'Assigned'].includes(props.trip.status)
})

const canComplete = computed(() => {
  return props.trip.status === 'Active'
})

function formatTime(dateTime) {
  if (!dateTime) return ''
  try {
    return format(parseISO(dateTime), 'HH:mm')
  } catch (e) {
    return dateTime
  }
}
</script>

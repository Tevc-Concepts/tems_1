<template>
  <div class="bg-white rounded-xl shadow-card p-4">
    <h2 class="text-lg font-bold text-gray-800 mb-4">Trip Timeline</h2>

    <div class="relative">
      <!-- Timeline line -->
      <div class="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-200"></div>

      <!-- Timeline items -->
      <div v-for="(event, index) in events" :key="index" class="relative pl-10 pb-6 last:pb-0">
        <!-- Timeline dot -->
        <div
          :class="[
            'absolute left-2.5 w-3 h-3 rounded-full',
            event.completed ? 'bg-success-600' : 'bg-gray-300',
          ]"
        ></div>

        <!-- Event content -->
        <div>
          <div class="flex items-center justify-between">
            <div class="font-medium text-gray-800">{{ event.title }}</div>
            <div class="text-xs text-gray-500">{{ event.time }}</div>
          </div>
          <div v-if="event.description" class="text-sm text-gray-600 mt-1">
            {{ event.description }}
          </div>
          <div v-if="event.location" class="text-xs text-gray-500 mt-1 flex items-center">
            <MapPin class="w-3 h-3 mr-1" />
            {{ event.location }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { MapPin } from 'lucide-vue-next'
import { format, parseISO } from 'date-fns'

const props = defineProps({
  trip: {
    type: Object,
    required: true,
  },
})

const events = computed(() => {
  const timeline = []

  if (props.trip.departure_time) {
    timeline.push({
      title: 'Departure',
      time: formatTime(props.trip.departure_time),
      location: props.trip.origin,
      completed: true,
    })
  }

  if (props.trip.checkpoints) {
    props.trip.checkpoints.forEach((checkpoint) => {
      timeline.push({
        title: checkpoint.name,
        time: checkpoint.time ? formatTime(checkpoint.time) : 'Pending',
        location: checkpoint.location,
        completed: checkpoint.completed,
      })
    })
  }

  if (props.trip.arrival_time) {
    timeline.push({
      title: 'Arrival',
      time: formatTime(props.trip.arrival_time),
      location: props.trip.destination,
      completed: props.trip.status === 'Completed',
    })
  }

  return timeline
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

<template>
  <span 
    class="badge"
    :class="badgeClass"
  >
    <component v-if="icon" :is="icon" class="w-3 h-3 mr-1" />
    {{ label }}
  </span>
</template>

<script setup>
import { computed } from 'vue'
import { 
  CheckCircle, 
  Clock, 
  XCircle, 
  AlertCircle,
  PlayCircle 
} from 'lucide-vue-next'

const props = defineProps({
  status: {
    type: String,
    required: true
  },
  label: {
    type: String,
    default: ''
  }
})

const statusConfig = {
  'Active': { class: 'badge-success', icon: PlayCircle },
  'Completed': { class: 'badge-success', icon: CheckCircle },
  'Assigned': { class: 'badge-info', icon: Clock },
  'Planned': { class: 'badge-info', icon: Clock },
  'Cancelled': { class: 'badge-danger', icon: XCircle },
  'Open': { class: 'badge-warning', icon: AlertCircle },
  'In Progress': { class: 'badge-warning', icon: Clock },
  'Closed': { class: 'badge-success', icon: CheckCircle }
}

const badgeClass = computed(() => 
  statusConfig[props.status]?.class || 'badge-info'
)

const icon = computed(() => 
  statusConfig[props.status]?.icon || null
)
</script>
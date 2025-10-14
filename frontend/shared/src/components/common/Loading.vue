<template>
  <div v-if="visible" :class="containerClasses">
    <!-- Spinner Loading -->
    <div v-if="type === 'spinner'" :class="spinnerClasses">
      <svg class="animate-spin" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>

    <!-- Dots Loading -->
    <div v-else-if="type === 'dots'" class="flex space-x-2">
      <div
        v-for="i in 3"
        :key="i"
        :class="[
          'rounded-full animate-bounce',
          dotSizeClasses,
          colorClasses
        ]"
        :style="{ animationDelay: `${i * 0.15}s` }"
      ></div>
    </div>

    <!-- Pulse Loading -->
    <div v-else-if="type === 'pulse'" :class="pulseClasses">
      <div class="w-full h-full rounded-full animate-ping"></div>
    </div>

    <!-- Bar Loading (Skeleton) -->
    <div v-else-if="type === 'bar'" class="space-y-3 w-full">
      <div
        v-for="i in bars"
        :key="i"
        :class="[
          'animate-pulse rounded',
          barClasses
        ]"
        :style="{ width: getBarWidth(i) }"
      ></div>
    </div>

    <!-- Custom Skeleton -->
    <div v-else-if="type === 'skeleton'" class="w-full">
      <slot name="skeleton">
        <div class="animate-pulse space-y-4">
          <!-- Avatar -->
          <div class="flex items-center space-x-4">
            <div class="rounded-full bg-gray-300 h-12 w-12"></div>
            <div class="flex-1 space-y-2">
              <div class="h-4 bg-gray-300 rounded w-3/4"></div>
              <div class="h-4 bg-gray-300 rounded w-1/2"></div>
            </div>
          </div>
          <!-- Content -->
          <div class="space-y-2">
            <div class="h-4 bg-gray-300 rounded"></div>
            <div class="h-4 bg-gray-300 rounded w-5/6"></div>
            <div class="h-4 bg-gray-300 rounded w-4/6"></div>
          </div>
        </div>
      </slot>
    </div>

    <!-- Loading Text -->
    <p v-if="text" :class="textClasses">{{ text }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: true
  },
  type: {
    type: String,
    default: 'spinner',
    validator: (value) => ['spinner', 'dots', 'pulse', 'bar', 'skeleton'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg', 'xl'].includes(value)
  },
  color: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'white', 'gray'].includes(value)
  },
  text: {
    type: String,
    default: ''
  },
  fullscreen: {
    type: Boolean,
    default: false
  },
  overlay: {
    type: Boolean,
    default: false
  },
  bars: {
    type: Number,
    default: 3
  }
})

// Computed classes
const containerClasses = computed(() => {
  const classes = ['flex flex-col items-center justify-center']

  if (props.fullscreen) {
    classes.push('fixed inset-0 z-50')
  }

  if (props.overlay) {
    classes.push('bg-black bg-opacity-50')
  }

  return classes.join(' ')
})

const spinnerClasses = computed(() => {
  const sizeMap = {
    sm: 'w-6 h-6',
    md: 'w-10 h-10',
    lg: 'w-16 h-16',
    xl: 'w-24 h-24'
  }

  return [sizeMap[props.size], colorClasses.value].join(' ')
})

const dotSizeClasses = computed(() => {
  const sizeMap = {
    sm: 'w-2 h-2',
    md: 'w-3 h-3',
    lg: 'w-4 h-4',
    xl: 'w-6 h-6'
  }
  return sizeMap[props.size]
})

const pulseClasses = computed(() => {
  const sizeMap = {
    sm: 'w-6 h-6',
    md: 'w-10 h-10',
    lg: 'w-16 h-16',
    xl: 'w-24 h-24'
  }

  return [sizeMap[props.size], colorClasses.value, 'relative'].join(' ')
})

const barClasses = computed(() => {
  const heightMap = {
    sm: 'h-2',
    md: 'h-3',
    lg: 'h-4',
    xl: 'h-6'
  }

  return [heightMap[props.size], 'bg-gray-300'].join(' ')
})

const colorClasses = computed(() => {
  const colorMap = {
    primary: 'text-neon-green',
    secondary: 'text-charcoal',
    white: 'text-white',
    gray: 'text-gray-500'
  }
  return colorMap[props.color]
})

const textClasses = computed(() => {
  const sizeMap = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg',
    xl: 'text-xl'
  }

  const classes = [
    sizeMap[props.size],
    'mt-4 font-medium',
    props.overlay ? 'text-white' : 'text-gray-700'
  ]

  return classes.join(' ')
})

// Methods
function getBarWidth(index) {
  const widths = ['100%', '85%', '70%', '95%', '80%']
  return widths[index % widths.length]
}
</script>

<style scoped>
/* Additional animation styles */
@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-25%);
  }
}
</style>

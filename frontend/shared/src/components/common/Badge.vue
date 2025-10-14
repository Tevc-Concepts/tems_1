<template>
  <span :class="badgeClasses">
    <!-- Icon (left) -->
    <component v-if="icon && !iconRight" :is="icon" class="w-3 h-3" />

    <!-- Dot indicator -->
    <span v-if="dot" :class="dotClasses"></span>

    <!-- Content -->
    <span v-if="$slots.default || label">
      <slot>{{ label }}</slot>
    </span>

    <!-- Icon (right) -->
    <component v-if="icon && iconRight" :is="icon" class="w-3 h-3" />

    <!-- Close button -->
    <button
      v-if="closable"
      type="button"
      @click.stop="handleClose"
      class="ml-1 -mr-0.5 flex-shrink-0 hover:opacity-70 transition-opacity"
    >
      <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
      </svg>
    </button>
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: {
    type: [String, Number],
    default: ''
  },
  variant: {
    type: String,
    default: 'default',
    validator: (value) => [
      'default', 'primary', 'secondary', 'success', 'danger', 'warning', 'info'
    ].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  rounded: {
    type: String,
    default: 'full',
    validator: (value) => ['sm', 'md', 'lg', 'full'].includes(value)
  },
  dot: {
    type: Boolean,
    default: false
  },
  icon: {
    type: [Object, String],
    default: null
  },
  iconRight: {
    type: Boolean,
    default: false
  },
  closable: {
    type: Boolean,
    default: false
  },
  outline: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])

// Computed classes
const badgeClasses = computed(() => {
  const classes = [
    'inline-flex items-center justify-center font-medium',
    'transition-all duration-200'
  ]

  // Size classes
  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs gap-1',
    md: 'px-2.5 py-0.5 text-xs gap-1',
    lg: 'px-3 py-1 text-sm gap-1.5'
  }
  classes.push(sizeClasses[props.size])

  // Rounded classes
  const roundedClasses = {
    sm: 'rounded',
    md: 'rounded-md',
    lg: 'rounded-lg',
    full: 'rounded-full'
  }
  classes.push(roundedClasses[props.rounded])

  // Variant classes
  if (props.outline) {
    const outlineVariants = {
      default: 'border border-gray-300 text-gray-700 hover:bg-gray-50',
      primary: 'border border-neon-green text-neon-green hover:bg-neon-green hover:text-charcoal',
      secondary: 'border border-charcoal text-charcoal hover:bg-charcoal hover:text-white',
      success: 'border border-green-500 text-green-700 hover:bg-green-50',
      danger: 'border border-red-500 text-red-700 hover:bg-red-50',
      warning: 'border border-yellow-500 text-yellow-700 hover:bg-yellow-50',
      info: 'border border-blue-500 text-blue-700 hover:bg-blue-50'
    }
    classes.push(outlineVariants[props.variant])
  } else {
    const variantClasses = {
      default: 'bg-gray-100 text-gray-800',
      primary: 'bg-neon-green text-charcoal',
      secondary: 'bg-charcoal text-white',
      success: 'bg-green-100 text-green-800',
      danger: 'bg-red-100 text-red-800',
      warning: 'bg-yellow-100 text-yellow-800',
      info: 'bg-blue-100 text-blue-800'
    }
    classes.push(variantClasses[props.variant])
  }

  return classes.join(' ')
})

const dotClasses = computed(() => {
  const classes = ['w-2 h-2 rounded-full']

  const dotColors = {
    default: 'bg-gray-400',
    primary: 'bg-neon-green-700',
    secondary: 'bg-white',
    success: 'bg-green-500',
    danger: 'bg-red-500',
    warning: 'bg-yellow-500',
    info: 'bg-blue-500'
  }
  classes.push(dotColors[props.variant])

  // Pulse animation for certain variants
  if (['success', 'danger', 'warning'].includes(props.variant)) {
    classes.push('animate-pulse')
  }

  return classes.join(' ')
})

// Methods
function handleClose() {
  emit('close')
}
</script>

<style scoped>
/* Additional custom styles if needed */
</style>

<template>
  <component
    :is="tag"
    :type="tag === 'button' ? type : undefined"
    :disabled="disabled || loading"
    :class="buttonClasses"
    @click="handleClick"
  >
    <!-- Loading Spinner -->
    <svg
      v-if="loading"
      class="animate-spin -ml-1 mr-2 h-5 w-5"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    </svg>

    <!-- Icon (left) -->
    <component v-if="icon && !iconRight" :is="icon" :class="iconClasses" />

    <!-- Content -->
    <span v-if="$slots.default || label">
      <slot>{{ label }}</slot>
    </span>

    <!-- Icon (right) -->
    <component v-if="icon && iconRight" :is="icon" :class="iconClasses" />
  </component>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: {
    type: String,
    default: ''
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'danger', 'success', 'outline', 'ghost', 'link'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(value)
  },
  type: {
    type: String,
    default: 'button',
    validator: (value) => ['button', 'submit', 'reset'].includes(value)
  },
  tag: {
    type: String,
    default: 'button',
    validator: (value) => ['button', 'a'].includes(value)
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  block: {
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
  rounded: {
    type: String,
    default: 'lg',
    validator: (value) => ['none', 'sm', 'md', 'lg', 'full'].includes(value)
  }
})

const emit = defineEmits(['click'])

// Computed classes
const buttonClasses = computed(() => {
  const classes = [
    'inline-flex items-center justify-center font-medium transition-all duration-200',
    'focus:outline-none focus:ring-2 focus:ring-offset-2',
    'disabled:opacity-50 disabled:cursor-not-allowed'
  ]

  // Size classes
  const sizeClasses = {
    xs: 'px-2.5 py-1.5 text-xs',
    sm: 'px-3 py-2 text-sm',
    md: 'px-4 py-2.5 text-sm',
    lg: 'px-5 py-3 text-base',
    xl: 'px-6 py-3.5 text-base'
  }
  classes.push(sizeClasses[props.size])

  // Rounded classes
  const roundedClasses = {
    none: 'rounded-none',
    sm: 'rounded-sm',
    md: 'rounded-md',
    lg: 'rounded-lg',
    full: 'rounded-full'
  }
  classes.push(roundedClasses[props.rounded])

  // Variant classes
  const variantClasses = {
    primary: 'bg-neon-green text-charcoal hover:bg-neon-green-600 focus:ring-neon-green shadow-sm',
    secondary: 'bg-charcoal text-white hover:bg-charcoal-light focus:ring-charcoal shadow-sm',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500 shadow-sm',
    success: 'bg-green-600 text-white hover:bg-green-700 focus:ring-green-500 shadow-sm',
    outline: 'border-2 border-neon-green text-neon-green hover:bg-neon-green hover:text-charcoal focus:ring-neon-green',
    ghost: 'text-gray-700 hover:bg-gray-100 focus:ring-gray-300',
    link: 'text-neon-green hover:text-neon-green-600 underline-offset-4 hover:underline focus:ring-neon-green'
  }
  classes.push(variantClasses[props.variant])

  // Block
  if (props.block) {
    classes.push('w-full')
  }

  return classes.join(' ')
})

const iconClasses = computed(() => {
  const classes = ['flex-shrink-0']
  
  const iconSizes = {
    xs: 'w-3 h-3',
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-5 h-5',
    xl: 'w-6 h-6'
  }
  classes.push(iconSizes[props.size])

  // Add margin if there's text
  if (props.label || props.$slots.default) {
    if (props.iconRight) {
      classes.push('ml-2')
    } else {
      classes.push('mr-2')
    }
  }

  return classes.join(' ')
})

// Methods
function handleClick(event) {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>

<style scoped>
/* Additional custom styles if needed */
</style>

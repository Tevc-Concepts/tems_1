<template>
  <div :class="cardClasses">
    <!-- Header -->
    <div
      v-if="title || $slots.header || $slots.actions"
      :class="[
        'flex items-center justify-between',
        headerClass || 'px-6 py-4 border-b border-gray-200'
      ]"
    >
      <slot name="header">
        <div class="flex items-center space-x-3">
          <component v-if="icon" :is="icon" class="w-6 h-6 text-gray-600" />
          <div>
            <h3 class="text-lg font-semibold text-gray-900">{{ title }}</h3>
            <p v-if="subtitle" class="text-sm text-gray-500">{{ subtitle }}</p>
          </div>
        </div>
      </slot>
      <div v-if="$slots.actions" class="flex items-center space-x-2">
        <slot name="actions"></slot>
      </div>
    </div>

    <!-- Body -->
    <div :class="bodyClass || 'px-6 py-4'">
      <slot></slot>
    </div>

    <!-- Footer -->
    <div
      v-if="$slots.footer"
      :class="footerClass || 'px-6 py-4 border-t border-gray-200 bg-gray-50'"
    >
      <slot name="footer"></slot>
    </div>

    <!-- Loading Overlay -->
    <div
      v-if="loading"
      class="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center rounded-lg"
    >
      <Loading type="spinner" size="lg" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import Loading from './Loading.vue'

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  subtitle: {
    type: String,
    default: ''
  },
  icon: {
    type: [Object, String],
    default: null
  },
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'bordered', 'elevated', 'flat'].includes(value)
  },
  hoverable: {
    type: Boolean,
    default: false
  },
  clickable: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  padding: {
    type: Boolean,
    default: true
  },
  rounded: {
    type: String,
    default: 'lg',
    validator: (value) => ['none', 'sm', 'md', 'lg', 'xl'].includes(value)
  },
  headerClass: {
    type: String,
    default: ''
  },
  bodyClass: {
    type: String,
    default: ''
  },
  footerClass: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['click'])

// Computed classes
const cardClasses = computed(() => {
  const classes = [
    'relative bg-white transition-all duration-200'
  ]

  // Rounded
  const roundedClasses = {
    none: 'rounded-none',
    sm: 'rounded-sm',
    md: 'rounded-md',
    lg: 'rounded-lg',
    xl: 'rounded-xl'
  }
  classes.push(roundedClasses[props.rounded])

  // Variant
  const variantClasses = {
    default: 'border border-gray-200',
    bordered: 'border-2 border-gray-300',
    elevated: 'shadow-lg',
    flat: ''
  }
  classes.push(variantClasses[props.variant])

  // Hoverable
  if (props.hoverable) {
    classes.push('hover:shadow-xl hover:scale-[1.02]')
  }

  // Clickable
  if (props.clickable) {
    classes.push('cursor-pointer hover:shadow-md')
  }

  // Loading
  if (props.loading) {
    classes.push('overflow-hidden')
  }

  return classes.join(' ')
})

// Methods
function handleClick(event) {
  if (props.clickable) {
    emit('click', event)
  }
}
</script>

<style scoped>
/* Additional custom styles if needed */
</style>

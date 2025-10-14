<template>
  <teleport to="body">
    <transition
      enter-active-class="transition ease-out duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="isOpen"
        class="fixed inset-0 z-50 overflow-y-auto"
        @click.self="handleBackdropClick"
      >
        <!-- Backdrop -->
        <div class="fixed inset-0 bg-black bg-opacity-50 transition-opacity"></div>

        <!-- Modal Container -->
        <div class="flex min-h-full items-center justify-center p-4">
          <transition
            enter-active-class="transition ease-out duration-300"
            enter-from-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enter-to-class="opacity-100 translate-y-0 sm:scale-100"
            leave-active-class="transition ease-in duration-200"
            leave-from-class="opacity-100 translate-y-0 sm:scale-100"
            leave-to-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          >
            <div
              v-if="isOpen"
              :class="modalClasses"
              @click.stop
            >
              <!-- Header -->
              <div v-if="title || $slots.header || showClose" class="flex items-start justify-between px-6 py-4 border-b border-gray-200">
                <slot name="header">
                  <h3 class="text-lg font-semibold text-gray-900">{{ title }}</h3>
                </slot>
                <button
                  v-if="showClose"
                  type="button"
                  @click="handleClose"
                  class="text-gray-400 hover:text-gray-600 transition-colors"
                >
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                  </svg>
                </button>
              </div>

              <!-- Body -->
              <div class="px-6 py-4">
                <slot></slot>
              </div>

              <!-- Footer -->
              <div v-if="$slots.footer || showFooter" class="flex items-center justify-end space-x-3 px-6 py-4 border-t border-gray-200 bg-gray-50">
                <slot name="footer">
                  <Button
                    v-if="showCancel"
                    variant="ghost"
                    @click="handleCancel"
                  >
                    {{ cancelText }}
                  </Button>
                  <Button
                    v-if="showConfirm"
                    :variant="confirmVariant"
                    :loading="loading"
                    @click="handleConfirm"
                  >
                    {{ confirmText }}
                  </Button>
                </slot>
              </div>
            </div>
          </transition>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup>
import { computed, watch, onMounted, onUnmounted } from 'vue'
import Button from './Button.vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg', 'xl', 'full'].includes(value)
  },
  showClose: {
    type: Boolean,
    default: true
  },
  showFooter: {
    type: Boolean,
    default: false
  },
  showCancel: {
    type: Boolean,
    default: true
  },
  showConfirm: {
    type: Boolean,
    default: true
  },
  cancelText: {
    type: String,
    default: 'Cancel'
  },
  confirmText: {
    type: String,
    default: 'Confirm'
  },
  confirmVariant: {
    type: String,
    default: 'primary'
  },
  closeOnBackdrop: {
    type: Boolean,
    default: true
  },
  closeOnEscape: {
    type: Boolean,
    default: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:isOpen', 'close', 'cancel', 'confirm'])

// Computed
const modalClasses = computed(() => {
  const classes = [
    'relative bg-white rounded-lg shadow-xl transform transition-all',
    'w-full'
  ]

  const sizeClasses = {
    sm: 'max-w-md',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl',
    full: 'max-w-7xl mx-4'
  }
  classes.push(sizeClasses[props.size])

  return classes.join(' ')
})

// Methods
function handleClose() {
  emit('update:isOpen', false)
  emit('close')
}

function handleCancel() {
  emit('cancel')
  if (!props.loading) {
    handleClose()
  }
}

function handleConfirm() {
  emit('confirm')
}

function handleBackdropClick() {
  if (props.closeOnBackdrop && !props.loading) {
    handleClose()
  }
}

function handleEscapeKey(event) {
  if (event.key === 'Escape' && props.closeOnEscape && props.isOpen && !props.loading) {
    handleClose()
  }
}

// Watch for modal open/close to manage body scroll
watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})

// Lifecycle
onMounted(() => {
  if (props.closeOnEscape) {
    document.addEventListener('keydown', handleEscapeKey)
  }
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscapeKey)
  document.body.style.overflow = ''
})
</script>

<style scoped>
/* Additional custom styles if needed */
</style>

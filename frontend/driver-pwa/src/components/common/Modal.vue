<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="modelValue"
        class="fixed inset-0 z-50 flex items-end sm:items-center justify-center"
        @click.self="closeOnBackdrop && close()"
      >
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="closeOnBackdrop && close()"></div>
        
        <!-- Modal Content -->
        <div
          class="relative bg-white rounded-t-2xl sm:rounded-2xl shadow-xl w-full max-w-lg mx-auto transform transition-all"
          :class="[
            size === 'sm' ? 'max-w-sm' : '',
            size === 'lg' ? 'max-w-2xl' : '',
            size === 'xl' ? 'max-w-4xl' : '',
            fullHeight ? 'h-[90vh] sm:h-auto sm:max-h-[90vh]' : ''
          ]"
        >
          <!-- Header -->
          <div v-if="$slots.header || title" class="flex items-center justify-between p-4 border-b">
            <slot name="header">
              <h3 class="text-lg font-semibold text-gray-900">{{ title }}</h3>
            </slot>
            <button
              v-if="showClose"
              @click="close"
              class="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-gray-100 transition-colors"
            >
              <X class="w-5 h-5 text-gray-500" />
            </button>
          </div>

          <!-- Body -->
          <div
            class="p-4 overflow-y-auto"
            :class="fullHeight ? 'max-h-[calc(90vh-8rem)]' : ''"
          >
            <slot></slot>
          </div>

          <!-- Footer -->
          <div v-if="$slots.footer" class="p-4 border-t bg-gray-50 rounded-b-2xl">
            <slot name="footer"></slot>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { X } from 'lucide-vue-next'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'md', // sm, md, lg, xl
    validator: (value) => ['sm', 'md', 'lg', 'xl'].includes(value)
  },
  showClose: {
    type: Boolean,
    default: true
  },
  closeOnBackdrop: {
    type: Boolean,
    default: true
  },
  fullHeight: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'close'])

function close() {
  emit('update:modelValue', false)
  emit('close')
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active > div:last-child,
.modal-leave-active > div:last-child {
  transition: transform 0.3s ease;
}

.modal-enter-from > div:last-child {
  transform: translateY(100%) scale(0.9);
}

.modal-leave-to > div:last-child {
  transform: translateY(100%) scale(0.9);
}

@media (min-width: 640px) {
  .modal-enter-from > div:last-child {
    transform: translateY(0) scale(0.9);
  }
  
  .modal-leave-to > div:last-child {
    transform: translateY(0) scale(0.9);
  }
}
</style>

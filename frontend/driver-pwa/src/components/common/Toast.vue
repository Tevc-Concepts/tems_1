<template>
  <Teleport to="body">
    <Transition name="toast">
      <div
        v-if="visible"
        class="fixed top-4 right-4 z-50 max-w-sm w-full sm:w-96"
      >
        <div
          class="bg-white rounded-xl shadow-lg border overflow-hidden"
          :class="[
            type === 'success' ? 'border-l-4 border-l-green-500' : '',
            type === 'error' ? 'border-l-4 border-l-red-500' : '',
            type === 'warning' ? 'border-l-4 border-l-amber-500' : '',
            type === 'info' ? 'border-l-4 border-l-blue-500' : ''
          ]"
        >
          <div class="p-4 flex items-start space-x-3">
            <div
              class="flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center"
              :class="iconBgClass"
            >
              <component :is="icon" class="w-5 h-5" :class="iconColorClass" />
            </div>
            
            <div class="flex-1 min-w-0">
              <p class="text-sm font-semibold text-gray-900">{{ title }}</p>
              <p v-if="message" class="text-sm text-gray-600 mt-1">{{ message }}</p>
            </div>

            <button
              @click="close"
              class="flex-shrink-0 w-8 h-8 flex items-center justify-center rounded-lg hover:bg-gray-100 transition-colors"
            >
              <X class="w-4 h-4 text-gray-500" />
            </button>
          </div>

          <!-- Progress bar -->
          <div
            v-if="duration > 0"
            class="h-1 bg-gray-200"
          >
            <div
              class="h-full transition-all ease-linear"
              :class="progressBarClass"
              :style="{ width: progress + '%' }"
            ></div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { CheckCircle, XCircle, AlertTriangle, Info, X } from 'lucide-vue-next'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  type: {
    type: String,
    default: 'info', // success, error, warning, info
    validator: (value) => ['success', 'error', 'warning', 'info'].includes(value)
  },
  title: {
    type: String,
    required: true
  },
  message: {
    type: String,
    default: ''
  },
  duration: {
    type: Number,
    default: 5000 // milliseconds, 0 = don't auto-close
  }
})

const emit = defineEmits(['update:modelValue', 'close'])

const visible = ref(props.modelValue)
const progress = ref(100)
let progressInterval = null

const icon = computed(() => {
  switch (props.type) {
    case 'success': return CheckCircle
    case 'error': return XCircle
    case 'warning': return AlertTriangle
    default: return Info
  }
})

const iconBgClass = computed(() => {
  switch (props.type) {
    case 'success': return 'bg-green-100'
    case 'error': return 'bg-red-100'
    case 'warning': return 'bg-amber-100'
    default: return 'bg-blue-100'
  }
})

const iconColorClass = computed(() => {
  switch (props.type) {
    case 'success': return 'text-green-600'
    case 'error': return 'text-red-600'
    case 'warning': return 'text-amber-600'
    default: return 'text-blue-600'
  }
})

const progressBarClass = computed(() => {
  switch (props.type) {
    case 'success': return 'bg-green-500'
    case 'error': return 'bg-red-500'
    case 'warning': return 'bg-amber-500'
    default: return 'bg-blue-500'
  }
})

watch(() => props.modelValue, (newVal) => {
  visible.value = newVal
  if (newVal && props.duration > 0) {
    startProgress()
  }
})

function close() {
  visible.value = false
  emit('update:modelValue', false)
  emit('close')
  clearInterval(progressInterval)
}

function startProgress() {
  progress.value = 100
  const step = 100 / (props.duration / 100)
  
  progressInterval = setInterval(() => {
    progress.value -= step
    if (progress.value <= 0) {
      clearInterval(progressInterval)
      close()
    }
  }, 100)
}

onMounted(() => {
  if (props.modelValue && props.duration > 0) {
    startProgress()
  }
})
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  transform: translateX(100%);
  opacity: 0;
}

.toast-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style>

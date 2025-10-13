<template>
  <Modal :model-value="modelValue" @update:model-value="emit('update:modelValue', $event)" title="Take Photo" size="lg" full-height>
    <div class="space-y-4">
      <!-- Video Preview -->
      <div class="relative bg-black rounded-lg overflow-hidden" style="aspect-ratio: 4/3;">
        <video
          ref="videoElement"
          autoplay
          playsinline
          class="w-full h-full object-cover"
        ></video>
        
        <div v-if="!isActive" class="absolute inset-0 flex items-center justify-center bg-black/50">
          <p class="text-white">Initializing camera...</p>
        </div>
      </div>

      <!-- Controls -->
      <div class="flex items-center justify-center space-x-4">
        <button
          type="button"
          @click="switchCamera"
          class="btn-secondary p-3"
          :disabled="!isActive"
        >
          <RefreshCw class="w-6 h-6" />
        </button>

        <button
          type="button"
          @click="capture"
          class="w-16 h-16 bg-primary-600 hover:bg-primary-700 rounded-full flex items-center justify-center shadow-lg active:scale-95 transition-transform"
          :disabled="!isActive"
        >
          <Camera class="w-8 h-8 text-white" />
        </button>

        <button
          type="button"
          @click="close"
          class="btn-secondary p-3"
        >
          <X class="w-6 h-6" />
        </button>
      </div>

      <p v-if="error" class="text-sm text-red-600 text-center">{{ error }}</p>
    </div>
  </Modal>
</template>

<script setup>
import { ref, watch, onUnmounted } from 'vue'
import { Camera, RefreshCw, X } from 'lucide-vue-next'
import { useCamera } from '@/composables/useMedia'
import Modal from './Modal.vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'capture'])

const videoElement = ref(null)
const { isActive, error, startCamera, stopCamera, capturePhoto, switchCamera: toggleCamera } = useCamera()

watch(() => props.modelValue, async (newVal) => {
  if (newVal && videoElement.value) {
    try {
      await startCamera(videoElement.value)
    } catch (err) {
      console.error('Failed to start camera:', err)
    }
  } else if (!newVal) {
    stopCamera()
  }
})

async function switchCamera() {
  await toggleCamera()
}

async function capture() {
  try {
    const photo = await capturePhoto()
    emit('capture', photo)
    close()
  } catch (err) {
    console.error('Failed to capture photo:', err)
  }
}

function close() {
  stopCamera()
  emit('update:modelValue', false)
}

onUnmounted(() => {
  stopCamera()
})
</script>

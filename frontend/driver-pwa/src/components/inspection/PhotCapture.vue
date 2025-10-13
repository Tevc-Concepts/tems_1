<template>
  <div class="space-y-4">
    <button
      type="button"
      @click="capturePhoto"
      class="w-full px-4 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition flex items-center justify-center"
    >
      <Camera class="w-5 h-5 mr-2" />
      {{ photos.length ? 'Take Another Photo' : 'Take Photo' }}
    </button>

    <!-- Photo Grid -->
    <div v-if="photos.length" class="grid grid-cols-2 gap-3">
      <div v-for="(photo, index) in photos" :key="index" class="relative">
        <img :src="photo.dataUrl" alt="Captured photo" class="w-full h-32 object-cover rounded-lg" />
        <button
          type="button"
          @click="removePhoto(index)"
          class="absolute top-1 right-1 p-1 bg-danger-600 text-white rounded-full hover:bg-danger-700"
        >
          <X class="w-4 h-4" />
        </button>
      </div>
    </div>

    <CameraModal
      v-if="showCamera"
      @close="showCamera = false"
      @capture="handleCapture"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Camera, X } from 'lucide-vue-next'
import CameraModal from '@/components/common/CameraModal.vue'

const emit = defineEmits(['update:photos'])

defineProps({
  photos: {
    type: Array,
    default: () => [],
  },
})

const showCamera = ref(false)
const photos = ref([])

const capturePhoto = () => {
  showCamera.value = true
}

const handleCapture = (photo) => {
  photos.value.push(photo)
  emit('update:photos', photos.value)
  showCamera.value = false
}

const removePhoto = (index) => {
  photos.value.splice(index, 1)
  emit('update:photos', photos.value)
}
</script>

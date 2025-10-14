<template>
  <form @submit.prevent="submitForm" class="space-y-4">
    <div class="bg-white rounded-xl shadow-card p-4">
      <!-- Incident Type -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-2">Incident Type</label>
        <select
          v-model="form.incident_type"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          required
        >
          <option value="">Select Type</option>
          <option value="Accident">Accident</option>
          <option value="Breakdown">Breakdown</option>
          <option value="Medical">Medical Emergency</option>
          <option value="Security">Security Issue</option>
          <option value="Other">Other</option>
        </select>
      </div>

      <!-- Description -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
        <textarea
          v-model="form.description"
          rows="4"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          placeholder="Describe what happened..."
          required
        ></textarea>
      </div>

      <!-- Location -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-2">Location</label>
        <div class="flex space-x-2">
          <input
            v-model="form.location"
            type="text"
            class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            placeholder="Location details"
            required
          />
          <button
            type="button"
            @click="captureLocation"
            class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            <MapPin class="w-5 h-5" />
          </button>
        </div>
      </div>

      <!-- Photo -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-2">Photos</label>
        <button
          type="button"
          @click="takePhoto"
          class="w-full px-4 py-2 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary-500 flex items-center justify-center"
        >
          <Camera class="w-5 h-5 mr-2" />
          Take Photo
        </button>
        <div v-if="form.photo" class="mt-2">
          <img :src="form.photo" alt="Incident photo" class="w-full h-40 object-cover rounded-lg" />
        </div>
      </div>

      <!-- Submit -->
      <button
        type="submit"
        class="w-full py-3 bg-danger-600 text-white rounded-lg font-medium hover:bg-danger-700 transition"
      >
        Submit Report
      </button>
    </div>

    <CameraModal
      v-if="showCamera"
      @close="showCamera = false"
      @capture="handlePhotoCapture"
    />
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { MapPin, Camera } from 'lucide-vue-next'
import { useGeolocation } from '@shared'
import CameraModal from '@/components/common/CameraModal.vue'

const emit = defineEmits(['submit'])

const { getCurrentPosition } = useGeolocation()
const showCamera = ref(false)

const form = ref({
  incident_type: '',
  description: '',
  location: '',
  photo: null,
  coordinates: null,
})

const captureLocation = async () => {
  try {
    const position = await getCurrentPosition()
    form.value.coordinates = {
      latitude: position.coords.latitude,
      longitude: position.coords.longitude,
    }
    form.value.location = `${position.coords.latitude.toFixed(6)}, ${position.coords.longitude.toFixed(6)}`
  } catch (error) {
    console.error('Failed to get location:', error)
  }
}

const takePhoto = () => {
  showCamera.value = true
}

const handlePhotoCapture = (photo) => {
  form.value.photo = photo.dataUrl
  showCamera.value = false
}

const submitForm = () => {
  emit('submit', form.value)
}
</script>

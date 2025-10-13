<template>
  <form @submit.prevent="submitForm" class="bg-white rounded-xl shadow-card p-4 space-y-4">
    <h2 class="text-lg font-bold text-gray-800">Vehicle Spot Check</h2>

    <!-- Checklist Items -->
    <div class="space-y-2">
      <div v-for="item in checklistItems" :key="item.id" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
        <span class="text-sm font-medium">{{ item.label }}</span>
        <input
          type="checkbox"
          v-model="form.checklist[item.id]"
          class="w-5 h-5 text-primary-600 rounded focus:ring-2 focus:ring-primary-500"
        />
      </div>
    </div>

    <!-- Notes -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">Additional Notes</label>
      <textarea
        v-model="form.notes"
        rows="3"
        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        placeholder="Any issues or observations..."
      ></textarea>
    </div>

    <!-- Photos -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">Photos</label>
      <button
        type="button"
        @click="takePhoto"
        class="w-full px-4 py-2 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary-500 flex items-center justify-center"
      >
        <Camera class="w-5 h-5 mr-2" />
        Take Photo
      </button>
      <div v-if="form.photos.length" class="mt-2 grid grid-cols-3 gap-2">
        <img
          v-for="(photo, index) in form.photos"
          :key="index"
          :src="photo"
          alt="Inspection photo"
          class="w-full h-20 object-cover rounded-lg"
        />
      </div>
    </div>

    <!-- Submit -->
    <button
      type="submit"
      class="w-full py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition"
    >
      Submit Inspection
    </button>

    <CameraModal
      v-if="showCamera"
      @close="showCamera = false"
      @capture="handlePhotoCapture"
    />
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { Camera } from 'lucide-vue-next'
import CameraModal from '@/components/common/CameraModal.vue'

const emit = defineEmits(['submit'])

const showCamera = ref(false)

const checklistItems = [
  { id: 'tires', label: 'Tire Condition' },
  { id: 'lights', label: 'Lights Functional' },
  { id: 'brakes', label: 'Brakes Working' },
  { id: 'fluids', label: 'Fluid Levels OK' },
  { id: 'mirrors', label: 'Mirrors Adjusted' },
  { id: 'wipers', label: 'Wipers Working' },
  { id: 'horn', label: 'Horn Functional' },
  { id: 'seatbelts', label: 'Seatbelts OK' },
]

const form = ref({
  checklist: {},
  notes: '',
  photos: [],
})

const takePhoto = () => {
  showCamera.value = true
}

const handlePhotoCapture = (photo) => {
  form.value.photos.push(photo.dataUrl)
  showCamera.value = false
}

const submitForm = () => {
  emit('submit', form.value)
}
</script>

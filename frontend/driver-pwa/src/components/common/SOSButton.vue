<template>
  <Teleport to="body">
    <!-- SOS Floating Button -->
    <button
      v-if="!showModal"
      @click="openModal"
      class="fixed bottom-24 right-4 z-40 w-16 h-16 bg-red-600 hover:bg-red-700 rounded-full shadow-lg flex items-center justify-center animate-pulse active:scale-95 transition-transform"
      :class="{ 'opacity-50': sending }"
      :disabled="sending"
    >
      <AlertCircle class="w-8 h-8 text-white" />
    </button>

    <!-- SOS Modal -->
    <Modal v-model="showModal" title="Emergency SOS" size="md" :close-on-backdrop="false">
      <div class="space-y-4">
        <!-- Warning -->
        <div class="p-4 bg-red-50 border border-red-200 rounded-lg">
          <div class="flex items-start space-x-3">
            <AlertTriangle class="w-6 h-6 text-red-600 flex-shrink-0 mt-0.5" />
            <div>
              <p class="font-semibold text-red-900">Emergency Alert</p>
              <p class="text-sm text-red-700 mt-1">
                This will send an immediate alert to the operations control room with your current location.
              </p>
            </div>
          </div>
        </div>

        <!-- Current Location -->
        <div v-if="locationData" class="p-4 bg-gray-50 rounded-lg">
          <div class="flex items-start space-x-3">
            <MapPin class="w-5 h-5 text-gray-600 flex-shrink-0 mt-0.5" />
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">Current Location</p>
              <p class="text-xs text-gray-600 mt-1">
                {{ formatCoordinates(locationData.latitude, locationData.longitude) }}
              </p>
              <p class="text-xs text-gray-500 mt-1">
                Accuracy: ±{{ Math.round(locationData.accuracy) }}m
              </p>
            </div>
          </div>
        </div>

        <div v-else-if="gettingLocation" class="p-4 bg-gray-50 rounded-lg text-center">
          <div class="inline-block w-6 h-6 border-2 border-gray-300 border-t-primary-600 rounded-full animate-spin mb-2"></div>
          <p class="text-sm text-gray-600">Getting your location...</p>
        </div>

        <div v-else-if="locationError" class="p-4 bg-amber-50 border border-amber-200 rounded-lg">
          <div class="flex items-start space-x-2">
            <AlertTriangle class="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
            <div>
              <p class="text-sm font-medium text-amber-900">Location Error</p>
              <p class="text-xs text-amber-700 mt-1">{{ locationError }}</p>
              <button @click="retryLocation" class="mt-2 text-xs text-amber-700 underline">
                Try Again
              </button>
            </div>
          </div>
        </div>

        <!-- Additional Notes -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Additional Information (Optional)
          </label>
          <textarea
            v-model="notes"
            rows="3"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-red-500 focus:border-transparent"
            placeholder="Describe the emergency situation..."
          ></textarea>
        </div>

        <!-- Quick Emergency Types -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Emergency Type
          </label>
          <div class="grid grid-cols-2 gap-2">
            <button
              v-for="type in emergencyTypes"
              :key="type.value"
              @click="selectEmergencyType(type)"
              class="p-3 border rounded-lg text-left hover:bg-gray-50 transition-colors"
              :class="selectedType === type.value ? 'border-red-600 bg-red-50' : 'border-gray-300'"
            >
              <component :is="type.icon" class="w-5 h-5 mb-1" :class="selectedType === type.value ? 'text-red-600' : 'text-gray-600'" />
              <p class="text-sm font-medium text-gray-900">{{ type.label }}</p>
            </button>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex space-x-3 pt-4">
          <button
            @click="showModal = false"
            class="flex-1 btn-secondary py-3"
            :disabled="sending"
          >
            Cancel
          </button>
          <button
            @click="sendSOS"
            class="flex-1 bg-red-600 hover:bg-red-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors flex items-center justify-center"
            :disabled="sending || (!locationData && !locationError)"
          >
            <AlertCircle v-if="!sending" class="w-5 h-5 mr-2" />
            <div v-else class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
            {{ sending ? 'Sending...' : 'Send SOS Alert' }}
          </button>
        </div>
      </div>
    </Modal>

    <!-- Success Toast -->
    <Toast
      v-model="showToast"
      type="success"
      title="SOS Alert Sent"
      message="Emergency services have been notified. Help is on the way."
    />
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue'
import { AlertCircle, AlertTriangle, MapPin, Phone, Ambulance, Car, Wrench } from 'lucide-vue-next'
import { useGeolocation, formatCoordinates } from '@shared'
import { useIncidentStore } from '@/stores/incident'
import Modal from './Modal.vue'
import Toast from './Toast.vue'

const { coords, error: locationError, getCurrentPosition } = useGeolocation()

const showModal = ref(false)
const showToast = ref(false)
const sending = ref(false)
const gettingLocation = ref(false)
const locationData = ref(null)
const notes = ref('')
const selectedType = ref('general')

const incidentStore = useIncidentStore()

const emergencyTypes = [
  { value: 'medical', label: 'Medical', icon: Ambulance },
  { value: 'accident', label: 'Accident', icon: Car },
  { value: 'breakdown', label: 'Breakdown', icon: Wrench },
  { value: 'general', label: 'Other', icon: AlertCircle }
]

async function openModal() {
  showModal.value = true
  notes.value = ''
  selectedType.value = 'general'
  
  // Get current location
  await getLocation()
}

async function getLocation() {
  gettingLocation.value = true
  
  try {
    const position = await getCurrentPosition()
    locationData.value = position
  } catch (error) {
    console.error('Failed to get location:', error)
  } finally {
    gettingLocation.value = false
  }
}

async function retryLocation() {
  await getLocation()
}

function selectEmergencyType(type) {
  selectedType.value = type.value
  if (!notes.value) {
    notes.value = `${type.label} emergency`
  }
}

async function sendSOS() {
  sending.value = true
  
  try {
    const sosData = {
      lat: locationData.value?.latitude,
      lng: locationData.value?.longitude,
      accuracy: locationData.value?.accuracy
    }
    
    const fullNotes = `${selectedType.value.toUpperCase()}: ${notes.value || 'Emergency situation'}`
    
    await incidentStore.sendSOSAlert(sosData, fullNotes)
    
    showModal.value = false
    showToast.value = true
    
    // Clear form
    notes.value = ''
    selectedType.value = 'general'
    locationData.value = null
    
    // Vibrate if supported
    if ('vibrate' in navigator) {
      navigator.vibrate([200, 100, 200, 100, 200])
    }
  } catch (error) {
    console.error('Failed to send SOS:', error)
    alert('Failed to send SOS alert. Please try calling emergency services directly.')
  } finally {
    sending.value = false
  }
}

watch(() => coords.value, (newCoords) => {
  if (newCoords && !locationData.value) {
    locationData.value = newCoords
  }
})
</script>

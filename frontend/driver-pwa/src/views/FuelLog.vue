<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="card p-4 bg-gradient-to-r from-amber-500 to-orange-500 text-white">
      <div class="flex items-center space-x-3">
        <div class="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center backdrop-blur-sm">
          <Fuel class="w-6 h-6" />
        </div>
        <div>
          <h2 class="text-xl font-bold">Fuel Log</h2>
          <p class="text-sm text-amber-50">Record your fuel purchases</p>
        </div>
      </div>
    </div>

    <!-- Fuel Entry Form -->
    <div class="card p-6">
      <form @submit.prevent="submitFuelLog">
        <div class="space-y-4">
          <!-- Vehicle Selection -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Vehicle <span class="text-red-500">*</span>
            </label>
            <select
              v-model="fuelData.vehicle"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            >
              <option value="">Select Vehicle</option>
              <option
                v-for="vehicle in vehicles"
                :key="vehicle.name"
                :value="vehicle.name"
              >
                {{ vehicle.license_plate || vehicle.name }}
              </option>
            </select>
          </div>

          <!-- Odometer Reading -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Odometer Reading (km) <span class="text-red-500">*</span>
            </label>
            <input
              v-model.number="fuelData.odometer"
              type="number"
              required
              step="0.1"
              min="0"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              placeholder="12345.6"
            />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <!-- Liters -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Liters <span class="text-red-500">*</span>
              </label>
              <input
                v-model.number="fuelData.liters"
                type="number"
                required
                step="0.01"
                min="0"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                placeholder="45.50"
              />
            </div>

            <!-- Price per Liter -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Price/Liter <span class="text-red-500">*</span>
              </label>
              <input
                v-model.number="fuelData.pricePerLiter"
                type="number"
                required
                step="0.01"
                min="0"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                placeholder="1.50"
              />
            </div>
          </div>

          <!-- Total Cost (calculated) -->
          <div class="p-4 bg-primary-50 rounded-lg">
            <div class="flex items-center justify-between">
              <span class="text-sm font-medium text-gray-700">Total Cost</span>
              <span class="text-2xl font-bold text-primary-600">
                {{ totalCost.toFixed(2) }}
              </span>
            </div>
          </div>

          <!-- Station (optional) -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Fuel Station
            </label>
            <input
              v-model="fuelData.station"
              type="text"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              placeholder="Shell Station - Main St"
            />
          </div>

          <!-- Location -->
          <div>
            <button
              type="button"
              @click="captureLocation"
              class="w-full flex items-center justify-center space-x-2 px-4 py-3 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary-500 transition-colors"
              :disabled="locationLoading"
            >
              <MapPin class="w-5 h-5" :class="locationCaptured ? 'text-green-600' : 'text-gray-400'" />
              <span v-if="locationLoading" class="text-gray-600">Getting location...</span>
              <span v-else-if="locationCaptured" class="text-green-600">Location captured</span>
              <span v-else class="text-gray-600">Capture Location</span>
            </button>
            <p v-if="locationError" class="mt-2 text-sm text-red-600">{{ locationError }}</p>
          </div>

          <!-- Photo -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Receipt Photo
            </label>
            <div class="flex items-center space-x-3">
              <button
                type="button"
                @click="takePhoto"
                class="flex-1 flex items-center justify-center space-x-2 px-4 py-3 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary-500 transition-colors"
              >
                <Camera class="w-5 h-5 text-gray-400" />
                <span class="text-gray-600">Take Photo</span>
              </button>
              <input
                ref="fileInput"
                type="file"
                accept="image/*"
                @change="handleFileSelect"
                class="hidden"
              />
              <button
                type="button"
                @click="$refs.fileInput.click()"
                class="flex-1 flex items-center justify-center space-x-2 px-4 py-3 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary-500 transition-colors"
              >
                <Upload class="w-5 h-5 text-gray-400" />
                <span class="text-gray-600">Upload</span>
              </button>
            </div>
            <div v-if="fuelData.photo" class="mt-3">
              <img :src="fuelData.photo" alt="Receipt" class="w-full h-48 object-cover rounded-lg" />
            </div>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            class="w-full btn-primary py-3"
            :disabled="loading || !isFormValid"
          >
            <Loader v-if="loading" class="w-5 h-5 mr-2 animate-spin" />
            <span>{{ loading ? 'Saving...' : 'Save Fuel Log' }}</span>
          </button>
        </div>
      </form>
    </div>

    <!-- Recent Fuel Logs -->
    <div class="card p-4">
      <h3 class="section-title mb-4">Recent Entries</h3>
      <div v-if="recentLogs.length === 0" class="text-center py-8 text-gray-500">
        No recent fuel logs
      </div>
      <div v-else class="space-y-3">
        <div
          v-for="log in recentLogs"
          :key="log.name"
          class="p-3 bg-gray-50 rounded-lg"
        >
          <div class="flex items-center justify-between mb-2">
            <span class="font-medium text-gray-900">{{ log.vehicle }}</span>
            <span class="text-sm text-gray-600">{{ formatDate(log.date) }}</span>
          </div>
          <div class="grid grid-cols-3 gap-2 text-sm">
            <div>
              <p class="text-gray-500">Liters</p>
              <p class="font-medium">{{ log.liters }}</p>
            </div>
            <div>
              <p class="text-gray-500">Odometer</p>
              <p class="font-medium">{{ log.odometer }}</p>
            </div>
            <div>
              <p class="text-gray-500">Cost</p>
              <p class="font-medium">{{ log.total_cost }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Camera Modal -->
    <CameraModal
      v-model="showCamera"
      @capture="handlePhotoCapture"
    />

    <!-- Success Toast -->
    <Toast
      v-model="showToast"
      :type="toastType"
      :title="toastTitle"
      :message="toastMessage"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { format } from 'date-fns'
import { Fuel, MapPin, Camera, Upload, Loader } from 'lucide-vue-next'
import { useGeolocation } from '@/composables/useGeolocation'
import frappeClient from '@/utils/frappeClient'
import Toast from '@/components/common/Toast.vue'
import CameraModal from '@/components/common/CameraModal.vue'

const { getCurrentPosition } = useGeolocation()

const loading = ref(false)
const locationLoading = ref(false)
const locationCaptured = ref(false)
const locationError = ref('')
const showCamera = ref(false)
const showToast = ref(false)
const toastType = ref('success')
const toastTitle = ref('')
const toastMessage = ref('')
const fileInput = ref(null)
const vehicles = ref([])
const recentLogs = ref([])

const fuelData = ref({
  vehicle: '',
  odometer: null,
  liters: null,
  pricePerLiter: null,
  station: '',
  photo: null,
  location: null
})

const totalCost = computed(() => {
  return (fuelData.value.liters || 0) * (fuelData.value.pricePerLiter || 0)
})

const isFormValid = computed(() => {
  return fuelData.value.vehicle &&
    fuelData.value.odometer > 0 &&
    fuelData.value.liters > 0 &&
    fuelData.value.pricePerLiter > 0
})

async function captureLocation() {
  locationLoading.value = true
  locationError.value = ''
  
  try {
    const position = await getCurrentPosition()
    fuelData.value.location = {
      lat: position.latitude,
      lng: position.longitude,
      accuracy: position.accuracy
    }
    locationCaptured.value = true
  } catch (error) {
    locationError.value = 'Failed to capture location: ' + error.message
  } finally {
    locationLoading.value = false
  }
}

function takePhoto() {
  showCamera.value = true
}

function handlePhotoCapture(photoData) {
  fuelData.value.photo = photoData.dataUrl
  showCamera.value = false
}

function handleFileSelect(event) {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      fuelData.value.photo = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

async function submitFuelLog() {
  if (!isFormValid.value) return
  
  loading.value = true
  
  try {
    const result = await frappeClient.call('tems.api.pwa.driver.log_fuel', {
      vehicle: fuelData.value.vehicle,
      liters: fuelData.value.liters,
      price_per_liter: fuelData.value.pricePerLiter,
      odometer: fuelData.value.odometer,
      station: fuelData.value.station,
      location_data: fuelData.value.location
    })
    
    toastType.value = 'success'
    toastTitle.value = 'Success'
    toastMessage.value = 'Fuel log saved successfully'
    showToast.value = true
    
    // Reset form
    fuelData.value = {
      vehicle: fuelData.value.vehicle, // Keep vehicle selected
      odometer: null,
      liters: null,
      pricePerLiter: null,
      station: '',
      photo: null,
      location: null
    }
    locationCaptured.value = false
    
    // Refresh recent logs
    await fetchRecentLogs()
    
  } catch (error) {
    toastType.value = 'error'
    toastTitle.value = 'Error'
    toastMessage.value = error.message || 'Failed to save fuel log'
    showToast.value = true
  } finally {
    loading.value = false
  }
}

async function fetchRecentLogs() {
  try {
    const logs = await frappeClient.getList(
      'Fuel Log',
      ['name', 'vehicle', 'date', 'liters', 'odometer', 'total_cost'],
      {},
      5,
      'date desc'
    )
    recentLogs.value = logs
  } catch (error) {
    console.error('Failed to fetch recent logs:', error)
  }
}

async function fetchVehicles() {
  try {
    // Get vehicles assigned to current driver
    const data = await frappeClient.call('tems.api.pwa.driver.get_driver_dashboard')
    
    // Extract unique vehicles from trips
    const vehicleNames = [...new Set([
      ...(data.journey_plans || []).map(jp => jp.vehicle),
      ...(data.operation_plans || []).map(op => op.vehicle)
    ])].filter(Boolean)
    
    if (vehicleNames.length > 0) {
      vehicles.value = await frappeClient.getList(
        'Vehicle',
        ['name', 'license_plate', 'make', 'model'],
        { name: ['in', vehicleNames] }
      )
    }
  } catch (error) {
    console.error('Failed to fetch vehicles:', error)
  }
}

function formatDate(date) {
  return format(new Date(date), 'MMM d, yyyy HH:mm')
}

onMounted(() => {
  fetchVehicles()
  fetchRecentLogs()
})
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold text-gray-900">Vehicle Inspection</h1>
    </div>

    <!-- Vehicle Selection -->
    <div v-if="!selectedVehicle" class="card p-4">
      <h3 class="section-title">Select Vehicle</h3>
      <LoadingSpinner v-if="vehicleStore.loading" />
      
      <div v-else class="space-y-3">
        <button
          v-for="vehicle in vehicleStore.assignedVehicles"
          :key="vehicle.name"
          @click="selectVehicle(vehicle)"
          class="w-full p-4 border-2 border-gray-200 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-all text-left"
        >
          <div class="flex items-center space-x-4">
            <div class="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
              <Truck class="w-6 h-6 text-gray-600" />
            </div>
            <div class="flex-1">
              <p class="font-semibold text-gray-900">{{ vehicle.license_plate }}</p>
              <p class="text-sm text-gray-600">
                {{ vehicle.make }} {{ vehicle.model }}
              </p>
            </div>
            <ChevronRight class="w-5 h-5 text-gray-400" />
          </div>
        </button>
      </div>
    </div>

    <!-- Inspection Form -->
    <SpotCheckForm
      v-else
      :vehicle="selectedVehicle"
      @cancel="selectedVehicle = null"
      @submit="handleSubmitInspection"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Truck, ChevronRight } from 'lucide-vue-next'
import { useVehicleStore } from '@/stores/vehicle'
import { useNotifications } from '@/composables/useNotifications'
import SpotCheckForm from '@/components/inspection/SpotCheckForm.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

const route = useRoute()
const router = useRouter()
const vehicleStore = useVehicleStore()
const { showSuccess } = useNotification()

const selectedVehicle = ref(null)

function selectVehicle(vehicle) {
  selectedVehicle.value = vehicle
  vehicleStore.setCurrentVehicle(vehicle)
}

async function handleSubmitInspection(result) {
  showSuccess('Inspection submitted successfully')
  selectedVehicle.value = null
  router.push('/driver')
}

onMounted(async () => {
  await vehicleStore.fetchMyVehicles()
  
  // Auto-select if vehicle in query
  if (route.query.vehicle) {
    const vehicle = vehicle = vehicleStore.assignedVehicles.find(v => v.name === route.query.vehicle)
    if (vehicle) {
      selectVehicle(vehicle)
    }
  }
})
</script>
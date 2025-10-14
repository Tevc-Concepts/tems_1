<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="card p-4">
      <div class="flex items-center justify-between mb-2">
        <div class="flex items-center space-x-3">
          <button @click="$router.back()" class="btn-secondary p-2">
            <ArrowLeft class="w-5 h-5" />
          </button>
          <div>
            <h2 class="text-xl font-bold text-gray-900">Cargo Management</h2>
            <p class="text-sm text-gray-600">Trip {{ tripId }}</p>
          </div>
        </div>
        <button @click="scanBarcode" class="btn-primary">
          <Scan class="w-5 h-5 mr-2" />
          Scan
        </button>
      </div>
    </div>

    <!-- Summary Cards -->
    <div class="grid grid-cols-3 gap-3">
      <div class="card p-4 text-center">
        <Package class="w-6 h-6 mx-auto mb-2 text-primary-600" />
        <p class="text-2xl font-bold text-gray-900">{{ consignments.length }}</p>
        <p class="text-xs text-gray-600">Total</p>
      </div>
      <div class="card p-4 text-center">
        <CheckCircle class="w-6 h-6 mx-auto mb-2 text-green-600" />
        <p class="text-2xl font-bold text-gray-900">{{ deliveredCount }}</p>
        <p class="text-xs text-gray-600">Delivered</p>
      </div>
      <div class="card p-4 text-center">
        <Clock class="w-6 h-6 mx-auto mb-2 text-amber-600" />
        <p class="text-2xl font-bold text-gray-900">{{ pendingCount }}</p>
        <p class="text-xs text-gray-600">Pending</p>
      </div>
    </div>

    <!-- Consignments List -->
    <div class="card">
      <div class="p-4 border-b">
        <h3 class="font-semibold text-gray-900">Consignments</h3>
      </div>

      <div v-if="loading" class="p-8">
        <LoadingSpinner message="Loading consignments..." />
      </div>

      <div v-else-if="consignments.length === 0" class="p-8">
        <EmptyState
          :icon="Package"
          title="No cargo"
          message="No cargo consignments assigned to this trip."
        />
      </div>

      <div v-else class="divide-y">
        <div
          v-for="consignment in consignments"
          :key="consignment.name"
          class="p-4 hover:bg-gray-50 cursor-pointer"
          @click="selectConsignment(consignment)"
        >
          <div class="flex items-start justify-between mb-2">
            <div class="flex-1">
              <div class="flex items-center space-x-2 mb-1">
                <p class="font-semibold text-gray-900">{{ consignment.consignment_no }}</p>
                <StatusBadge :status="consignment.status" />
              </div>
              <p class="text-sm text-gray-600">{{ consignment.tracking_no }}</p>
            </div>
            <button
              v-if="consignment.status !== 'Delivered'"
              @click.stop="updateStatus(consignment, 'Delivered')"
              class="btn-sm btn-primary"
            >
              Mark Delivered
            </button>
          </div>

          <div class="grid grid-cols-2 gap-3 mt-3 text-sm">
            <div>
              <p class="text-gray-500">From</p>
              <p class="font-medium text-gray-900">{{ consignment.sender }}</p>
            </div>
            <div>
              <p class="text-gray-500">To</p>
              <p class="font-medium text-gray-900">{{ consignment.receiver }}</p>
            </div>
            <div>
              <p class="text-gray-500">Weight</p>
              <p class="font-medium text-gray-900">{{ consignment.weight }} kg</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Barcode Scanner Modal -->
    <Modal v-model="showScanner" title="Scan Barcode" size="lg">
      <div class="space-y-4">
        <div class="p-4 bg-gray-100 rounded-lg text-center">
          <Scan class="w-16 h-16 mx-auto mb-4 text-gray-400" />
          <p class="text-gray-600 mb-4">Position the barcode within the frame</p>
          
          <!-- Manual Entry Fallback -->
          <div class="mt-4">
            <input
              v-model="manualBarcode"
              type="text"
              placeholder="Or enter tracking number manually"
              class="w-full px-4 py-2 border rounded-lg"
              @keydown.enter="processBarcode"
            />
          </div>
        </div>

        <div class="flex space-x-2">
          <button @click="showScanner = false" class="flex-1 btn-secondary">
            Cancel
          </button>
          <button @click="processBarcode" class="flex-1 btn-primary" :disabled="!manualBarcode">
            Scan
          </button>
        </div>
      </div>
    </Modal>

    <!-- Delivery Confirmation Modal -->
    <Modal v-model="showDeliveryModal" title="Confirm Delivery" size="md">
      <div v-if="selectedConsignment" class="space-y-4">
        <div class="p-4 bg-gray-50 rounded-lg">
          <p class="text-sm text-gray-600">Consignment</p>
          <p class="font-semibold text-gray-900">{{ selectedConsignment.consignment_no }}</p>
          <p class="text-sm text-gray-600 mt-2">Receiver</p>
          <p class="font-medium text-gray-900">{{ selectedConsignment.receiver }}</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Signature
          </label>
          <div class="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
            <button @click="captureSignature" class="btn-secondary">
              <Edit class="w-5 h-5 mr-2" />
              Capture Signature
            </button>
          </div>
        </div>

        <div class="flex space-x-2">
          <button @click="showDeliveryModal = false" class="flex-1 btn-secondary">
            Cancel
          </button>
          <button @click="confirmDelivery" class="flex-1 btn-primary" :disabled="updating">
            {{ updating ? 'Confirming...' : 'Confirm Delivery' }}
          </button>
        </div>
      </div>
    </Modal>

    <!-- Toast -->
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
import { useRoute } from 'vue-router'
import { Package, Scan, CheckCircle, Clock, ArrowLeft, Edit } from 'lucide-vue-next'
import { useCargoStore } from '@/stores/cargo'
import { useGeolocation } from '@shared'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import StatusBadge from '@/components/common/StatusBadge.vue'
import Modal from '@/components/common/Modal.vue'
import Toast from '@/components/common/Toast.vue'

const route = useRoute()
const cargoStore = useCargoStore()
const { getCurrentPosition } = useGeolocation()

const tripId = computed(() => route.params.id)
const consignments = computed(() => cargoStore.consignments)
const loading = ref(false)
const showScanner = ref(false)
const showDeliveryModal = ref(false)
const showToast = ref(false)
const toastType = ref('success')
const toastTitle = ref('')
const toastMessage = ref('')
const manualBarcode = ref('')
const selectedConsignment = ref(null)
const updating = ref(false)

const deliveredCount = computed(() => 
  consignments.value.filter(c => c.status === 'Delivered').length
)

const pendingCount = computed(() => 
  consignments.value.filter(c => c.status !== 'Delivered').length
)

function scanBarcode() {
  showScanner.value = true
  manualBarcode.value = ''
}

async function processBarcode() {
  if (!manualBarcode.value) return

  try {
    const result = await cargoStore.scanBarcode(manualBarcode.value, tripId.value)
    
    toastType.value = 'success'
    toastTitle.value = 'Scanned'
    toastMessage.value = 'Consignment found'
    showToast.value = true
    showScanner.value = false
    
    // Refresh list
    await cargoStore.fetchConsignments(tripId.value)
  } catch (error) {
    toastType.value = 'error'
    toastTitle.value = 'Error'
    toastMessage.value = error.message || 'Failed to scan barcode'
    showToast.value = true
  }
}

function selectConsignment(consignment) {
  selectedConsignment.value = consignment
  if (consignment.status !== 'Delivered') {
    showDeliveryModal.value = true
  }
}

async function updateStatus(consignment, status) {
  updating.value = true
  
  try {
    const location = await getCurrentPosition()
    
    await cargoStore.updateDeliveryStatus(
      consignment.name,
      status,
      {
        lat: location.latitude,
        lng: location.longitude
      }
    )
    
    toastType.value = 'success'
    toastTitle.value = 'Updated'
    toastMessage.value = 'Delivery status updated successfully'
    showToast.value = true
    
    await cargoStore.fetchConsignments(tripId.value)
  } catch (error) {
    toastType.value = 'error'
    toastTitle.value = 'Error'
    toastMessage.value = error.message || 'Failed to update status'
    showToast.value = true
  } finally {
    updating.value = false
  }
}

function captureSignature() {
  // TODO: Implement signature capture
  console.log('Capture signature')
}

async function confirmDelivery() {
  if (!selectedConsignment.value) return
  
  await updateStatus(selectedConsignment.value, 'Delivered')
  showDeliveryModal.value = false
  selectedConsignment.value = null
}

onMounted(async () => {
  loading.value = true
  try {
    await cargoStore.fetchConsignments(tripId.value)
  } finally {
    loading.value = false
  }
})
</script>

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
            <h2 class="text-xl font-bold text-gray-900">Passenger Manifest</h2>
            <p class="text-sm text-gray-600">Trip {{ tripId }}</p>
          </div>
        </div>
        <button @click="scanTicket" class="btn-primary">
          <Scan class="w-5 h-5 mr-2" />
          Scan Ticket
        </button>
      </div>
    </div>

    <!-- Seat Occupancy Summary -->
    <div class="card p-4">
      <div class="flex items-center justify-between mb-3">
        <h3 class="font-semibold text-gray-900">Seat Occupancy</h3>
        <span class="text-sm text-gray-600">
          {{ occupiedSeats }} / {{ totalSeats }} seats
        </span>
      </div>
      
      <!-- Progress Bar -->
      <div class="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
        <div
          class="h-full bg-primary-600 transition-all duration-300"
          :style="{ width: occupancyPercentage + '%' }"
        ></div>
      </div>
      
      <div class="grid grid-cols-3 gap-3 mt-4">
        <div class="text-center">
          <p class="text-2xl font-bold text-green-600">{{ boardedCount }}</p>
          <p class="text-xs text-gray-600">Boarded</p>
        </div>
        <div class="text-center">
          <p class="text-2xl font-bold text-amber-600">{{ confirmedCount }}</p>
          <p class="text-xs text-gray-600">Confirmed</p>
        </div>
        <div class="text-center">
          <p class="text-2xl font-bold text-gray-600">{{ availableSeats }}</p>
          <p class="text-xs text-gray-600">Available</p>
        </div>
      </div>
    </div>

    <!-- Passenger List -->
    <div class="card">
      <div class="p-4 border-b flex items-center justify-between">
        <h3 class="font-semibold text-gray-900">Passengers</h3>
        <div class="flex items-center space-x-2">
          <button
            @click="filterStatus = 'all'"
            class="px-3 py-1 rounded-lg text-sm"
            :class="filterStatus === 'all' ? 'bg-primary-600 text-white' : 'bg-gray-100 text-gray-700'"
          >
            All
          </button>
          <button
            @click="filterStatus = 'Boarded'"
            class="px-3 py-1 rounded-lg text-sm"
            :class="filterStatus === 'Boarded' ? 'bg-primary-600 text-white' : 'bg-gray-100 text-gray-700'"
          >
            Boarded
          </button>
          <button
            @click="filterStatus = 'Confirmed'"
            class="px-3 py-1 rounded-lg text-sm"
            :class="filterStatus === 'Confirmed' ? 'bg-primary-600 text-white' : 'bg-gray-100 text-gray-700'"
          >
            Pending
          </button>
        </div>
      </div>

      <div v-if="loading" class="p-8">
        <LoadingSpinner message="Loading manifest..." />
      </div>

      <div v-else-if="filteredBookings.length === 0" class="p-8">
        <EmptyState
          :icon="Users"
          title="No passengers"
          :message="filterStatus === 'all' ? 'No passengers booked for this trip.' : `No ${filterStatus.toLowerCase()} passengers.`"
        />
      </div>

      <div v-else class="divide-y max-h-[500px] overflow-y-auto">
        <div
          v-for="booking in filteredBookings"
          :key="booking.name"
          class="p-4 hover:bg-gray-50"
        >
          <div class="flex items-start justify-between">
            <div class="flex items-center space-x-3 flex-1">
              <div
                class="w-12 h-12 rounded-full flex items-center justify-center font-bold text-white"
                :class="booking.status === 'Boarded' ? 'bg-green-500' : 'bg-gray-400'"
              >
                {{ booking.seat_number }}
              </div>
              
              <div class="flex-1">
                <div class="flex items-center space-x-2 mb-1">
                  <p class="font-semibold text-gray-900">{{ booking.passenger_name }}</p>
                  <StatusBadge :status="booking.status" />
                </div>
                <p class="text-sm text-gray-600">Ticket: {{ booking.ticket_code }}</p>
                <p v-if="booking.boarding_time" class="text-xs text-gray-500 mt-1">
                  Boarded: {{ formatTime(booking.boarding_time) }}
                </p>
              </div>
            </div>

            <button
              v-if="booking.status !== 'Boarded'"
              @click="checkInPassenger(booking)"
              class="btn-sm btn-primary whitespace-nowrap"
              :disabled="updating"
            >
              Check In
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Ticket Scanner Modal -->
    <Modal v-model="showScanner" title="Scan Ticket" size="lg">
      <div class="space-y-4">
        <div class="p-4 bg-gray-100 rounded-lg text-center">
          <Scan class="w-16 h-16 mx-auto mb-4 text-gray-400" />
          <p class="text-gray-600 mb-4">Position the QR code within the frame</p>
          
          <!-- Manual Entry Fallback -->
          <div class="mt-4">
            <input
              v-model="manualTicketCode"
              type="text"
              placeholder="Or enter ticket code manually"
              class="w-full px-4 py-2 border rounded-lg"
              @keydown.enter="processTicket"
            />
          </div>
        </div>

        <div class="flex space-x-2">
          <button @click="showScanner = false" class="flex-1 btn-secondary">
            Cancel
          </button>
          <button @click="processTicket" class="flex-1 btn-primary" :disabled="!manualTicketCode">
            Scan
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
import { format, parseISO } from 'date-fns'
import { Users, Scan, ArrowLeft } from 'lucide-vue-next'
import { usePassengerStore } from '@/stores/passenger'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import StatusBadge from '@/components/common/StatusBadge.vue'
import Modal from '@/components/common/Modal.vue'
import Toast from '@/components/common/Toast.vue'

const route = useRoute()
const passengerStore = usePassengerStore()

const tripId = computed(() => route.params.id)
const loading = ref(false)
const updating = ref(false)
const showScanner = ref(false)
const showToast = ref(false)
const toastType = ref('success')
const toastTitle = ref('')
const toastMessage = ref('')
const manualTicketCode = ref('')
const filterStatus = ref('all')

const totalSeats = computed(() => passengerStore.totalSeats)
const occupiedSeats = computed(() => passengerStore.occupiedSeats)
const availableSeats = computed(() => passengerStore.availableSeats)

const occupancyPercentage = computed(() => {
  if (totalSeats.value === 0) return 0
  return (occupiedSeats.value / totalSeats.value) * 100
})

const boardedCount = computed(() => 
  passengerStore.bookings.filter(b => b.status === 'Boarded').length
)

const confirmedCount = computed(() => 
  passengerStore.bookings.filter(b => b.status === 'Confirmed').length
)

const filteredBookings = computed(() => {
  if (filterStatus.value === 'all') {
    return passengerStore.bookings
  }
  return passengerStore.bookings.filter(b => b.status === filterStatus.value)
})

function scanTicket() {
  showScanner.value = true
  manualTicketCode.value = ''
}

async function processTicket() {
  if (!manualTicketCode.value) return

  updating.value = true

  try {
    const result = await passengerStore.scanTicket(manualTicketCode.value, tripId.value)
    
    toastType.value = result.success ? 'success' : 'warning'
    toastTitle.value = result.success ? 'Success' : 'Already Boarded'
    toastMessage.value = result.message
    showToast.value = true
    showScanner.value = false
    manualTicketCode.value = ''
    
    // Refresh manifest
    await passengerStore.fetchPassengerManifest(tripId.value)
  } catch (error) {
    toastType.value = 'error'
    toastTitle.value = 'Error'
    toastMessage.value = error.message || 'Failed to scan ticket'
    showToast.value = true
  } finally {
    updating.value = false
  }
}

async function checkInPassenger(booking) {
  updating.value = true

  try {
    await passengerStore.updateBoardingStatus(booking.name, 'Boarded')
    
    toastType.value = 'success'
    toastTitle.value = 'Checked In'
    toastMessage.value = `${booking.passenger_name} checked in successfully`
    showToast.value = true
  } catch (error) {
    toastType.value = 'error'
    toastTitle.value = 'Error'
    toastMessage.value = error.message || 'Failed to check in passenger'
    showToast.value = true
  } finally {
    updating.value = false
  }
}

function formatTime(dateTime) {
  if (!dateTime) return ''
  try {
    return format(parseISO(dateTime), 'HH:mm')
  } catch (e) {
    return dateTime
  }
}

onMounted(async () => {
  loading.value = true
  try {
    await passengerStore.fetchPassengerManifest(tripId.value)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="min-h-screen bg-background pb-20">
    <!-- Profile Header -->
    <div class="bg-gradient-to-br from-primary-600 to-primary-700 text-white p-6 rounded-b-3xl shadow-lg">
      <div class="flex items-center space-x-4">
        <div class="w-20 h-20 bg-white rounded-full flex items-center justify-center text-primary-600 text-3xl font-bold">
          {{ initials }}
        </div>
        <div>
          <h1 class="text-2xl font-bold">{{ driver?.employee_name || 'Driver' }}</h1>
          <p class="text-primary-100">{{ driver?.employee || 'N/A' }}</p>
          <p class="text-sm text-primary-200 mt-1">{{ driver?.mobile || 'No phone' }}</p>
        </div>
      </div>
    </div>

    <!-- Profile Details -->
    <div class="p-4 space-y-4">
      <!-- License Information -->
      <div class="bg-white rounded-xl shadow-card p-4">
        <div class="flex items-center justify-between mb-3">
          <h2 class="text-lg font-semibold text-gray-800 flex items-center">
            <CreditCard class="w-5 h-5 mr-2 text-primary-600" />
            License Information
          </h2>
        </div>
        <div class="space-y-2 text-sm">
          <div class="flex justify-between">
            <span class="text-gray-600">License Number:</span>
            <span class="font-medium">{{ driver?.license_number || 'N/A' }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-600">License Class:</span>
            <span class="font-medium">{{ driver?.license_class || 'N/A' }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-600">Expiry Date:</span>
            <span :class="licenseExpiryClass">
              {{ driver?.license_expiry ? formatDate(driver.license_expiry) : 'N/A' }}
            </span>
          </div>
        </div>
      </div>

      <!-- Performance Stats -->
      <div class="bg-white rounded-xl shadow-card p-4">
        <h2 class="text-lg font-semibold text-gray-800 mb-3 flex items-center">
          <TrendingUp class="w-5 h-5 mr-2 text-primary-600" />
          Performance
        </h2>
        <div class="grid grid-cols-2 gap-4">
          <div class="text-center p-3 bg-primary-50 rounded-lg">
            <div class="text-2xl font-bold text-primary-600">{{ stats.totalTrips }}</div>
            <div class="text-xs text-gray-600">Total Trips</div>
          </div>
          <div class="text-center p-3 bg-success-50 rounded-lg">
            <div class="text-2xl font-bold text-success-600">{{ stats.completedTrips }}</div>
            <div class="text-xs text-gray-600">Completed</div>
          </div>
          <div class="text-center p-3 bg-yellow-50 rounded-lg">
            <div class="text-2xl font-bold text-yellow-600">{{ stats.safetyScore }}%</div>
            <div class="text-xs text-gray-600">Safety Score</div>
          </div>
          <div class="text-center p-3 bg-purple-50 rounded-lg">
            <div class="text-2xl font-bold text-purple-600">{{ stats.onTimeRate }}%</div>
            <div class="text-xs text-gray-600">On-Time</div>
          </div>
        </div>
      </div>

      <!-- Documents -->
      <div class="bg-white rounded-xl shadow-card p-4">
        <h2 class="text-lg font-semibold text-gray-800 mb-3 flex items-center">
          <FileText class="w-5 h-5 mr-2 text-primary-600" />
          Documents
        </h2>
        <div class="space-y-2">
          <div v-for="doc in documents" :key="doc.id" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div class="flex items-center">
              <File class="w-4 h-4 mr-2 text-gray-500" />
              <span class="text-sm font-medium">{{ doc.name }}</span>
            </div>
            <StatusBadge :status="doc.status" size="sm" />
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="bg-white rounded-xl shadow-card p-4">
        <h2 class="text-lg font-semibold text-gray-800 mb-3">Quick Actions</h2>
        <div class="grid grid-cols-2 gap-3">
          <button
            @click="editProfile"
            class="flex items-center justify-center p-3 bg-primary-50 text-primary-600 rounded-lg hover:bg-primary-100 transition"
          >
            <Edit class="w-4 h-4 mr-2" />
            Edit Profile
          </button>
          <button
            @click="viewHistory"
            class="flex items-center justify-center p-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition"
          >
            <History class="w-4 h-4 mr-2" />
            Trip History
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuth as useAuthStore } from '@shared'
import { useTripStore } from '@/stores/trip'
import { CreditCard, TrendingUp, FileText, File, Edit, History } from 'lucide-vue-next'
import StatusBadge from '@/components/common/StatusBadge.vue'
import { format, parseISO, differenceInDays } from 'date-fns'

const authStore = useAuthStore()
const tripStore = useTripStore()

const driver = computed(() => authStore.user)

const initials = computed(() => {
  const name = driver.value?.employee_name || 'D'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
})

const licenseExpiryClass = computed(() => {
  if (!driver.value?.license_expiry) return 'font-medium'
  
  const daysUntilExpiry = differenceInDays(parseISO(driver.value.license_expiry), new Date())
  
  if (daysUntilExpiry < 0) return 'font-medium text-danger-600'
  if (daysUntilExpiry < 30) return 'font-medium text-warning-600'
  return 'font-medium text-success-600'
})

const stats = computed(() => {
  const trips = tripStore.trips || []
  return {
    totalTrips: trips.length,
    completedTrips: trips.filter(t => t.status === 'Completed').length,
    safetyScore: 95, // Mock data - should come from backend
    onTimeRate: 88, // Mock data - should come from backend
  }
})

const documents = computed(() => [
  { id: 1, name: 'Driver License', status: 'Valid' },
  { id: 2, name: 'Medical Certificate', status: 'Valid' },
  { id: 3, name: 'Police Clearance', status: 'Expiring Soon' },
  { id: 4, name: 'Training Certificate', status: 'Valid' },
])

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  try {
    return format(parseISO(dateString), 'dd MMM yyyy')
  } catch (error) {
    return 'Invalid Date'
  }
}

const editProfile = () => {
  // Navigate to edit profile or show modal
  console.log('Edit profile')
}

const viewHistory = () => {
  // Navigate to trip history
  console.log('View history')
}
</script>

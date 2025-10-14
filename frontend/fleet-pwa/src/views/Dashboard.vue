<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Fleet Dashboard</h1>
        <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
          Asset management and maintenance overview
        </p>
      </div>
      <button
        @click="refreshDashboard"
        :disabled="loading"
        class="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 disabled:opacity-50 transition-colors flex items-center gap-2"
      >
        <svg class="w-5 h-5" :class="{ 'animate-spin': loading }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        Refresh
      </button>
    </div>

    <!-- KPI Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Total Assets</p>
            <p class="text-3xl font-bold text-gray-900 dark:text-white mt-2">
              {{ assetStore.totalAssets }}
            </p>
          </div>
          <div class="p-3 bg-emerald-100 dark:bg-emerald-900 rounded-full">
            <svg class="w-8 h-8 text-emerald-600 dark:text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
          </div>
        </div>
        <div class="mt-4 flex items-center text-sm">
          <span class="text-emerald-600 dark:text-emerald-400 font-medium">{{ assetStore.activeAssets }}</span>
          <span class="text-gray-600 dark:text-gray-400 ml-1">active</span>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Maintenance Due</p>
            <p class="text-3xl font-bold text-gray-900 dark:text-white mt-2">
              {{ maintenanceStore.openWorkOrders.length }}
            </p>
          </div>
          <div class="p-3 bg-orange-100 dark:bg-orange-900 rounded-full">
            <svg class="w-8 h-8 text-orange-600 dark:text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </div>
        </div>
        <div class="mt-4 flex items-center text-sm">
          <span class="text-red-600 dark:text-red-400 font-medium">{{ maintenanceStore.overdueCount }}</span>
          <span class="text-gray-600 dark:text-gray-400 ml-1">overdue</span>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Fuel Efficiency</p>
            <p class="text-3xl font-bold text-gray-900 dark:text-white mt-2">
              {{ fuelStore.averageFuelEfficiency.toFixed(1) }}
            </p>
          </div>
          <div class="p-3 bg-blue-100 dark:bg-blue-900 rounded-full">
            <svg class="w-8 h-8 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
        </div>
        <div class="mt-4 text-sm text-gray-600 dark:text-gray-400">
          km/liter average
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Asset Utilization</p>
            <p class="text-3xl font-bold text-gray-900 dark:text-white mt-2">
              {{ assetStore.assetUtilization }}%
            </p>
          </div>
          <div class="p-3 bg-purple-100 dark:bg-purple-900 rounded-full">
            <svg class="w-8 h-8 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
        </div>
        <div class="mt-4 text-sm text-gray-600 dark:text-gray-400">
          of total fleet
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Quick Actions</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <button
          @click="router.push('/assets')"
          class="p-4 border-2 border-emerald-200 dark:border-emerald-800 rounded-lg hover:bg-emerald-50 dark:hover:bg-emerald-900/20 transition-colors text-center"
        >
          <svg class="w-8 h-8 text-emerald-600 dark:text-emerald-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          <p class="text-sm font-medium text-gray-900 dark:text-white">Add Asset</p>
        </button>

        <button
          @click="router.push('/maintenance')"
          class="p-4 border-2 border-orange-200 dark:border-orange-800 rounded-lg hover:bg-orange-50 dark:hover:bg-orange-900/20 transition-colors text-center"
        >
          <svg class="w-8 h-8 text-orange-600 dark:text-orange-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <p class="text-sm font-medium text-gray-900 dark:text-white">Schedule Maintenance</p>
        </button>

        <button
          @click="router.push('/fuel')"
          class="p-4 border-2 border-blue-200 dark:border-blue-800 rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors text-center"
        >
          <svg class="w-8 h-8 text-blue-600 dark:text-blue-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
          </svg>
          <p class="text-sm font-medium text-gray-900 dark:text-white">Log Fuel</p>
        </button>

        <button
          @click="router.push('/reports')"
          class="p-4 border-2 border-purple-200 dark:border-purple-800 rounded-lg hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors text-center"
        >
          <svg class="w-8 h-8 text-purple-600 dark:text-purple-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p class="text-sm font-medium text-gray-900 dark:text-white">View Reports</p>
        </button>
      </div>
    </div>

    <!-- Recent Maintenance -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Recent Maintenance Activity</h2>
      
      <div v-if="loading" class="text-center py-8">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-600 mx-auto"></div>
        <p class="text-gray-600 dark:text-gray-400 mt-4">Loading...</p>
      </div>

      <div v-else-if="maintenanceStore.workOrders.length === 0" class="text-center py-8">
        <p class="text-gray-600 dark:text-gray-400">No maintenance records found</p>
      </div>

      <div v-else class="space-y-3">
        <div
          v-for="wo in maintenanceStore.workOrders.slice(0, 5)"
          :key="wo.name"
          class="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
        >
          <div class="flex-1">
            <h3 class="font-medium text-gray-900 dark:text-white">{{ wo.asset_name }}</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">{{ wo.maintenance_type }}</p>
          </div>
          <div class="text-right">
            <span
              class="inline-flex px-3 py-1 text-xs font-medium rounded-full"
              :class="{
                'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200': wo.status === 'open',
                'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200': wo.status === 'in_progress',
                'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200': wo.status === 'completed',
                'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200': wo.is_overdue
              }"
            >
              {{ wo.status }}
            </span>
            <p class="text-xs text-gray-600 dark:text-gray-400 mt-1">{{ formatDate(wo.scheduled_date) }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAssetStore } from '../stores/assets'
import { useMaintenanceStore } from '../stores/maintenance'
import { useFuelStore } from '../stores/fuel'
import { formatDate } from '@shared'

const router = useRouter()
const assetStore = useAssetStore()
const maintenanceStore = useMaintenanceStore()
const fuelStore = useFuelStore()

const loading = ref(false)

async function loadDashboardData() {
  loading.value = true
  
  try {
    await Promise.all([
      assetStore.fetchAssets(),
      maintenanceStore.fetchWorkOrders({ limit: 10 }),
      fuelStore.fetchFuelStats()
    ])
  } catch (error) {
    console.error('Error loading dashboard:', error)
  } finally {
    loading.value = false
  }
}

async function refreshDashboard() {
  await loadDashboardData()
}

onMounted(() => {
  loadDashboardData()
})
</script>

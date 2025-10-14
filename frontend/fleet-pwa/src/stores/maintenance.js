import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { frappeClient } from '@shared'

export const useMaintenanceStore = defineStore('maintenance', () => {
    const workOrders = ref([])
    const upcomingMaintenance = ref([])
    const loading = ref(false)
    const error = ref(null)

    // Computed
    const totalWorkOrders = computed(() => workOrders.value.length)
    const openWorkOrders = computed(() =>
        workOrders.value.filter(wo => wo.status === 'open' || wo.status === 'in_progress')
    )
    const overdueCount = computed(() =>
        workOrders.value.filter(wo => wo.is_overdue).length
    )

    // Actions
    async function fetchWorkOrders(filters = {}) {
        loading.value = true
        error.value = null

        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.fleet.get_work_orders',
                args: { filters }
            })

            workOrders.value = response.message || []
            return workOrders.value
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function fetchUpcomingMaintenance(days = 30) {
        loading.value = true
        error.value = null

        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.fleet.get_upcoming_maintenance',
                args: { days }
            })

            upcomingMaintenance.value = response.message || []
            return upcomingMaintenance.value
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function createWorkOrder(workOrderData) {
        loading.value = true
        error.value = null

        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.fleet.create_work_order',
                args: { work_order_data: workOrderData }
            })

            const newWorkOrder = response.message
            workOrders.value.unshift(newWorkOrder)

            return newWorkOrder
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function updateWorkOrderStatus(workOrderId, status) {
        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.fleet.update_work_order_status',
                args: {
                    work_order_id: workOrderId,
                    status: status
                }
            })

            // Update local state
            const index = workOrders.value.findIndex(wo => wo.name === workOrderId)
            if (index !== -1) {
                workOrders.value[index].status = status
            }

            return response.message
        } catch (err) {
            error.value = err.message
            throw err
        }
    }

    async function schedulePreventiveMaintenance(assetId, scheduledDate, maintenanceType) {
        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.fleet.schedule_preventive_maintenance',
                args: {
                    asset_id: assetId,
                    scheduled_date: scheduledDate,
                    maintenance_type: maintenanceType
                }
            })

            return response.message
        } catch (err) {
            error.value = err.message
            throw err
        }
    }

    function clearError() {
        error.value = null
    }

    return {
        // State
        workOrders,
        upcomingMaintenance,
        loading,
        error,

        // Computed
        totalWorkOrders,
        openWorkOrders,
        overdueCount,

        // Actions
        fetchWorkOrders,
        fetchUpcomingMaintenance,
        createWorkOrder,
        updateWorkOrderStatus,
        schedulePreventiveMaintenance,
        clearError
    }
})

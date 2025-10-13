import { defineStore } from 'pinia'
import { ref } from 'vue'
import frappeClient from '@/utils/frappeClient'

export const useCargoStore = defineStore('cargo', () => {
    const consignments = ref([])
    const loading = ref(false)
    const error = ref(null)

    async function fetchConsignments(tripId) {
        loading.value = true
        error.value = null

        try {
            const data = await frappeClient.call('tems.api.pwa.driver.get_cargo_consignments', {
                trip_id: tripId
            })
            consignments.value = data || []
            return data
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function scanBarcode(barcode, tripId) {
        loading.value = true

        try {
            const result = await frappeClient.call('tems.api.pwa.driver.scan_cargo_barcode', {
                barcode: barcode,
                trip_id: tripId
            })

            return result
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function updateDeliveryStatus(consignmentId, status, location, signature = null) {
        loading.value = true

        try {
            const result = await frappeClient.call('tems.api.pwa.driver.update_delivery_status', {
                consignment_id: consignmentId,
                status: status,
                location_data: location,
                signature: signature,
                timestamp: new Date().toISOString()
            })

            // Update local list
            const consignment = consignments.value.find(c => c.name === consignmentId)
            if (consignment) {
                consignment.status = status
            }

            return result
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    return {
        consignments,
        loading,
        error,
        fetchConsignments,
        scanBarcode,
        updateDeliveryStatus
    }
})

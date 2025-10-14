import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { frappeClient } from '@shared'

export const usePassengerStore = defineStore('passenger', () => {
    const manifest = ref(null)
    const bookings = ref([])
    const loading = ref(false)
    const error = ref(null)

    const totalSeats = computed(() => manifest.value?.total_seats || 0)
    const occupiedSeats = computed(() => bookings.value.filter(b => b.status === 'Boarded').length)
    const availableSeats = computed(() => totalSeats.value - occupiedSeats.value)

    async function fetchPassengerManifest(tripId) {
        loading.value = true
        error.value = null

        try {
            const data = await frappeClient.call('tems.api.pwa.driver.get_passenger_manifest', {
                trip_id: tripId
            })

            manifest.value = data.manifest
            bookings.value = data.bookings || []

            return data
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function scanTicket(ticketCode, tripId) {
        loading.value = true

        try {
            const result = await frappeClient.call('tems.api.pwa.driver.scan_passenger_ticket', {
                ticket_code: ticketCode,
                trip_id: tripId
            })

            // Update booking status if found
            const booking = bookings.value.find(b => b.ticket_code === ticketCode)
            if (booking) {
                booking.status = 'Boarded'
                booking.boarding_time = new Date().toISOString()
            }

            return result
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function updateBoardingStatus(bookingId, status) {
        loading.value = true

        try {
            const result = await frappeClient.call('tems.api.pwa.driver.update_boarding_status', {
                booking_id: bookingId,
                status: status,
                timestamp: new Date().toISOString()
            })

            const booking = bookings.value.find(b => b.name === bookingId)
            if (booking) {
                booking.status = status
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
        manifest,
        bookings,
        totalSeats,
        occupiedSeats,
        availableSeats,
        loading,
        error,
        fetchPassengerManifest,
        scanTicket,
        updateBoardingStatus
    }
})

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { frappeClient } from '@shared'

export const useTripStore = defineStore('trip', () => {
  const trips = ref([])
  const activeTrip = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const upcomingTrips = computed(() => 
    trips.value.filter(t => new Date(t.start_time) > new Date())
  )
  
  const inProgressTrips = computed(() => 
    trips.value.filter(t => t.status === 'Active')
  )

  async function fetchDashboard() {
    loading.value = true
    error.value = null
    
    try {
      const data = await frappeClient.call('tems.api.pwa.driver.get_driver_dashboard')
      
      trips.value = [
        ...data.journey_plans.map(jp => ({ ...jp, type: 'journey' })),
        ...data.operation_plans.map(op => ({ ...op, type: 'operation' }))
      ]
      
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchTripDetails(tripId) {
    loading.value = true
    
    try {
      const data = await frappeClient.call('tems.api.pwa.driver.get_journey_details', {
        journey_plan_name: tripId
      })
      
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function startTrip(tripId, odometerReading, locationData) {
    try {
      const result = await frappeClient.call('tems.api.pwa.driver.start_trip', {
        journey_plan_name: tripId,
        odometer_reading: odometerReading,
        location_data: locationData
      })
      
      activeTrip.value = tripId
      await fetchDashboard()
      
      return result
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  async function completeTrip(tripId, odometerReading, locationData, notes) {
    try {
      const result = await frappeClient.call('tems.api.pwa.driver.complete_trip', {
        journey_plan_name: tripId,
        odometer_reading: odometerReading,
        location_data: locationData,
        notes: notes
      })
      
      activeTrip.value = null
      await fetchDashboard()
      
      return result
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  return {
    trips,
    activeTrip,
    loading,
    error,
    upcomingTrips,
    inProgressTrips,
    fetchDashboard,
    fetchTripDetails,
    startTrip,
    completeTrip
  }
})
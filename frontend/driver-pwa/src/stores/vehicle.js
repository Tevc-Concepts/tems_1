import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import frappeClient from '@/utils/frappeClient'

export const useVehicleStore = defineStore('vehicle', () => {
  const vehicles = ref([])
  const currentVehicle = ref(null)
  const vehicleHistory = ref([])
  const fuelLogs = ref([])
  const maintenanceRecords = ref([])
  const loading = ref(false)
  const error = ref(null)

  const assignedVehicles = computed(() => 
    vehicles.value.filter(v => v.status === 'Active')
  )

  const currentVehicleDetails = computed(() => {
    if (!currentVehicle.value) return null
    
    return {
      ...currentVehicle.value,
      lastFuel: fuelLogs.value[0] || null,
      pendingMaintenance: maintenanceRecords.value.filter(
        m => m.status === 'Open' || m.status === 'In Progress'
      )
    }
  })

  async function fetchVehicleInfo(vehicleName) {
    loading.value = true
    error.value = null
    
    try {
      const data = await frappeClient.call('tems.api.pwa.driver.get_vehicle_info', {
        vehicle_name: vehicleName
      })
      
      currentVehicle.value = data.vehicle
      fuelLogs.value = data.last_fuel ? [data.last_fuel] : []
      maintenanceRecords.value = data.pending_maintenance || []
      
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchMyVehicles() {
    loading.value = true
    error.value = null
    
    try {
      // Get vehicles assigned to current driver's trips
      const trips = await frappeClient.call('tems.api.pwa.driver.get_driver_dashboard')
      
      const vehicleNames = [
        ...new Set([
          ...trips.journey_plans.map(jp => jp.vehicle),
          ...trips.operation_plans.map(op => op.vehicle)
        ].filter(Boolean))
      ]
      
      if (vehicleNames.length > 0) {
        const vehicleData = await Promise.all(
          vehicleNames.map(name => 
            frappeClient.getDoc('Vehicle', name).catch(() => null)
          )
        )
        
        vehicles.value = vehicleData.filter(Boolean)
      }
      
      return vehicles.value
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function logFuel(fuelData) {
    loading.value = true
    error.value = null
    
    try {
      const result = await frappeClient.call('tems.api.pwa.driver.log_fuel', {
        vehicle: fuelData.vehicle,
        liters: fuelData.liters,
        price_per_liter: fuelData.pricePerLiter,
        odometer: fuelData.odometer,
        station: fuelData.station,
        location_data: fuelData.locationData
      })
      
      // Add to local fuel logs
      fuelLogs.value.unshift({
        name: result.fuel_log,
        vehicle: fuelData.vehicle,
        liters: fuelData.liters,
        total_cost: result.total_cost,
        date: new Date().toISOString(),
        odometer: fuelData.odometer
      })
      
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function submitSpotCheck(checkData) {
    loading.value = true
    error.value = null
    
    try {
      // Upload photos first if any
      const uploadedPhotos = []
      if (checkData.photos && checkData.photos.length > 0) {
        for (const photo of checkData.photos) {
          if (photo.file) {
            const uploadResult = await frappeClient.uploadFile(
              photo.file,
              false,
              'Home/Vehicle Inspections'
            )
            uploadedPhotos.push({
              image: uploadResult.file_url,
              caption: photo.caption || ''
            })
          }
        }
      }
      
      const result = await frappeClient.call('tems.api.pwa.driver.submit_spot_check', {
        vehicle: checkData.vehicle,
        location: checkData.location,
        notes: checkData.notes,
        photos: uploadedPhotos
      })
      
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchFuelHistory(vehicleName, limit = 10) {
    loading.value = true
    
    try {
      const logs = await frappeClient.getList(
        'Fuel Log',
        ['name', 'date', 'liters', 'total_cost', 'odometer', 'station'],
        { vehicle: vehicleName },
        limit,
        'date desc'
      )
      
      fuelLogs.value = logs
      return logs
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchMaintenanceHistory(vehicleName, limit = 10) {
    loading.value = true
    
    try {
      const records = await frappeClient.getList(
        'Maintenance Work Order',
        ['name', 'status', 'planned_date', 'completion_date', 'cost', 'vendor'],
        { vehicle: vehicleName },
        limit,
        'planned_date desc'
      )
      
      maintenanceRecords.value = records
      return records
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function getVehicleUtilization(vehicleName, startDate, endDate) {
    try {
      const data = await frappeClient.getList(
        'Asset Utilization Log',
        ['log_date', 'utilization_hours'],
        { 
          vehicle: vehicleName,
          log_date: ['between', [startDate, endDate]]
        },
        100,
        'log_date desc'
      )
      
      return data
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  function setCurrentVehicle(vehicle) {
    currentVehicle.value = vehicle
  }

  function clearCurrentVehicle() {
    currentVehicle.value = null
    fuelLogs.value = []
    maintenanceRecords.value = []
  }

  return {
    vehicles,
    currentVehicle,
    vehicleHistory,
    fuelLogs,
    maintenanceRecords,
    loading,
    error,
    assignedVehicles,
    currentVehicleDetails,
    fetchVehicleInfo,
    fetchMyVehicles,
    logFuel,
    submitSpotCheck,
    fetchFuelHistory,
    fetchMaintenanceHistory,
    getVehicleUtilization,
    setCurrentVehicle,
    clearCurrentVehicle
  }
})
import { ref, onUnmounted } from 'vue'

/**
 * Geolocation composable with tracking capabilities
 * Provides GPS coordinates and location tracking
 * 
 * @param {object} options - Geolocation options
 * @returns {object} Geolocation state and methods
 * 
 * @example
 * ```javascript
 * import { useGeolocation } from '@shared/composables/useGeolocation'
 * 
 * const { coords, getCurrentPosition, startWatching, stopWatching } = useGeolocation()
 * 
 * // Get current position once
 * await getCurrentPosition()
 * console.log(coords.value.latitude, coords.value.longitude)
 * 
 * // Start continuous tracking
 * startWatching()
 * 
 * // Stop tracking
 * stopWatching()
 * ```
 */
export function useGeolocation(options = {}) {
    const coords = ref(null)
    const error = ref(null)
    const loading = ref(false)
    const watchId = ref(null)
    const isWatching = ref(false)

    const defaultOptions = {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0,
        ...options
    }

    /**
     * Get current position once
     */
    async function getCurrentPosition() {
        loading.value = true
        error.value = null

        return new Promise((resolve, reject) => {
            if (!navigator.geolocation) {
                const err = new Error('Geolocation is not supported by your browser')
                error.value = err
                loading.value = false
                reject(err)
                return
            }

            navigator.geolocation.getCurrentPosition(
                (position) => {
                    coords.value = {
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude,
                        accuracy: position.coords.accuracy,
                        altitude: position.coords.altitude,
                        altitudeAccuracy: position.coords.altitudeAccuracy,
                        heading: position.coords.heading,
                        speed: position.coords.speed,
                        timestamp: position.timestamp
                    }
                    loading.value = false
                    resolve(coords.value)
                },
                (err) => {
                    error.value = err
                    loading.value = false
                    reject(err)
                },
                defaultOptions
            )
        })
    }

    /**
     * Start continuous position tracking
     */
    function startWatching() {
        if (!navigator.geolocation) {
            error.value = new Error('Geolocation is not supported by your browser')
            return
        }

        if (watchId.value) {
            stopWatching()
        }

        watchId.value = navigator.geolocation.watchPosition(
            (position) => {
                coords.value = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude,
                    accuracy: position.coords.accuracy,
                    altitude: position.coords.altitude,
                    altitudeAccuracy: position.coords.altitudeAccuracy,
                    heading: position.coords.heading,
                    speed: position.coords.speed,
                    timestamp: position.timestamp
                }
                error.value = null
                isWatching.value = true
            },
            (err) => {
                error.value = err
                isWatching.value = false
            },
            defaultOptions
        )
    }

    /**
     * Stop position tracking
     */
    function stopWatching() {
        if (watchId.value !== null) {
            navigator.geolocation.clearWatch(watchId.value)
            watchId.value = null
            isWatching.value = false
        }
    }

    /**
     * Calculate distance between two coordinates (Haversine formula)
     * @param {number} lat1 - Latitude 1
     * @param {number} lon1 - Longitude 1
     * @param {number} lat2 - Latitude 2
     * @param {number} lon2 - Longitude 2
     * @returns {number} Distance in meters
     */
    function calculateDistance(lat1, lon1, lat2, lon2) {
        const R = 6371e3 // Earth's radius in meters
        const φ1 = lat1 * Math.PI / 180
        const φ2 = lat2 * Math.PI / 180
        const Δφ = (lat2 - lat1) * Math.PI / 180
        const Δλ = (lon2 - lon1) * Math.PI / 180

        const a = Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
            Math.cos(φ1) * Math.cos(φ2) *
            Math.sin(Δλ / 2) * Math.sin(Δλ / 2)
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))

        return R * c
    }

    /**
     * Calculate bearing between two coordinates
     * @param {number} lat1 - Latitude 1
     * @param {number} lon1 - Longitude 1
     * @param {number} lat2 - Latitude 2
     * @param {number} lon2 - Longitude 2
     * @returns {number} Bearing in degrees (0-360)
     */
    function calculateBearing(lat1, lon1, lat2, lon2) {
        const φ1 = lat1 * Math.PI / 180
        const φ2 = lat2 * Math.PI / 180
        const Δλ = (lon2 - lon1) * Math.PI / 180

        const y = Math.sin(Δλ) * Math.cos(φ2)
        const x = Math.cos(φ1) * Math.sin(φ2) -
            Math.sin(φ1) * Math.cos(φ2) * Math.cos(Δλ)
        const θ = Math.atan2(y, x)
        const bearing = (θ * 180 / Math.PI + 360) % 360

        return bearing
    }

    /**
     * Format coordinates as string
     * @param {number} lat - Latitude
     * @param {number} lng - Longitude
     * @returns {string} Formatted coordinates
     */
    function formatCoords(lat, lng) {
        if (lat === null || lat === undefined || lng === null || lng === undefined) {
            return 'N/A'
        }
        return `${lat.toFixed(6)}, ${lng.toFixed(6)}`
    }

    /**
     * Check if coordinates are valid
     * @param {number} lat - Latitude
     * @param {number} lng - Longitude
     * @returns {boolean}
     */
    function isValidCoords(lat, lng) {
        return (
            typeof lat === 'number' &&
            typeof lng === 'number' &&
            lat >= -90 &&
            lat <= 90 &&
            lng >= -180 &&
            lng <= 180
        )
    }

    // Cleanup on unmount
    onUnmounted(() => {
        stopWatching()
    })

    return {
        // State
        coords,
        error,
        loading,
        isWatching,

        // Actions
        getCurrentPosition,
        startWatching,
        stopWatching,

        // Utilities
        calculateDistance,
        calculateBearing,
        formatCoords,
        isValidCoords
    }
}

/**
 * Formatting utilities for TEMS PWAs
 */

import { format, formatDistance as formatDateDistance, formatRelative, parseISO, isValid } from 'date-fns'

/**
 * Format date to localized string
 * @param {string|Date} date - Date to format
 * @param {string} formatStr - Format string (date-fns format)
 * @returns {string}
 */
export function formatDate(date, formatStr = 'MMM dd, yyyy') {
    if (!date) return '-'
    const d = typeof date === 'string' ? parseISO(date) : date
    if (!isValid(d)) return '-'
    return format(d, formatStr)
}

/**
 * Format datetime to localized string
 * @param {string|Date} datetime - Datetime to format
 * @param {string} formatStr - Format string
 * @returns {string}
 */
export function formatDatetime(datetime, formatStr = 'MMM dd, yyyy HH:mm') {
    if (!datetime) return '-'
    const d = typeof datetime === 'string' ? parseISO(datetime) : datetime
    if (!isValid(d)) return '-'
    return format(d, formatStr)
}

/**
 * Format time only
 * @param {string|Date} time - Time to format
 * @param {string} formatStr - Format string
 * @returns {string}
 */
export function formatTime(time, formatStr = 'HH:mm') {
    if (!time) return '-'
    const d = typeof time === 'string' ? parseISO(time) : time
    if (!isValid(d)) return '-'
    return format(d, formatStr)
}

/**
 * Format relative time (e.g., "2 hours ago")
 * @param {string|Date} date - Date to format
 * @returns {string}
 */
export function formatRelativeTime(date) {
    if (!date) return '-'
    const d = typeof date === 'string' ? parseISO(date) : date
    if (!isValid(d)) return '-'
    return formatDateDistance(d, new Date(), { addSuffix: true })
}

/**
 * Format relative date (e.g., "yesterday at 5:30 PM")
 * @param {string|Date} date - Date to format
 * @returns {string}
 */
export function formatRelativeDate(date) {
    if (!date) return '-'
    const d = typeof date === 'string' ? parseISO(date) : date
    if (!isValid(d)) return '-'
    return formatRelative(d, new Date())
}

/**
 * Format duration in minutes to human readable
 * @param {number} minutes - Duration in minutes
 * @returns {string}
 */
export function formatDuration(minutes) {
    if (!minutes || minutes === 0) return '0m'

    const hours = Math.floor(minutes / 60)
    const mins = minutes % 60

    if (hours === 0) return `${mins}m`
    if (mins === 0) return `${hours}h`
    return `${hours}h ${mins}m`
}

/**
 * Format number with thousands separator
 * @param {number} num - Number to format
 * @param {number} decimals - Decimal places
 * @returns {string}
 */
export function formatNumber(num, decimals = 0) {
    if (num === null || num === undefined) return '-'
    return new Intl.NumberFormat('en-US', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    }).format(num)
}

/**
 * Format currency
 * @param {number} amount - Amount to format
 * @param {string} currency - Currency code (USD, EUR, etc.)
 * @param {string} locale - Locale for formatting
 * @returns {string}
 */
export function formatCurrency(amount, currency = 'USD', locale = 'en-US') {
    if (amount === null || amount === undefined) return '-'
    return new Intl.NumberFormat(locale, {
        style: 'currency',
        currency: currency
    }).format(amount)
}

/**
 * Format percentage
 * @param {number} value - Value to format
 * @param {number} decimals - Decimal places
 * @returns {string}
 */
export function formatPercent(value, decimals = 1) {
    if (value === null || value === undefined) return '-'
    return `${formatNumber(value, decimals)}%`
}

/**
 * Format distance in meters/kilometers
 * @param {number} meters - Distance in meters
 * @returns {string}
 */
export function formatDistance(meters) {
    if (!meters || meters === 0) return '0m'

    if (meters < 1000) {
        return `${Math.round(meters)}m`
    }

    const km = meters / 1000
    return `${formatNumber(km, km < 10 ? 2 : 1)}km`
}

/**
 * Format coordinates (latitude, longitude)
 * @param {number} lat - Latitude
 * @param {number} lng - Longitude
 * @returns {string}
 */
export function formatCoordinates(lat, lng) {
    if (!lat || !lng) return 'No location'
    return `${lat.toFixed(6)}°, ${lng.toFixed(6)}°`
}

/**
 * Format speed
 * @param {number} kmh - Speed in km/h
 * @returns {string}
 */
export function formatSpeed(kmh) {
    if (!kmh || kmh === 0) return '0 km/h'
    return `${formatNumber(kmh, 1)} km/h`
}

/**
 * Format fuel consumption
 * @param {number} liters - Liters
 * @returns {string}
 */
export function formatFuel(liters) {
    if (!liters || liters === 0) return '0L'
    return `${formatNumber(liters, 2)}L`
}

/**
 * Format fuel efficiency
 * @param {number} kmPerLiter - Km per liter
 * @returns {string}
 */
export function formatFuelEfficiency(kmPerLiter) {
    if (!kmPerLiter || kmPerLiter === 0) return '-'
    return `${formatNumber(kmPerLiter, 2)} km/L`
}

/**
 * Format phone number
 * @param {string} phone - Phone number
 * @param {string} format - Format pattern
 * @returns {string}
 */
export function formatPhone(phone, format = 'international') {
    if (!phone) return '-'

    // Remove all non-numeric characters
    const cleaned = phone.replace(/\D/g, '')

    if (format === 'international' && cleaned.length >= 10) {
        const country = cleaned.slice(0, -10)
        const area = cleaned.slice(-10, -7)
        const first = cleaned.slice(-7, -4)
        const last = cleaned.slice(-4)
        return `${country ? '+' + country + ' ' : ''}(${area}) ${first}-${last}`
    }

    return phone
}

/**
 * Format license plate
 * @param {string} plate - License plate
 * @returns {string}
 */
export function formatLicensePlate(plate) {
    if (!plate) return '-'
    return plate.toUpperCase().trim()
}

/**
 * Format VIN
 * @param {string} vin - Vehicle Identification Number
 * @returns {string}
 */
export function formatVIN(vin) {
    if (!vin) return '-'
    return vin.toUpperCase().trim()
}

/**
 * Format status badge
 * @param {string} status - Status value
 * @returns {string}
 */
export function formatStatus(status) {
    if (!status) return '-'
    return status.replace(/_/g, ' ').split(' ').map(word =>
        word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
    ).join(' ')
}

/**
 * Format file size
 * @param {number} bytes - File size in bytes
 * @returns {string}
 */
export function formatFileSize(bytes) {
    if (!bytes || bytes === 0) return '0 B'

    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))

    return `${formatNumber(bytes / Math.pow(k, i), 2)} ${sizes[i]}`
}

/**
 * Format GPS coordinates
 * @param {number} lat - Latitude
 * @param {number} lng - Longitude
 * @returns {string}
 */
export function formatGPS(lat, lng) {
    if (lat === null || lat === undefined || lng === null || lng === undefined) return '-'
    return `${lat.toFixed(6)}, ${lng.toFixed(6)}`
}

/**
 * Format address
 * @param {object} address - Address object
 * @returns {string}
 */
export function formatAddress(address) {
    if (!address) return '-'

    const parts = []
    if (address.address_line1) parts.push(address.address_line1)
    if (address.address_line2) parts.push(address.address_line2)
    if (address.city) parts.push(address.city)
    if (address.state) parts.push(address.state)
    if (address.postal_code) parts.push(address.postal_code)
    if (address.country) parts.push(address.country)

    return parts.join(', ') || '-'
}

/**
 * Format name (proper case)
 * @param {string} name - Name to format
 * @returns {string}
 */
export function formatName(name) {
    if (!name) return '-'
    return name.split(' ').map(word =>
        word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
    ).join(' ')
}

/**
 * Format initials
 * @param {string} name - Full name
 * @returns {string}
 */
export function formatInitials(name) {
    if (!name) return '?'
    return name
        .split(' ')
        .map(word => word.charAt(0).toUpperCase())
        .slice(0, 2)
        .join('')
}

/**
 * Format list to comma-separated string
 * @param {Array} items - Items to format
 * @param {string} property - Property to extract (optional)
 * @returns {string}
 */
export function formatList(items, property = null) {
    if (!items || items.length === 0) return '-'

    const values = property
        ? items.map(item => item[property])
        : items

    if (values.length === 1) return values[0]
    if (values.length === 2) return values.join(' and ')

    const last = values.pop()
    return `${values.join(', ')}, and ${last}`
}

/**
 * Format boolean as Yes/No
 * @param {boolean} value - Boolean value
 * @returns {string}
 */
export function formatBoolean(value) {
    return value ? 'Yes' : 'No'
}

/**
 * Truncate text with ellipsis
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length
 * @returns {string}
 */
export function truncateText(text, maxLength = 50) {
    if (!text) return '-'
    if (text.length <= maxLength) return text
    return text.slice(0, maxLength) + '...'
}

/**
 * Format score/rating
 * @param {number} score - Score value
 * @param {number} maxScore - Maximum score
 * @returns {string}
 */
export function formatScore(score, maxScore = 100) {
    if (score === null || score === undefined) return '-'
    return `${formatNumber(score)}/${maxScore}`
}

/**
 * Format temperature
 * @param {number} celsius - Temperature in Celsius
 * @param {string} unit - Display unit ('C' or 'F')
 * @returns {string}
 */
export function formatTemperature(celsius, unit = 'C') {
    if (celsius === null || celsius === undefined) return '-'

    if (unit === 'F') {
        const fahrenheit = (celsius * 9 / 5) + 32
        return `${formatNumber(fahrenheit, 1)}°F`
    }

    return `${formatNumber(celsius, 1)}°C`
}

/**
 * Sanitize HTML to prevent XSS
 * @param {string} html - HTML string
 * @returns {string}
 */
export function sanitizeHtml(html) {
    if (!html) return ''
    const temp = document.createElement('div')
    temp.textContent = html
    return temp.innerHTML
}

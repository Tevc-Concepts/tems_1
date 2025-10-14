/**
 * Helper utilities for TEMS PWAs
 */

/**
 * Debounce function execution
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in ms
 * @returns {Function}
 */
export function debounce(func, wait = 300) {
    let timeout
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout)
            func(...args)
        }
        clearTimeout(timeout)
        timeout = setTimeout(later, wait)
    }
}

/**
 * Throttle function execution
 * @param {Function} func - Function to throttle
 * @param {number} limit - Time limit in ms
 * @returns {Function}
 */
export function throttle(func, limit = 300) {
    let inThrottle
    return function (...args) {
        if (!inThrottle) {
            func.apply(this, args)
            inThrottle = true
            setTimeout(() => inThrottle = false, limit)
        }
    }
}

/**
 * Deep clone an object
 * @param {any} obj - Object to clone
 * @returns {any}
 */
export function deepClone(obj) {
    if (obj === null || typeof obj !== 'object') return obj
    if (obj instanceof Date) return new Date(obj.getTime())
    if (obj instanceof Array) return obj.map(item => deepClone(item))
    if (obj instanceof Object) {
        const clonedObj = {}
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                clonedObj[key] = deepClone(obj[key])
            }
        }
        return clonedObj
    }
}

/**
 * Generate a unique ID
 * @returns {string}
 */
export function generateId() {
    return `${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
}

/**
 * Sleep for specified milliseconds
 * @param {number} ms - Milliseconds to sleep
 * @returns {Promise<void>}
 */
export function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
}

/**
 * Safely parse JSON
 * @param {string} json - JSON string
 * @param {any} fallback - Fallback value
 * @returns {any}
 */
export function safeJsonParse(json, fallback = null) {
    try {
        return JSON.parse(json)
    } catch {
        return fallback
    }
}

/**
 * Check if value is empty
 * @param {any} value - Value to check
 * @returns {boolean}
 */
export function isEmpty(value) {
    if (value === null || value === undefined) return true
    if (typeof value === 'string') return value.trim().length === 0
    if (Array.isArray(value)) return value.length === 0
    if (typeof value === 'object') return Object.keys(value).length === 0
    return false
}

/**
 * Capitalize first letter of string
 * @param {string} str - String to capitalize
 * @returns {string}
 */
export function capitalize(str) {
    if (!str) return ''
    return str.charAt(0).toUpperCase() + str.slice(1)
}

/**
 * Truncate string with ellipsis
 * @param {string} str - String to truncate
 * @param {number} maxLength - Maximum length
 * @returns {string}
 */
export function truncate(str, maxLength = 50) {
    if (!str || str.length <= maxLength) return str
    return str.slice(0, maxLength) + '...'
}

/**
 * Get nested object property safely
 * @param {object} obj - Object to traverse
 * @param {string} path - Dot-notation path
 * @param {any} defaultValue - Default value if not found
 * @returns {any}
 */
export function getNestedProperty(obj, path, defaultValue = null) {
    const keys = path.split('.')
    let result = obj

    for (const key of keys) {
        if (result && typeof result === 'object' && key in result) {
            result = result[key]
        } else {
            return defaultValue
        }
    }

    return result
}

/**
 * Convert bytes to human readable format
 * @param {number} bytes - Bytes
 * @returns {string}
 */
export function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes'

    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))

    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

/**
 * Group array by key
 * @param {Array} array - Array to group
 * @param {string} key - Key to group by
 * @returns {object}
 */
export function groupBy(array, key) {
    return array.reduce((result, item) => {
        const groupKey = item[key]
        if (!result[groupKey]) {
            result[groupKey] = []
        }
        result[groupKey].push(item)
        return result
    }, {})
}

/**
 * Sort array of objects by key
 * @param {Array} array - Array to sort
 * @param {string} key - Key to sort by
 * @param {boolean} ascending - Sort order
 * @returns {Array}
 */
export function sortBy(array, key, ascending = true) {
    return [...array].sort((a, b) => {
        const aVal = getNestedProperty(a, key)
        const bVal = getNestedProperty(b, key)

        if (aVal < bVal) return ascending ? -1 : 1
        if (aVal > bVal) return ascending ? 1 : -1
        return 0
    })
}

/**
 * Filter array by multiple criteria
 * @param {Array} array - Array to filter
 * @param {object} filters - Filter criteria
 * @returns {Array}
 */
export function filterBy(array, filters) {
    return array.filter(item => {
        return Object.entries(filters).every(([key, value]) => {
            const itemValue = getNestedProperty(item, key)
            if (Array.isArray(value)) {
                return value.includes(itemValue)
            }
            return itemValue === value
        })
    })
}

/**
 * Remove duplicates from array
 * @param {Array} array - Array with duplicates
 * @param {string} key - Optional key for objects
 * @returns {Array}
 */
export function unique(array, key = null) {
    if (!key) {
        return [...new Set(array)]
    }

    const seen = new Set()
    return array.filter(item => {
        const value = getNestedProperty(item, key)
        if (seen.has(value)) return false
        seen.add(value)
        return true
    })
}

/**
 * Copy text to clipboard
 * @param {string} text - Text to copy
 * @returns {Promise<boolean>}
 */
export async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text)
        return true
    } catch {
        // Fallback for older browsers
        const textarea = document.createElement('textarea')
        textarea.value = text
        textarea.style.position = 'fixed'
        textarea.style.opacity = '0'
        document.body.appendChild(textarea)
        textarea.select()
        const success = document.execCommand('copy')
        document.body.removeChild(textarea)
        return success
    }
}

/**
 * Download data as file
 * @param {string} data - Data to download
 * @param {string} filename - File name
 * @param {string} type - MIME type
 */
export function downloadFile(data, filename, type = 'text/plain') {
    const blob = new Blob([data], { type })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    link.click()
    window.URL.revokeObjectURL(url)
}

/**
 * Check if device is mobile
 * @returns {boolean}
 */
export function isMobile() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
}

/**
 * Check if app is in standalone mode (PWA)
 * @returns {boolean}
 */
export function isStandalone() {
    return window.matchMedia('(display-mode: standalone)').matches ||
        window.navigator.standalone === true
}

/**
 * Get query parameters from URL
 * @returns {object}
 */
export function getQueryParams() {
    const params = {}
    const searchParams = new URLSearchParams(window.location.search)
    for (const [key, value] of searchParams) {
        params[key] = value
    }
    return params
}

/**
 * Build query string from object
 * @param {object} params - Parameters object
 * @returns {string}
 */
export function buildQueryString(params) {
    const searchParams = new URLSearchParams()
    Object.entries(params).forEach(([key, value]) => {
        if (value !== null && value !== undefined) {
            searchParams.append(key, value)
        }
    })
    return searchParams.toString()
}

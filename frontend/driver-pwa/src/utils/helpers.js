import { format, parseISO } from 'date-fns'

export function formatDateTime(dateString, formatStr = 'PPp') {
    if (!dateString) return 'N/A'
    try {
        return format(parseISO(dateString), formatStr)
    } catch (error) {
        return 'Invalid Date'
    }
}

export function formatDate(dateString, formatStr = 'PP') {
    if (!dateString) return 'N/A'
    try {
        return format(parseISO(dateString), formatStr)
    } catch (error) {
        return 'Invalid Date'
    }
}

export function formatTime(dateString, formatStr = 'p') {
    if (!dateString) return 'N/A'
    try {
        return format(parseISO(dateString), formatStr)
    } catch (error) {
        return 'Invalid Time'
    }
}

export function truncate(str, length = 50) {
    if (!str) return ''
    return str.length > length ? str.substring(0, length) + '...' : str
}

export function capitalize(str) {
    if (!str) return ''
    return str.charAt(0).toUpperCase() + str.slice(1)
}

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

export function throttle(func, limit = 300) {
    let inThrottle
    return function (...args) {
        if (!inThrottle) {
            func.apply(this, args)
            inThrottle = true
            setTimeout(() => (inThrottle = false), limit)
        }
    }
}

export function isEmpty(value) {
    if (value === null || value === undefined) return true
    if (typeof value === 'string') return value.trim().length === 0
    if (Array.isArray(value)) return value.length === 0
    if (typeof value === 'object') return Object.keys(value).length === 0
    return false
}

export function generateId() {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
}

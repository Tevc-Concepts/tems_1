/**
 * Validation utilities for TEMS PWAs
 */

/**
 * Validate email format
 * @param {string} email - Email to validate
 * @returns {boolean}
 */
export function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return re.test(email)
}

/**
 * Validate phone number
 * @param {string} phone - Phone number to validate
 * @returns {boolean}
 */
export function isValidPhone(phone) {
    // Accepts various formats: +1234567890, (123) 456-7890, 123-456-7890, etc.
    const re = /^[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,9}$/
    return re.test(phone.replace(/\s/g, ''))
}

/**
 * Validate required field
 * @param {any} value - Value to validate
 * @returns {boolean}
 */
export function isRequired(value) {
    if (value === null || value === undefined) return false
    if (typeof value === 'string') return value.trim().length > 0
    if (Array.isArray(value)) return value.length > 0
    if (typeof value === 'object') return Object.keys(value).length > 0
    return true
}

/**
 * Validate minimum length
 * @param {string} value - Value to validate
 * @param {number} min - Minimum length
 * @returns {boolean}
 */
export function minLength(value, min) {
    if (!value) return false
    return value.length >= min
}

/**
 * Validate maximum length
 * @param {string} value - Value to validate
 * @param {number} max - Maximum length
 * @returns {boolean}
 */
export function maxLength(value, max) {
    if (!value) return true
    return value.length <= max
}

/**
 * Validate numeric value
 * @param {any} value - Value to validate
 * @returns {boolean}
 */
export function isNumeric(value) {
    return !isNaN(parseFloat(value)) && isFinite(value)
}

/**
 * Validate min value
 * @param {number} value - Value to validate
 * @param {number} min - Minimum value
 * @returns {boolean}
 */
export function minValue(value, min) {
    return isNumeric(value) && parseFloat(value) >= min
}

/**
 * Validate max value
 * @param {number} value - Value to validate
 * @param {number} max - Maximum value
 * @returns {boolean}
 */
export function maxValue(value, max) {
    return isNumeric(value) && parseFloat(value) <= max
}

/**
 * Validate date format (YYYY-MM-DD)
 * @param {string} date - Date string to validate
 * @returns {boolean}
 */
export function isValidDate(date) {
    if (!date) return false
    const re = /^\d{4}-\d{2}-\d{2}$/
    if (!re.test(date)) return false

    const d = new Date(date)
    return d instanceof Date && !isNaN(d)
}

/**
 * Validate datetime format
 * @param {string} datetime - Datetime string to validate
 * @returns {boolean}
 */
export function isValidDatetime(datetime) {
    if (!datetime) return false
    const d = new Date(datetime)
    return d instanceof Date && !isNaN(d)
}

/**
 * Validate future date
 * @param {string} date - Date string
 * @returns {boolean}
 */
export function isFutureDate(date) {
    if (!isValidDate(date)) return false
    const d = new Date(date)
    return d > new Date()
}

/**
 * Validate past date
 * @param {string} date - Date string
 * @returns {boolean}
 */
export function isPastDate(date) {
    if (!isValidDate(date)) return false
    const d = new Date(date)
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    return d < today
}

/**
 * Validate URL format
 * @param {string} url - URL to validate
 * @returns {boolean}
 */
export function isValidUrl(url) {
    try {
        new URL(url)
        return true
    } catch {
        return false
    }
}

/**
 * Validate GPS coordinates
 * @param {number} lat - Latitude
 * @param {number} lng - Longitude
 * @returns {boolean}
 */
export function isValidGPS(lat, lng) {
    return (
        isNumeric(lat) &&
        isNumeric(lng) &&
        lat >= -90 &&
        lat <= 90 &&
        lng >= -180 &&
        lng <= 180
    )
}

/**
 * Validate barcode format
 * @param {string} barcode - Barcode to validate
 * @returns {boolean}
 */
export function isValidBarcode(barcode) {
    // Accepts alphanumeric barcodes
    const re = /^[A-Z0-9\-_]+$/i
    return re.test(barcode)
}

/**
 * Validate license plate
 * @param {string} plate - License plate
 * @returns {boolean}
 */
export function isValidLicensePlate(plate) {
    // Flexible format for various countries
    const re = /^[A-Z0-9\s\-]+$/i
    return re.test(plate) && plate.length >= 3
}

/**
 * Validate VIN (Vehicle Identification Number)
 * @param {string} vin - VIN to validate
 * @returns {boolean}
 */
export function isValidVIN(vin) {
    // Standard VIN is 17 characters, alphanumeric (no I, O, Q)
    const re = /^[A-HJ-NPR-Z0-9]{17}$/i
    return re.test(vin)
}

/**
 * Validate file size
 * @param {File} file - File object
 * @param {number} maxSizeMB - Maximum size in MB
 * @returns {boolean}
 */
export function isValidFileSize(file, maxSizeMB = 10) {
    if (!file) return false
    const maxBytes = maxSizeMB * 1024 * 1024
    return file.size <= maxBytes
}

/**
 * Validate file type
 * @param {File} file - File object
 * @param {string[]} allowedTypes - Allowed MIME types
 * @returns {boolean}
 */
export function isValidFileType(file, allowedTypes = []) {
    if (!file || allowedTypes.length === 0) return true
    return allowedTypes.some(type => {
        if (type.endsWith('/*')) {
            return file.type.startsWith(type.slice(0, -2))
        }
        return file.type === type
    })
}

/**
 * Validate image file
 * @param {File} file - File object
 * @returns {boolean}
 */
export function isValidImage(file) {
    return isValidFileType(file, ['image/jpeg', 'image/png', 'image/gif', 'image/webp'])
}

/**
 * Validate password strength
 * @param {string} password - Password to validate
 * @returns {object} { valid: boolean, strength: string, message: string }
 */
export function validatePassword(password) {
    if (!password || password.length < 8) {
        return { valid: false, strength: 'weak', message: 'Password must be at least 8 characters' }
    }

    let strength = 0
    const checks = {
        lowercase: /[a-z]/.test(password),
        uppercase: /[A-Z]/.test(password),
        numbers: /\d/.test(password),
        special: /[!@#$%^&*(),.?":{}|<>]/.test(password),
        length: password.length >= 12
    }

    strength = Object.values(checks).filter(Boolean).length

    if (strength < 3) {
        return { valid: false, strength: 'weak', message: 'Password is too weak' }
    } else if (strength === 3) {
        return { valid: true, strength: 'medium', message: 'Password strength is medium' }
    } else {
        return { valid: true, strength: 'strong', message: 'Password is strong' }
    }
}

/**
 * Create a validation schema
 * @param {object} rules - Validation rules
 * @returns {Function}
 */
export function createValidator(rules) {
    return (data) => {
        const errors = {}

        for (const [field, fieldRules] of Object.entries(rules)) {
            const value = data[field]
            const fieldErrors = []

            for (const rule of fieldRules) {
                const { validator, message } = rule
                if (!validator(value, data)) {
                    fieldErrors.push(message)
                }
            }

            if (fieldErrors.length > 0) {
                errors[field] = fieldErrors
            }
        }

        return {
            valid: Object.keys(errors).length === 0,
            errors
        }
    }
}

/**
 * Common validation rules
 */
export const rules = {
    required: (message = 'This field is required') => ({
        validator: isRequired,
        message
    }),

    email: (message = 'Invalid email address') => ({
        validator: isValidEmail,
        message
    }),

    phone: (message = 'Invalid phone number') => ({
        validator: isValidPhone,
        message
    }),

    minLength: (min, message = `Minimum length is ${min}`) => ({
        validator: (value) => minLength(value, min),
        message
    }),

    maxLength: (max, message = `Maximum length is ${max}`) => ({
        validator: (value) => maxLength(value, max),
        message
    }),

    numeric: (message = 'Must be a number') => ({
        validator: isNumeric,
        message
    }),

    minValue: (min, message = `Minimum value is ${min}`) => ({
        validator: (value) => minValue(value, min),
        message
    }),

    maxValue: (max, message = `Maximum value is ${max}`) => ({
        validator: (value) => maxValue(value, max),
        message
    }),

    date: (message = 'Invalid date') => ({
        validator: isValidDate,
        message
    }),

    futureDate: (message = 'Date must be in the future') => ({
        validator: isFutureDate,
        message
    }),

    pastDate: (message = 'Date must be in the past') => ({
        validator: isPastDate,
        message
    }),

    url: (message = 'Invalid URL') => ({
        validator: isValidUrl,
        message
    }),

    custom: (validator, message) => ({
        validator,
        message
    })
}

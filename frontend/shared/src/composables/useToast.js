import { ref, computed } from 'vue'

/**
 * Toast notification composable
 * Provides methods to show toast notifications
 * 
 * @returns {object} Toast state and methods
 * 
 * @example
 * ```javascript
 * import { useToast } from '@shared/composables/useToast'
 * 
 * const toast = useToast()
 * 
 * // Show different types
 * toast.success('Operation completed!')
 * toast.error('Something went wrong')
 * toast.warning('Please be careful')
 * toast.info('New message received')
 * 
 * // Custom duration
 * toast.success('Saved!', 5000)
 * 
 * // Manual dismiss
 * const id = toast.info('Loading...')
 * // Later...
 * toast.dismiss(id)
 * ```
 */

// Global toast state (shared across all components)
const toasts = ref([])
let nextId = 0

export function useToast() {
    const activeToasts = computed(() => toasts.value)

    /**
     * Show a toast notification
     * @param {string} message - Toast message
     * @param {string} type - Toast type (success, error, warning, info)
     * @param {number} duration - Duration in ms (0 = no auto-dismiss)
     * @returns {number} Toast ID
     */
    function show(message, type = 'info', duration = 3000) {
        const id = nextId++

        const toast = {
            id,
            message,
            type,
            visible: true,
            timestamp: Date.now()
        }

        toasts.value.push(toast)

        // Auto-dismiss
        if (duration > 0) {
            setTimeout(() => {
                dismiss(id)
            }, duration)
        }

        return id
    }

    /**
     * Dismiss a toast
     * @param {number} toastId - Toast ID to dismiss
     */
    function dismiss(toastId) {
        const index = toasts.value.findIndex(t => t.id === toastId)
        if (index > -1) {
            toasts.value.splice(index, 1)
        }
    }

    /**
     * Dismiss all toasts
     */
    function dismissAll() {
        toasts.value = []
    }

    /**
     * Show success toast
     * @param {string} message - Message
     * @param {number} duration - Duration in ms
     * @returns {number} Toast ID
     */
    function success(message, duration = 3000) {
        return show(message, 'success', duration)
    }

    /**
     * Show error toast
     * @param {string} message - Message
     * @param {number} duration - Duration in ms (0 = manual dismiss)
     * @returns {number} Toast ID
     */
    function error(message, duration = 5000) {
        return show(message, 'error', duration)
    }

    /**
     * Show warning toast
     * @param {string} message - Message
     * @param {number} duration - Duration in ms
     * @returns {number} Toast ID
     */
    function warning(message, duration = 4000) {
        return show(message, 'warning', duration)
    }

    /**
     * Show info toast
     * @param {string} message - Message
     * @param {number} duration - Duration in ms
     * @returns {number} Toast ID
     */
    function info(message, duration = 3000) {
        return show(message, 'info', duration)
    }

    /**
     * Show loading toast (no auto-dismiss)
     * @param {string} message - Message
     * @returns {number} Toast ID (use to dismiss later)
     */
    function loading(message = 'Loading...') {
        return show(message, 'info', 0)
    }

    /**
     * Show promise toast
     * Automatically shows loading, then success or error
     * @param {Promise} promise - Promise to track
     * @param {object} messages - Messages for each state
     * @returns {Promise}
     */
    async function promise(promise, messages = {}) {
        const {
            loading: loadingMsg = 'Loading...',
            success: successMsg = 'Success!',
            error: errorMsg = 'Error occurred'
        } = messages

        const loadingId = show(loadingMsg, 'info', 0)

        try {
            const result = await promise
            dismiss(loadingId)
            success(successMsg)
            return result
        } catch (err) {
            dismiss(loadingId)
            error(errorMsg + (err.message ? `: ${err.message}` : ''))
            throw err
        }
    }

    return {
        // State
        toasts: activeToasts,

        // Methods
        show,
        dismiss,
        dismissAll,
        success,
        error,
        warning,
        info,
        loading,
        promise
    }
}

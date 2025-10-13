import { ref } from 'vue'

const toasts = ref([])
let idCounter = 0

export function useToast() {
    const showToast = (message, type = 'info', duration = 5000) => {
        const id = ++idCounter
        const toast = {
            id,
            message,
            type, // 'success', 'error', 'warning', 'info'
            duration,
        }

        toasts.value.push(toast)

        if (duration > 0) {
            setTimeout(() => {
                removeToast(id)
            }, duration)
        }

        return id
    }

    const removeToast = (id) => {
        const index = toasts.value.findIndex(t => t.id === id)
        if (index > -1) {
            toasts.value.splice(index, 1)
        }
    }

    return {
        toasts,
        showToast,
        removeToast,
    }
}

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import frappeClient from '@/utils/frappeClient'

export const useCommunicationStore = defineStore('communication', () => {
    const messages = ref([])
    const notifications = ref([])
    const unreadCount = ref(0)
    const loading = ref(false)
    const error = ref(null)

    const unreadNotifications = computed(() =>
        notifications.value.filter(n => !n.read)
    )

    async function fetchMessages() {
        loading.value = true
        error.value = null

        try {
            const data = await frappeClient.call('tems.api.pwa.driver.get_messages')
            messages.value = data || []
            return data
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function sendMessage(recipientType, recipientId, message) {
        loading.value = true

        try {
            const result = await frappeClient.call('tems.api.pwa.driver.send_message', {
                recipient_type: recipientType,
                recipient_id: recipientId,
                message: message,
                timestamp: new Date().toISOString()
            })

            // Add to local messages
            messages.value.push({
                ...result,
                sender: 'me',
                message: message,
                timestamp: new Date().toISOString()
            })

            return result
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function fetchNotifications() {
        loading.value = true

        try {
            const data = await frappeClient.call('tems.api.pwa.driver.get_notifications')
            notifications.value = data || []
            unreadCount.value = unreadNotifications.value.length
            return data
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function markNotificationRead(notificationId) {
        try {
            await frappeClient.call('tems.api.pwa.driver.mark_notification_read', {
                notification_id: notificationId
            })

            const notification = notifications.value.find(n => n.name === notificationId)
            if (notification) {
                notification.read = true
                unreadCount.value = unreadNotifications.value.length
            }
        } catch (err) {
            error.value = err.message
            throw err
        }
    }

    function addLocalNotification(notification) {
        notifications.value.unshift({
            ...notification,
            read: false,
            timestamp: new Date().toISOString()
        })
        unreadCount.value++
    }

    return {
        messages,
        notifications,
        unreadCount,
        unreadNotifications,
        loading,
        error,
        fetchMessages,
        sendMessage,
        fetchNotifications,
        markNotificationRead,
        addLocalNotification
    }
})

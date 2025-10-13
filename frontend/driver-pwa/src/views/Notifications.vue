<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="card p-4">
      <h2 class="text-xl font-bold text-gray-900 mb-2">Notifications</h2>
      <p class="text-sm text-gray-600">Stay updated with important alerts</p>
    </div>

    <!-- Unread Count Badge -->
    <div v-if="unreadCount > 0" class="card p-4 bg-primary-50 border-l-4 border-primary-600">
      <div class="flex items-center space-x-3">
        <Bell class="w-6 h-6 text-primary-600" />
        <div>
          <p class="font-semibold text-gray-900">{{ unreadCount }} Unread Notification{{ unreadCount > 1 ? 's' : '' }}</p>
          <p class="text-sm text-gray-600">Tap on a notification to mark as read</p>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="commStore.loading" class="card p-8">
      <LoadingSpinner message="Loading notifications..." />
    </div>

    <!-- Empty State -->
    <div v-else-if="notifications.length === 0" class="card p-8">
      <EmptyState
        :icon="Bell"
        title="No notifications"
        message="You're all caught up! No new notifications at the moment."
      />
    </div>

    <!-- Notifications List -->
    <div v-else class="card divide-y">
      <div
        v-for="notification in notifications"
        :key="notification.name"
        class="p-4 hover:bg-gray-50 cursor-pointer transition-colors"
        :class="{ 'bg-blue-50': !notification.read }"
        @click="markAsRead(notification)"
      >
        <div class="flex items-start space-x-3">
          <div
            class="flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center"
            :class="getNotificationIconBg(notification.document_type)"
          >
            <component :is="getNotificationIcon(notification.document_type)" class="w-5 h-5" />
          </div>

          <div class="flex-1 min-w-0">
            <div class="flex items-start justify-between mb-1">
              <p class="font-semibold text-gray-900 truncate">{{ notification.subject }}</p>
              <span v-if="!notification.read" class="w-2 h-2 bg-blue-600 rounded-full ml-2 mt-2"></span>
            </div>
            
            <div
              v-if="notification.email_content"
              class="text-sm text-gray-600 line-clamp-2"
              v-html="notification.email_content"
            ></div>

            <div class="flex items-center space-x-4 mt-2 text-xs text-gray-500">
              <span>{{ formatTimestamp(notification.creation) }}</span>
              <span v-if="notification.document_type && notification.document_name" class="flex items-center space-x-1">
                <FileText class="w-3 h-3" />
                <span>{{ notification.document_type }}</span>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Refresh Button -->
    <button
      @click="refreshNotifications"
      class="w-full btn-secondary py-3"
      :disabled="commStore.loading"
    >
      <RefreshCw class="w-5 h-5 mr-2" :class="{ 'animate-spin': commStore.loading }" />
      Refresh
    </button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { formatDistanceToNow, parseISO } from 'date-fns'
import { 
  Bell, RefreshCw, FileText, AlertTriangle, CheckCircle, 
  Info, Truck, Package, Users 
} from 'lucide-vue-next'
import { useCommunicationStore } from '@/stores/communication'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const commStore = useCommunicationStore()

const notifications = computed(() => commStore.notifications)
const unreadCount = computed(() => commStore.unreadCount)

function getNotificationIcon(docType) {
  const iconMap = {
    'Journey Plan': Truck,
    'Operation Plan': Truck,
    'Safety Incident': AlertTriangle,
    'Cargo Consignment': Package,
    'Passenger Booking': Users,
    'Vehicle': Truck,
  }
  return iconMap[docType] || Info
}

function getNotificationIconBg(docType) {
  const bgMap = {
    'Journey Plan': 'bg-blue-100 text-blue-600',
    'Operation Plan': 'bg-blue-100 text-blue-600',
    'Safety Incident': 'bg-red-100 text-red-600',
    'Cargo Consignment': 'bg-amber-100 text-amber-600',
    'Passenger Booking': 'bg-green-100 text-green-600',
    'Vehicle': 'bg-purple-100 text-purple-600',
  }
  return bgMap[docType] || 'bg-gray-100 text-gray-600'
}

function formatTimestamp(timestamp) {
  if (!timestamp) return ''
  try {
    const date = typeof timestamp === 'string' ? parseISO(timestamp) : timestamp
    return formatDistanceToNow(date, { addSuffix: true })
  } catch (e) {
    return ''
  }
}

async function markAsRead(notification) {
  if (!notification.read) {
    try {
      await commStore.markNotificationRead(notification.name)
    } catch (error) {
      console.error('Failed to mark notification as read:', error)
    }
  }
}

async function refreshNotifications() {
  try {
    await commStore.fetchNotifications()
  } catch (error) {
    console.error('Failed to refresh notifications:', error)
  }
}

onMounted(async () => {
  await commStore.fetchNotifications()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

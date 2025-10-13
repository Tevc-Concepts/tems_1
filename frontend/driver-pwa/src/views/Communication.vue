<template>
  <div class="h-[calc(100vh-12rem)] flex flex-col">
    <!-- Header -->
    <div class="card p-4 mb-4">
      <h2 class="text-xl font-bold text-gray-900 mb-2">Messages</h2>
      <p class="text-sm text-gray-600">Communication with Operations Control</p>
    </div>

    <!-- Messages List -->
    <div class="flex-1 card overflow-hidden flex flex-col">
      <div v-if="commStore.loading" class="flex-1 flex items-center justify-center">
        <LoadingSpinner message="Loading messages..." />
      </div>

      <div v-else-if="messages.length === 0" class="flex-1 flex items-center justify-center">
        <EmptyState
          :icon="MessageCircle"
          title="No messages"
          message="You don't have any messages yet. Start a conversation with operations control."
        />
      </div>

      <div v-else ref="messageContainer" class="flex-1 overflow-y-auto p-4 space-y-4">
        <div
          v-for="message in messages"
          :key="message.name || message.timestamp"
          class="flex"
          :class="message.sender === 'me' ? 'justify-end' : 'justify-start'"
        >
          <div
            class="max-w-[75%] rounded-2xl px-4 py-2"
            :class="message.sender === 'me' 
              ? 'bg-primary-600 text-white' 
              : 'bg-gray-100 text-gray-900'"
          >
            <p class="text-sm whitespace-pre-wrap">{{ message.message }}</p>
            <p
              class="text-xs mt-1"
              :class="message.sender === 'me' ? 'text-primary-100' : 'text-gray-500'"
            >
              {{ formatMessageTime(message.timestamp) }}
            </p>
          </div>
        </div>
      </div>

      <!-- Message Input -->
      <div class="p-4 border-t bg-white">
        <form @submit.prevent="sendMessage" class="flex items-end space-x-2">
          <div class="flex-1">
            <textarea
              v-model="newMessage"
              placeholder="Type your message..."
              rows="2"
              class="w-full px-4 py-2 border border-gray-300 rounded-xl resize-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              @keydown.enter.exact.prevent="sendMessage"
            ></textarea>
          </div>
          
          <button
            type="button"
            @click="attachFile"
            class="btn-secondary p-3"
            :disabled="commStore.loading"
          >
            <Paperclip class="w-5 h-5" />
          </button>
          
          <button
            type="submit"
            class="btn-primary p-3"
            :disabled="!newMessage.trim() || commStore.loading"
          >
            <Send class="w-5 h-5" />
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { format, parseISO } from 'date-fns'
import { MessageCircle, Send, Paperclip } from 'lucide-vue-next'
import { useCommunicationStore } from '@/stores/communication'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const commStore = useCommunicationStore()
const newMessage = ref('')
const messageContainer = ref(null)

const messages = computed(() => commStore.messages)

async function sendMessage() {
  if (!newMessage.value.trim()) return

  try {
    await commStore.sendMessage('Operations Control', 'operations', newMessage.value)
    newMessage.value = ''
    
    // Scroll to bottom
    await nextTick()
    if (messageContainer.value) {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight
    }
  } catch (error) {
    console.error('Failed to send message:', error)
  }
}

function attachFile() {
  // TODO: Implement file attachment
  console.log('Attach file')
}

function formatMessageTime(timestamp) {
  if (!timestamp) return ''
  try {
    const date = typeof timestamp === 'string' ? parseISO(timestamp) : timestamp
    return format(date, 'HH:mm')
  } catch (e) {
    return ''
  }
}

onMounted(async () => {
  await commStore.fetchMessages()
  
  // Scroll to bottom after loading
  await nextTick()
  if (messageContainer.value) {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight
  }
})
</script>

<script setup>
import { onMounted } from 'vue'
import { useOfflineStore } from './stores/offline'

const offlineStore = useOfflineStore()

onMounted(() => {
  offlineStore.initializeOnlineListener()
})
</script>

<template>
  <RouterView />
</template>

<style>
/* Global styles are in style.css */
</style>

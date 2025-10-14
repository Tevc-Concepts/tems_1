<script setup>
import { onMounted } from 'vue'
import { Toast, useOfflineSync } from '@shared'

// Initialize offline sync
const offlineSync = useOfflineSync({ autoInit: false })

onMounted(() => {
  offlineSync.init()
})
</script>

<template>
  <RouterView />
  <Toast />
</template>

<style>
/* Global styles are in style.css */
</style>

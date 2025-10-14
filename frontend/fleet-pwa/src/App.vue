<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <router-view />
    <Toast />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { Toast, useOfflineSync } from '@shared'

const { startSync } = useOfflineSync()

onMounted(() => {
  // Start background sync for offline operations
  startSync()
})
</script>

<style>
@import './assets/main.css';
</style>

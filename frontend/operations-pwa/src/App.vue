<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <router-view />
    <Toast />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { Toast, useOfflineSync } from '@shared'

const { init } = useOfflineSync()

onMounted(() => {
  // Initialize offline sync for operations
  init()
})
</script>

<style>
@import './assets/main.css';
</style>

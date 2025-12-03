import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './assets/styles/main.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

app.mount('#app')

// Service worker registration disabled until sw.js is properly configured
// TODO: Re-enable after setting up proper service worker
// if ('serviceWorker' in navigator) {
//   window.addEventListener('load', () => {
//     navigator.serviceWorker.register('/driver/sw.js').catch(err => {
//       console.warn('Service worker registration failed:', err)
//     })
//   })
// }
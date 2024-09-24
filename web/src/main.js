import { createApp } from 'vue'
import App from './App.vue'
import router from './router/router' // Router being imported
import './registerServiceWorker'

createApp(App).use(router).mount('#app')

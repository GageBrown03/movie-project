// Entry point for the Vue application
import { createApp } from 'vue'
import App from './App.vue'

// Routing (pages)
import router from './router'

// UI framework
import vuetify from './plugins/vuetify'

// Fonts for Vuetify
import { loadFonts } from './plugins/webfontloader'

loadFonts()

createApp(App)
  .use(router)
  .use(vuetify)
  .mount('#app')
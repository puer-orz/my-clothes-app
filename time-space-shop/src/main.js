import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

import 'vant/lib/index.css'
import './style.css'

import { NavBar, Popup, Button } from 'vant'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(NavBar)
app.use(Popup)
app.use(Button)

app.mount('#app')
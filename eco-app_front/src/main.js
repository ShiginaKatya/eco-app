import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import { store } from './store.js'
import VueApexCharts from "vue3-apexcharts";


const app = createApp(App)

app.use(VueApexCharts)
app.use(store)
app.use(router)
app.mount('#app')

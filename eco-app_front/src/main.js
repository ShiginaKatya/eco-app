import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import { store } from './store.js'
import VueApexCharts from "vue3-apexcharts";
import { createHead } from '@vueuse/head'


const app = createApp(App)
const head = createHead()

app.use(VueApexCharts)
app.use(store)
app.use(router)
app.use(head)
app.mount('#app')

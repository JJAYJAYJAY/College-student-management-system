import { createApp } from 'vue'
import pinia from '@/stores/index.js'
import ArcoVue from '@arco-design/web-vue';
import ArcoVueIcon from '@arco-design/web-vue/es/icon';
import '@arco-design/web-vue/dist/arco.css';
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(pinia)
app.use(router)
app.use(ArcoVue)
app.use(ArcoVueIcon)


app.mount('#app')

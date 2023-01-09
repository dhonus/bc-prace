import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios';

const app = createApp(App);
app.use(router).mount('#app');

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://130.162.49.62:8002/';  // the FastAPI backend
//axios.defaults.baseURL = 'http://localhost:8002/';  // the FastAPI backend
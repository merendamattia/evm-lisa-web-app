import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import About from '../views/About.vue'
import Create from '../views/Create.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/about', component: About },
  { path: '/create', component: Create },
]

const router = createRouter({
  history: createWebHistory(), // usa createWebHistory per modalità 'history'
  routes,
})

export default router

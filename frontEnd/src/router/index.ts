import { createRouter, createWebHistory } from 'vue-router'
import Create from '../views/Create.vue'

const routes = [
  { path: '/create', component: Create },
]

const router = createRouter({
  history: createWebHistory(), 
  routes,
})

export default router
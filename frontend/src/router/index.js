import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import MemoryGameView from '@/views/MemoryGameView.vue'
import ClicSpeedView from '@/views/ClickSpeedView.vue'
import ClickSpeedView from '@/views/ClickSpeedView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
  },
  {
    path: '/register',
    name: 'register',
    component: Register,
  },
  {
    path: '/games',
    name: 'games',
    component: () => import('../views/GamesView.vue'),
  },
  {
    path: '/games/memory',
    name: 'memory',
    component: MemoryGameView,
  },
  {
    path: '/games/clickspeed',
    name: 'clickspeed',
    component: ClickSpeedView,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

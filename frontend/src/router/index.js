import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import MemoryGameView from '@/views/MemoryGameView.vue'
import ClickSpeedView from '@/views/ClickSpeedView.vue'
import MemoryLeaderBoardView from '@/views/MemoryLeaderBoardView.vue'
import ClickSpeedLeaderboard from '@/views/ClickSpeedLeaderboard.vue'
import ReflexGameView from '@/views/ReflexGameView.vue'
import ReflexLeaderboard from '@/views/ReflexLeaderboard.vue'

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
    path: '/games/leaderboard/memory',
    name: 'memory-leaderboard',
    component: MemoryLeaderBoardView,
  },
  {
    path: '/games/clickspeed',
    name: 'clickspeed',
    component: ClickSpeedView,
  },
  {
    path: '/games/leaderboard/clickspeed',
    name: 'clickspeed-leaderboard',
    component: ClickSpeedLeaderboard,
  },
  {
    path: '/games/reflex',
    name: 'reflex',
    component: ReflexGameView,
  },
  {
    path: '/games/leaderboard/reflex',
    name: 'reflex-leaderboard',
    component: ReflexLeaderboard,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

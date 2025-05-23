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
import SnakeGame from '@/views/SnakeGame.vue'
import SnakeLeaderboard from '@/views/SnakeLeaderboard.vue'
import Personal from '@/views/PersonalView.vue'
import TypingGame from '@/views/TypingGame.vue'
import TypingLeaderboard from '@/views/TypingLeaderboard.vue'
import RunnerGame from '@/views/RunnerGameView.vue'
import RunnerLeaderboard from '@/views/RunnerLeaderboard.vue'
import GlobalLeaderboardView from '@/views/GlobalLeaderboardView.vue'
import AboutView from '@/views/AboutView.vue'

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
    path: '/games/leaderboard',
    name: 'leaderboard',
    component: GlobalLeaderboardView,
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
  {
    path: '/games/snake',
    name: 'snake',
    component: SnakeGame,
  },
  {
    path: '/games/leaderboard/snake',
    name: 'snake-leaderboard',
    component: SnakeLeaderboard,
  },
  {
    path: '/personal',
    name: 'personal',
    component: Personal,
  },
  {
    path: '/games/typing',
    name: 'typing',
    component: TypingGame,
  },
  {
    path: '/games/leaderboard/typing',
    name: 'typing-leaderboard',
    component: TypingLeaderboard,
  },
  {
    path: '/games/runner',
    name: 'runner',
    component: RunnerGame,
  },
  {
    path: '/games/leaderboard/runner',
    name: 'runner-leaderboard',
    component: RunnerLeaderboard,
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView,
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

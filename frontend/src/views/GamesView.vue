<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../services/auth'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { API_BASE_URL } from '@/config'
import { RouterLink } from 'vue-router'

const games = ref([])

const authStore = useAuthStore()
const router = useRouter()

const fetchGames = async () => {
  const res = await axios.get(`${API_BASE_URL}/games/`)
  games.value = res.data
}

onMounted(async () => {
  await authStore.fetchUser()
  console.log('User loaded:', authStore.user)
  if (!authStore.user) {
    router.push('/login')
    return
  }
  fetchGames()
})
</script>

<template>
  <div class="container">
    <h1>Games</h1>
    <p v-if="games.length === 0">No games to display</p>
    <ul v-else>
      <li v-for="game in games">
        <h2>
          {{ game.name }}
        </h2>
        <div class="button-group">
          <RouterLink :to="'/games/' + game.name.toLowerCase()">
            <button @click="console.log('play: ' + game.id)">Play</button>
          </RouterLink>
          <RouterLink :to="'/games/leaderboard/' + game.name.toLowerCase()">
            <button @click="console.log('leaderboard: ' + game.id)">Leaderboard</button>
          </RouterLink>
        </div>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.container {
  max-width: 800px;
  margin-inline: auto;
  text-align: center;
  border-radius: 10px;
  background: white;
  padding: 20px;
}

h1 {
  color: #007acc;
  margin-bottom: 20px;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  border: 3px solid #007acc;
  font-size: 1.5rem;
  color: #005f99;
  font-weight: bold;
  padding: 10px 20px 30px 20px;
  margin: 1.2rem 0;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

li > h2 {
  font-size: 1.6rem;
  font-weight: bold;
  text-align: center;
  margin-bottom: 1.8rem;
}

.button-group {
  display: flex;
  flex-direction: row;
  gap: 10px;
}

button {
  background: #007acc;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;
  font-size: 1.2rem;
}

button:hover {
  background: #005f99;
}
</style>

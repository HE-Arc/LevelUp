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
    <h1>{{ authStore.user?.username }}</h1>
    <p v-if="games.length === 0">No games to display</p>
    <ul v-else>
      <li v-for="game in games">
        <h2>
          {{ game.name }}
        </h2>
        <div>
          score here
        </div>
      </li>
    </ul>

  </div>
</template>

<style scoped>


.container {
  max-width: 600px;
  margin-inline: auto;
  text-align: center;
  border-radius: 10px;
  font-size: 1.1rem;
  padding: 20px;
}

h1 {
  color: #007acc;
}

.auth-box {
  background: white;
  padding: 15px;
  border-radius: 8px;
  margin-top: 20px;
}

.btn {
  background: #007acc;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;
  font-size: 1.3rem;
  width: 80%;
}

.btn:hover {
  background: #005f99;
}

.login-message {
  margin-top: 20px;
}

.login-link {
  color: #007acc;
  text-decoration: none;
  font-weight: bold;
}

.login-link:hover {
  text-decoration: underline;
}
</style>

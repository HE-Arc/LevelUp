<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../services/auth'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { API_BASE_URL } from '@/config'

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
    <button>my scores</button>
    <button>Edit</button>
    <button class="logout-btn" @click="authStore.logout(this.$router)">Logout</button>

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
  flex-direction: column;
}

h1 {
  color: #007acc;
  text-align: center;
}

h2 {
  text-align: left;
}

button {
  background: #007acc;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;
  font-size: 1.2rem;
  margin-top: 10px;
  width: 80%;
}

button:hover {
  background: #005f99;
}

.logout-btn {
  background: #e07234;
}

.logout-btn:hover {
  background: #e4641e
}

</style>

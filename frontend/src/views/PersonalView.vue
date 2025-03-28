<script setup>
  import { ref, onMounted } from 'vue'
  import { useAuthStore } from '../services/auth'
  import { useRouter } from 'vue-router'
  import axios from 'axios'
  import { API_BASE_URL } from '@/config'
  import { getUserFullScore } from '@/utils/requests'

  const games = ref([])
  const userFullScore = ref({})
  const authStore = useAuthStore()
  const router = useRouter()

  const fetchGames = async () => {
    const res = await axios.get(`${API_BASE_URL}/games/`)
    games.value = res.data
  }

  const fetchUserFullScore = async () => {
    const res = await getUserFullScore(authStore.user.id)
    userFullScore.value = res
  }

  onMounted(async () => {
    await authStore.fetchUser()
    console.log('User loaded:', authStore.user)
    if (!authStore.user) {
      router.push('/login')
      return
    }
    fetchGames()
    fetchUserFullScore()
  })
</script>
<script>
  export default {
    data() {
      return {
        scoresVisible: false,
        infoVisible: false,
      };
    },
    methods: {
      toggleScoreVisibility() {
        this.scoresVisible = !this.scoresVisible;
      },
      toggleInfoVisibility() {
        this.infoVisible = !this.infoVisible;
      },
    },
  };
</script>

<template>
  <div class="container">
    <h1>{{ authStore.user?.username }}</h1>
    <button @click="toggleScoreVisibility">my scores</button>
    <div v-if="scoresVisible" class="content">
      <p v-if="games.length === 0">No games to display</p>
      <table v-else>
        <thead>
          <tr>
            <th></th>
            <th>Ranks</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Global</td>
            <td>{{ userFullScore["rank_score_rank"] }}</td>
            <td>{{ Math.round(userFullScore["rank_score_sum"]) }}</td>
          </tr>
          <tr v-for="game in games">
            <td>{{ game.name }}</td>
            <td>{{ userFullScore["ranks"][game.name] }}</td>
            <td>{{ userFullScore["scores"][game.name] }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <button @click="toggleInfoVisibility">Edit</button>
    <div v-if="infoVisible" class="content">
      <table>
        <tbody>
          <tr>
            <td>Username :</td>
            <td>{{ authStore.user?.username }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <button class="logout-btn" @click="authStore.logout(this.$router)">Logout</button>
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
  display: flex;
  justify-content: center;
}

h1 {
  color: #007acc;
}

.content {
  width: 80%;
  margin: 0 auto;
  display: flex;
  justify-content: center;
}

table {
  margin: 1% 0 2% 0;
  width: 100%;
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
  margin: 0 auto;
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

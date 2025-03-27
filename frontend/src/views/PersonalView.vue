<script setup>
  import { ref, onMounted } from 'vue'
  import { useAuthStore } from '../services/auth'
  import { useRouter } from 'vue-router'
  import axios from 'axios'
  import { API_BASE_URL } from '@/config'
  import { RouterLink } from 'vue-router'
  import { getLeaderboard } from '@/utils/requests.js';

  const games = ref([])
  const userRanks = ref({})
  const userFullScore = ref({})
  const authStore = useAuthStore()
  const router = useRouter()

  const fetchGames = async () => {
    const res = await axios.get(`${API_BASE_URL}/games/`)
    games.value = res.data
    if (authStore.user) {
      await fetchUserRanks()
    }
  }

  const fetchUserFullScore = async () => {
    const jsonResult = await axios.get(`${API_BASE_URL}/user_full_score/`)
    const result = JSON.parse(jsonResult)
    userFullScore.value = result
  }

  const fetchUserRanks = async () => {
    const username = authStore.user.username
    for (const game of games.value) {
      try {
        const leaderboard = await getLeaderboard(game.name);

        const userEntry = leaderboard.find(player => player.username === username);
        userRanks.value[game.id] = userEntry ? leaderboard.indexOf(userEntry) + 1 : '-';
      } catch (error) {
        console.error(`Error with ${game.name}:`, error)
        userRanks.value[game.id] = 'N/A'
      }
    }
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
    <div v-if="scoresVisible">
      <p v-if="games.length === 0">No games to display</p>
      <ul v-else>
        <li>
          <h2>
            Global
          </h2>
          <div>

          </div>
        </li>
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
    <button @click="toggleInfoVisibility">Edit</button>
    <div v-if="infoVisible">
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

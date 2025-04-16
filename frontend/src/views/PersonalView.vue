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
        editUsernameActive: false,
        editMailActive: false,
        oldPassword: '',
        newPassword: '',
        message: '',
      };
    },
    methods: {
      toggleScoreVisibility() {
        this.scoresVisible = !this.scoresVisible;
      },
      toggleInfoVisibility() {
        this.infoVisible = !this.infoVisible;
      },
      activateNameEdit() {
        this.editUsernameActive = !this.editUsernameActive;
      },
      activateMailEdit() {
        this.editMailActive = !this.editMailActive;
      },
      async changePassword() {
        try {
          const response = await this.$axios.post('/api/edit_password/', {
            old_password: this.oldPassword,
            new_password: this.newPassword
          });
          print(response),
          this.message = response.data.detail;
        } catch (error) {
          this.message = error.response.data.detail || 'Error changing password.';
        }
      }
    },
  };
</script>

<template>
  <div class="container">
    <h1>{{ authStore.user?.username }}</h1>
    <button @click=toggleScoreVisibility>My high scores</button>
    <div v-if="scoresVisible" class="content">
      <p v-if="games.length === 0">No games to display</p>
      <table v-else>
        <thead>
          <tr>
            <th></th>
            <th class="number-col">Ranks</th>
            <th class="number-col">Score</th>
          </tr>
        </thead>
        <tbody>
          <tr class="global-row">
            <td>Global</td>
            <td class="number-col">{{ userFullScore["rank_score_rank"] }}</td>
            <td class="number-col">{{ Math.round(userFullScore["rank_score_sum"]) }}</td>
          </tr>
          <tr v-for="game in games">
            <td>{{ game.name }}</td>
            <td class="number-col">{{ userFullScore["ranks"][game.name] }}</td>
            <td class="number-col">{{ userFullScore["scores"][game.name] }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <button @click="toggleInfoVisibility">My Profile</button>
    <div v-if="infoVisible" class="content">
      <table>
        <tbody>
          <tr>
            <td>Username :</td>
            <td>{{ authStore.user?.username }}</td>
            <td>
              <!-- button class="small-btn" title="edit username">
                <i class="fas fa-edit"></i>
              </button -->
            </td>
          </tr>
          <tr>
            <td>email :</td>
            <td>{{ authStore.user?.email }}</td>
            <td>
              <!-- button class="small-btn" title="Edit email address">
                <i class="fas fa-edit"></i>
              </button -->
            </td>
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
  margin: 2% 0 3% 2%;
  width: 100%;
  text-align: left;
}

.number-col {
  text-align: center;
}

.global-row {
  font-weight: bold;
}

button {
  background: #007acc;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1.2rem;
  margin: 0 auto;
  margin-top: 10px;
  width: 80%;
}


.small-btn {
  margin: 0;
  padding: 3px 8px;
  font-size: 1rem;
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

<script>
import { useAuthStore } from '../services/auth'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()

    return { authStore, router }
  },
  methods: {
    async logout() {
      try {
        await this.authStore.logout(this.$router)
      } catch (error) {
        console.error(error)
      }
    },
  },
  async mounted() {
    await this.authStore.fetchUser()
  },
}
</script>

<template>
  <div class="container">
    <h1>LevelUp</h1>
    <p class="subtitle">
      Challenge yourself and compete with friends on our collection of mini-games!
    </p>

    <div v-if="authStore.isAuthenticated" class="auth-box">
      <p>
        Welcome back, <strong>{{ authStore.user?.username }}</strong
      >!
      </p>
      <p>Ready to beat your high scores?</p>
      <button @click="logout" class="btn">Logout</button>
    </div>
    <p v-else class="login-message">
      You are not logged in.
      <router-link to="/login" class="login-link">Login</router-link>
      to save your scores and compete!
    </p>

    <div class="games-section">
      <h2>Our Games Collection</h2>

      <div class="game-list">
        <div class="game-item">
          <h3>Memory</h3>
          <p>
            Match all pairs of symbols by flipping cards two at a time. The fewer attempts you make,
            the higher your score!
          </p>
        </div>

        <div class="game-item">
          <h3>Reflex</h3>
          <p>
            Click on the different colors as fast as you can! You have 30 seconds to click as many
            as possible!
          </p>
        </div>

        <div class="game-item">
          <h3>ClickSpeed</h3>
          <p>Test your clicking speed! How many times can you click in just 10 seconds?</p>
        </div>

        <div class="game-item">
          <h3>Snake</h3>
          <p>
            The classic snake game. Grow as long as possible without hitting the walls or yourself!
          </p>
        </div>

        <div class="game-item">
          <h3>Runner</h3>
          <p>Dodge the most objects heading towards you in this endless runner challenge!</p>
        </div>

        <div class="game-item">
          <h3>Typing</h3>
          <p>Measure your typing speed. How many words per minute can you type accurately?</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 800px;
  margin-inline: auto;
  text-align: center;
  font-size: 1.1rem;
  padding: 20px;
}

h1 {
  color: #007acc;
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #555;
  font-size: 1.2rem;
  margin-bottom: 2rem;
}

.auth-box {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 8px;
  margin: 20px auto;
  max-width: 400px;
}

.btn {
  background: #007acc;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;
  font-size: 1rem;
  width: 80%;
  margin-top: 10px;
}

.btn:hover {
  background: #005f99;
}

.login-message {
  margin: 20px 0;
}

.login-link {
  color: #007acc;
  text-decoration: none;
  font-weight: bold;
}

.login-link:hover {
  text-decoration: underline;
}

.games-section {
  margin: 40px 0;
  text-align: center;
}

.games-section h2 {
  color: #007acc;
  margin-bottom: 20px;
  border-bottom: 2px solid #007acc;
  padding-bottom: 10px;
  display: inline-block;
}

.game-list {
  display: flex;
  flex-direction: column;
  gap: 25px;
  margin-top: 30px;
  text-align: left;
}

.game-item {
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.game-item:last-child {
  border-bottom: none;
}

.game-item h3 {
  color: #007acc;
  margin: 0 0 8px 0;
  font-size: 1.3rem;
}

.game-item p {
  margin: 0;
  color: #555;
}

</style>

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
    <div v-if="authStore.isAuthenticated" class="auth-box">
      <p>
        Hi there, <strong>{{ authStore.user?.username }}</strong
        >!
      </p>
      <p>You are logged in.</p>
      <button @click="logout" class="btn">Logout</button>
    </div>
    <p v-else class="login-message">
      You are not logged in.
      <router-link to="/login" class="login-link">Login</router-link>
    </p>
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

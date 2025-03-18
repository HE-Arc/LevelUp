<template>
  <div class="container">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="identifier">Username or Email:</label>
        <input v-model="identifier" id="identifier" type="text" required @input="resetError" />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input v-model="password" id="password" type="password" required @input="resetError" />
      </div>
      <button type="submit">Login</button>
    </form>

    <p>No account?
      <router-link to="/register">
        <button>Register</button>
      </router-link>
    </p>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import { useAuthStore } from '../services/auth'

export default {
  setup() {
    const authStore = useAuthStore()
    return { authStore }
  },
  data() {
    return {
      identifier: "", // Peut être un username ou un email
      password: "",
      error: ""
    }
  },
  methods: {
    async login() {
      await this.authStore.login(this.identifier, this.password, this.$router)
      if (!this.authStore.isAuthenticated) {
        this.error = 'Login failed. Please check your credentials.'
      }
    },
    resetError() {
      this.error = ""
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 500px;
  margin: 50px auto;
  padding: 20px;
  background: white;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #007acc;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  text-align: left;
  margin-bottom: 15px;
  margin-right: 22px;
}

label {
  font-weight: bold;
  margin-bottom: 5px;
}

input {
  padding: 10px;
  border: 1px solid #005f99;
  border-radius: 5px;
  font-size: 1rem;
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
  margin-top: 10px;
}

button:hover {
  background: #005f99;
}

.error {
  color: red;
  font-weight: bold;
  margin-top: 10px;
}
</style>

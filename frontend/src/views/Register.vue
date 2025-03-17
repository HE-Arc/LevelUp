<template>
  <div class="container">
    <h2>Register</h2>
    <form @submit.prevent="register">
      <div class="form-group">
        <label for="username">Username:</label>
        <input v-model="username" id="username" type="text" required />
      </div>
      <div class="form-group">
        <label for="email">Email:</label>
        <input v-model="email" id="email" type="email" required />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input v-model="password1" id="password" type="password" required />
      </div>
      <div class="form-group">
        <label for="password2">Confirm Password:</label>
        <input v-model="password2" id="password2" type="password" required />
      </div>
      <button type="submit">Register</button>
    </form>

    <p>Already registered?
      <router-link to="/login">
        <button>Login</button>
      </router-link>
    </p>

    <div v-for="(errors, field) in error" :key="field" class="error">
      <p v-for="(err, index) in errors" :key="index">
        {{ err.message }}
      </p>
    </div>
    <p v-if="success" class="success">{{ success }}</p>
  </div>
</template>

<script>
import { getCSRFToken } from '../services/auth'
import { API_BASE_URL } from '@/config'

export default {
  data() {
    return {
      username: '',
      email: '',
      password1: '',
      password2: '',
      error: '',
      success: ''
    }
  },
  methods: {
    async register() {
      try {
        const response = await fetch(`${API_BASE_URL}/register`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
          },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
            password1: this.password1,
            password2: this.password2
          }),
          credentials: 'include'
        })
        const data = await response.json()
        if (response.ok) {
          this.success = 'Registration successful! Please log in.'
          setTimeout(() => {
            this.$router.push('/login')
          }, 1000)
        } else {
          this.error = JSON.parse(data.error);
        }
      } catch (err) {
        this.error = 'An error occurred during registration: ' + err
      }
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

.error p {
  list-style: none;
  padding: 0;
  margin: 10px 0;
  color: red;
  font-weight: bold;
}

.success {
  color: green;
  font-weight: bold;
  margin-top: 10px;
}
</style>

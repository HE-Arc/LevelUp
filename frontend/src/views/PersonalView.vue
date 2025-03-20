<script>
import { getCSRFToken } from '../services/auth'
import { API_BASE_URL } from '@/config'
</script>

<template>
  <div class="container">
    <h2>personnal</h2>
    <div>
      <p>
        Hello there!
      </p>
      <p>Here are your scores</p>
    </div>
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

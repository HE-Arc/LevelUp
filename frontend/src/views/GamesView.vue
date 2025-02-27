<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const games = ref([])

const fetchGames = async () => {
  const res = await axios.get('http://localhost:8000/api/games/')
  games.value = res.data
}

onMounted(fetchGames)
</script>

<template>
  <h1>Games</h1>
  <ul>
    <li v-for="game in games">
      {{ game.name }}

      <button @click="console.log('play: ' + game.id)">Play</button>

      <button @click="console.log('leaderboard: ' + game.id)">Leaderboard</button>
    </li>
  </ul>
</template>

<style scoped></style>

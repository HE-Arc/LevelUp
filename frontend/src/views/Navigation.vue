<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  gameTitle: {
    type: String
  },
  gameName: {
    type: String,
    required: true
  },
  modeId: { //false in a game page, true in a leaderboard page
    type: Boolean,
    required: true
  }
})

const router = useRouter()

const goToMenu = () => {
  router.push('/games')
}

const goToLeaderboard = () => {
  router.push(`/games/leaderboard/${props.gameName}`)
}

const goToGame = () => {
  router.push(`/games/${props.gameName}`)
}
</script>

<template>
  <div class="game-nav">
    <button @click="goToMenu">Back to games</button>
    <button v-if="modeId==false" @click="goToLeaderboard">Check leaderboard</button>
    <button v-if="modeId==true" @click="goToGame">Play {{ gameTitle }}</button>
  </div>
</template>

<style scoped>
.game-nav {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 20px;
}

button {
  background: #007acc;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s;
  font-size: 1rem;
}

button:hover {
  background: #005f99;
}
</style>

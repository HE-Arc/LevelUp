<script setup>
import { onMounted, ref } from 'vue'
import { GameName, saveScore } from '@/utils/requests.js'
import { useAuthStore } from '@/services/auth.js'
import { useRouter } from 'vue-router'
import Navigation from './Navigation.vue'

const timeLeft = ref(10)
const nbClick = ref(0)
const gameRunning = ref(false)
let timer = null

const startButtonShow = ref(true)
const timeToShowStartButton = ref(11)

const authStore = useAuthStore()
const router = useRouter()

onMounted(async () => {
  await authStore.fetchUser()
  if (!authStore.user) {
    router.push('/login')
  }
})

const startGame = () => {
  nbClick.value = 0
  timeLeft.value = 10
  timeToShowStartButton.value = 11
  gameRunning.value = true
  startButtonShow.value = false

  timer = setInterval(() => {
    timeLeft.value--
    if (timeLeft.value === 0) {
      gameRunning.value = false
      gameEnd()
    }
    if (timeToShowStartButton.value > 0) {
      timeToShowStartButton.value--
    } else {
      clearInterval(timer)
      startButtonShow.value = true
    }
  }, 1000)
}

const incrementScore = (event) => {
  if (event.pointerId === -1) {
    // If the player "clicked" with the enter key, ignore it
    return;
  }
  if (gameRunning.value) {
    nbClick.value++
  }
}

const gameEnd = async () => {
  await saveScore(GameName.CLICKSPEED, nbClick.value, authStore.user.id)
}
</script>

<template>
  <Navigation :gameName="GameName.CLICKSPEED" :modeId="false"/>
  <div class="game-container">
    <h1>Click Speed Game</h1>
    <p v-if="!gameRunning">Press “Start” and click as much as you can in 10 seconds!</p>
    <h2 v-else>Time left : {{ timeLeft }}s</h2>

    <button class="counter" v-if="gameRunning" @click="incrementScore">{{ nbClick }}</button>

    <p v-if="!gameRunning && nbClick > 0">Final score : {{ nbClick }} clicks</p>

    <button class="start" v-if="!gameRunning && startButtonShow" @click="startGame">Start</button>
  </div>
</template>

<style scoped>
.game-container {
  text-align: center;
  margin-inline: auto;
  max-width: 400px;
  padding: 20px;
}

h1 {
  color: #007acc;
  margin-bottom: 20px;
}

h2 {
  margin-top: 0.5rem;
  margin-bottom: 1rem;
  font-size: 1.6rem;
}

p {
  font-size: 1.3rem;
  margin-bottom: 15px;
}

button {
  background: #007acc;
  color: white;
  border: none;
  padding: 15px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;
  width: 300px;
  font-size: 1.4rem;
  margin-top: 30px;
}

button:hover {
  background: #005f99;
}

.counter {
  border-radius: 50%;
  width: 200px;
  height: 200px;
}
</style>

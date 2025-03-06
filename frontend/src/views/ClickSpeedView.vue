<script setup>
import { ref } from 'vue'
import { GameId, saveScore } from '@/utils/requests.js'

const timeLeft = ref(10)
const nbClick = ref(0)
const gameRunning = ref(false)
let timer = null

const startButtonShow = ref(true)
const timeToShowStartButton = ref(13)

const startGame = () => {
  nbClick.value = 0
  timeLeft.value = 10
  timeToShowStartButton.value = 13
  gameRunning.value = true
  startButtonShow.value = false

  timer = setInterval(() => {
    timeLeft.value--
    if (timeLeft.value === 0) {
      gameRunning.value = false
      gameEnd();
    }
    if (timeToShowStartButton.value > 0) {
      timeToShowStartButton.value--
    } else {
      clearInterval(timer)
      startButtonShow.value = true
    }
  }, 1000)
}

const incrementScore = () => {
  if (gameRunning.value) {
    nbClick.value++
  }
}

const gameEnd = async () => {
  await saveScore(1, GameId.CLICKSPEED, nbClick.value)
}
</script>

<template>
  <div class="game-container">
    <h1>Click Speed Game</h1>
    <p v-if="!gameRunning">Press “Start” and click as much as you can in 10 seconds!</p>
    <p v-else>Time left : {{ timeLeft }}s</p>

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

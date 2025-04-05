<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { GameName, saveScore } from '@/utils/requests.js'
import { useAuthStore } from '@/services/auth.js'
import { useRouter } from 'vue-router'
import Navigation from './Navigation.vue'

const columns = 5
const rows = 10
const nbSpaces = ref(4)
const intervalCounter = ref(0)
const playerPosition = ref(2) //joueur spawn au centre
const blocks = ref([])
const gameOver = ref(false)
const gameStarted = ref(false)
const score = ref(0)
const interval = ref(null)
const authStore = useAuthStore()
const router = useRouter()

const cellSize = computed(() => {
  return Math.min(Math.min(window.innerWidth * 0.9, window.innerHeight * 0.9) / columns - 2, 40)
})

const getDifficulty = () => {
  if (score.value >= 150) return { minEmpty: 1, maxEmpty: 2, nbSpaces: 1 }
  if (score.value >= 100) return { minEmpty: 2, maxEmpty: 2, nbSpaces: 1 }
  if (score.value >= 50) return { minEmpty: 1, maxEmpty: 2, nbSpaces: 2 }
  if (score.value >= 25) return { minEmpty: 1, maxEmpty: 2, nbSpaces: 3 }
  return { minEmpty: 2, maxEmpty: 3, nbSpaces: 3 }
}

const generateBlockRow = () => {
  const { minEmpty, maxEmpty } = getDifficulty()
  let row = new Array(columns).fill('X')
  let emptySpaces = Math.floor(Math.random() * (maxEmpty - minEmpty + 1)) + minEmpty
  for (let i = 0; i < emptySpaces; i++) {
    let index
    do {
      index = Math.floor(Math.random() * columns)
    } while (row[index] === '-')
    row[index] = '-'
  }
  return row
}

const moveBlocks = () => {
  if (gameOver.value || !gameStarted.value) return

  nbSpaces.value = getDifficulty().nbSpaces

  if (intervalCounter.value % (nbSpaces.value+1) == 0) {
    blocks.value.unshift(generateBlockRow())
  } else {
    blocks.value.unshift(new Array(columns).fill('-')) // ligne vide
  }
  intervalCounter.value++

  if (blocks.value.length > rows) {
    blocks.value.pop()
    score.value++
  }
  checkDeath()
}

const startGame = () => {
  gameStarted.value = true
  gameOver.value = false
  restartGame()
}

const restartGame = () => {
  playerPosition.value = 2
  blocks.value = []
  score.value = 0
  interval.value = setInterval(moveBlocks, 500)
}

const movePlayer = (direction) => {
  if (!gameStarted.value) return
  let newPos = playerPosition.value + direction
  if (newPos >= 0 && newPos < columns) {
    playerPosition.value = newPos
  }
  checkDeath()
}

const checkDeath = () => {
  if (blocks.value.length >= rows && blocks.value[rows - 1][playerPosition.value] === 'X') {
    gameOver.value = true
    gameStarted.value = false
    clearInterval(interval.value)
    gameEnd()
  }
}

const gameEnd = async () => {
  await saveScore(GameName.RUNNER, score.value, authStore.user.id)
}

const handleKeydown = (event) => {
  if (!gameStarted.value) return
  if (event.key === 'ArrowLeft') movePlayer(-1)
  if (event.key === 'ArrowRight') movePlayer(1)
}

onMounted(async () => {
  await authStore.fetchUser()
  if (!authStore.user) {
    router.push('/login')
    return
  }
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  clearInterval(interval.value)
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <Navigation v-if="!gameStarted" :gameName="GameName.RUNNER" :modeId="false"/>
  <div class="game-container">
    <h1>Runner Game</h1>
    <h2 v-if="gameStarted">Score: {{ score }}</h2>
    <h2 v-if="gameOver">Final score: {{ score }}</h2>

    <div v-if="!gameStarted" class="start-screen">
      <p>Move the player using the arrow keys.</p>
      <button @click="startGame" class="start-button">Start Game</button>
    </div>

    <div class="grid" v-if="gameStarted">
      <div v-for="(row, y) in rows" :key="y" class="row">
        <div
          v-for="(cell, x) in columns"
          :key="x"
          class="cell"
          :class="{
            block: blocks[y] && blocks[y][x] === 'X',
            player: y === rows - 1 && x === playerPosition,
            'no-top-border': y === 0,
            'no-bottom-border': y === rows - 1
          }"
          :style="{ width: cellSize + 'px', height: cellSize + 'px' }"
        ></div>
      </div>
    </div>

    <div class="controls" v-if="gameStarted">
      <button @click="movePlayer(-1)" style="margin-right: 3px;">◀</button>
      <button @click="movePlayer(1)" style="margin-left: 3px;">▶</button>
    </div>
  </div>
</template>

<style scoped>
.game-container {
  text-align: center;
  margin-inline: auto;
}

h1 {
  color: #007acc;
}

h2 {
  margin-top: 0.5rem;
  margin-bottom: 1rem;
  font-size: 1.6rem;
}

.grid {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.row {
  display: flex;
}

.cell {
  border: 1px solid #91acc2;
  background-color: white;
}

.block {
  background-color: #e33;
}

.player {
  background-color: #007acc;
}

button {
  background: #007acc;
  color: white;
  border: none;
  padding: 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;
  font-size: 1.5rem;
  margin-top: 10px;
}

button:hover {
  background: #005f99;
}

.no-top-border {
  border-top: none;
}

.no-bottom-border {
  border-bottom: none;
}

.controls {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>

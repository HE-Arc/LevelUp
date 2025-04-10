<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { GameName, saveScore } from '@/utils/requests.js'
import { useAuthStore } from '@/services/auth.js'
import { useRouter } from 'vue-router'

const tileCount = 15
const snake = ref([{ x: 10, y: 10 }])
const food = ref({ x: 5, y: 5, color: 'red' })
const direction = ref({ x: 1, y: 0 })
const nextDirection = ref({ x: 1, y: 0 })
const interval = ref(null)
const gameOver = ref(false)
const score = ref(0)
const speed = ref(200)
const gameStarted = ref(false)
const authStore = useAuthStore()
const router = useRouter()

const cellSize = computed(() => {
  return Math.min(Math.min(window.innerWidth * 0.9, window.innerHeight * 0.9) / tileCount - 2, 30)
})

const moveSnake = () => {
  if (gameOver.value || !gameStarted.value) return

  direction.value = nextDirection.value
  const head = { x: snake.value[0].x + direction.value.x, y: snake.value[0].y + direction.value.y }

  if (
    head.x < 0 ||
    head.y < 0 ||
    head.x >= tileCount ||
    head.y >= tileCount ||
    snake.value.some((segment) => segment.x === head.x && segment.y === head.y)
  ) {
    gameOver.value = true
    gameStarted.value = false
    clearInterval(interval.value)
    gameEnd()
    return
  }

  snake.value.unshift(head)
  if (head.x === food.value.x && head.y === food.value.y) {
    score.value++
    if (score.value % 2 === 0) speed.value = Math.max(50, speed.value - 5)
    restartInterval()
    placeFood()
  } else {
    snake.value.pop()
  }
}

const placeFood = () => {
  let newFood
  do {
    newFood = {
      x: Math.floor(Math.random() * tileCount),
      y: Math.floor(Math.random() * tileCount),
      color: getRandomColor(),
    }
  } while (snake.value.some((segment) => segment.x === newFood.x && segment.y === newFood.y))
  food.value = newFood
}

const getRandomColor = () => {
  const colors = ['#e33', '#e93', '#ed3', '#3b9', '#93e', '#e39']
  return colors[Math.floor(Math.random() * colors.length)]
}

const restartInterval = () => {
  clearInterval(interval.value)
  interval.value = setInterval(moveSnake, speed.value)
}

const handleKeydown = (event) => {
  if (!gameStarted.value) return

  const keyMap = {
    w: { x: 0, y: -1 },
    s: { x: 0, y: 1 },
    a: { x: -1, y: 0 },
    d: { x: 1, y: 0 },
  }
  let key = event.key.toLowerCase()
  if (keyMap[key]) {
    const newDir = keyMap[key]
    if (newDir.x !== -direction.value.x || newDir.y !== -direction.value.y) {
      nextDirection.value = newDir
    }
  }
}

const startGame = () => {
  gameStarted.value = true
  gameOver.value = false
  restartGame()
}

const restartGame = () => {
  snake.value = [{ x: 10, y: 10 }]
  direction.value = { x: 1, y: 0 }
  nextDirection.value = { x: 1, y: 0 }
  score.value = 0
  speed.value = 200
  placeFood()
  restartInterval()
}

const changeDirection = (x, y) => {
  if (gameStarted.value) {
    if (x !== -direction.value.x || y !== -direction.value.y) {
      nextDirection.value = { x, y }
    }
  }
}

const gameEnd = async () => {
  await saveScore(GameName.SNAKE, score.value, authStore.user.id)
}

onMounted(async () => {
  await authStore.fetchUser()
  console.log('User loaded:', authStore.user)
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
  <div class="game-container">
    <h1>Snake Game</h1>
    <h2 v-if="gameStarted">Score: {{ score }}</h2>

      <h2 v-if="gameOver">Final score: {{ score }}</h2>

    <div v-if="!gameStarted" class="start-screen">
      <p class="description">Move the snake using WASD keys or the arrow buttons below.</p>
      <button @click="startGame" class="start-button">Start Game</button>
    </div>

    <div class="grid" v-if="gameStarted">
      <div v-for="y in tileCount" :key="y" class="row">
        <div
          v-for="x in tileCount"
          :key="x"
          class="cell"
          :class="{
            snake: snake.some((segment) => segment.x === x - 1 && segment.y === y - 1),
            food: food.x === x - 1 && food.y === y - 1,
          }"
          :style="{
            width: cellSize + 'px',
            height: cellSize + 'px',
            backgroundColor: food.x === x - 1 && food.y === y - 1 ? food.color : '',
          }"
        ></div>
      </div>
    </div>

    <div class="controls" v-if="gameStarted">
      <button class="left" @click="changeDirection(-1, 0)">◀</button>
      <div class="vertical-controls">
        <button @click="changeDirection(0, -1)">▲</button>
        <button @click="changeDirection(0, 1)">▼</button>
      </div>
      <button class="right" @click="changeDirection(1, 0)">▶</button>
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
  font-size: 1.3rem;
}

.grid {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.description {
  margin-top: 10px;
  font-size: 1.2rem;
}

.row {
  display: flex;
}

.cell {
  border: 1px solid #91acc2;
  background-color: white;
}

.snake {
  background-color: #007acc;
}

.food {
  background-color: #e79c49;
}

.start-screen {
  justify-content: center;
  margin-top: 30px;
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
  margin-top: 10px;
}

button:hover {
  background: #005f99;
}

.controls {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
  margin-bottom: 50px;
}

.vertical-controls {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 0;
}

.controls button {
  background: #007acc;
  color: white;
  border: none;
  padding: 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;
  font-size: 1.5rem;
  margin: 5px;
  width: 60px;
  height: 60px;
}

.controls button:hover {
  background: #005f99;
}

.left {
  margin-right: auto;
}

.right {
  margin-left: auto;
}
</style>

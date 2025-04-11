<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../services/auth'
import { useRouter } from 'vue-router'
import { GameName, saveScore } from '@/utils/requests.js'
import Navigation from './Navigation.vue'

const icons = ['φ', 'Ψ', 'λ', 'π', 'ξ', 'Ω', 'Σ', 'θ', 'Δ']
const cards = ref([])
const flippedCards = ref([])
const matchedCards = ref([])
const lockBoard = ref(false)
let score = 0
const gain = 100
const loss = 30
const flipCounts = ref({})
let nbFlipped = 0
const authStore = useAuthStore()
const router = useRouter()

const gameStarted = ref(false)
const gameOver = ref(false)

const restartGame = () => {
  gameStarted.value = true
  gameOver.value = false
  score = 0
  nbFlipped = 0
  flippedCards.value = []
  matchedCards.value = []
  flipCounts.value = {}
  generateCards()
}

onMounted(async () => {
  await authStore.fetchUser()
  if (!authStore.user) {
    router.push('/login')
    return
  }
  score = 0
  nbFlipped = 0
  generateCards()
})

const generateCards = () => {
  const duplicatedIcons = [...icons, ...icons]
  cards.value = duplicatedIcons
    .sort(() => Math.random() - 0.5)
    .map((icon, index) => ({
      id: index,
      icon,
      flipped: false,
    }))
}

const flipCard = (card) => {
  if (lockBoard.value || card.flipped) return

  if (!flipCounts.value[card.id]) flipCounts.value[card.id] = 0
  flipCounts.value[card.id]++

  card.flipped = true
  flippedCards.value.push(card)

  if (flippedCards.value.length === 2) {
    checkMatch()
  }
}

const checkMatch = () => {
  lockBoard.value = true
  const [card1, card2] = flippedCards.value

  if (card1.icon === card2.icon) {
    matchedCards.value.push(card1.id, card2.id)
    score += gain
    nbFlipped++
    if (nbFlipped === icons.length) gameEnd()
    resetTurn()
  } else {
    score -= loss * ((flipCounts.value[flippedCards.value[0].id] - 1) + (flipCounts.value[flippedCards.value[1].id] - 1))
    setTimeout(() => {
      card1.flipped = false
      card2.flipped = false
      resetTurn()
    }, 1000)
  }
}

const getCardColor = (card) => {
  const minFlips = Math.min(...Object.values(flipCounts.value), 1)
  const maxFlips = Math.max(...Object.values(flipCounts.value), 4)
  const flips = flipCounts.value[card.id] || 1


  const percentage = (flips - minFlips) / (maxFlips - minFlips)
  const hue = Math.round(100 * (1 - percentage))

  return `hsl(${hue}, 100%, 45%)`
}

const resetTurn = () => {
  flippedCards.value = []
  lockBoard.value = false
}

const gameEnd = async () => {
  await saveScore(GameName.MEMORY, score, authStore.user.id)
  gameOver.value = true
  gameStarted.value = false
}

onMounted(() => {
  score = 0
  nbFlipped = 0
  generateCards()
})
</script>

<template>
  <Navigation v-if="!gameStarted" :gameName="GameName.MEMORY" :modeId="false"/>
  <div class="memory">
    <h1>Memory Game</h1>
    <p v-if="!gameStarted"> Match all pairs of symbols by flipping cards two at a time. The fewer attempts you make, the higher your score!</p>
    <button v-if="!gameStarted" @click="restartGame" class="btn-start">Start</button><br>

    <h2 v-if="gameStarted || gameOver"> Score: {{ score }}</h2>

    <div v-if="gameStarted && !gameOver" class="grid">
      <div
        v-for="card in cards"
        :key="card.id"
        class="card"
        :class="{ flipped: card.flipped }"
        @click="flipCard(card)"
      >
        <span v-if="card.flipped">{{ card.icon }}</span>
      </div>
    </div>

    <div v-if="!gameStarted && gameOver">
      <div class="grid heatmap">
        <div
          v-for="card in cards"
          :key="card.id"
          class="card heatmap-card"
          :style="{ backgroundColor: getCardColor(card) }"
        >
          {{ card.icon }}
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped>
.memory {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  font-family: Arial, sans-serif;
  text-align: center;
  margin-inline: auto;
  padding: 20px;
}

.btn-start {
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

.btn-start:hover {
  background: #005f99;
}

.start-btn:hover {
  background: #005f99;
}

h1 {
  color: #007acc;
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

.grid {
  display: grid;
  gap: 10px;
  margin-inline: auto;
  margin-top: 0.8rem;
  max-width: 90vw;
}

.card {
  width: clamp(80px, 10vw, 120px);
  height: clamp(80px, 10vw, 120px);
  font-size: clamp(1.5rem, 3vw, 3rem);
  background: #007acc;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s,
  font-size 0.3s;
  color: white;
}

@media (max-width: 600px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
  }
}

@media (min-width: 601px) {
  .grid {
    grid-template-columns: repeat(6, 1fr);
  }
}

.card.flipped {
  transform: rotateY(180deg);
  background-color: #005f99;
}

.heatmap {
  margin-top: 1rem;
}

.heatmap-card {
  cursor: default;
}
</style>

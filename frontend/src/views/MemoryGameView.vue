<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../services/auth'

const icons = ['🍎', '🍌', '🍇', '🍉', '🍍', '🥑', '🥕', '🌽', '🎃']
const cards = ref([])
const flippedCards = ref([])
const matchedCards = ref([])
const lockBoard = ref(false)
let score = 0
const gain = 150
const loss = 50
let nbFlipped = 0
const authStore = useAuthStore()

onMounted(async () => {
  await authStore.fetchUser()
  console.log('User loaded:', authStore.user)
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
    score -= loss
    setTimeout(() => {
      card1.flipped = false
      card2.flipped = false
      resetTurn()
    }, 1000)
  }
}

const resetTurn = () => {
  flippedCards.value = []
  lockBoard.value = false
}

const gameEnd = () => {
  console.log('END ! with score ' + score)
  console.log(authStore.user?.id)
  // save the score
}

onMounted(() => {
  score = 0
  nbFlipped = 0
  generateCards()
})
</script>

<template>
  <div class="memory">
    <h1>Memory Game</h1>
    <h2>{{ score }}</h2>
    <div class="grid">
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
  </div>
</template>

<style scoped>
.memory {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 700px;
  font-family: Arial, sans-serif;
}

h1 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.grid {
  display: grid;
  gap: 10px;
  margin: auto;
  max-width: 90vw;
}

.card {
  width: clamp(60px, 10vw, 120px);
  height: clamp(60px, 10vw, 120px);
  font-size: clamp(1.5rem, 3vw, 3rem);
  background: lightskyblue;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s, font-size 0.3s;
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
}
</style>

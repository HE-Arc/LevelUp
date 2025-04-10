<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { useAuthStore } from '@/services/auth.js'
import { useRouter } from 'vue-router'
import { wordList } from '@/utils/wordList.js'
import { GameName, saveScore } from '@/utils/requests.js'

const authStore = useAuthStore()
const router = useRouter()
const textInput = ref(null)

const totalTime = 60
const currentLine = ref([])
const nextLine = ref([])
const currentWordIndex = ref(0)
const inputText = ref('')
const timeLeft = ref(totalTime)
const score = ref(0)
const gameStarted = ref(false)
const gameOver = ref(false)
const timer = ref(null)
const correctWords = ref([])
const wrongWords = ref([])
const wordStatus = ref([])
const shuffled = ref([])
const nbWordPerLine = ref(10)

const updateNbWordPerLine = () => {
  const screenWidth = window.innerWidth
  if (screenWidth < 480) {
    nbWordPerLine.value = 4
  } else if (screenWidth < 768) {
    nbWordPerLine.value = 6
  } else if (screenWidth < 1024) {
    nbWordPerLine.value = 8
  } else {
    nbWordPerLine.value = 10
  }
}

const displayWords = computed(() => {
  return [
    currentLine.value.map((word, index) => ({
      text: word,
      status: index < currentWordIndex.value ? wordStatus.value[index] : null,
      current: index === currentWordIndex.value && gameStarted.value,
    })),
    nextLine.value.map((word) => ({
      text: word,
      status: null,
      current: false,
    })),
  ]
})

const initGame = () => {
  currentLine.value = shuffled.value.slice(0, nbWordPerLine.value)
  nextLine.value = shuffled.value.slice(nbWordPerLine.value, nbWordPerLine.value*2)
  wordStatus.value = Array(10).fill(null)
  currentWordIndex.value = 0
  inputText.value = ''
}

const startGame = () => {
  initGame()
  gameStarted.value = true
  gameOver.value = false
  timeLeft.value = totalTime
  score.value = 0
  correctWords.value = []
  wrongWords.value = []

  timer.value = setInterval(() => {
    timeLeft.value--
    if (timeLeft.value <= 0) {
      endGame()
    }
  }, 1000)
}

const checkWord = () => {
  const currentWord = currentLine.value[currentWordIndex.value]
  const isCorrect = inputText.value.trim() === currentWord

  wordStatus.value[currentWordIndex.value] = isCorrect ? 'correct' : 'wrong'

  if (isCorrect) {
    score.value++
    correctWords.value.push(currentWord)
  } else {
    wrongWords.value.push(currentWord)
  }

  inputText.value = ''
  currentWordIndex.value++

  if (currentWordIndex.value >= currentLine.value.length) {
    currentLine.value = [...nextLine.value]
    wordStatus.value = Array(nbWordPerLine.value).fill(null)
    currentWordIndex.value = 0

    const usedWords = [...currentLine.value, ...nextLine.value]
    const availableWords = wordList.filter((word) => !usedWords.includes(word))
    const shuffled = [...availableWords].sort(() => Math.random() - 0.5)
    nextLine.value = shuffled.slice(0, nbWordPerLine.value)
  }
}

const handleInputChange = () => {
  if (!gameStarted.value) {
    startGame()
    return
  }
  if (inputText.value.endsWith(' ')) {
    inputText.value = inputText.value.trim()
    checkWord()
  }
}

const endGame = async () => {
  clearInterval(timer.value)
  await saveScore(GameName.TYPING, score.value, authStore.user.id)
  gameOver.value = true
  gameStarted.value = false
}

const restartGame = () => {
  shuffled.value = [...wordList].sort(() => Math.random() - 0.5)
  gameOver.value = false
  timeLeft.value = totalTime
  score.value = 0
  correctWords.value = []
  wrongWords.value = []
  initGame()
}

onMounted(async () => {
  await authStore.fetchUser()
  if (!authStore.user) {
    router.push('/login')
  }
  window.addEventListener('resize', updateNbWordPerLine)
  updateNbWordPerLine()
  shuffled.value = [...wordList].sort(() => Math.random() - 0.5)
  initGame()
})

onUnmounted(() => {
  window.removeEventListener('resize', updateNbWordPerLine)
})
</script>

<template>
  <div class="typing-game">
    <h1>Typing Game</h1>

    <div v-if="!gameOver" class="game-container">
      <div class="game-header">
        <div class="timer">Time: {{ timeLeft }}s</div>
        <div class="score">Score: {{ score }}</div>
      </div>

      <div class="word-display">
        <div class="word-line" v-for="(line, lineIndex) in displayWords" :key="lineIndex">
          <span
            v-for="(word, wordIndex) in line"
            :key="wordIndex"
            class="word"
            :class="{
              current: word.current,
              correct: word.status === 'correct',
              wrong: word.status === 'wrong',
            }"
          >
            {{ word.text }}
          </span>
        </div>
      </div>

      <input
        type="text"
        v-model="inputText"
        @input="handleInputChange"
        placeholder="Type the word and press space"
        ref="textInput"
        class="game-input"
        autofocus
      />
    </div>

    <div v-if="gameOver" class="results">
      <h2>Result</h2>
      <div class="stats">
        <div>Final score: {{ score }}</div>
        <div>
          Precision:
          {{
            Math.round((correctWords.length / (correctWords.length + wrongWords.length)) * 100) ||
            0
          }}%
        </div>
      </div>

      <div class="word-results">
        <div class="correct-words">
          <h3>Correct words ({{ correctWords.length }})</h3>
        </div>

        <div class="wrong-words">
          <h3>Wrong words ({{ wrongWords.length }})</h3>
        </div>
      </div>

      <button @click="restartGame" class="restart-button">Restart</button>
    </div>
  </div>
</template>

<style scoped>
.typing-game {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
  font-family: Arial, sans-serif;
}

h1 {
  color: #007acc;
  margin-bottom: 20px;
}

.game-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  font-size: 1.2rem;
  color: #007acc;
}

.word-display {
  margin: 30px 0;
  text-align: center;
  line-height: 1;
  padding-top: 10px;
}

.word-line {
  margin-bottom: 15px;
}

.word {
  margin-right: 5px;
  padding: 3px 5px;
  border-radius: 3px;
  font-size: 1.5rem;
}

.word.current {
  background-color: #007acc;
  color: white;
}

.word.correct {
  color: #4caf50;
}

.word.wrong {
  color: #f44336;
}

.game-input {
  width: 60%;
  padding: 15px;
  font-size: 1.2rem;
  border: 2px solid #007acc;
  border-radius: 5px;
  text-align: center;
  margin-top: 10px;
}

.results {
  margin-top: 30px;
}

.stats {
  display: flex;
  justify-content: space-around;
  margin: 30px 0;
  font-size: 1.2rem;
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 5px;
}

.word-results {
  display: flex;
  margin-top: 30px;
  text-align: center;
  gap: 20px;
}

.correct-words,
.wrong-words {
  flex: 1;
}

.correct-words h3 {
  color: #4caf50;
}

.wrong-words h3 {
  color: #f44336;
}

.restart-button {
  background: #007acc;
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 5px;
  font-size: 1.2rem;
  cursor: pointer;
  margin-top: 20px;
}

@media screen and (max-width: 768px) {
  .typing-game {
    padding: 10px;
  }

  @media screen and (max-width: 768px) {
    .word {
      font-size: 1.3rem;
    }

    .game-input {
      width: 80%;
      font-size: 1.2rem;
      padding: 10px;
    }
  }

  .word-results {
    flex-direction: column;
  }
}
</style>

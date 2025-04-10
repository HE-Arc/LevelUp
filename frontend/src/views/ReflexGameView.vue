<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useAuthStore } from '../services/auth';
import { useRouter } from 'vue-router';
import { GameName, saveScore } from '@/utils/requests.js'
import Navigation from './Navigation.vue'

const authStore = useAuthStore();
const router = useRouter();

const colors = ['e33', 'e93', 'ed3', '3b9', '39e', '93e', 'e39'];
const gridSize = 5;
const grid = ref([]);
const oddColorIndex = ref(0);
const score = ref(0);
const timeLeft = ref(30);
const timer = ref(null);
const gameStarted = ref(false);
const gameOver = ref(false);

const startButtonShow = ref(true)
const timeToShowStartButton = ref(1)

onMounted(async () => {
  await authStore.fetchUser();
  if (!authStore.user) {
    router.push('/login');
  }
});

const startGame = () => {
  score.value = 0;
  timeLeft.value = 30;
  gameStarted.value = true;
  gameOver.value = false;
  timeToShowStartButton.value = 1
  startButtonShow.value = false
  generateGrid();

  if (timer.value) clearInterval(timer.value);
  timer.value = setInterval(() => {
    timeLeft.value--;
    if (timeLeft.value <= 0) stopGame();
  }, 1000);
};

const stopGame = async () => {
  clearInterval(timer.value);
  timer.value = null;
  gameStarted.value = false;
  gameOver.value = true;
  await saveScore(GameName.REFLEX, score.value, authStore.user.id)

  if (timer.value) clearInterval(timer.value);
  timer.value = setInterval(() => {
    timeLeft.value--;
    if (timeToShowStartButton.value > 0) {
      timeToShowStartButton.value--
    } else {
      clearInterval(timer)
      startButtonShow.value = true
    }
  }, 1000);
};

const generateGrid = () => {
  const baseColorIndex = Math.floor(Math.random() * colors.length);
  const oddIndex = Math.floor(Math.random() * (gridSize * gridSize));
  const oddColorOffset = (2 + Math.floor(Math.random() * 2)) % colors.length;

  grid.value = Array.from({ length: gridSize * gridSize }, (_, index) => ({
    id: index,
    color: index === oddIndex ? `#${colors[(baseColorIndex + oddColorOffset) % colors.length]}` : `#${colors[baseColorIndex]}`,
  }));

  oddColorIndex.value = oddIndex;
};

const checkAnswer = (index) => {
  if (!gameStarted.value) return;

  if (index === oddColorIndex.value) {
    score.value++;
  } else {
    timeLeft.value = Math.max(0, timeLeft.value - 2);
  }
  generateGrid();
};

const formattedTime = computed(() => {
  return `${String(timeLeft.value).padStart(2, '0')}s`;
});

onBeforeUnmount(() => {
  stopGame();
});
</script>

<template>
  <Navigation v-if="!gameStarted" :gameName="GameName.REFLEX" :modeId="false"/>
  <div class="game-container">
    <h1>Reflex Game</h1>
    <p v-if="!gameStarted">Press “Start” and click on the differents colors, you have 30 secondes to click as much as ou can!</p>
    <h2 v-if="gameOver">Final score: {{ score }}</h2>
    <h2 v-if="gameStarted">Time left: {{ formattedTime }}, Score: {{ score }}</h2>
    <button class="btn-start" @click="startGame" v-if="!gameStarted && startButtonShow">Start</button>

    <div class="grid" v-if="gameStarted">
      <button
        v-for="(cell, index) in grid"
        :key="cell.id"
        :style="{ backgroundColor: cell.color }"
        @click="checkAnswer(index)"
      ></button>
    </div>
  </div>
</template>

<style scoped>
.game-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  font-family: Arial, sans-serif;
  text-align: center;
  margin-inline: auto;
  max-width: 400px;
  padding: 20px;
}

.grid {
  display: grid;
  grid-template-columns: v-bind(`repeat(${gridSize}, 1fr)`);
  gap: 10px;
  margin-top: 20px;
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

button {
  width: 60px;
  height: 60px;
  border: none;
  cursor: pointer;
  border-radius: 10px;
  transition: transform 0.1s ease-in-out;
}

button:active {
  transform: scale(0.9);
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

@media (max-width: 600px) {
  .grid {
    gap: 8px;
  }

  button {
    width: 50px;
    height: 50px;
  }
}
</style>

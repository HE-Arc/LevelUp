<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useAuthStore } from '../services/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const colors = ['e33', 'e93', 'ed3', '3b9', '39e', '93e', 'e39'];
const gridSize = 5; //taille de la grille (dynamique)
const grid = ref([]);
const oddColorIndex = ref(0);
const score = ref(0);
const timeLeft = ref(30); //temps de la partie
const timer = ref(null);
const gameStarted = ref(false);
const gameOver = ref(false);

onMounted(async () => {
  await authStore.fetchUser();
  if (!authStore.user) {
    router.push('/login');
    return;
  }
});

const startGame = () => {
  score.value = 0;
  timeLeft.value = 30;
  gameStarted.value = true;
  gameOver.value = false;
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
  await saveScore(1, GameId.REFLEX, score);
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
    timeLeft.value = Math.max(0, timeLeft.value - 2); //pénalité si mauvais carré, -2 sec
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
  <div class="game-container">
    <h1>Reflex Game</h1>
    <h2 v-if="gameOver">Score final : {{ score }}</h2>
    <h2 v-if="gameStarted">Temps restant: {{ formattedTime }}</h2>
    <h2 v-if="gameStarted">Score: {{ score }}</h2>
    <button @click="startGame" v-if="!gameStarted">Start</button>

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
}

.grid {
  display: grid;
  grid-template-columns: v-bind(`repeat(${gridSize}, 1fr)`);
  gap: 10px;
  margin-top: 20px;
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

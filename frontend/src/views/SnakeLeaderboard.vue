<script setup>
import { ref, onMounted } from 'vue';
import LeaderboardView from '@/views/LeaderboardView.vue';
import { GameName, getLeaderboard, getRecords } from '@/utils/requests.js'

const snakePlayers = ref([]);
const snakeRecords = ref([]);

onMounted(async () => {
  try {
    snakePlayers.value = await getLeaderboard(GameName.SNAKE);
    snakeRecords.value = await getRecords(GameName.SNAKE);
  } catch (error) {
    console.error(error);
  }
});
</script>

<template>
  <LeaderboardView title="Snake Game" :players="snakePlayers" :records="snakeRecords" />
</template>

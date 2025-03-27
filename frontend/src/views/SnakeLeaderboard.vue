<script setup>
import { ref, onMounted } from 'vue';
import LeaderboardView from '@/views/LeaderboardView.vue';
import { GameName, getLeaderboard } from '@/utils/requests.js';

const snakePlayers = ref([]);

onMounted(async () => {
  try {
    snakePlayers.value = await getLeaderboard(GameName.SNAKE);
  } catch (error) {
    console.error(error);
  }
});
</script>

<template>
  <LeaderboardView title="Snake Game" :players="snakePlayers" />
</template>

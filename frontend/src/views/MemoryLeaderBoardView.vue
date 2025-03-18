<script setup>
import { ref, onMounted } from 'vue';
import LeaderboardView from '@/views/LeaderboardView.vue';
import { GameId, getLeaderboard } from '@/utils/requests.js';

const memoryPlayers = ref([]);

onMounted(async () => {
  try {
    memoryPlayers.value = await getLeaderboard(GameId.MEMORY);
  } catch (error) {
    console.error(error);
  }
});
</script>

<template>
  <LeaderboardView title="Memory Game" :players="memoryPlayers" />
</template>

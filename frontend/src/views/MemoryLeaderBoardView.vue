<script setup>
import { ref, onMounted } from 'vue';
import LeaderboardView from '@/views/LeaderboardView.vue';
import { GameName, getLeaderboard } from '@/utils/requests.js';

const memoryPlayers = ref([]);

onMounted(async () => {
  try {
    memoryPlayers.value = await getLeaderboard(GameName.MEMORY);
  } catch (error) {
    console.error(error);
  }
});
</script>

<template>
  <LeaderboardView title="Memory Game" :players="memoryPlayers" />
</template>

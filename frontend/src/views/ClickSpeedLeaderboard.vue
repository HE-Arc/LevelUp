<script setup>
import { ref, onMounted } from 'vue';
import LeaderboardView from '@/views/LeaderboardView.vue';
import { GameId, getLeaderboard } from '@/utils/requests.js';

const clickSpeedPlayers = ref([]);

onMounted(async () => {
  try {
    clickSpeedPlayers.value = await getLeaderboard(GameId.CLICKSPEED);
  } catch (error) {
    console.error(error);
  }
});
</script>

<template>
  <LeaderboardView title="Click Speed Game" :players="clickSpeedPlayers" />
</template>

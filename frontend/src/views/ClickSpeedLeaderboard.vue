<script setup>
import { ref, onMounted } from 'vue';
import LeaderboardView from '@/views/LeaderboardView.vue';
import { GameName, getLeaderboard } from '@/utils/requests.js';

const clickSpeedPlayers = ref([]);

onMounted(async () => {
  try {
    clickSpeedPlayers.value = await getLeaderboard(GameName.CLICKSPEED);
  } catch (error) {
    console.error(error);
  }
});
</script>

<template>
  <LeaderboardView title="Click Speed Game" :players="clickSpeedPlayers" />
</template>

<script setup>
import { ref, onMounted } from 'vue';
import LeaderboardView from '@/views/LeaderboardView.vue';
import { GameName, getLeaderboard } from '@/utils/requests.js';

const reflexPlayers = ref([]);

onMounted(async () => {
  try {
    reflexPlayers.value = await getLeaderboard(GameName.REFLEX);
  } catch (error) {
    console.error(error);
  }
});
</script>

<template>
  <LeaderboardView title="Reflex Game" :players="reflexPlayers" />
</template>

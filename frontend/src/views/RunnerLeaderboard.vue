<script setup>
import { ref, onMounted } from 'vue';
import LeaderboardView from '@/views/LeaderboardView.vue';
import { GameName, getLeaderboard, getRecords } from '@/utils/requests.js'

const runnerPlayers = ref([]);
const runnerRecords = ref([]);

onMounted(async () => {
  try {
    runnerPlayers.value = await getLeaderboard(GameName.RUNNER);
    runnerRecords.value = await getRecords(GameName.RUNNER);
  } catch (error) {
    console.error(error);
  }
});
</script>

<template>
  <LeaderboardView title="Runner" :game="GameName.RUNNER" :players="runnerPlayers" :records="runnerRecords" />
</template>

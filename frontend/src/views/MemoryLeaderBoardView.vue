<script setup>
import { ref, onMounted } from 'vue';
import LeaderboardView from '@/views/LeaderboardView.vue';
import { GameName, getLeaderboard, getRecords } from '@/utils/requests.js'

const memoryPlayers = ref([]);
const memoryRecords = ref([]);

onMounted(async () => {
  try {
    memoryPlayers.value = await getLeaderboard(GameName.MEMORY);
    memoryRecords.value = await getRecords(GameName.MEMORY);
  } catch (error) {
    console.error(error);
  }
});
</script>

<template>
  <LeaderboardView title="Memory" :game="GameName.MEMORY" :players="memoryPlayers" :records="memoryRecords" />
</template>

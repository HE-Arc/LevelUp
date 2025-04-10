<script setup>
import { ref, onMounted } from 'vue';
import LeaderboardView from '@/views/LeaderboardView.vue';
import { GameName, getLeaderboard, getRecords } from '@/utils/requests.js'

const reflexPlayers = ref([]);
const reflexRecords = ref([]);

onMounted(async () => {
  try {
    reflexPlayers.value = await getLeaderboard(GameName.REFLEX);
    reflexRecords.value = await getRecords(GameName.REFLEX);
  } catch (error) {
    console.error(error);
  }
});
</script>

<template>
  <LeaderboardView title="Reflex" :game="GameName.REFLEX" :players="reflexPlayers" :records="reflexRecords" />
</template>

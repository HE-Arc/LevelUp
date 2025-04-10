<script setup>
import { ref, onMounted } from 'vue';
import LeaderboardView from '@/views/LeaderboardView.vue';
import { GameName, getLeaderboard, getRecords } from '@/utils/requests.js'
import Navigation from './Navigation.vue'

const clickSpeedPlayers = ref([]);
const clickSpeedRecords = ref([]);

onMounted(async () => {
  try {
    clickSpeedPlayers.value = await getLeaderboard(GameName.CLICKSPEED);
    clickSpeedRecords.value = await getRecords(GameName.CLICKSPEED);
  } catch (error) {
    console.error(error);
  }
});
</script>

<template>
  <LeaderboardView title="Click Speed" :game="GameName.CLICKSPEED" :players="clickSpeedPlayers" :records="clickSpeedRecords" />
</template>

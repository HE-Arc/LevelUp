<script setup>
import { ref, onMounted } from 'vue';
import LeaderboardView from '@/views/LeaderboardView.vue';
import { GameName, getLeaderboard, getRecords } from '@/utils/requests.js'

const typingPlayers = ref([]);
const typingRecords = ref([]);

onMounted(async () => {
  try {
    typingPlayers.value = await getLeaderboard(GameName.TYPING);
    typingRecords.value = await getRecords(GameName.TYPING);
  } catch (error) {
    console.error(error);
  }
});
</script>

<template>
  <LeaderboardView title="Typing" :game="GameName.TYPING" :players="typingPlayers" :records="typingRecords" />
</template>

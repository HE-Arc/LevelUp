<script setup>
import { ref, onMounted } from 'vue';
import LeaderboardView from '@/views/LeaderboardView.vue';
import { GameName, getLeaderboard } from '@/utils/requests.js';

const typingPlayers = ref([]);

onMounted(async () => {
  try {
    typingPlayers.value = await getLeaderboard(GameName.TYPING);
  } catch (error) {
    console.error(error);
  }
});
</script>

<template>
  <LeaderboardView title="Typing Game" :players="typingPlayers" />
</template>

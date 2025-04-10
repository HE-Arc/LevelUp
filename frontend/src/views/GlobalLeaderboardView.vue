<script setup>
import { ref, onMounted } from 'vue';
import LeaderboardView from '@/views/LeaderboardView.vue';
import axios from 'axios'
import { API_BASE_URL } from '@/config.js'

const globalPlayers = ref([]);

onMounted(async () => {
  try {
    const res = await axios.get(`${API_BASE_URL}/rank_score_leaderboard`)
    const leaderboard = res.data;

    // Change rank_score to points, to match game leaderboards
    leaderboard.forEach((entry) => {
      entry.points = Math.round(entry.rank_score, 1);
      delete entry.rank_score;
    })

    globalPlayers.value = leaderboard;
  } catch (error) {
    console.error(error);
  }
});
</script>

<template>
  <LeaderboardView title="Level-up" :is-gloabal="true" :players="globalPlayers" />
</template>

<script setup>
import { defineProps } from 'vue'
defineProps({
  title: String,
  players: Array,
})
</script>

<template>
  <div class="leaderboard">
    <h1>{{ title }} Leaderboard</h1>
    <table>
      <thead>
      <tr>
        <th>Rang</th>
        <th>Nom</th>
        <th>Points</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(player, index) in players" :key="player.username">
        <td>#{{ index + 1 }}</td>
        <td>{{ player.username }}</td>
        <td>{{ player.points }}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.leaderboard {
  text-align: center;
  width: 90%;
  max-width: 1200px;
  margin-top: 30px;
  display: block;
  margin-left: auto;
  margin-right: auto;
}

h1 {
  color: #007acc;
}

table {
  width: 100%;
  margin-top: 2.5rem;
  border-collapse: collapse;
}

th,
td {
  padding: 10px;
  border: 1px solid #ddd;
}

th {
  background-color: #007acc;
  color: white;
}
</style>

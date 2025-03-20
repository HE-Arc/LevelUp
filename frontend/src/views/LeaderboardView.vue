<script setup>
import { defineProps, computed } from 'vue'
import { useAuthStore } from '@/services/auth'

const props = defineProps({
  title: String,
  players: Array,
})

const authStore = useAuthStore()
const currentUser = authStore.user.username

const sortedPlayers = computed(() => props.players.slice(0, 1))
const userEntry = computed(() => props.players.find(player => player.username === currentUser))
const isUserInTop10 = computed(() => sortedPlayers.value.some(player => player.username === currentUser))

</script>

<template>
  <div class="leaderboard">
    <h1>{{ title }} Leaderboard</h1>
    <div class="scrollable-table">
      <table>
        <thead>
          <tr>
            <th>Rang</th>
            <th>Nom</th>
            <th>Points</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(player, index) in props.players" :key="player.username"
              :class="{ 'highlight-user': player.username === currentUser }">
            <td>#{{ index + 1 }}</td>
            <td>{{ player.username }}</td>
            <td>{{ player.points }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <br>
    <div>
      <table>
        <tbody>
          <tr v-if="userEntry && !isUserInTop10" class="highlight-user">
            <td>#{{ props.players.indexOf(userEntry) + 1 }}</td>
            <td>{{ userEntry.username }}</td>
            <td>{{ userEntry.points }}</td>
          </tr>
        </tbody>
      </table>
    </div>
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

.scrollable-table {
  max-height: 400px;
  overflow-y: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 10px;
  border: 1px solid #ddd;
  width: 33.33%;
  text-align: center;
}

th {
  background-color: #007acc;
  color: white;
}

.highlight-user {
  background-color: #8dd35f;
  font-weight: bold;
  color: white;
}
</style>

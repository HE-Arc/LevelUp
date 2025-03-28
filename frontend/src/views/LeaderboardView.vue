<script setup>
import { defineProps, computed } from 'vue'
import { useAuthStore } from '@/services/auth'
import { Line } from 'vue-chartjs'
// eslint-disable-next-line no-unused-vars
import { Chart } from 'chart.js/auto'
import 'chartjs-adapter-date-fns'
import { frCH } from 'date-fns/locale'
import { format } from 'date-fns'

const props = defineProps({
  title: String,
  players: Array,
  records: Array,
})

const authStore = useAuthStore()
const currentUser = authStore.user.username

const sortedPlayers = computed(() => props.players.slice(0, 1))
const userEntry = computed(() => props.players.find(player => player.username === currentUser))
const isUserInTop10 = computed(() => sortedPlayers.value.some(player => player.username === currentUser))

const recordChartData = computed(() => {
  return {
    datasets: [
      {
        label: props.title + " Records",
        data: props.records.map((record) => {
          return {
            x: record.date,
            y: record.points
          }
        }),
      },
    ],
  }
})

const recordChartOptions = {
  responsive: true,
  scales: {
    x: {
      type: 'time',
      position: 'bottom',
      time: {
        minUnit: 'day',
        displayFormats: {
          day: 'dd MMM',
          month: 'MMM yyyy'
        }
      },
      adapters: {
        date: {
          locale: frCH
        }
      }
    }
  },
  plugins: {
    // Show custom tooltip when hovering on a point : formatted date, username, nb of points
    tooltip: {
      callbacks: {
        title: (items) => {
          return format(props.records[items[0].dataIndex].date, "dd MMMM yyyy", {locale: frCH});
        },
        beforeLabel: (item) => {
          return props.records[item.dataIndex].username;
        },
        label: (item) => {
          return "Points: " + props.records[item.dataIndex].points;
        }
      }
    }
  }
}

</script>

<template>
  <div class="leaderboard">
    <h1>{{ title }} Leaderboard</h1>

    <!-- Conteneur fixe pour l'en-tête -->
    <div class="table-header">
      <table>
        <thead>
          <tr>
            <th>Rang</th>
            <th>Nom</th>
            <th>Points</th>
          </tr>
        </thead>
      </table>
    </div>
    <div class="table-body">
      <table>
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
  <div v-if="props.records" class="chart-container">
    <h2>{{ props.title }} Records</h2>
    <Line class="chart" id="record-chart" :data="recordChartData" :options="recordChartOptions"></Line>
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

h1, h2 {
  color: #007acc;
}

/* Conteneur de l'en-tête du tableau */
.table-header {
  width: 100%;
  position: relative;
  background-color: #007acc;
  color: white;
  padding: 10px 0;
}

/* Conteneur scrollable pour le corps du tableau */
.table-body {
  max-height: 400px;
  overflow-y: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed; /* Empêche la redimension dynamique */
}

th {
  background-color: #007acc;
  color: white;
}

th,
td {
  padding: 10px;
  width: 33.33%;
  text-align: center;
}

td {
  border: 1px solid #ddd;
}

.highlight-user {
  background-color: #8dd35f;
  font-weight: bold;
  color: white;
}

.chart-container {
  text-align: center;
  width: 90%;
  max-width: 1200px;
  margin-top: 20px;
  margin-left: auto;
  margin-right: auto;
}

.chart {
  max-height: 400px;
}
</style>

<script setup>
const team = [
  {
    avatar: new URL('/team_avatars/Mael.webp', import.meta.url).href,
    lastName: 'Brandt',
    firstName: 'Maël',
    githubName: 'MaelBrandt',
  },
  {
    avatar: new URL('/team_avatars/Noa.webp', import.meta.url).href,
    lastName: 'Devanthéry',
    firstName: 'Noa',
    githubName: 'noa-devv',
  },
  {
    avatar: new URL('/team_avatars/Lorenzo.webp', import.meta.url).href,
    lastName: 'Di Benedetto',
    firstName: 'Lorenzo',
    githubName: 'lorenzodibenede',
  },
  {
    avatar: new URL('/team_avatars/Arnaud.webp', import.meta.url).href,
    lastName: 'Maître',
    firstName: 'Arnaud',
    githubName: 'Arnaud-Maitre',
  },
]
const sus = Math.floor(Math.random() * team.length)
</script>
<template>
  <div class="container">
    <h1>About Level-Up</h1>
    <p>
      Level-Up is a web application that allows users to play a collection of mini-games and compare
      their scores to others.
    </p>
    <p>
      The app has been developed in 2025 by a team of four students at HE-Arc, as part of a 3rd year
      web development course.
    </p>
    <h2>The Team</h2>
    <div class="team">
      <div v-for="[i, teamMember] of team.entries()" class="team-member">
        <div class="team-member-avatar">
          <img
            class="team-member-avatar-image"
            :src="teamMember.avatar"
            alt="Avatar"
            width="140px"
            height="160px"
          />
          <img
            v-if="i === sus && typeof $route.query.sus !== 'undefined'"
            class="team-member-avatar-knife"
            src="/public/team_avatars/Knife.webp"
          />
        </div>
        <div class="team-member-name">
          <b>{{ teamMember.lastName }}</b>
          <br />{{ teamMember.firstName }}
        </div>
        <div class="team-member-contact">
          <a :href="'https://github.com/' + teamMember.githubName" target="_blank">
            @{{ teamMember.githubName }}
          </a>
        </div>
      </div>
    </div>
    <img class="logo" src="/public/logo_he_arc.jpg" alt="he-arc logo" />
  </div>
  <a v-if="typeof $route.query.sus === 'undefined'" class="sus" href="?sus">
    <img height="20" :src="team[sus].avatar" alt="easter egg" />
  </a>
</template>

<style>
.container {
  max-width: 800px;
  margin-inline: auto;
  border-radius: 10px;
  background: white;
  padding: 20px;
}

h1,
h2 {
  color: #007acc;
  margin-bottom: 20px;
  text-align: center;
}

.container > p {
  text-align: left;
}

.logo {
  height: 50px;
}

.team {
  display: flow;
  text-align: center;
}

.team-member {
  border: 1px solid black;
  border-radius: 10px;
  padding: 10px;
  margin: 10px;
  width: 150px;
  display: inline-block;
}

.team-member-avatar {
  position: relative;
  text-align: left;
  width: 140px;
  height: 160px;
}

.team-member-avatar-image {
  position: absolute;
  object-fit: contain;
  z-index: 1;
}

.team-member-avatar-knife {
  position: absolute;
  width: 50px;
  top: 75px;
  transform: scaleY(-1);
  left: 105px;
}

.logo {
  display: block;
  margin: auto;
}

.sus {
  position: fixed;
  bottom: 0;
  left: 0;
}
</style>

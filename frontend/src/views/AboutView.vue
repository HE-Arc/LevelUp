<script setup>
const team = [
  {
    avatar: '/public/team_avatars/Mael.webp',
    lastName: 'Brandt',
    firstName: 'Maël',
    githubName: 'MaelBrandt',
  },
  {
    avatar: '/public/team_avatars/Noa.webp',
    lastName: 'Devanthéry',
    firstName: 'Noa',
    githubName: 'noa-devv',
  },
  {
    avatar: '/public/team_avatars/Lorenzo.webp',
    lastName: 'Di Benedetto',
    firstName: 'Lorenzo',
    githubName: 'lorenzodibenede',
  },
  {
    avatar: '/public/team_avatars/Arnaud.webp',
    lastName: 'Maître',
    firstName: 'Arnaud',
    githubName: 'Arnaud-Maitre',
  },
];
const sus = Math.floor(Math.random() * team.length);
</script>
<template>
  <div class="container">
    <h1>About Level-Up</h1>
    <p>
      Level-Up is a web application that allows users to play a collection of mini-games and
      compare their scores to others.
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
          <img v-if="i === sus && typeof $route.query.sus !== 'undefined'" class="team-member-avatar-knife" src="/public/team_avatars/Knife.webp" />
        </div>
        <div class="team-member-name">
          <b>{{ teamMember.lastName }}</b>
          <br />{{ teamMember.firstName }}
        </div>
        <div class="team-member-contact">
          <a :href="'https://github.com/' + teamMember.githubName" target="_blank">@{{ teamMember.githubName }}</a>
        </div>
      </div>
    </div>
    <img class="logo" src="/public/logo_he_arc.jpg" alt="he-arc logo" />
    <a v-if="typeof $route.query.sus === 'undefined'" href="?sus"><img class="sus" height="20" :src="team[sus].avatar" alt="he-arc logo" /></a>
  </div>
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
  position: absolute;
  bottom: 0;
  left: 0;
}
</style>

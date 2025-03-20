<script setup>
import { ref } from 'vue';
import { RouterLink, RouterView } from 'vue-router';

const isOpen = ref(false);

const toggleMenu = () => {
  isOpen.value = !isOpen.value;
};
</script>

<template>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css">
  <div class="app-container">
    <header>
      <div class="wrapper">
        <button class="hamburger" @click="toggleMenu">
          <i v-if="!isOpen" class="fa fa-bars"></i>
          <i v-if="isOpen" class="fa-solid fa-xmark"></i>
        </button>
        <nav :class="{ 'open': isOpen }">
          <RouterLink to="/" @click="toggleMenu">Home</RouterLink>
          <RouterLink to="/about" @click="toggleMenu">About</RouterLink>
          <RouterLink to="/games" @click="toggleMenu">Games</RouterLink>
          <RouterLink to="/personal" @click="toggleMenu">My Account</RouterLink>
        </nav>
      </div>
    </header>
    <main>
      <RouterView/>
    </main>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 90vh;
  font-family: Arial, sans-serif;
}

header {
  line-height: 1.5;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background: #007acc;
  z-index: 1000;
  padding: 0.6rem;
  display: flex;
  align-items: center;
  height: 60px;
}

main {
  margin-top: 5em;
  flex: 1;
}

.hamburger {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  position: absolute;
  top: 50%;
  left: 10px;
  transform: translateY(-50%);
  z-index: 10;
  color: white;
}

nav {
  display: none;
  flex-direction: column;
  background: #007acc;
  position: absolute;
  top: 60px;
  right: 10px;
  padding: 1rem;
  border-radius: 5px;
  width: calc(100% - 20px);
}

nav.open {
  display: flex;
}

nav a {
  padding: 1rem;
  text-decoration: none;
  border-bottom: 1px solid white;
  color: white;
  font-size: 1.2rem;
}

nav a:last-child {
  border-bottom: none;
}

@media (min-width: 1024px) {
  .hamburger {
    display: none;
  }
  nav {
    display: flex;
    position: static;
    flex-direction: row;
    background: transparent;
    box-shadow: none;
    align-items: center;
    width: auto;
  }
  nav a {
    border: none;
    padding: 0 1rem;
    font-size: 1.2rem;
  }
}
</style>

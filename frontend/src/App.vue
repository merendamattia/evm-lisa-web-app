<script setup lang="ts">
import Navbar from './components/Navbar.vue';
import Footer from './components/Footer.vue';
</script>

<template>
  <Navbar />
  <div class="container mx-auto">
    <router-view />
  </div>
  <Footer />
</template>

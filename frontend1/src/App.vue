<script setup lang="ts">
  import Navbar from './components/Navbar.vue';
</script>

<template>

  <Navbar/>

  <div class="container mx-auto px-4">
    
    <router-view />
  
  </div>

</template>


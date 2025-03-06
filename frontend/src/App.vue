<script setup lang="ts">
import Navbar from './components/Navbar.vue';
import Footer from './components/Footer.vue';
import SuccessAlert from './components/SuccessAlert.vue';
import DangerPopup from './components/DangerPopup.vue';

</script>

<template>
  <Navbar />
  <div class="container mx-auto">
    <router-view />
  </div>
  <SuccessAlert />
  <DangerPopup/>
  <Footer />
</template>

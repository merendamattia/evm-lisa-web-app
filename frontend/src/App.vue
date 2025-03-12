<script setup lang="ts">
import MainNavbar from './components/MainNavbar.vue';
import MainFooter from './components/MainFooter.vue';
import SuccessAlert from './components/SuccessAlert.vue';
import DangerPopup from './components/DangerPopup.vue';

</script>

<template>
  <MainNavbar />
  <div class="container mx-auto">
    <router-view />
  </div>
  <SuccessAlert />
  <DangerPopup/>
  <MainFooter />
</template>

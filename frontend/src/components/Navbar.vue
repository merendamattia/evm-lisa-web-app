<script setup lang="ts">
import EtherscanAPIKey from './EtherscanAPIKey.vue';

</script>

<template>

  <nav class="bg-gray-100 w-full z-20 top-0 start-0 border-b border-gray-200 mb-3">
    <div class="container flex flex-wrap justify-between mx-auto p-4">
      <a href="" class="flex items-center space-x-3 rtl:space-x-reverse">
        <img src="/logo.png" class="h-12" alt="EVMLiSA Logo">
      </a>
      <div class="flex md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse">
        <EtherscanAPIKey/>
      </div>
    </div>
  </nav>

</template>
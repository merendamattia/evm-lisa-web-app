<template>
    <div>
      <div class="flex border-b">
        <button
          v-for="(tab, index) in tabs"
          :key="index"
          @click="activeTab = index"
          class="px-4 py-2 text-gray-600 hover:text-black border-b-2"
          :class="{
            'border-blue-500 text-blue-500 font-semibold': activeTab === index,
            'border-transparent': activeTab !== index
          }"
        >
          {{ tab.label }}
        </button>
      </div>
      <div class="p-4">
        <slot :name="tabs[activeTab].slotName"></slot>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, defineProps } from 'vue';
  
  const props = defineProps({
    tabs: {
      type: Array,
      required: true
    }
  });
  
  const activeTab = ref(0);
  </script>
  
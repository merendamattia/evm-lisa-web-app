<template>
  <div>
    <div class="flex border-b dark:border-gray-700 mt-5">
      <button
        v-for="(tab, index) in tabs"
        :key="index"
        @click="activeTab = index"
        class="px-4 py-2 text-gray-600 hover:text-black dark:text-gray-300 hover:dark:text-white border-b-2"
        :class="{
          'border-green-500 text-green-500 font-semibold dark:border-green-700 dark:text-green-400': activeTab === index,
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

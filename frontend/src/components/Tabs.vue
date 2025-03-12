<template>
  <div>
    <div class="flex border dark:border-gray-700 mt-5 sticky top-0 z-10 bg-white dark:bg-gray-800">
      <button
        v-for="(tab, index) in tabs"
        :key="index"
        @click="activeTab = index"
        class="px-4 py-2 border-2"
        :class="{
          'bg-green-500 text-white dark:bg-green-700 dark:text-white font-semibold': activeTab === index, // selezione tab
          'text-gray-600 dark:text-gray-300 hover:text-black hover:dark:text-white': activeTab !== index, // tab non selezionate
          'border-transparent': activeTab !== index, // rimuovi bordi per tab non selezionate
          'border-green-500': activeTab === index, // bordi per tab selezionata
        }"
      >
        {{ tab.label }}
      </button>
    </div>
    <div class="p-4 border dark:border-gray-700">
      <slot :name="props.tabs[activeTab].slotName"></slot>
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

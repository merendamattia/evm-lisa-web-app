<script setup>
const props = defineProps({
    data: {
        type: Array, // Accetta anche null
        required: true,
    },
});

// Funzione per formattare il PC con 5 cifre, aggiungendo zeri a sinistra
const formatPC = (pc) => {
    return pc.toString().padStart(5, '0'); // Aggiunge zeri a sinistra fino a 5 cifre
};
</script>

<template>
    <div v-if="props.data !== null" class="relative overflow-x-auto sm:rounded-lg">
      <!-- Itera sui BasicBlock -->
      <div v-for="(basicBlock, index) in props.data" :key="index" class="mb-5">
        <div class="border border-gray-300 dark:border-gray-700 rounded-lg">
          <div 
            class="p-1 border-b border-dashed border-gray-300 dark:border-gray-600" 
            v-for="(instruction, idx) in basicBlock.instructions" :key="idx"
          >
            <span 
              class="bg-gray-200 dark:bg-[#23592199] py-1 px-2 rounded-md font-mono mr-4"
            >
              {{ formatPC(instruction.pc) }}
            </span>
            <span 
              class="font-mono break-words max-w-full text-gray-900 dark:text-gray-300"
            >
              <strong>{{ instruction.instruction }}</strong>
            </span>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <p class="text-gray-600 dark:text-gray-300">No data available</p>
    </div>
  </template>


//#23592199

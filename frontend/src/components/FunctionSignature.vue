<template>
    <div v-for="fun in props.functions" :key="fun.selector">
      <div class="border border-gray-300 dark:border-gray-700 rounded-lg mb-5 p-3 font-mono">
        <div class="flex items-center">
          <div>
            <span class="bg-gray-200 dark:bg-[#23592199] py-1 px-2 rounded-md font-mono mr-4">
              {{ fun.selector }}
            </span>
          </div>
          <div class="flex flex-col space-y-2"> <!-- Flex col per allineamento verticale -->
            <div class="flex "> <!-- Allineamento verticale delle etichette -->
              <div class="font-bold">Signature:</div>
              <div>{{ fun.full_signature }}</div>
            </div>
            <div class="flex">
              <div class="font-bold">Type:</div>
              <div>{{ fun.type }}</div>
            </div>
            <div v-if="fun.output_param_count === 0" class="flex ">
              <div class="font-bold">Return Type:</div>
              <div>void</div>
            </div>
            <div v-else>
              <div v-for="(elem, index) in fun.output_param_types" :key="index" class="flex ">
                <div class="font-bold">Return Type:</div>
                <div>{{ elem }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { defineProps } from 'vue';
  
  export interface Fun {
    full_signature: string;
    name: string;
    selector: string;
    type: string;
    output_param_count: number;
    output_param_types: Array<string>;
  }
  
  const props = defineProps({
    functions: {
      type: Array as () => Fun[],
      required: true
    }
  });
  </script>
  
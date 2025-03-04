<script lang="ts">
// Define the component name for recursive references
export default {
  name: 'JsonViewer'
}
</script>

<script setup lang="ts">
import { defineProps, ref, computed } from "vue";

type JSONValue = string | number | boolean | null | JSONObject | JSONArray;
interface JSONObject { [key: string]: JSONValue; }
interface JSONArray extends Array<JSONValue> {}

const props = defineProps<{ data: JSONValue; level?: number }>();

const isObject = computed(() => typeof props.data === "object" && props.data !== null && !Array.isArray(props.data));
const isArray = computed(() => Array.isArray(props.data));

const isExpanded = ref(true);
</script>

<template>
  <div :style="{ marginLeft: `${(level || 0) * 15}px` }">
    <button v-if="(isObject || isArray) && (level || 0) > 0" @click="isExpanded = !isExpanded">
      {{ isExpanded ? "➖" : "➕" }}
    </button>

    <template v-if="isExpanded">
      <template v-if="isObject">
        <div v-for="(value, key) in data as JSONObject" :key="key">
          <strong class="jsonViewerKey">"{{ key }}": </strong> 
          <JsonViewer :data="value" :level="(level || 0) + 1" />
        </div>
      </template>

      <template v-else-if="isArray"> 
        <div v-for="(item, index) in data as JSONArray" :key="index">
          [{{ index }}]: 
          <JsonViewer :data="item" :level="(level || 0) + 1" />
        </div>
      </template>

      <template v-else>
        <span>{{ data }}</span>
      </template>
    </template>

    <template v-else>
      <span v-if="isObject">{...}</span>
      <span v-else-if="isArray">[...]</span>
    </template>
  </div>
</template>

<style lang="css" scoped>
.jsonViewerKey{
  color: #2b67c7;
}
</style>
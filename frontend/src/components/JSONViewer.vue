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
interface JSONArray extends Array<JSONValue> { }

const props = defineProps<{ data: JSONValue; level?: number }>();

// Funzioni per determinare il tipo dei dati
const isObject = computed(() => isObjectType(props.data));
const isArray = computed(() => isArrayType(props.data));
const isPrimitive = computed(() => isPrimitiveType(props.data));

// Funzione per determinare se è un oggetto
function isObjectType(value: JSONValue): boolean {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

// Funzione per determinare se è un array
function isArrayType(value: JSONValue): boolean {
  return Array.isArray(value);
}

// Funzione per determinare se è un tipo primitivo (stringa, numero, booleano, null)
function isPrimitiveType(value: JSONValue): boolean {
  return value === null || ["string", "number", "boolean"].includes(typeof value);
}

const isExpanded = ref(false);
</script>

<template>
  <div>

    <button @click="isExpanded = !isExpanded">
      {{ isExpanded ? "➖" : "➕" }}
    </button>

    <template v-if="isExpanded">
      <!-- Se è un oggetto -->
      <template v-if="isObject">

        <div v-for="(value, key) in data as JSONObject" :key="key">
          <div :style="{ marginLeft: (level || 0) * 15 + 'px' }">
            <span class="jsonViewerKey">"{{ key }}": </span>

                <span v-if="isObject && !isExpanded">{...}</span>
                <span v-else-if="isArray && isExpanded">[...] expand</span>
                
            <span v-if="isObjectType(value)"> {
              <JsonViewer :data="value" :level="(level || 0) + 1" />
              }
            </span>
            <span v-else-if="isArrayType(value)"> [
              <JsonViewer :data="value" :level="(level || 0) + 1" />
              ]
            </span>
            <span v-else class="jsonViewerValue">{{ value }}</span>,
          </div>
        </div>

      </template>

      <!-- Se è un array -->
      <template v-else-if="isArray">
        <div v-for="(item, index) in data as JSONArray" :key="index">
        <div :style="{ marginLeft: (level || 0) * 15 + 'px' }">
          <span v-if="isObjectType(item)"> {
            <JsonViewer :data="item" :level="(level || 0) + 1" />
            }, <span style="color : grey">[{{ index }}]</span>
          </span>
          <span v-else-if="isArrayType(item)"> [
            <JsonViewer :data="item" :level="(level || 0) + 1" />
            ]
          </span>
        </div>
        </div>
      </template>

      <!-- Se è un valore primitivo -->
      <template v-else>
        <span class="jsonViewerValue">{{ data }},</span>
      </template>
    </template>

    <template v-else>
      <span v-if="isObject">{...}</span>
      <span v-else-if="isArray">[...]</span>
    </template>
  </div>
</template>


<style lang="css" scoped>
.jsonViewerKey {
  color: #2b67c7;
  font-family: monospace;
}

.jsonViewerValue {
  color: #c7672b;
  font-family: monospace;
}
</style>
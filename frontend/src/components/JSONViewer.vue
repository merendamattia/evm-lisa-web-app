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

// Funzione per determinare se è un oggetto
function isObjectType(value: JSONValue): boolean {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

// Funzione per determinare se è un array
function isArrayType(value: JSONValue): boolean {
  return Array.isArray(value);
}

function toggleExpand() {
  isExpanded.value = !isExpanded.value;
  emit('toggleExpand', isExpanded.value); // Comunica al parent il cambio di stato
}

function isString(value: JSONValue): boolean {
  return typeof value === "string";
}

function isBoolean(value: JSONValue): boolean {
  return typeof value === "boolean";
}

function isInteger(value: JSONValue): boolean {
  return typeof value === "number" && Number.isInteger(value);
}

const isExpanded = ref(false);
const isValueExpanded = ref(false);

const emit = defineEmits(['toggleExpand']);

</script>

<template>
  <div>

    <template v-if="isExpanded">
      <!-- Se è un oggetto -->
      <template v-if="isObject">{

        <div v-for="(value, key) in data as JSONObject" :key="key">
          <div :style="{ marginLeft: (level || 0) * 10 + 'px', display: !isValueExpanded ? 'flex' : 'block' }">
            <span class="jsonViewerKey">"{{ key }}": </span>

            <span v-if="isObjectType(value)">
              <JsonViewer :data="value" :level="(level || 0) + 1" @toggleExpand="isValueExpanded = $event" />
            </span>
            <span v-else-if="isArrayType(value)">
              <JsonViewer :data="value" :level="(level || 0) + 1" @toggleExpand="isValueExpanded = $event" />
            </span>
            <span v-else :style="{ whiteSpace: 'nowrap' }">

              <span v-if="isString(value)" class="jsonViewerValueString" :style="{ whiteSpace: 'nowrap' }">"{{ value
                }}",</span>
              <span v-if="isInteger(value)" class="jsonViewerValueInt" :style="{ whiteSpace: 'nowrap' }">{{ value }},</span>
              <span v-if="isBoolean(value)" class="jsonViewerValueBool" :style="{ whiteSpace: 'nowrap' }">{{ value }},</span>

            </span>

          </div>
        </div>

        }<button @click="toggleExpand">
          <span class="bg-gray-100 text-gray-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded-lg">-</span>
        </button>
      </template>

      <!-- Se è un array -->
      <template v-else-if="isArray">[
        <div v-for="(item, index) in data as JSONArray" :key="index">
          <div :style="{ marginLeft: (level || 0) * 10 + 'px' }">

            <span v-if="isObjectType(item)">
              <JsonViewer :data="item" :level="(level || 0) + 1" @toggleExpand="isValueExpanded = $event" />
            </span>

            <span v-else-if="isArrayType(item)">
              <JsonViewer :data="item" :level="(level || 0) + 1" @toggleExpand="isValueExpanded = $event" />
            </span>

            <span v-else :style="{ whiteSpace: 'nowrap' }">

              <span v-if="isString(item)" class="jsonViewerValueString" :style="{ whiteSpace: 'nowrap' }">"{{ item
                }}",</span>
              <span v-if="isInteger(item)" class="jsonViewerValueInt" :style="{ whiteSpace: 'nowrap' }">{{ item }},</span>
              <span v-if="isBoolean(item)" class="jsonViewerValueBool" :style="{ whiteSpace: 'nowrap' }">{{ item }},</span>

            </span>

          </div>
        </div>

        ]
        <button @click="toggleExpand">
          <span class="bg-gray-100 text-gray-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded-lg">-</span>
        </button>
      </template>

      <!-- Se è un valore primitivo -->
      <template v-else>
        <span class="jsonViewerValue" :style="{ whiteSpace: 'nowrap' }">{{ data }}</span>
      </template>
    </template>

    <template v-else>
      <span v-if="isObject">{ ... }</span>
      <span v-else-if="isArray">[ ... ]</span>
      <button @click="toggleExpand">
        <span class="bg-gray-100 text-gray-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded-lg">+</span>
      </button>
    </template>

  </div>
</template>


<style lang="css" scoped>
.jsonViewerKey {
  color: #2b67c7;
  font-family: monospace;
}

.jsonViewerValueString {
  color: #c7672b;
  font-family: monospace;
}

.jsonViewerValueInt {
  color: #b7c72b;
  font-family: monospace;
}

.jsonViewerValueBool {
  color: #c7672b;
  font-family: monospace;
  font-weight: 700;
}
</style>
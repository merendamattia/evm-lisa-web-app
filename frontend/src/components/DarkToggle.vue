<script setup>
import { ref, onMounted, watch } from 'vue'

// Controlla il tema attuale
const isDark = ref(localStorage.getItem('theme') === 'dark' || false)

// Funzione per cambiare tema
const toggleTheme = () => {
  isDark.value = !isDark.value
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')

  if (isDark.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

// Applica il tema corretto all'avvio
onMounted(() => {
  if (isDark.value) document.documentElement.classList.add('dark')
})

// Guarda i cambiamenti di tema
watch(isDark, (newVal) => {
  localStorage.setItem('theme', newVal ? 'dark' : 'light')
})
</script>

<template>
  <button 
    @click="toggleTheme"
    class="relative flex items-center w-14 h-7 p-1 bg-gray-300 dark:bg-gray-700 rounded-full transition-colors duration-300"
  >
    <!-- Pallino con icone sole/luna -->
    <div 
      class="absolute left-1 w-5 h-5 flex items-center justify-center text-sm font-bold 
             bg-white dark:bg-gray-900 rounded-full shadow-md transform transition-transform duration-300"
      :class="{ 'translate-x-7': isDark }"
    >
      <span v-if="isDark">🌙</span>
      <span v-else>🌞</span>
    </div>
  </button>
</template>

<style>
/* Abilita il tema scuro */
.dark {
  background-color: #1a202c;
  color: #ffffff;
}
</style>

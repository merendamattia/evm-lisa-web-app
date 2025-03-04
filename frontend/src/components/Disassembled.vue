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
            <div style="border: 1px gray solid; border-radius: 5px;">
                <div style="display: flex; align-items: center; border-bottom: 1px dashed grey;" class="p-1" v-for="(instruction, idx) in basicBlock.instructions" :key="idx">
                    <span style="background-color: #dfdfdf; padding: 3px; padding-left: 8px; padding-right: 8px; border-radius: 5px; align-items: center;" class="font-mono mr-4">{{ formatPC(instruction.pc) }}</span>
                    <!-- Aggiungi word-wrap o word-break per far andare a capo -->
                    <span style="align-items: center; word-wrap: break-word; word-break: break-word; max-width: 100vw;" class="font-mono"><strong>{{ instruction.instruction }}</strong></span>
                </div>
            </div>
        </div>
    </div>
    <div v-else>
        <p>No data available</p> <!-- Aggiungi un messaggio nel caso in cui data sia null -->
    </div>
</template>

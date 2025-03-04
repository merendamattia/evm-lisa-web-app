<template>
    <div class="custom-node" :class="{ 'expanded': isExpanded }">
        <div class="custom-node__header">{{ data.label }}</div>
        <div class="custom-node__body" :style="{ backgroundColor: `${data.bgColor}` }">
            <div v-for="(item, index) in visibleInstructions" :key="index" class="instruction-container">
                <!-- Istruzioni -->
                <div v-if="item.type === 'instruction'" class="instruction">
                    <div><span class="span_pc">{{ item.data.pc }}</span> {{ item.data.instruction }}</div>
                </div>

                <!-- Puntini cliccabili -->
                <div v-else 
                     class="dots-container" 
                     @click="toggleExpand"
                     :title="isExpanded ? 'Click to collapse' : 'Click to expand'">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                </div>
            </div>

            <!-- X di chiusura come ultimo elemento -->
            <button v-if="isExpanded" class="close-btn" @click="collapseNode" title="Collapse">
                ×
            </button>
        </div>
        <div class="custom-node__handles">
            <div class="custom-node__handle custom-node__handle--source" :data-handleid="'source'" :data-nodeid="id"></div>
            <div class="custom-node__handle custom-node__handle--target" :data-handleid="'target'" :data-nodeid="id"></div>
        </div>
    </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
    id: {
        type: String,
        required: true
    },
    data: {
        type: Object,
        required: true
    }
})

const isExpanded = ref(false)

const collapseNode = () => {
    isExpanded.value = false
}

const toggleExpand = () => {
    isExpanded.value = !isExpanded.value
}

const formatPC = (pc) => pc.toString().padStart(5, '0')

const visibleInstructions = computed(() => {
    const instructions = props.data.instructions || []
    if (instructions.length === 0) return []

    const formatted = instructions.map(inst => ({
        ...inst,
        pc: formatPC(inst.pc)
    }))

    if (isExpanded.value || instructions.length <= 4) {
        return formatted.map(inst => ({ type: 'instruction', data: inst }))
    }

    return [
        { type: 'instruction', data: formatted[0] },
        { type: 'instruction', data: formatted[1] },
        { type: 'dots' },
        { type: 'instruction', data: formatted[formatted.length - 2] },
        { type: 'instruction', data: formatted[formatted.length - 1] }
    ]
})

defineExpose({
    collapseNode
})
</script>

<style scoped>
.custom-node {
    border: 1px solid black;
    border-radius: 5px;
    background: white;
    transition: all 0.3s ease;
    position: relative;
}

.custom-node.expanded {
    min-width: 250px;
    z-index: 1000;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.custom-node__header {
    background: #636466;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    padding: 5px 10px;
    color: white;
    font-family: monospace;
    font-size: 0.9rem;
}

.custom-node__body {
    color: black;
    padding: 10px;
    font-family: monospace;
    min-height: 60px;
    position: relative;
}

.close-btn {
    position: absolute;
    bottom: 5px;
    right: 5px;
    background: transparent;
    border: none;
    color: #666;
    cursor: pointer;
    font-size: 1.5rem;
    line-height: 1;
    padding: 0 5px;
    transition: color 0.2s;
}

.close-btn:hover {
    color: #ff4444;
}

/* Resto degli stili invariato */
.span_pc {
    font-family: monospace;
    font-weight: 700;
    margin-right: 5px;
}

.dots-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 2px;
    margin: 8px 0;
    cursor: pointer;
    transition: opacity 0.2s;
    padding: 2px 0;
}

.dots-container:hover {
    opacity: 0.8;
}

.dot {
    width: 3px;
    height: 3px;
    background-color: #666;
    border-radius: 50%;
}

.custom-node__handles {
    position: relative;
    height: 0;
}


.custom-node__handle--source {
    top: -6px;
    right: -6px;
}

.custom-node__handle--target {
    bottom: -6px;
    left: -6px;
}

.instruction-container {
    transition: opacity 0.2s ease;
}

.instruction {
    padding: 2px 0;
    font-size: 0.85rem;
}
</style>
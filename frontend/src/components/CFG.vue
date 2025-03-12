<script setup>
import { ref, watch, nextTick } from 'vue'
import { VueFlow } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { ControlButton, Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'
import { useLayout } from './useLayout'
import CustomNode from '@/components/CustomNode.vue';
import { MarkerType } from '@vue-flow/core'
import { useLegendModalStore } from '@/stores/legendModalStore'
import CFGLegends from '@/components/CFGLegends.vue'

const legendModal = useLegendModalStore()

/**
 * Function to toggle the legend modal.
 * 
 * This function triggers the `openLegend` method from the `legendModal` store to show the legend modal.
 */
function toggleLegend() {
    legendModal.openLegend()
}

/**
 * The props passed to the component.
 * 
 * @typedef {Object} Props
 * @property {Array} data - The data to be displayed in the flow, including blocks and edges.
 */
const props = defineProps({
    /**
     * Data for the flow, consisting of an array of blocks.
     * Each block has an `id`, `label`, `instructions`, and `background_color`.
     * 
     * @type {Array}
     * @required
     */
    data: {
        type: Array,
        required: true,
    },
});

const nodes = ref([])  // Array of nodes
const edges = ref([])  // Array of edges
const { layout } = useLayout()

/**
 * Function to layout the nodes and edges according to a specified direction.
 * 
 * This function updates the positions of the nodes based on the layout algorithm provided.
 * 
 * @param {string} direction - The direction for layout, typically 'TB' (top to bottom).
 */
async function layoutGraph(direction) {
    nodes.value = layout(nodes.value, edges.value, direction)
}

/**
 * Maps the data into VueFlow nodes and edges.
 * 
 * This function processes the provided `data` prop, creating VueFlow-compatible nodes
 * and edges. The nodes are created first, followed by the edges that connect the nodes.
 */
const mapDataToFlow = async () => {
    nodes.value = []
    edges.value = []

    // Create nodes
    const newNodes = props.data.map((block) => ({
        id: block.id.toString(),  // Convert ID to string
        type: 'custom',
        data: {
            label: block.label,
            instructions: block.instructions,
            bgColor: block.background_color
        },
        position: { x: 0, y: 0 },
    }))

    nodes.value = newNodes

    await nextTick()

    // Create edges after nodes are created
    const newEdges = props.data.flatMap((block) =>
        block.outgoing_edges.map((outgoingEdge) => {
            const sourceId = block.id.toString()
            const targetId = outgoingEdge.target.toString()
            const strokeColor = outgoingEdge.color;

            if (
                nodes.value.some(n => n.id === sourceId) &&
                nodes.value.some(n => n.id === targetId)
            ) {
                return {
                    id: `${sourceId}-${targetId}`,
                    source: sourceId,
                    target: targetId,
                    markerEnd: MarkerType.ArrowClosed,
                    style: {
                        stroke: strokeColor
                    },
                }
            } else {
                return null
            }
        }).filter(edge => edge !== null)
    )

    edges.value = newEdges
}

/**
 * Watches the `data` prop and calls `mapDataToFlow` when it changes.
 * 
 * @watch
 * @param {Array} data - The prop that contains the data for nodes and edges.
 */
watch(() => props.data, mapDataToFlow, { immediate: true })
</script>

<template>
<div class="mt-5 w-full h-[80vh] rounded-lg dark:bg-gray-800 dark:text-white" style="width: 100%; height: 80vh; border-radius: 15px;">
    <VueFlow :nodes="nodes" :edges="edges" class="basic-flow" :default-viewport="{ zoom: 0.2 }" :min-zoom="0.2"
        :max-zoom="4" @nodes-initialized="layoutGraph('TB')">
        <template #node-custom="nodeProps">
            <CustomNode v-bind="nodeProps" />
        </template>

        <Background pattern-color="#aaa" :gap="16" />
        <MiniMap />
        <Controls position="top-left">
            <ControlButton class="dark:text-black" title="Legend" @click="toggleLegend" style="width: 100%; border-radius: 15px;">
                Show legend
            </ControlButton>
        </Controls>
    </VueFlow>
</div>

<CFGLegends/>
</template>

<style>
.basic-flow {
    border-radius: 5px;
    border: 1px solid black;
}

.basic-flow.dark .vue-flow__node {
    border-radius: 5px;
    border: 1px solid black;
}
</style>

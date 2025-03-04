<script setup>
import { ref, reactive, watch, nextTick } from 'vue'
import { Panel, VueFlow, useVueFlow } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { ControlButton, Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'
import { initialEdges, initialNodes } from './initial_element.js'
import Icon from './Icon.vue'
import { useLayout } from './useLayout'
import CustomNode from './CustomNode.vue';
import { MarkerType } from '@vue-flow/core'



const props = defineProps({
    data: {
        type: Array,
        required: true,
    },
});

const { onInit, onNodeDragStop, onConnect, addEdges, setViewport, toObject } = useVueFlow()

const nodes = ref([])
const edges = ref([])
const { layout } = useLayout()


const dark = ref(true)

onInit((vueFlowInstance) => {
    vueFlowInstance.fitView()
})

onNodeDragStop(({ event, nodes, node }) => {
    console.log('Node Drag Stop', { event, nodes, node })
})

onConnect((connection) => {
    addEdges(connection)
})

async function layoutGraph(direction) {
    nodes.value = layout(nodes.value, edges.value, direction)

    nextTick(() => {
        fitView()
    })
}

function updatePos() {
    nodes.value = nodes.value.map((node) => {
        return {
            ...node,
            position: {
                x: Math.random() * 400,
                y: Math.random() * 400,
            },
        }
    })
}

function logToObject() {
    console.log(toObject())
}

function resetTransform() {
    setViewport({ x: 0, y: 0, zoom: 1 })
}

function toggleDarkMode() {
    dark.value = !dark.value
}

const mapDataToFlow = async () => {
    nodes.value = []
    edges.value = []

    // Crea i nodi prima

    const newNodes = props.data.map((block) => ({
        id: block.id.toString(), // Converti ID in stringa
        type: 'custom',
        data: {
            label: `Block: ${block.id}`,
            label: block.label,
            instructions: block.instructions,
            bgColor: block.background_color
        },
        position: { x: 0, y: 0 },
    }))

    nodes.value = newNodes

    await nextTick()

    // Debugging: Stampa tutti i nodi creati
    console.log('Nodi creati:', nodes.value)

    // Crea gli edge dopo che i nodi sono stati creati
    const newEdges = props.data.flatMap((block) =>
        block.outgoing_edges.map((outgoingEdge) => {
            const sourceId = block.id.toString()
            const targetId = outgoingEdge.target.toString()
            const strokeColor = outgoingEdge.color;

            console.log(strokeColor)

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
                console.warn(`Edge skipped: ${sourceId} -> ${targetId}`)
                return null
            }
        }).filter(edge => edge !== null)
    )

    edges.value = newEdges

    // Debugging: Stampa gli archi creati
    console.log('Archi creati:', edges.value)
}


watch(() => props.data, mapDataToFlow, { immediate: true })
</script>

<template>
    <div class="mt-5" style="width: 100%; height: 80vh; border-radius: 15px;">
        <VueFlow :nodes="nodes" :edges="edges" class="basic-flow" :default-viewport="{ zoom: 1.5 }" :min-zoom="0.2"
            :max-zoom="4" @nodes-initialized="layoutGraph('TB')">
            <template #node-custom="nodeProps">
                <CustomNode v-bind="nodeProps" />
            </template>
            <div class="w-1/4 p-4 bg-gray-100 rounded-lg">
                <h3 class="text-lg font-semibold text-gray-800">Legenda</h3>
                <tr>
                    <td align="right">black edge&nbsp;</td>
                    <td align="left">
                        <font color="#000000">sequential edge</font>
                    </td>
                </tr>
                <tr>
                    <td align="right">green edge&nbsp;</td>
                    <td align="left">
                        <font color="#5F9747">true edge</font>
                    </td>
                </tr>
                <tr>
                    <td align="right">red edge&nbsp;</td>
                    <td align="left">
                        <font color="#B70000">false edge</font>
                    </td>
                </tr>
                <tr>
                    <td align="right">orange edge&nbsp;</td>
                    <td align="left">
                        <font color="#FF9248">sequential multiple edge</font>
                    </td>
                </tr>
                <tr>
                    <td align="right">green background&nbsp;</td>
                    <td align="left">
                        <font color="#A6EC99">correct termination</font>
                    </td>
                </tr>
                <tr>
                    <td align="right">red background&nbsp;</td>
                    <td align="left">
                        <font color="#EF8683">error termination</font>
                    </td>
                </tr>
                <tr>
                    <td align="right">orange background&nbsp;</td>
                    <td align="left">
                        <font color="#FFB38A">jump to multiple blocks</font>
                    </td>
                </tr>
                <tr>
                    <td align="right">blue background&nbsp;</td>
                    <td align="left">
                        <font color="#6FA8DC">function entrypoint</font>
                    </td>
                </tr>
            </div>
            <Background pattern-color="#aaa" :gap="16" />
            <MiniMap />
            <Controls position="top-left">
                <ControlButton title="Reset Transform" @click="resetTransform">
                    <Icon name="reset" />
                </ControlButton>

            </Controls>
        </VueFlow>
    </div>
</template>

<style>
.basic-flow {
    border-radius: 5px;
    border: 1px solide black;
}

.basic-flow.dark .vue-flow__node {
    border-radius: 5px;
    border: 1px solide black;
}
</style>
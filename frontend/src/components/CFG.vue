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
const isLegendModalOpen = ref(false)

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

function toggleLegend() {
    isLegendModalOpen.value = !isLegendModalOpen.value;
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

    // Crea gli edge dopo che i nodi sono stati creati
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
                console.warn(`Edge skipped: ${sourceId} -> ${targetId}`)
                return null
            }
        }).filter(edge => edge !== null)
    )

    edges.value = newEdges

    // Debugging: Stampa gli archi creati
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

            <Background pattern-color="#aaa" :gap="16" />
            <MiniMap />
            <Controls position="top-left">
                <ControlButton title="Reset Transform" @click="resetTransform">
                    <Icon name="reset" />
                </ControlButton>
                <ControlButton title="Legend" @click="toggleLegend" style="width: 100%; border-radius: 15px;">
                    Show legend
                </ControlButton>
            </Controls>
        </VueFlow>
    </div>

    <!-- Main modal -->
    <div v-if="isLegendModalOpen" id="static-modal" data-modal-backdrop="static" tabindex="-1" aria-hidden="true"
        class="fixed inset-0 z-50 flex justify-center items-center bg-gray-200 bg-opacity-50">
        <div class="relative p-4 w-full max-w-2xl max-h-full">
            <!-- Modal content -->
            <div class="relative bg-white rounded-lg shadow-md">
                <!-- Modal header -->
                <div class="flex items-center justify-between p-4 md:p-5 border-b border-gray-300 rounded-t">
                    <h3 class="text-xl font-semibold text-gray-900">
                        Static modal
                    </h3>
                    <button @click="toggleLegend" type="button"
                        class="text-gray-600 bg-transparent hover:bg-gray-300 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center"
                        data-modal-hide="static-modal">
                        <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                            viewBox="0 0 14 14">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
                        </svg>
                        <span class="sr-only">Close modal</span>
                    </button>
                </div>

                <!-- Modal body -->
                <div class="p-4 md:p-5 space-y-4">
                    <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
                        <table class="w-full text-sm text-left text-gray-700">
                            <thead class="text-xs text-gray-800 uppercase bg-gray-100">
                                <tr>
                                    <th scope="col" class="px-6 py-3">Type</th>
                                    <th scope="col" class="px-6 py-3">Color</th>
                                    <th scope="col" class="px-6 py-3">Meaning</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="border-b dark:border-gray-700 border-gray-200">
                                    <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">
                                        Black
                                        Edge</th>
                                    <td class="px-6 py-4 text-black"><svg class="w-6 h-6 text-gray-800"
                                            aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                            fill="none" viewBox="0 0 24 24" style="color:black">
                                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                                                stroke-width="2" d="M19 12H5m14 0-4 4m4-4-4-4" />
                                        </svg>
                                    </td>
                                    <td class="px-6 py-4">Sequential Edge</td>
                                </tr>
                                <tr class="border-b dark:border-gray-700 border-gray-200">
                                    <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">
                                        Green
                                        Edge</th>
                                    <td class="px-6 py-4 text-black"><svg class="w-6 h-6 text-gray-800"
                                            aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                            fill="none" viewBox="0 0 24 24" style="color:#5F9747">
                                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                                                stroke-width="2" d="M19 12H5m14 0-4 4m4-4-4-4" />
                                        </svg>
                                    </td>
                                    <td class="px-6 py-4">True Edge</td>
                                </tr>
                                <tr class="border-b dark:border-gray-700 border-gray-200">
                                    <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">
                                        Red
                                        Edge</th>
                                    <td class="px-6 py-4 text-black"><svg class="w-6 h-6 text-gray-800"
                                            aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                            fill="none" viewBox="0 0 24 24" style="color:#B70000">
                                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                                                stroke-width="2" d="M19 12H5m14 0-4 4m4-4-4-4" />
                                        </svg>
                                    </td>

                                    <td class="px-6 py-4">False Edge</td>
                                </tr>
                                <tr class="border-b dark:border-gray-700 border-gray-200">
                                    <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">
                                        Orange
                                        Edge</th>

                                    <td class="px-6 py-4 text-black"><svg class="w-6 h-6 text-gray-800"
                                            aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                            fill="none" viewBox="0 0 24 24" style="color:#FF9248">
                                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                                                stroke-width="2" d="M19 12H5m14 0-4 4m4-4-4-4" />
                                        </svg>
                                    </td>
                                    <td class="px-6 py-4">Sequential Multiple Edge</td>
                                </tr>
                                <tr
                                    class="border-b dark:border-gray-700 border-gray-200 bg-green-100 dark:bg-green-900">
                                    <th scope="row" class="px-6 py-4 font-medium text-white whitespace-nowrap">Green
                                        Background</th>
                                    <td class="px-6 py-4">
                                        <svg class="w-6 h-6 text-white" aria-hidden="true"
                                            xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none"
                                            viewBox="0 0 24 24">
                                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                                                stroke-width="2"
                                                d="M11 9h6m-6 3h6m-6 3h6M6.996 9h.01m-.01 3h.01m-.01 3h.01M4 5h16a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Z" />
                                        </svg>
                                    </td>
                                    <td class="px-6 py-4 text-white">Correct Termination</td>
                                </tr>
                                <tr class="border-b dark:border-gray-700 border-gray-200 bg-red-100 dark:bg-red-900">
                                    <th scope="row" class="px-6 py-4 font-medium text-white whitespace-nowrap">Red
                                        Background</th>
                                    <td class="px-6 py-4">
                                        <svg class="w-6 h-6 text-white" aria-hidden="true"
                                            xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none"
                                            viewBox="0 0 24 24">
                                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                                                stroke-width="2"
                                                d="M11 9h6m-6 3h6m-6 3h6M6.996 9h.01m-.01 3h.01m-.01 3h.01M4 5h16a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Z" />
                                        </svg>
                                    </td>
                                    <td class="px-6 py-4 text-white">Error Termination</td>
                                </tr>
                                <tr
                                    class="border-b dark:border-gray-700 border-gray-200 bg-orange-100 dark:bg-orange-900">
                                    <th scope="row" class="px-6 py-4 font-medium text-white whitespace-nowrap">Orange
                                        Background</th>
                                    <td class="px-6 py-4">
                                        <svg class="w-6 h-6 text-white" aria-hidden="true"
                                            xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none"
                                            viewBox="0 0 24 24">
                                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                                                stroke-width="2"
                                                d="M11 9h6m-6 3h6m-6 3h6M6.996 9h.01m-.01 3h.01m-.01 3h.01M4 5h16a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Z" />
                                        </svg>
                                    </td>
                                    <td class="px-6 py-4 text-white">Jump to Multiple Blocks</td>
                                </tr>
                                <tr class="border-b dark:border-gray-700 border-gray-200 bg-blue-100 dark:bg-blue-900">
                                    <th scope="row" class="px-6 py-4 font-medium text-white whitespace-nowrap">Blue
                                        Background</th>
                                    <td class="px-6 py-4">
                                        <svg class="w-6 h-6 text-white" aria-hidden="true"
                                            xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none"
                                            viewBox="0 0 24 24">
                                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                                                stroke-width="2"
                                                d="M11 9h6m-6 3h6m-6 3h6M6.996 9h.01m-.01 3h.01m-.01 3h.01M4 5h16a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Z" />
                                        </svg>
                                    </td>
                                    <td class="px-6 py-4 text-white">Function Entrypoint</td>
                                </tr>

                            </tbody>
                        </table>

                    </div>

                </div>

            </div>
        </div>
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
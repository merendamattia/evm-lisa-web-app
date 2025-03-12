import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useLegendModalStore = defineStore('legendModal', () => {
    const isLegendModalOpen = ref(false)

    function toggleLegend() {
        isLegendModalOpen.value = !isLegendModalOpen.value
    }

    function openLegend() {
        isLegendModalOpen.value = true
    }

    function closeLegend() {
        isLegendModalOpen.value = false
    }

    return { isLegendModalOpen, toggleLegend, openLegend, closeLegend }
})

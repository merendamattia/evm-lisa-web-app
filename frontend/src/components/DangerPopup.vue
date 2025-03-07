<script setup lang="ts">
import { usePopupStore } from '../stores/errorPopupStores';
import { watchEffect } from 'vue';

const popupStore = usePopupStore();

// Impedisce lo scroll del body quando il popup è aperto
watchEffect(() => {
    if (popupStore.isVisible) {
        document.body.classList.add('overflow-hidden');
    } else {
        document.body.classList.remove('overflow-hidden');
    }
});
</script>

<template>
    <div v-if="popupStore.isVisible" class="fixed inset-0 z-50 flex justify-center items-center">
        <div class="fixed inset-0 bg-black bg-opacity-50"></div>

        <!-- Popup -->
        <div class="relative p-4 w-full max-w-md bg-white rounded-lg shadow-lg z-50">
            <button type="button"
                class="absolute top-3 end-2.5 text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center"
                @click="popupStore.hidePopup">
                <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                    viewBox="0 0 14 14">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
                </svg>
                <span class="sr-only">Close modal</span>
            </button>
            <div class="p-4 md:p-5 text-center">
                <svg class="w-12 h-12 mx-auto mb-4 text-red-500" xmlns="http://www.w3.org/2000/svg" fill="none"
                    viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 9v2m0 4h.01M5.64 18h12.72a2 2 0 001.732-3L13.732 4a2 2 0 00-3.464 0L3.908 15a2 2 0 001.732 3z" />
                </svg>

                <h3 class="mb-5 text-lg font-normal text-gray-500">{{ popupStore.message }}</h3>
                <button @click="popupStore.hidePopup" type="button" class="w-full text-white bg-red-600 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 
    font-medium rounded-lg text-sm flex justify-center items-center px-5 py-2.5">
                    OK, understood!
                </button>

            </div>
        </div>
    </div>
</template>

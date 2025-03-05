<script setup>
import { ref } from 'vue';

const isModalOpen = ref(false);
const apiKey = ref('');

const toggleModal = () => {
    isModalOpen.value = !isModalOpen.value;
};

const saveApiKey = async () => {
    try {
        const response = await fetch('http://localhost:9273/save-api-key', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ api_key: apiKey.value }),
        });

        const data = await response.json();

        if (response.ok) {
            toggleModal();
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        alert('Errore durante la comunicazione con il server.');
    }
};
</script>

<template>
    <button @click="toggleModal"
        class="block text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
        type="button">
        Etherscan API key
    </button>

    <!-- Main modal -->
    <div v-if="isModalOpen"
        class="fixed inset-0 z-50 flex justify-center items-center bg-gray-900 bg-opacity-50">
        <div class="relative p-4 w-full max-w-2xl max-h-full bg-white rounded-lg shadow-md">
            <!-- Modal content -->
            <!-- Modal header -->
            <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t">
                <h3 class="text-xl font-semibold text-gray-900">
                    Insert your Etherscan API key
                </h3>
                <button @click="toggleModal" type="button" class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 inline-flex justify-center items-center">
                    <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
                    </svg>
                    <span class="sr-only">Close modal</span>
                </button>
            </div>
            <!-- Modal body -->
            <div class="p-4 md:p-5">
                <form class="space-y-4" @submit.prevent="saveApiKey">
                    <div>
                        <label for="apiKey" class="block mb-2 text-sm font-medium text-gray-900">Etherscan API Key</label>
                        <input v-model="apiKey" type="password" name="apiKey" id="apiKey" placeholder="Insert your Etherscan API key..." 
                            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-green-500 focus:border-green-500 block w-full p-2.5" required />
                    </div>
                    <button type="submit" class="w-full text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center">
                        Save API Key
                    </button>
                    <div class="text-sm font-medium text-gray-500">
                        Don't you have an Etherscan API key? <a href="https://etherscan.io/myapikey" class="text-green-700 hover:underline">Create it now!</a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
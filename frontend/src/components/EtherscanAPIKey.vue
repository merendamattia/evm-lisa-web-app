<script setup>
import { ref } from 'vue';
import { useToastStore } from '../stores/toastStore';

const toastStore = useToastStore();

const triggerToast = () => {
    toastStore.showToast();
    toastStore.setText('API Key saved successfully.')
};

const isModalOpen = ref(false);
const apiKey = ref('');
const isSubmitting = ref(false);

const toggleModal = () => {
    isModalOpen.value = !isModalOpen.value;
};

const saveApiKey = async () => {
    try {
        isSubmitting.value = true;
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
            triggerToast();
        } else {
            alert(`Error: ${data.error}`);
        }
        isSubmitting.value = false;
    } catch (error) {
        isSubmitting.value = false;
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
    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex justify-center items-center bg-gray-900 bg-opacity-50">
        <div class="relative p-4 w-full max-w-2xl max-h-full bg-white rounded-lg shadow-md">
            <!-- Modal content -->
            <!-- Modal header -->
            <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t">
                <h3 class="text-xl font-semibold text-gray-900">
                    Insert your Etherscan API key 
                </h3>
                <button @click="toggleModal" type="button"
                    class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 inline-flex justify-center items-center">
                    <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                        viewBox="0 0 14 14">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
                    </svg>
                    <span class="sr-only">Close modal</span>
                </button>
            </div>
            <!-- Modal body -->
            <div class="p-4 md:p-5">
                <form class="space-y-4" @submit.prevent="saveApiKey">
                    <div>
                        <label for="apiKey" class="block mb-2 text-sm font-medium text-gray-900">Etherscan API
                            Key <span style="color: red;">*</span></label>
                        <input v-model="apiKey" type="password" name="apiKey" id="apiKey"
                            placeholder="Insert your Etherscan API key..."
                            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-green-500 focus:border-green-500 block w-full p-2.5"
                            required />
                    </div>
                    <button type="submit"
                        :disabled="isSubmitting"
                        class="w-full text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center">
                        <svg aria-hidden="true" v-if="isSubmitting" role="status"
                            class="inline w-4 h-4 me-3 text-white animate-spin" viewBox="0 0 100 101" fill="none"
                            xmlns="http://www.w3.org/2000/svg">
                            <path
                                d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                                fill="#E5E7EB" />
                            <path
                                d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                                fill="currentColor" />
                        </svg>
                        {{ isSubmitting ? 'Saving...' : 'Save API Key' }}
                    </button>
                    <div class="text-sm font-medium text-gray-500">
                        Don't you have an Etherscan API key? <a href="https://etherscan.io/myapikey"
                            class="text-green-700 hover:underline">Create it now!</a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
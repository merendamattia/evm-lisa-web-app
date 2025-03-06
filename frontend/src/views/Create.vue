<template>
    <section class="bg-white">
        <div class="px-4 mx-auto">
            <h1 class="mb-4 text-xl font-bold text-gray-900">EVMLiSA: an abstract interpretation-based static analyzer
                for EVM bytecode</h1>
            <p>EVMLiSA is a static analyzer based on abstract interpretation for EVM bytecode of smart contracts
                deployed on Ethereum blockchain and built upon LiSA. Given a EVM bytecode smart contract, EVMLiSA builds
                a sound and precise control-flow graph of the smart contract.</p>

            <div class="flex space-x-2 mb-4 mt-2">
                <img src="https://img.shields.io/github/actions/workflow/status/lisa-analyzer/evm-lisa/gradle-master.yml"
                    alt="GitHub Actions Workflow Status" />
                <img src="https://img.shields.io/github/last-commit/lisa-analyzer/evm-lisa" alt="GitHub last commit" />
                <img src="https://img.shields.io/github/commit-activity/y/lisa-analyzer/evm-lisa"
                    alt="GitHub commit activity" />
                <img src="https://img.shields.io/github/issues-raw/lisa-analyzer/evm-lisa" alt="GitHub issues" />
            </div>

            <hr class="mb-4 mt-4">

            <h1 class="mb-4 text-xl font-bold text-gray-900">Run new EVM analysis</h1>

            <form @submit.prevent="handleSubmit">
                <div class="grid gap-4 sm:grid-cols-1 sm:gap-6">
                    <!-- Address Field -->
                    <div class="sm:col-span-2">
                        <label for="address" class="block mb-2 text-sm font-medium text-gray-900">
                            Contract Address<span class="text-red-500"> *</span>
                        </label>
                        <input type="text" id="address" v-model="formData.address"
                            :class="{ 'border-red-500': v$.address.$error }"
                            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
                            placeholder="Enter contract address" autocomplete="off" @blur="v$.address.$touch()">
                        <p v-for="error in v$.address.$errors" :key="error.$uid" class="mt-2 text-sm text-red-500">
                            {{ error.$message }}
                        </p>
                    </div>

                    <!-- Bytecode Field -->
                    <div class="sm:col-span-2">
                        <label for="bytecode" class="block mb-2 text-sm font-medium text-gray-900">
                            Contract Bytecode<span class="text-red-500"> *</span>
                        </label>
                        <textarea id="bytecode" v-model="formData.bytecode" rows="8"
                            :class="{ 'border-red-500': v$.bytecode.$error }"
                            class="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-primary-500 focus:border-primary-50"
                            placeholder="Enter contract bytecode here" @blur="v$.bytecode.$touch()"></textarea>
                        <p v-for="error in v$.bytecode.$errors" :key="error.$uid" class="mt-2 text-sm text-red-500">
                            {{ error.$message }}
                        </p>
                    </div>
                </div>

                <button type="submit"
                    class="mt-5 text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2"
                    :disabled="v$.$invalid || isSubmitting">
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
                    {{ isSubmitting ? processingText : 'Start analysis' }}
                </button>
            </form>

            <Tabs v-show="showCFG && cfgData" :tabs="tabs">
                <template #cfg>
                    <CFG v-show="showCFG && cfgData" :data="cfgData" />
                </template>
                <template #disassembled>
                    <Disassembled :data="cfgData" />
                </template>
                <template #json>
                    <div class="json-scroll-container"
                        style="width: 100%; overflow-x: scroll; overflow-y: scroll; height: 80vh;">
                        <JSONViewer :data="JSONViewerData" />
                    </div>
                </template>
            </Tabs>
        </div>
    </section>
</template>

<script setup lang="ts">
import { reactive, ref, watch, computed } from 'vue';
import { useVuelidate } from '@vuelidate/core';
import { helpers } from '@vuelidate/validators';
import BasicBlock from '../models/BasicBlock';
import CFG from '../components/CFG.vue';
import Tabs from '../components/Tabs.vue';
import JSONViewer from '../components/JSONViewer.vue';
import Disassembled from '../components/Disassembled.vue';
import { useToastStore } from '../stores/toastStore';
import { usePopupStore } from '../stores/popupStores';

const popupStore = usePopupStore();
const toastStore = useToastStore();

const triggerErrorPopup = (errorMessage : string) => {
    popupStore.showPopup(errorMessage);
}

const triggerToast = () => {
    toastStore.showToast();
    toastStore.setText('Analysis run successfully!')
};

interface ApiResponse {
    // Definisci qui la struttura attesa dei dati (opzionale)
    [key: string]: any;
}

const tabs = [
    { label: 'CFG', slotName: 'cfg' },
    { label: 'JSON', slotName: 'json' },
    { label: 'Disassembled', slotName: 'disassembled' },
];

const showCFG = ref(false);
const cfgData = ref<BasicBlock[] | null>(null);
const JSONViewerData = ref<ApiResponse | null>(null);
const isSubmitting = ref(false);
const processingText = ref('')

const ethAddressRegex = /^0x[a-fA-F0-9]{40}$/;
const bytecodeRegex = /^0x([a-fA-F0-9]{2})+$/;

const formData = reactive({
    address: '',
    bytecode: ''
});

// Custom validators
const ethAddress = (value: string) => !value || ethAddressRegex.test(value);
const validBytecode = (value: string) => !value || bytecodeRegex.test(value);
const atLeastOne = () => !!formData.address || !!formData.bytecode;

// Define validation rules
const rules = computed(() => {
    return {
        address: {
            ethAddress: helpers.withMessage('Invalid Ethereum address format', ethAddress)
        },
        bytecode: {
            validBytecode: helpers.withMessage(
                'Invalid bytecode format (must start with 0x and have even number of hex characters)',
                validBytecode
            )
        }
    };
});

// Create Vuelidate instance
const v$ = useVuelidate(rules, formData);

// Watch for address changes - clear bytecode if address has value
watch(() => formData.address, (newVal) => {
    if (newVal) {
        // Only clear bytecode when address has some content
        formData.bytecode = '';
    }
}, { immediate: true });

// Watch for bytecode changes - clear address if bytecode has value
watch(() => formData.bytecode, (newVal) => {
    if (newVal) {
        // Only clear address when bytecode has some content
        formData.address = '';
    }
}, { immediate: true });

// Handle form-level validations manually
const validateForm = () => {
    const errors = [];

    if (!atLeastOne()) {
        errors.push('EVM address or bytecode must be provided');
    }

    return errors;
};

const handleSubmit = async () => {
    const isValid = await v$.value.$validate();
    const formErrors = validateForm();
    let timerId = setInterval(printCurrentTime, 10);

    if (!isValid || formErrors.length > 0) {
        if (formErrors.length > 0) {
            alert(formErrors.join('\n'));
        }
        return;
    }

    try {
        isSubmitting.value = true;

        console.log(formData);

        const response = await fetch('http://127.0.0.1:9273/run-command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        resetTimer(timerId);

        const data = await response.json();

        if (!response.ok) {         
            triggerErrorPopup(data.error); 
            throw new Error(data.error || "Unknow error");
        }

        JSONViewerData.value = data;

        cfgData.value = data.basic_blocks.map((block: any) =>
            new BasicBlock(
                block.label,
                block.background_color,
                block.id,
                block.ingoing_edge_color,
                block.instructions,
                block.last_instruction,
                block.outgoing_edges
            )
        );

        triggerToast();
        console.log(cfgData);
        v$.value.$reset();
        showCFG.value = true;

    } catch (error) {
        console.error('Error:', error);
        console.error(error instanceof Error ? error.message : 'An unexpected error occurred');
    } finally {
        isSubmitting.value = false;
    }
};


let timeInHundredths = 0; // Inizializza il tempo a 0 centesimi di secondo

function resetTimer (timerId : number) {

timeInHundredths = 0;
clearInterval(timerId);

}

function printCurrentTime() {
    // Calcola i minuti, secondi e centesimi di secondo
    const minutes = Math.floor(timeInHundredths / 6000); // 6000 centesimi in un minuto
    const seconds = Math.floor((timeInHundredths % 6000) / 100); // Resto diviso 100 per ottenere i secondi
    const hundredths = timeInHundredths % 100; // Restante per i centesimi

    // Format del tempo, ma senza i minuti se sono 0
    let formattedTime = `${String(seconds).padStart(2, '0')}.${String(hundredths).padStart(2, '0')}`;

    // Se i minuti sono diversi da 0, includili nel formato
    if (minutes > 0) {
        formattedTime = `${String(minutes).padStart(2, '0')}:${formattedTime}`;
    }

    processingText.value = `Processing... ${formattedTime}`;

    // Incrementa il contatore ogni 10 millisecondi
    timeInHundredths++;
}
</script>

<style lang="css" scoped>
.bodyTabs {
    border: 1px solid black;
    padding-left: 10px;
    padding-right: 10px;
    margin-bottom: 100px;
}

.json-scroll-container::-webkit-scrollbar {
    width: 12px;
    /* Larghezza della scrollbar verticale */
    height: 12px;
    /* Altezza della scrollbar orizzontale */
    border-radius: 10px;
    /* Arrotonda i bordi della scrollbar */
}

.json-scroll-container::-webkit-scrollbar-track {
    background: #f1f1f1;
    /* Colore della traccia della scrollbar */
    border-radius: 10px;
    /* Arrotonda i bordi della traccia */
}

.json-scroll-container::-webkit-scrollbar-thumb {
    background: green;
    /* Colore della parte mobile (thumb) della scrollbar */
    border-radius: 10px;
    /* Arrotonda i bordi del thumb */
}

.json-scroll-container::-webkit-scrollbar-thumb:hover {
    background: #555;
    /* Colore del thumb quando si passa sopra con il mouse */
}

.json-scroll-container::-webkit-scrollbar-corner {
    background: transparent;
    /* Angolo della scrollbar (dove si incontrano x e y) */
}

/* Per Firefox */
.json-scroll-container {
    scrollbar-width: thin;
    /* Imposta la larghezza della scrollbar */
    scrollbar-color: green #f1f1f1;
    /* Colori del thumb e della traccia */
    border-radius: 10px;
    /* Arrotonda i bordi del contenitore */
}
</style>
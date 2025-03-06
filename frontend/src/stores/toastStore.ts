import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useToastStore = defineStore('toast', () => {
    const isVisible = ref(false);
    const textToast = ref('');

    function showToast() {
        isVisible.value = true;
        setTimeout(() => {
            isVisible.value = false;
        }, 3000); // Nasconde il toast dopo 3 secondi
    }

    function setText (text : string) {
        textToast.value = text;
    } 

    return { isVisible, showToast,setText , textToast };
});

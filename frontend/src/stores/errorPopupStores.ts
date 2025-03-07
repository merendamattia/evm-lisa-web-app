import { defineStore } from 'pinia';
import { ref } from 'vue';

export const usePopupStore = defineStore('popup', () => {
    const isVisible = ref(false);
    const message = ref('Are you sure you want to delete this product?');

    function showPopup(newMessage?: string) {
        if (newMessage) {
            message.value = newMessage;
        }
        isVisible.value = true;
    }

    function hidePopup() {
        isVisible.value = false;
    }

    return { isVisible, message, showPopup, hidePopup };
});

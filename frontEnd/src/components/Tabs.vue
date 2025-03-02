<template>
  <div class="tabs">
    <ul class="flex border-b border-gray-200">
      <li
        v-for="(tab, index) in tabs"
        :key="tab.id"
        class="mr-2"
      >
        <a
          href="#"
          :class="[
            'inline-block p-4',
            { 'bg-blue-500 text-white': tab.id === activeTabId, 'text-blue-500': tab.id !== activeTabId }
          ]"
          @click.prevent="setActiveTab(tab.id)"
        >
          {{ tab.name }}
        </a>
      </li>
    </ul>
    <div v-for="(tab, index) in tabs" :key="tab.id" v-show="tab.id === activeTabId" class="tab-content p-4">
      <slot :name="tab.id" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'Tabs',
  props: {
    // La tab attiva iniziale può essere passata come prop
    initialActiveTab: {
      type: String,
      default: null
    },
    // Le tabs sono un array di oggetti passati come prop
    tabs: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      activeTabId: this.initialActiveTab || (this.tabs.length ? this.tabs[0].id : '')
    };
  },
  methods: {
    setActiveTab(id) {
      this.activeTabId = id;
      this.$emit('tab-changed', id); // Emissione dell'evento per permettere la gestione esterna
    }
  }
};
</script>

<style scoped>
.tabs {
  width: 100%;
}

.tab-content {
  display: none;
}

.tab-content[style] {
  display: block;
}
</style>

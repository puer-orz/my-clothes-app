<template>
  <div class="w-full bg-white shadow-sm border-b overflow-hidden">
    <div class="px-4 py-3 text-sm font-medium text-gray-800">
      选择您的时空导购
    </div>
    <div class="flex overflow-x-auto no-scrollbar px-4 pb-4 space-x-4">
      <div 
        v-for="celeb in shopStore.celebrities" 
        :key="celeb.id"
        @click="shopStore.changeCelebrity(celeb.id)"
        class="flex-shrink-0 flex flex-col items-center justify-center p-3 rounded-xl border-2 transition-all duration-300 w-28"
        :class="shopStore.currentCelebrityId === celeb.id ? 'border-blue-500 bg-blue-50' : 'border-gray-100 bg-gray-50'"
      >
        <div class="text-3xl mb-2">{{ celeb.avatar }}</div>
        <div class="font-bold text-sm text-gray-800 mb-1">{{ celeb.name }}</div>
        <div class="text-xs text-gray-500 flex flex-wrap justify-center gap-1">
          <span v-for="tag in celeb.tags" :key="tag" class="bg-gray-200 px-1 rounded">{{ tag }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useShopStore } from '@/stores/shop'

const shopStore = useShopStore()
</script>

<style scoped>
/* The custom scrollbar hide class is in style.css */
</style>
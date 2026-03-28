<template>
  <div class="h-screen w-screen flex flex-col bg-gray-100 overflow-hidden">
    <!-- Header -->
    <van-nav-bar title="时空伴购" fixed placeholder class="font-bold" />

    <!-- Celebrity Selection (Horizontal Scroll) -->
    <CelebritySelection />

    <!-- Chat Area -->
    <div class="flex-1 relative overflow-hidden">
      <ChatSystem @showProduct="openProductModal" />
    </div>

    <!-- Product Details Modal -->
    <van-popup
      v-model:show="showModal"
      position="bottom"
      round
      closeable
      class="h-[80%]"
      @close="closeModal"
    >
      <div v-if="selectedProduct" class="p-5 h-full flex flex-col">
        <!-- Image Area (Emoji) -->
        <div class="w-full h-48 bg-gray-50 rounded-xl flex items-center justify-center text-8xl mb-4 shadow-inner">
          {{ selectedProduct.image }}
        </div>
        
        <!-- Info -->
        <div class="flex-1 overflow-y-auto">
          <div class="text-2xl font-bold text-red-500 mb-2">
            <span class="text-sm">¥</span> {{ selectedProduct.price }}
          </div>
          <h2 class="text-lg font-bold text-gray-800 mb-2 leading-tight">{{ selectedProduct.title }}</h2>
          
          <div class="flex gap-2 mb-4">
            <span 
              v-for="tag in selectedProduct.tags" 
              :key="tag" 
              class="px-2 py-1 bg-red-50 text-red-500 text-xs rounded-md"
            >
              {{ tag }}
            </span>
          </div>
          
          <!-- AI Recommendation Reason -->
          <div class="bg-blue-50 p-4 rounded-xl mt-4 border border-blue-100 relative">
            <div class="absolute -top-3 left-4 bg-white px-2 text-xs text-blue-500 font-bold border border-blue-100 rounded-full flex items-center gap-1">
              <span>{{ shopStore.currentCelebrity.avatar }}</span>
              <span>{{ shopStore.currentCelebrity.name }} 推荐</span>
            </div>
            <p class="text-sm text-gray-600 mt-2 leading-relaxed">
              {{ shopStore.currentCelebrity.templates.success }} 这款商品是您的不二之选。
            </p>
          </div>
        </div>
        
        <!-- Action Button -->
        <div class="mt-4 pt-4 border-t border-gray-100 flex gap-3">
          <van-button 
            type="default" 
            block 
            round 
            class="flex-1 shadow-sm"
            @click="closeModal"
          >
            返回
          </van-button>
          <van-button 
            type="primary" 
            block 
            round 
            class="flex-1 shadow-md bg-gradient-to-r from-blue-500 to-indigo-500 border-none"
            @click="addToCart"
          >
            加入购物车
          </van-button>
        </div>
      </div>
    </van-popup>
    <!-- Custom Toast Component -->
    <CustomToast ref="toastRef" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useShopStore } from '@/stores/shop'
import CelebritySelection from '@/components/CelebritySelection.vue'
import ChatSystem from '@/components/ChatSystem.vue'
import CustomToast from '@/components/Toast.vue'

const shopStore = useShopStore()

// Modal State
const showModal = ref(false)
const selectedProduct = ref(null)
const toastRef = ref(null)

const openProductModal = (product) => {
  selectedProduct.value = product
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  setTimeout(() => {
    selectedProduct.value = null
  }, 300)
}

const addToCart = () => {
  if (toastRef.value) {
    toastRef.value.show('已加入购物车', 2000)
  }
  closeModal()
}
</script>

<style>
/* Optional global adjustments */
.van-nav-bar__title {
  font-weight: bold !important;
}
</style>